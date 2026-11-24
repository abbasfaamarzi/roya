"""Compile the parsed AST into the existing registered Roya components."""
import hashlib
import html
import re
from roya.core.properties import Property
from roya.core.registry import registry
from roya.actions.registry import action_registry
from .errors import RoyaLanguageError, RoyaSyntaxError
from .expressions import evaluate


def _snake_case(name):
    value = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    return value.replace("-", "_").lower()


def _declared_properties(component_class):
    result = set()
    for base in component_class.__mro__:
        for name, descriptor in vars(base).items():
            if isinstance(descriptor, Property):
                result.add(name)
    return result


def _json_value(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    raise RoyaSyntaxError(f"Action arguments must be JSON-compatible; got {type(value).__name__}.")


def _style_value(raw, scope):
    value = str(raw).strip()
    try:
        return evaluate(value, scope)
    except Exception:
        return value.strip("\"'")


def _inject_styles(markup, styles_by_id, classes_by_id):
    component_ids = set(styles_by_id) | set(classes_by_id)
    for component_id in component_ids:
        safe_id = re.escape(str(component_id))
        pattern = re.compile(r'(<[A-Za-z][^>]*\bid=["\']' + safe_id + r'["\'][^>]*)(/?>)', re.I | re.S)
        match = pattern.search(markup)
        if not match:
            continue
        opening = match.group(1)
        custom_class = classes_by_id.get(component_id, "").strip()
        if custom_class:
            class_match = re.search(r'\sclass=(["\'])(.*?)\1', opening, re.I | re.S)
            if class_match:
                existing = class_match.group(2).split()
                for name in custom_class.split():
                    if name not in existing:
                        existing.append(name)
                replacement = " ".join(existing)
                opening = opening[:class_match.start()] + f' class="{html.escape(replacement, quote=True)}"' + opening[class_match.end():]
            else:
                opening += f' class="{html.escape(custom_class, quote=True)}"'
        declarations = styles_by_id.get(component_id, {})
        css = "; ".join(f"{key}: {value}" for key, value in declarations.items())
        if css:
            style_match = re.search(r'\sstyle=(["\'])(.*?)\1', opening, re.I | re.S)
            if style_match:
                combined = (style_match.group(2).rstrip("; ") + "; " + css).strip()
                opening = opening[:style_match.start()] + f' style="{html.escape(combined, quote=True)}"' + opening[style_match.end():]
            else:
                opening += f' style="{html.escape(css, quote=True)}"'
        markup = markup[:match.start()] + opening + match.group(2) + markup[match.end():]
    return markup


class Builder:
    def __init__(self, rules=None):
        self.rules = rules or {}
        self.actions = {}
        self.styles_by_id = {}
        self.classes_by_id = {}
        if not registry.has("box_layout"):
            from roya.components import register_all
            register_all(registry)

    def _component_class(self, declared_name):
        rule = self.rules.get(declared_name)
        base_name = rule.base if rule else declared_name
        return registry.get(_snake_case(base_name)), rule

    def _build_statement(self, node, scope, parent=None, key_prefix="root"):
        if node.kind == "for":
            values = evaluate(node.expression, scope)
            if values is None:
                return
            if isinstance(values, dict):
                values = list(values.values())
            if isinstance(values, (str, bytes)) or not hasattr(values, "__iter__"):
                raise RoyaSyntaxError("A for-loop expression must produce an iterable collection.", node.line)
            for index, item in enumerate(values):
                child_scope = dict(scope)
                child_scope[node.variable] = item
                if node.key_expression:
                    stable_key = evaluate(node.key_expression, child_scope)
                else:
                    stable_key = index
                child_prefix = f"{key_prefix}/{stable_key}"
                for child_index, child in enumerate(node.children):
                    self._build_statement(child, child_scope, parent, f"{child_prefix}/{child_index}")
            return

        if node.kind == "if":
            if evaluate(node.expression, scope):
                for child_index, child in enumerate(node.children):
                    self._build_statement(child, scope, parent, f"{key_prefix}/{child_index}")
            return

        if node.kind != "component":
            raise RoyaSyntaxError(f"Unsupported AST node '{node.kind}'.", node.line)

        component_class, rule = self._component_class(node.name)
        allowed = _declared_properties(component_class)
        raw_properties = {}
        if rule:
            raw_properties.update(rule.properties)
        raw_properties.update(node.properties)
        properties = {}
        for name, expression in raw_properties.items():
            if name not in allowed:
                raise RoyaSyntaxError(f"Unknown property '{name}' on component '{component_class.__name__}'.", node.line)
            properties[name] = evaluate(expression, scope)

        if "id" not in properties and (rule or key_prefix != "root"):
            seed = f"{getattr(parent, 'id', 'root')}:{key_prefix}:{node.name}"
            digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12]
            properties["id"] = f"roya-{digest}"

        component = component_class(**properties)
        custom_class = str(getattr(component, "class_name", "") or "").strip()
        if custom_class:
            self.classes_by_id[component.id] = custom_class
        style_values = {}
        if rule:
            style_values.update(rule.styles)
        style_values.update(node.styles)
        if style_values:
            resolved = {}
            for key, raw in style_values.items():
                css_name = re.sub(r"([A-Z])", r"-\1", key).replace("_", "-").lower()
                if not re.fullmatch(r"(?:--)?[a-zA-Z][a-zA-Z0-9_-]*", css_name):
                    raise RoyaSyntaxError(f"Invalid CSS property '{key}'.", node.line)
                css_value = _style_value(raw, scope)
                if any(token in str(css_value).lower() for token in ("</", "javascript:", "expression(")):
                    raise RoyaSyntaxError(f"Unsafe CSS value for '{key}'.", node.line)
                resolved[css_name] = str(css_value)
            self.styles_by_id[component.id] = resolved

        for event_name, binding in node.events.items():
            if not hasattr(component_class, event_name):
                raise RoyaSyntaxError(f"Component '{component_class.__name__}' does not declare event '{event_name}'.", node.line)
            action_name = binding["action"]
            if action_registry.get(action_name) is None:
                raise RoyaSyntaxError(f"Action '{action_name}' is not registered. Load its Python logic module with #:logic.", node.line)
            args = {key: _json_value(evaluate(value, scope)) for key, value in binding.get("args", {}).items()}
            self.actions.setdefault(component.id, {})[event_name] = {"action": action_name, "args": args}

        if parent is not None:
            parent.add_child(component)
        for child_index, child in enumerate(node.children):
            self._build_statement(child, scope, component, f"{key_prefix}/{child_index}")
        return component

    def build(self, document, context):
        root = self._build_statement(document.root, dict(context))
        markup = str(root.render())
        markup = _inject_styles(markup, self.styles_by_id, self.classes_by_id)
        return root, markup
