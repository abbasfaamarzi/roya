"""NavigationRail component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, ListProperty, Property, StringProperty

logger = logging.getLogger("roya.components.navigation.rail")


class NavigationRail(Component):
    name = "navigation_rail"
    template_name = "roya/components/navigation/rail.html"

    items = ListProperty(default=list)
    selected_item = StringProperty(default="")
    expanded = BooleanProperty(default=False)
    position = Property(type=str, default="start", choices=["start", "end"])
    label_mode = Property(type=str, default="selected",
                          choices=["selected", "all", "none"])
    show_fab = BooleanProperty(default=False)

    on_select = Event("navigation:select")
    on_change = Event("navigation:change")
    on_expand = Event("rail:expand")
    on_collapse = Event("rail:collapse")