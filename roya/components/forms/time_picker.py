"""TimePicker - accessible native time input with Roya events."""
import logging
from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.forms.time_picker")

class TimePicker(Component):
    name = "time_picker"
    template_name = "roya/components/forms/time_picker.html"
    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    min_time = StringProperty(default="")
    max_time = StringProperty(default="")
    step = StringProperty(default="")
    helper_text = StringProperty(default="")
    required = BooleanProperty(default=False)
    on_change = Event("time-picker:change")
    on_input = Event("time-picker:input")

    def set_value(self, value: str):
        self.value = value
        self.on_change.emit(detail={"value": value})
        return self.value
