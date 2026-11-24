"""Template tags for Roya.

Provides ``{% roya_component %}`` and the ``{% load roya %}`` library.
Component discovery walks ``roya.components`` and registers any class
that defines both ``name`` and ``template_name`` attributes.
"""
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

_COMPONENT_CACHE = None


def _discover_components():
    """Return {component_name: component_class} for all Roya components."""
    import importlib
    import pkgutil

    import roya.components as components_pkg

    found = {}
    for _, modname, _ in pkgutil.iter_modules(components_pkg.__path__):
        try:
            module = importlib.import_module(f"roya.components.{modname}")
        except Exception:
            continue
        for attr in dir(module):
            obj = getattr(module, attr)
            if not isinstance(obj, type):
                continue
            cname = getattr(obj, "name", None)
            tpl = getattr(obj, "template_name", None)
            if cname and tpl and cname not in {"component", "base"}:
                found[cname] = obj
    return found


def _get_component(name):
    global _COMPONENT_CACHE
    if _COMPONENT_CACHE is None:
        try:
            _COMPONENT_CACHE = _discover_components()
        except Exception:
            _COMPONENT_CACHE = {}
    return _COMPONENT_CACHE.get(name)


@register.simple_tag(takes_context=True)
def roya_component(context, name, **kwargs):
    """Render a Roya component by registered name.

    Example::

        {% roya_component "button" label="Save" variant="filled" %}
    """
    cls = _get_component(name)
    if cls is None:
        available = sorted(_COMPONENT_CACHE or {})
        raise template.TemplateSyntaxError(
            f"Unknown Roya component {name!r}. Available: {available}"
        )
    try:
        component = cls(**kwargs)
    except TypeError:
        component = cls()
        for key, value in kwargs.items():
            setattr(component, key, value)
    ctx = dict(context.flatten())
    try:
        ctx.update(component.get_context() or {})
    except AttributeError:
        pass
    html = render_to_string(
        component.template_name, ctx, request=ctx.get("request")
    )
    return mark_safe(html)
