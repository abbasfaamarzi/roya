"""ViewportController - viewport size and orientation tracking."""
import logging

from roya.core.events import Event
from roya.foundation.breakpoints import Breakpoints
from .base import BaseController

logger = logging.getLogger("roya.controllers.viewport")


class ViewportController(BaseController):
    name = "viewport"

    on_resize = Event("viewport:resize")
    on_orientation_change = Event("viewport:orientation-change")
    on_breakpoint_change = Event("viewport:breakpoint-change")

    def __init__(self, **options):
        super().__init__(**options)
        self.viewport_width = 0
        self.viewport_height = 0
        self.pixel_ratio = 1.0
        self.current_breakpoint = "xs"

    def update(self, width: int, height: int, pixel_ratio: float = 1.0):
        old_bp = self.current_breakpoint
        self.viewport_width = width
        self.viewport_height = height
        self.pixel_ratio = pixel_ratio
        self.current_breakpoint = Breakpoints.for_width(width)
        self.on_resize.emit(detail={"width": width, "height": height})
        if old_bp != self.current_breakpoint:
            self.on_breakpoint_change.emit(
                detail={"old": old_bp, "new": self.current_breakpoint}
            )

    def get_orientation(self) -> str:
        return "landscape" if self.viewport_width >= self.viewport_height else "portrait"

    def get_breakpoint(self) -> str:
        return self.current_breakpoint