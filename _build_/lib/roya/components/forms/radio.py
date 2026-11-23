"""RadioGroup component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import ListProperty, StringProperty

logger = logging.getLogger("roya.components.forms.radio")


class RadioGroup(Component):
    name = "radio_group"
    template_name = "roya/components/forms/radio.html"

    value = StringProperty(default="")
    field_name = StringProperty(default="")
    options = ListProperty(default=list)
    direction = StringProperty(default="column")

    on_change = Event("radio:change")