"""Django integration for loading and rendering .roya files."""
import importlib
import os
import re
from pathlib import Path
from django.conf import settings
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import reverse, NoReverseMatch
from django.utils.html import json_script
from django.utils.safestring import mark_safe
from django.middleware.csrf import get_token
from .builder import Builder
from .errors import RoyaLanguageError
from .parser import parse

_INCLUDE = re.compile(r"^\s*#:include\s+['\"]([^'\"]+)['\"]\s*$")


def _inside_root(path, root):
    try:
        return os.path.commonpath([str(path), str(root)]) == str(root)
    except ValueError:
        return False


def _expand_includes(source, origin, project_root, seen=None):
    seen = seen or set()
    resolved_origin = Path(origin).resolve()
    if resolved_origin in seen:
        raise RoyaLanguageError(f"Circular .roya include detected: {resolved_origin}")
    seen.add(resolved_origin)
    output = []
    for line in source.splitlines():
        match = _INCLUDE.match(line)
        if not match:
            output.append(line)
            continue
        include_path = (resolved_origin.parent / match.group(1)).resolve()
        if include_path.suffix != ".roya" or not _inside_root(include_path, project_root) or not include_path.is_file():
            raise RoyaLanguageError(f"Invalid or inaccessible .roya include: {match.group(1)}")
        nested = include_path.read_text(encoding="utf-8")
        output.append(_expand_includes(nested, include_path, project_root, seen.copy()))
    return "\n".join(output)


def render_roya(request, template_name, context=None, *, include_runtime=True):
    """Render a .roya template as a safe HTML fragment for a Django response/template."""
    template = get_template(template_name)
    django_template = getattr(template, "template", template)
    source = getattr(django_template, "source", None)
    origin = getattr(django_template, "origin", None)
    if source is None or origin is None or not getattr(origin, "name", None):
        raise RoyaLanguageError(f"Could not resolve source path for .roya template '{template_name}'.")

    project_root = Path(settings.BASE_DIR).resolve()
    expanded_source = _expand_includes(source, origin.name, project_root)
    document = parse(expanded_source)

    for module_name in document.logic_modules:
        importlib.import_module(module_name)

    builder = Builder(document.rules)
    values = dict(context or {})
    values.setdefault("request", request)
    root, markup = builder.build(document, values)

    try:
        endpoint = reverse("roya-action-dispatch")
    except NoReverseMatch:
        endpoint = getattr(settings, "ROYA_ACTION_URL", "/roya/actions/")

    config = {
        "endpoint": endpoint,
        "csrf_token": get_token(request),
        "actions": builder.actions,
    }
    config_id = f"roya-actions-config-{root.id}"
    output = markup + str(json_script(config, config_id))
    if include_runtime:
        output += f'<script src="{static("roya/js/roya-actions.js")}" defer></script>'
    return mark_safe(output)
