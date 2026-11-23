"""NavigationDrawer component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, ListProperty, Property, StringProperty

logger = logging.getLogger("roya.components.navigation.drawer")


class NavigationDrawer(Component):
    name = "navigation_drawer"
    template_name = "roya/components/navigation/drawer.html"

    open = BooleanProperty(default=False)
    position = Property(type=str, default="start", choices=["start", "end", "bottom"])
    mode = Property(type=str, default="modal",
                    choices=["modal", "standard", "dismissible"])
    width = StringProperty(default="360px")
    mini = BooleanProperty(default=False)
    modal = BooleanProperty(default=True)
    auto_close = BooleanProperty(default=True)
    overlay = BooleanProperty(default=True)
    selected_item = StringProperty(default="")
    items = ListProperty(default=list)

    on_open = Event("drawer:open")
    on_close = Event("drawer:close")
    on_before_open = Event("drawer:before-open")
    on_before_close = Event("drawer:before-close")
    on_item_select = Event("drawer:item-select")

    def show(self):
        self.on_before_open.emit()
        self.open = True
        self.on_open.emit()

    def hide(self):
        self.on_before_close.emit()
        self.open = False
        self.on_close.emit()