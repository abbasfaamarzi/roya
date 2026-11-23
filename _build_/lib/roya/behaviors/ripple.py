"""RippleBehavior - Material touch feedback."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.ripple")


class RippleBehavior(Behavior):
    name = "ripple"

    on_start = Event("ripple:start")
    on_end = Event("ripple:end")

    ripple = True
    ripple_color = "on_surface"
    ripple_duration = 400
    ripple_origin = "center"

    def trigger(self, x=None, y=None):
        self.on_start.emit(detail={"x": x, "y": y})
        self.on_end.emit()