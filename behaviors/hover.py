"""HoverBehavior - hover state tracking."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.hover")


class HoverBehavior(Behavior):
    name = "hover"

    on_enter = Event("hover:enter")
    on_leave = Event("hover:leave")
    on_change = Event("hover:change")

    hovering = False
    hover_color = "primary"
    hover_scale = 1.0

    def enter(self):
        self.hovering = True
        self.on_enter.emit(detail={"target": getattr(self.component, "id", None)})
        self.on_change.emit(detail={"hovering": True})

    def leave(self):
        self.hovering = False
        self.on_leave.emit(detail={"target": getattr(self.component, "id", None)})
        self.on_change.emit(detail={"hovering": False})