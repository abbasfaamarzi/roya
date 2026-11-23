"""TextField - Material Design text input."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.forms.textfield")


class TextField(Component):
    """Material Design 3 text field."""

    name = "textfield"
    template_name = "roya/components/forms/textfield.html"

    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    placeholder = StringProperty(default="")
    type = Property(type=str, default="text",
                    choices=["text", "email", "password", "number", "tel", "url", "search"])
    multiline = BooleanProperty(default=False)
    rows = IntegerProperty(default=1)
    max_length = IntegerProperty(default=0)
    min_length = IntegerProperty(default=0)
    pattern = StringProperty(default="")
    helper_text = StringProperty(default="")
    error_text = StringProperty(default="")
    leading_icon = StringProperty(default="")
    trailing_icon = StringProperty(default="")
    variant = Property(type=str, default="outlined", choices=["outlined", "filled"])
    clearable = BooleanProperty(default=False)
    show_counter = BooleanProperty(default=False)

    on_input = Event("input")
    on_change = Event("change")
    on_focus = Event("focus")
    on_blur = Event("blur")
    on_validation_error = Event("validation:error")
    on_submit = Event("submit")

    def validate(self) -> bool:
        if self.required and not self.value:
            self.error_text = "This field is required"
            self.on_validation_error.emit(detail={"reason": "required"})
            return False
        return True

    def clear(self):
        self.value = ""
        self.on_change.emit(detail={"value": ""})

    def focus(self):
        self.on_focus.emit()

    def blur(self):
        self.on_blur.emit()