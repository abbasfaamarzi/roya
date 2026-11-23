"""DatePicker - accessible native date input with Roya events."""
import logging
from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.forms.date_picker")

class DatePicker(Component):
    name = "date_picker"
    template_name = "roya/components/forms/date_picker.html"
    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    min_date = StringProperty(default="")
    max_date = StringProperty(default="")
    helper_text = StringProperty(default="")
    required = BooleanProperty(default=False)
    clearable = BooleanProperty(default=False)
    on_change = Event("date-picker:change")
    on_input = Event("date-picker:input")

    def set_value(self, value: str):
        self.value = value
        self.on_change.emit(detail={"value": value})
        return self.value
