"""List component with items."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, ListProperty, Property

logger = logging.getLogger("roya.components.data_display.list")


class ListComponent(Component):
    name = "list"
    template_name = "roya/components/data_display/list.html"

    items = ListProperty(default=list)
    selectable = BooleanProperty(default=False)
    selection_mode = Property(type=str, default="single",
                              choices=["single", "multiple"])
    selected_items = ListProperty(default=list)
    divider = BooleanProperty(default=False)
    dense = BooleanProperty(default=False)
    interactive = BooleanProperty(default=True)
    sortable = BooleanProperty(default=False)

    on_item_click = Event("list:item-click")
    on_item_select = Event("list:item-select")
    on_item_deselect = Event("list:item-deselect")
    on_change = Event("list:change")