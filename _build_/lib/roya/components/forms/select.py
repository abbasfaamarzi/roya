"""Select / dropdown component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, ListProperty, Property, StringProperty

logger = logging.getLogger("roya.components.forms.select")


class Select(Component):
    name = "select"
    template_name = "roya/components/forms/select.html"

    value = StringProperty(default="")
    field_name = StringProperty(default="")
    label = StringProperty(default="")
    items = ListProperty(default=list)
    multiple = BooleanProperty(default=False)
    searchable = BooleanProperty(default=False)
    variant = Property(type=str, default="outlined", choices=["outlined", "filled"])

    on_change = Event("select:change")
    on_select = Event("select:select")