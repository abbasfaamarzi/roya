"""MotionBehavior - animated transitions."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.motion")


class MotionBehavior(Behavior):
    name = "motion"

    on_start = Event("motion:start")
    on_progress = Event("motion:progress")
    on_end = Event("motion:end")
    on_cancel = Event("motion:cancel")

    duration = 300
    easing = "standard"
    motion_type = "fade"

    def start(self):
        self.on_start.emit()
        self.on_progress.emit(detail={"progress": 0.5})
        self.on_end.emit()

    def cancel(self):
        self.on_cancel.emit()