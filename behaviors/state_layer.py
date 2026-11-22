"""StateLayerBehavior - Material state layer visualization."""
import logging

from core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.state_layer")


class StateLayerBehavior(Behavior):
    name = "state_layer"

    on_change = Event("state-layer:change")

    state_layer_color = "on_surface"
    state_layer_opacity = {
        "hovered": 0.08, "focused": 0.12,
        "pressed": 0.12, "dragged": 0.16, "disabled": 0.38,
    }

    def set_state(self, state: str):
        self.on_change.emit(detail={"state": state})
