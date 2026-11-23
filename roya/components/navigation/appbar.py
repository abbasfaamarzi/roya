"""AppBar - top application bar."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, ListProperty, Property, StringProperty

logger = logging.getLogger("roya.components.navigation.appbar")


class AppBar(Component):
    name = "appbar"
    template_name = "roya/components/navigation/appbar.html"

    title = StringProperty(default="")
    subtitle = StringProperty(default="")
    position = Property(type=str, default="top", choices=["top", "bottom"])
    fixed = BooleanProperty(default=True)
    sticky = BooleanProperty(default=True)
    elevation = IntegerProperty(default=2)
    scroll_behavior = Property(type=str, default="elevate",
                               choices=["elevate", "collapse", "hide"])
    variant = Property(type=str, default="small",
                       choices=["small", "medium", "large", "center-aligned"])
    left_icon = StringProperty(default="menu")
    right_icons = ListProperty(default=list)
    bg_color = StringProperty(default="")
    text_color = StringProperty(default="")

    on_action = Event("appbar:action")
    on_menu_open = Event("appbar:menu-open")
    on_menu_close = Event("appbar:menu-close")
    on_scroll = Event("appbar:scroll")
    on_collapse = Event("appbar:collapse")