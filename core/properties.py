"""Declarative, type-checked Property descriptors."""
import logging
from typing import Any, Callable, Iterable

from .exceptions import PropertyError, ValidationError

logger = logging.getLogger("roya.core.properties")


class Property:
    """Declarative, type-checked, validated component property."""

    def __init__(self, type=None, default=None, choices: Iterable = None,
                 validator: Callable[[Any], bool] = None, required: bool = False,
                 doc: str = "", on_change: Callable = None):
        self.type = type
        self.default = default
        self.choices = list(choices) if choices else None
        self.validator = validator
        self.required = required
        self.doc = doc
        self.on_change = on_change
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        private = f"_prop_{self.name}"
        if not hasattr(obj, private):
            setattr(obj, private, self._clone_default())
        return getattr(obj, private)

    def __set__(self, obj, value):
        self.validate(value)
        private = f"_prop_{self.name}"
        old = getattr(obj, private, None)
        if old == value:
            return
        setattr(obj, private, value)
        logger.debug("%s.%s: %r -> %r", obj.__class__.__name__, self.name, old, value)
        if self.on_change:
            self.on_change(obj, value)

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError(f"{self.name} is required")
        if value is None and not self.required:
            return
        if self.type is not None and not isinstance(value, self.type):
            raise PropertyError(
                f"{self.name}: expected {getattr(self.type, '__name__', self.type)}, "
                f"got {type(value).__name__}"
            )
        if self.choices is not None and value not in self.choices:
            raise PropertyError(f"{self.name}: value {value!r} not in {self.choices}")
        if self.validator is not None and not self.validator(value):
            raise ValidationError(f"{self.name}: validator rejected {value!r}")

    def _clone_default(self):
        if callable(self.default):
            try:
                return self.default()
            except TypeError:
                return self.default
        return self.default


class BooleanProperty(Property):
    def __init__(self, default: bool = False, **kw):
        super().__init__(type=bool, default=default, **kw)


class StringProperty(Property):
    def __init__(self, default: str = "", **kw):
        super().__init__(type=str, default=default, **kw)


class IntegerProperty(Property):
    def __init__(self, default: int = 0, **kw):
        super().__init__(type=int, default=default, **kw)


class ListProperty(Property):
    def __init__(self, default=None, **kw):
        super().__init__(type=list, default=default or list, **kw)


class DictProperty(Property):
    def __init__(self, default=None, **kw):
        super().__init__(type=dict, default=default or dict, **kw)