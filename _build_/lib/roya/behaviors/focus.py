"""FocusBehavior - keyboard focus ring management."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.focus")


class FocusBehavior(Behavior):
    name = "focus"

    on_enter = Event("focus:enter")
    on_leave = Event("focus:leave")
    on_change = Event("focus:change")

    focused = False
    focus_visible = False

    def focus(self):
        self.focused = True
        self.on_enter.emit()
        self.on_change.emit(detail={"focused": True})

    def blur(self):
        self.focused = False
        self.on_leave.emit()
        self.on_change.emit(detail={"focused": False})