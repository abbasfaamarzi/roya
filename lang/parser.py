"""Recursive parser for components, properties, loops, conditions and events."""
import re
from .ast import Document, Node, StyleRule
from .errors import RoyaSyntaxError
from .lexer import lex

_IDENTIFIER = r"[A-Za-z_][A-Za-z0-9_]*"
_COMPONENT = re.compile(rf"^({_IDENTIFIER}):$")
_RULE = re.compile(rf"^<({_IDENTIFIER})@({_IDENTIFIER})>:$")
_PROPERTY = re.compile(rf"^({_IDENTIFIER})\s*:\s*(.*?)$")
_FOR = re.compile(rf"^for\s+({_IDENTIFIER})\s+in\s+(.+?)(?:\s+key\s+(.+))?:$")
_IF = re.compile(r"^if\s+(.+):$")
_EVENT = re.compile(r"^(on_[A-Za-z0-9_]+)\s*:\s*(.*?)$")


def _parse_mapping(lines, index, parent_indent):
    values = {}
    while index < len(lines) and lines[index].indent > parent_indent:
        line = lines[index]
        if line.indent != parent_indent + 4:
            raise RoyaSyntaxError("Mapping entries must be indented exactly one level.", line.number)
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*?)$", line.text)
        if not match:
            raise RoyaSyntaxError("Expected 'name: expression' in mapping.", line.number)
        values[match.group(1)] = match.group(2)
        index += 1
    return values, index


def _parse_event(lines, index, event_indent, inline_value, line_number):
    action_name = inline_value.strip().strip("\"'")
    args = {}
    if inline_value:
        return {"action": action_name, "args": args}, index + 1
    index += 1
    while index < len(lines) and lines[index].indent > event_indent:
        line = lines[index]
        if line.indent != event_indent + 4:
            raise RoyaSyntaxError("Event entries must be indented exactly one level.", line.number)
        match = _PROPERTY.match(line.text)
        if not match:
            raise RoyaSyntaxError("Expected 'action:' or 'args:' inside an event.", line.number)
        key, value = match.groups()
        if key == "action":
            action_name = value.strip().strip("\"'")
            index += 1
        elif key == "args":
            args, index = _parse_mapping(lines, index + 1, line.indent)
        else:
            raise RoyaSyntaxError(f"Unknown event field '{key}'.", line.number)
    if not action_name:
        raise RoyaSyntaxError("An event binding requires an action name.", line_number)
    return {"action": action_name, "args": args}, index


def _parse_component(lines, index, name, indent):
    node = Node(kind="component", name=name, line=lines[index].number)
    index += 1
    while index < len(lines) and lines[index].indent > indent:
        line = lines[index]
        if line.indent != indent + 4:
            raise RoyaSyntaxError("Child statements must be indented exactly one level.", line.number)

        event_match = _EVENT.match(line.text)
        if event_match:
            event_name, value = event_match.groups()
            binding, index = _parse_event(lines, index, line.indent, value, line.number)
            node.events[event_name] = binding
            continue

        match = _PROPERTY.match(line.text)
        if match and match.group(1) == "style" and not match.group(2):
            node.styles, index = _parse_mapping(lines, index + 1, line.indent)
            continue

        child_match = _COMPONENT.match(line.text)
        if child_match:
            child, index = _parse_component(lines, index, child_match.group(1), line.indent)
            node.children.append(child)
            continue

        if match:
            key, value = match.groups()
            node.properties[key] = value
            index += 1
            continue

        loop_match = _FOR.match(line.text)
        if loop_match:
            variable, expression, key_expression = loop_match.groups()
            block = Node(kind="block", line=line.number)
            next_index = index + 1
            _, _, block.children, next_index = _parse_body(lines, next_index, line.indent, block)
            node.children.append(Node(kind="for", variable=variable, expression=expression.strip(), key_expression=(key_expression or "").strip(), children=block.children, line=line.number))
            index = next_index
            continue

        if_match = _IF.match(line.text)
        if if_match:
            block = Node(kind="block", line=line.number)
            next_index = index + 1
            _, _, block.children, next_index = _parse_body(lines, next_index, line.indent, block)
            node.children.append(Node(kind="if", expression=if_match.group(1).strip(), children=block.children, line=line.number))
            index = next_index
            continue

        raise RoyaSyntaxError(f"Unrecognized statement '{line.text}'.", line.number)
    return node, index


def _parse_body(lines, index, indent, container):
    properties, styles, children = {}, {}, []
    while index < len(lines) and lines[index].indent > indent:
        line = lines[index]
        if line.indent != indent + 4:
            raise RoyaSyntaxError("Block statements must be indented exactly one level.", line.number)
        match = _COMPONENT.match(line.text)
        if match:
            child, index = _parse_component(lines, index, match.group(1), line.indent)
            children.append(child)
            continue
        loop_match = _FOR.match(line.text)
        if loop_match:
            variable, expression, key_expression = loop_match.groups()
            block = Node(kind="block", line=line.number)
            _, _, block_children, index = _parse_body(lines, index + 1, line.indent, block)
            children.append(Node(kind="for", variable=variable, expression=expression.strip(), key_expression=(key_expression or "").strip(), children=block_children, line=line.number))
            continue
        if_match = _IF.match(line.text)
        if if_match:
            block = Node(kind="block", line=line.number)
            _, _, block_children, index = _parse_body(lines, index + 1, line.indent, block)
            children.append(Node(kind="if", expression=if_match.group(1).strip(), children=block_children, line=line.number))
            continue
        event_match = _EVENT.match(line.text)
        if event_match:
            event_name, value = event_match.groups()
            binding, index = _parse_event(lines, index, line.indent, value, line.number)
            container.events[event_name] = binding
            continue
        prop_match = _PROPERTY.match(line.text)
        if prop_match:
            key, value = prop_match.groups()
            if key == "style" and not value:
                styles, index = _parse_mapping(lines, index + 1, line.indent)
            else:
                properties[key] = value
                index += 1
            continue
        raise RoyaSyntaxError(f"Unrecognized statement '{line.text}'.", line.number)
    return properties, styles, children, index


def parse(source: str) -> Document:
    lines = lex(source)
    rules = {}
    root = None
    logic_modules = []
    includes = []
    version = "1.0"
    index = 0

    while index < len(lines):
        line = lines[index]
        if line.indent != 0:
            raise RoyaSyntaxError("Top-level declarations must start at column zero.", line.number)
        if line.text.startswith("#:"):
            directive = line.text[2:].strip()
            if directive.startswith("roya "):
                version = directive.split(None, 1)[1].strip()
            elif directive.startswith("logic "):
                module = directive.split(None, 1)[1].strip()
                if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*", module):
                    raise RoyaSyntaxError("Invalid Python logic module path.", line.number)
                logic_modules.append(module)
            elif directive.startswith("include "):
                includes.append(directive.split(None, 1)[1].strip().strip("\"'"))
            else:
                raise RoyaSyntaxError(f"Unknown directive '{directive}'.", line.number)
            index += 1
            continue

        rule_match = _RULE.match(line.text)
        if rule_match:
            alias, base = rule_match.groups()
            node, index = _parse_component(lines, index, alias, 0)
            if alias in rules:
                raise RoyaSyntaxError(f"Duplicate style rule '{alias}'.", line.number)
            rules[alias] = StyleRule(alias, base, node.properties, node.styles, line.number)
            continue

        root_match = _COMPONENT.match(line.text)
        if root_match:
            if root is not None:
                raise RoyaSyntaxError("A .roya file must contain exactly one root component.", line.number)
            root, index = _parse_component(lines, index, root_match.group(1), 0)
            continue
        raise RoyaSyntaxError(f"Invalid top-level declaration '{line.text}'.", line.number)

    if root is None:
        raise RoyaSyntaxError("No root component was declared.")
    return Document(root=root, rules=rules, logic_modules=logic_modules, includes=includes, version=version)
