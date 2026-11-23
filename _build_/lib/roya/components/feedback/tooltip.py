"""Tooltip component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.feedback.tooltip")


class Tooltip(Component):
    name = "tooltip"
    template_name = "roya/components/feedback/tooltip.html"

    text = StringProperty(default="")
    title = StringProperty(default="")
    placement = Property(type=str, default="top",
                         choices=["top", "bottom", "start", "end"])
    trigger = Property(type=str, default="hover",
                       choices=["hover", "focus", "click", "manual"])
    delay = IntegerProperty(default=200)
    duration = IntegerProperty(default=0)
    interactive = BooleanProperty(default=False)

    on_show = Event("tooltip:show")
    on_hide = Event("tooltip:hide")