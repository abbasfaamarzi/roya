"""Django template tags for rendering Roya components."""
import logging

from django import template
from django.utils.safestring import mark_safe

from roya.core.registry import registry

logger = logging.getLogger("roya.templatetags")

register = template.Library()


@register.simple_tag(takes_context=True)
def roya_component(context, name: str, **kwargs):
    """Render a Roya component by name from the registry."""
    cls = registry.get(name)
    instance = cls(**kwargs)
    instance.mount()
    return mark_safe(instance.render())


@register.filter
def roya_class(component, extra: str = ""):
    base = getattr(component, "class_name", "") or ""
    return f"{base} {extra}".strip()


@register.filter
def roya_token(name: str):
    from roya.theme.manager import theme_manager
    return theme_manager.get_token(name)