"""TouchBehavior - gesture recognition."""
import logging

from roya.core.events import Event
from .base import Behavior

logger = logging.getLogger("roya.behaviors.touch")


class TouchBehavior(Behavior):
    name = "touch"

    on_start = Event("touch:start")
    on_move = Event("touch:move")
    on_end = Event("touch:end")
    on_long = Event("touch:long")
    on_double = Event("touch:double")

    long_touch_duration = 500
    double_tap_interval = 300
    gesture_threshold = 10