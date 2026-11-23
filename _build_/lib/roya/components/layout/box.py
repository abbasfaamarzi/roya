"""FlexContainer (BoxLayout) - linear flex layout."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, ListProperty, StringProperty

logger = logging.getLogger("roya.components.layout.box")


class BoxLayout(Component):
    """Flex container: arrange children in a single row or column."""

    name = "box_layout"
    template_name = "roya/components/layout/box.html"

    direction = StringProperty(default="column")
    gap = StringProperty(default="md")
    wrap = BooleanProperty(default=False)
    justify = StringProperty(default="start")
    align = StringProperty(default="stretch")
    flex = StringProperty(default="")
    children = ListProperty(default=list)

    on_layout_change = Event("layout:change")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "flex_direction": "row" if self.direction == "row" else "column",
            "wrap": "wrap" if self.wrap else "nowrap",
            "justify": self.justify,
            "align": self.align,
            "gap": self.gap,
        })
        return ctx

    def add_child(self, child):
        super().add_child(child)
        self.on_layout_change.emit(
            detail={"action": "add", "child": getattr(child, "id", None)}
        )
        return child