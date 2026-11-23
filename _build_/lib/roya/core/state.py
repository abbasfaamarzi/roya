"""Reactive key/value state store."""
import logging
from typing import Any, Callable, Dict, List

logger = logging.getLogger("roya.core.state")


class StateStore:
    """Observable key/value store with change notifications."""

    def __init__(self, initial: Dict[str, Any] = None):
        self._data: Dict[str, Any] = dict(initial or {})
        self._subscribers: List[Callable[[str, Any, Any], None]] = []

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any):
        old = self._data.get(key)
        if old == value:
            return
        self._data[key] = value
        logger.debug("State[%s]: %r -> %r", key, old, value)
        for sub in list(self._subscribers):
            sub(key, old, value)

    def update(self, mapping: Dict[str, Any]):
        for key, value in mapping.items():
            self.set(key, value)

    def subscribe(self, callback: Callable[[str, Any, Any], None]):
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._data)

    def reset(self, initial: Dict[str, Any] = None):
        self._data = dict(initial or {})