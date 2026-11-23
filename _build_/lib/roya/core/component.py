"""Base Component for all Roya components."""
import uuid
import logging
from typing import Any, Dict

from .events import Event, EventPayload, bus
from .exceptions import ComponentError
from .lifecycle import Lifecycle, LifecycleState
from .logging import LogMixin
from .properties import (
    BooleanProperty, DictProperty, Property, StringProperty,
)
from .state import StateStore

logger = logging.getLogger("roya.core.component")


class Component(LogMixin):
    """Abstract base for every Roya component.

    Object-oriented, declarative, observable and lifecycle-managed.
    """

    name = "component"
    template_name = None

    id = StringProperty(default="")
    class_name = StringProperty(default="")
    variant = StringProperty(default="default")
    size = StringProperty(default="medium")
    color = StringProperty(default="primary")
    disabled = BooleanProperty(default=False)
    hidden = BooleanProperty(default=False)
    visible = BooleanProperty(default=True)
    loading = BooleanProperty(default=False)
    readonly = BooleanProperty(default=False)
    required = BooleanProperty(default=False)
    role = StringProperty(default="")
    aria_label = StringProperty(default="")
    theme = StringProperty(default="inherited")
    direction = StringProperty(default="auto")
    responsive = BooleanProperty(default=True)
    animation = BooleanProperty(default=True)
    data = DictProperty(default=dict)

    on_mount = Event("component:mount")
    on_ready = Event("component:ready")
    on_update = Event("component:update")
    on_unmount = Event("component:unmount")

    def __init__(self, **kwargs):
        self._id = kwargs.pop("id", None) or f"roya-{uuid.uuid4().hex[:8]}"
        self.id = self._id
        self.children = []
        self.parent = None
        self.state = StateStore()
        self.lifecycle = Lifecycle(self)

        for key, value in kwargs.items():
            if not hasattr(self.__class__, key):
                raise ComponentError(f"{self.__class__.__name__}: unknown property '{key}'")
            setattr(self, key, value)

        self.lifecycle.transition(LifecycleState.INITIALIZED)
        self._validate()
        self.lifecycle.transition(LifecycleState.VALIDATED)
        logger.debug("Instantiated %s [%s]", self.__class__.__name__, self._id)

    def _validate(self):
        for attr_name, attr in vars(self.__class__).items():
            if isinstance(attr, Property):
                attr.validate(getattr(self, attr_name))

    def render(self) -> str:
        if self.lifecycle.is_(LifecycleState.VALIDATED):
            self.lifecycle.transition(LifecycleState.RENDERED)
        return self._render()

    def _render(self) -> str:
        if not self.template_name:
            return self._fallback_render()
        try:
            from django.template.loader import render_to_string
            return render_to_string(self.template_name, self.get_context())
        except Exception as exc:
            logger.warning("Template '%s' failed for %s: %s", self.template_name, self, exc)
            return self._fallback_render()

    def _fallback_render(self) -> str:
        classes = f"roya-component {self.class_name}".strip()
        return (
            f'<div id="{self.id}" class="{classes}" '
            f'data-roya-component="{self.name}"></div>'
        )

    def get_context(self) -> Dict[str, Any]:
        context = {"component": self, "children": self.children}
        for klass in type(self).__mro__:
            for attr_name, attr in vars(klass).items():
                if isinstance(attr, Property) and attr_name not in context:
                    context[attr_name] = getattr(self, attr_name)
        return context

    def mount(self):
        if not self.lifecycle.is_(LifecycleState.RENDERED, LifecycleState.READY):
            self.render()
        if self.lifecycle.is_(LifecycleState.RENDERED):
            self.lifecycle.transition(LifecycleState.MOUNTED)
            self.on_mount.emit()
            self.lifecycle.transition(LifecycleState.READY)
            self.on_ready.emit()
            bus.emit(self._event("component:mount"))

    def unmount(self):
        if self.lifecycle.is_(LifecycleState.UNMOUNTED, LifecycleState.DESTROYED):
            return
        self.on_unmount.emit()
        self.lifecycle.transition(LifecycleState.UNMOUNTED)
        bus.emit(self._event("component:unmount"))

    def destroy(self):
        self.unmount()
        if self.lifecycle.is_(LifecycleState.UNMOUNTED):
            self.lifecycle.transition(LifecycleState.DESTROYED)

    def add_child(self, child: "Component") -> "Component":
        child.parent = self
        self.children.append(child)
        return child

    def remove_child(self, child: "Component"):
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def set_state(self, key: str, value: Any):
        self.state.set(key, value)

    def get_state(self, key: str, default=None):
        return self.state.get(key, default)

    def _event(self, event_type: str) -> EventPayload:
        return EventPayload(type=event_type, component_id=self.id, source=self)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"