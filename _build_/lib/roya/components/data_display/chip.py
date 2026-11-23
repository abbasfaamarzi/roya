"""Chip component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, Property, StringProperty

logger = logging.getLogger("roya.components.data_display.chip")


class Chip(Component):
    name = "chip"
    template_name = "roya/components/data_display/chip.html"

    label = StringProperty(default="")
    value = StringProperty(default="")
    selected = BooleanProperty(default=False)
    removable = BooleanProperty(default=False)
    clickable = BooleanProperty(default=True)
    leading_icon = StringProperty(default="")
    trailing_icon = StringProperty(default="")
    color = StringProperty(default="default")
    variant = Property(type=str, default="assist",
                       choices=["assist", "filter", "input", "suggestion"])

    on_click = Event("chip:click")
    on_select = Event("chip:select")
    on_deselect = Event("chip:deselect")
    on_remove = Event("chip:remove")