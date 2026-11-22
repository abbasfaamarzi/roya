"""BottomNavigationBar component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, ListProperty, Property

logger = logging.getLogger("roya.components.navigation.navbar")


class NavigationBar(Component):
    name = "navigation_bar"
    template_name = "roya/components/navigation/navbar.html"

    items = ListProperty(default=list)
    active_item = IntegerProperty(default=0)
    show_labels = BooleanProperty(default=True)
    position = Property(type=str, default="bottom", choices=["top", "bottom"])
    fixed = BooleanProperty(default=True)
    responsive = BooleanProperty(default=True)

    on_change = Event("navigation:change")
    on_select = Event("navigation:select")
    on_before_change = Event("navigation:before-change")