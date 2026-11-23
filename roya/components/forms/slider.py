"""Slider component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property

logger = logging.getLogger("roya.components.forms.slider")


class Slider(Component):
    name = "slider"
    template_name = "roya/components/forms/slider.html"

    value = IntegerProperty(default=0)
    min = IntegerProperty(default=0)
    max = IntegerProperty(default=100)
    step = IntegerProperty(default=1)
    orientation = Property(type=str, default="horizontal",
                           choices=["horizontal", "vertical"])
    show_value = BooleanProperty(default=False)
    range = BooleanProperty(default=False)

    on_input = Event("input")
    on_change = Event("change")
    on_slide_start = Event("slide:start")
    on_slide_end = Event("slide:end")