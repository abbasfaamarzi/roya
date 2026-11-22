"""Tabs component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, ListProperty, Property

logger = logging.getLogger("roya.components.navigation.tabs")


class Tabs(Component):
    name = "tabs"
    template_name = "roya/components/navigation/tabs.html"

    items = ListProperty(default=list)
    active_tab = IntegerProperty(default=0)
    orientation = Property(type=str, default="horizontal",
                           choices=["horizontal", "vertical"])
    scrollable = BooleanProperty(default=False)
    centered = BooleanProperty(default=False)
    lazy_load = BooleanProperty(default=True)
    preserve_state = BooleanProperty(default=True)
    variant = Property(type=str, default="primary", choices=["primary", "secondary"])

    on_change = Event("tab:change")
    on_select = Event("tab:select")
    on_before_change = Event("tab:before-change")
    on_loaded = Event("tab:loaded")

    def select(self, index: int):
        self.on_before_change.emit(detail={"index": index})
        self.active_tab = index
        self.on_select.emit(detail={"index": index})
        self.on_change.emit(detail={"index": index})