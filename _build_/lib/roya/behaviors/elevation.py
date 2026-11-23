"""ElevationBehavior - shadow transitions."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.elevation")


class ElevationBehavior(Behavior):
    name = "elevation"

    on_change = Event("elevation:change")
    on_animate = Event("elevation:animate")

    elevation = 0

    def set_elevation(self, level: int):
        self.elevation = level
        self.on_change.emit(detail={"elevation": level})
        self.on_animate.emit(detail={"elevation": level})