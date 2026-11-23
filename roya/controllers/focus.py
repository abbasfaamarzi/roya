"""FocusController - global focus management."""
import logging

from roya.core.events import Event
from .base import BaseController

logger = logging.getLogger("roya.controllers.focus")


class FocusController(BaseController):
    name = "focus"

    on_change = Event("focus:change")
    on_enter = Event("focus:enter")
    on_leave = Event("focus:leave")

    def __init__(self, **options):
        super().__init__(**options)
        self.active_element = None
        self.trap_focus = False

    def set_active(self, element_id: str):
        old = self.active_element
        self.active_element = element_id
        self.on_change.emit(detail={"old": old, "new": element_id})