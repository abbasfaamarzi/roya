"""Page transition effects."""
import logging

from roya.core.events import Event
from .base import BaseEffect

logger = logging.getLogger("roya.effects.transition")


class TransitionEffect(BaseEffect):
    name = "transition"

    on_start = Event("transition:start")
    on_progress = Event("transition:progress")
    on_complete = Event("transition:complete")
    on_cancel = Event("transition:cancel")

    def __init__(self, target=None, transition_type="fade", duration=300,
                 easing="standard", **options):
        super().__init__(target, **options)
        self.transition_type = transition_type
        self.duration = duration
        self.easing = easing

    def start(self):
        super().start()
        self.on_start.emit(detail={"type": self.transition_type})
        self.on_complete.emit()