"""Event system: payload, events, global bus."""
import logging
import time
from typing import Any, Callable, Dict, List

logger = logging.getLogger("roya.core.events")


class EventPayload:
    """Serializable payload for every Roya event."""

    def __init__(self, type: str, component_id: str = None, detail: dict = None,
                 source: Any = None, native_event: Any = None):
        self.type = type
        self.component_id = component_id
        self.timestamp = time.time()
        self.detail = detail or {}
        self.source = source
        self.native_event = native_event
        self.cancelled = False

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "componentId": self.component_id,
            "timestamp": self.timestamp,
            "detail": self.detail,
        }

    def cancel(self):
        self.cancelled = True


class Event:
    """Declarative event that a component emits."""

    def __init__(self, name: str, cancelable: bool = False, doc: str = ""):
        self.name = name
        self.cancelable = cancelable
        self.doc = doc
        self._listeners: List[Callable] = []

    def __set_name__(self, owner, name):
        self.attr_name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, "_evt_map"):
            obj._evt_map = {}
        if self.name not in obj._evt_map:
            obj._evt_map[self.name] = _BoundEvent(obj, self)
        return obj._evt_map[self.name]


class _BoundEvent:
    def __init__(self, owner, event: Event):
        self.owner = owner
        self.event = event
        self._listeners: List[Callable] = []

    def subscribe(self, handler: Callable) -> Callable:
        self._listeners.append(handler)
        return handler

    def unsubscribe(self, handler: Callable):
        if handler in self._listeners:
            self._listeners.remove(handler)

    def emit(self, detail: dict = None, native_event=None) -> EventPayload:
        payload = EventPayload(
            type=self.event.name,
            component_id=getattr(self.owner, "id", None),
            detail=detail,
            source=self.owner,
            native_event=native_event,
        )
        logger.debug("Emit %s from %s", self.event.name, self.owner)
        for handler in list(self._listeners):
            handler(payload)
            if payload.cancelled:
                break
        return payload


class EventBus:
    """Global pub/sub used across components, behaviors, controllers."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def on(self, event_type: str, handler: Callable) -> Callable:
        self._handlers.setdefault(event_type, []).append(handler)
        return handler

    def off(self, event_type: str, handler: Callable):
        handlers = self._handlers.get(event_type, [])
        if handler in handlers:
            handlers.remove(handler)

    def emit(self, payload: EventPayload):
        for handler in list(self._handlers.get(payload.type, [])):
            handler(payload)
        for handler in list(self._handlers.get("*", [])):
            handler(payload)

    def clear(self):
        self._handlers.clear()


bus = EventBus()