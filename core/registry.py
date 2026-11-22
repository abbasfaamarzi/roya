"""Component registry."""
import logging
from typing import Dict, List, Type

from .exceptions import RegistryError

logger = logging.getLogger("roya.core.registry")


class ComponentRegistry:
    """Global registry mapping component names to classes."""

    def __init__(self):
        self._components: Dict[str, Type] = {}

    def register(self, cls: Type, name: str = None) -> Type:
        key = (name or getattr(cls, "name", None) or cls.__name__).lower()
        if key in self._components and self._components[key] is not cls:
            raise RegistryError(f"Component '{key}' already registered")
        self._components[key] = cls
        logger.debug("Registered component: %s", key)
        return cls

    def unregister(self, name: str):
        self._components.pop(name.lower(), None)

    def get(self, name: str) -> Type:
        key = name.lower()
        if key not in self._components:
            raise RegistryError(f"Component '{name}' not found")
        return self._components[key]

    def has(self, name: str) -> bool:
        return name.lower() in self._components

    def list(self) -> List[str]:
        return sorted(self._components.keys())

    def count(self) -> int:
        return len(self._components)

    def clear(self):
        self._components.clear()


registry = ComponentRegistry()