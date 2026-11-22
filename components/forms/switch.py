"""Switch component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.forms.switch")


class Switch(Component):
    name = "switch"
    template_name = "roya/components/forms/switch.html"

    checked = BooleanProperty(default=False)
    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    color = StringProperty(default="primary")
    size = StringProperty(default="medium")

    on_change = Event("switch:change")
    on_on = Event("switch:on")
    on_off = Event("switch:off")

    def toggle(self):
        self.checked = not self.checked
        self.on_change.emit(detail={"checked": self.checked})
        (self.on_on if self.checked else self.on_off).emit()