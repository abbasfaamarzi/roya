"""Checkbox component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.forms.checkbox")


class Checkbox(Component):
    name = "checkbox"
    template_name = "roya/components/forms/checkbox.html"

    checked = BooleanProperty(default=False)
    indeterminate = BooleanProperty(default=False)
    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    color = StringProperty(default="primary")

    on_change = Event("change")
    on_check = Event("check")
    on_uncheck = Event("uncheck")

    def toggle(self):
        self.checked = not self.checked
        self.on_change.emit(detail={"checked": self.checked})
        (self.on_check if self.checked else self.on_uncheck).emit()