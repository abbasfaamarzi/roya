"""Server-side Python actions callable from .roya event bindings."""
from .registry import action, action_registry

__all__ = ["action", "action_registry"]
