"""VirtualList - fixed-row-height windowed list for large string collections."""
import json
import logging
from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import IntegerProperty, ListProperty, StringProperty
from roya.core.exceptions import ValidationError

logger = logging.getLogger("roya.components.layout.virtual_list")

class VirtualList(Component):
    name = "virtual_list"
    template_name = "roya/components/layout/virtual_list.html"
    items = ListProperty(default=list)
    item_height = IntegerProperty(default=48)
    overscan = IntegerProperty(default=3)
    aria_label = StringProperty(default="Scrollable list")
    on_item_click = Event("virtual-list:item-click")

    def _validate(self):
        super()._validate()
        if self.item_height <= 0:
            raise ValidationError("item_height must be greater than zero")
        if self.overscan < 0:
            raise ValidationError("overscan cannot be negative")
        if not all(isinstance(item, str) for item in self.items):
            raise ValidationError("VirtualList items must be strings")

    def get_context(self):
        ctx = super().get_context()
        ctx["items_json"] = json.dumps(self.items, ensure_ascii=False)
        ctx["total_count"] = len(self.items)
        ctx["total_height"] = len(self.items) * self.item_height
        return ctx
