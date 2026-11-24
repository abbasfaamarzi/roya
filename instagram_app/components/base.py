"""Small adapter that renders real registered Roya components."""
from roya.core.properties import Property
from roya.core.registry import registry


def _properties(component_class):
    result = {}
    for base in component_class.__mro__:
        for name, descriptor in vars(base).items():
            if isinstance(descriptor, Property):
                result.setdefault(name, descriptor)
    return result


def roya_html(name, **props):
    try:
        component_class = registry.get(name)
        if component_class is None:
            return ""
        accepted = _properties(component_class)
        instance = component_class(**{key: value for key, value in props.items() if key in accepted})
        mount = getattr(instance, "mount", None)
        if callable(mount):
            mount()
        return str(instance.render())
    except Exception:
        # A widget still has semantic HTML fallback in its template.
        return ""
