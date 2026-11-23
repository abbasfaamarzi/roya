"""ResponsiveController - adapts layout to breakpoints."""
import logging

from roya.core.events import Event
from roya.foundation.breakpoints import Breakpoints
from .base import BaseController

logger = logging.getLogger("roya.controllers.responsive")


class ResponsiveController(BaseController):
    name = "responsive"

    on_change = Event("responsive:change")
    on_breakpoint_change = Event("breakpoint:change")

    def __init__(self, **options):
        super().__init__(**options)
        self.current_breakpoint = "xs"
        self.container_width = 0

    def adapt(self, width: int):
        bp = Breakpoints.for_width(width)
        if bp != self.current_breakpoint:
            old = self.current_breakpoint
            self.current_breakpoint = bp
            self.on_breakpoint_change.emit(detail={"old": old, "new": bp})
            self.on_change.emit(detail={"breakpoint": bp})