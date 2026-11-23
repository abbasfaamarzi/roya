"""StackContainer - stacking layout with wrap."""
import logging

from roya.core.component import Component
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.layout.stack")


class StackContainer(Component):
    name = "stack_container"
    template_name = "roya/components/layout/stack.html"

    direction = StringProperty(default="row")
    gap = StringProperty(default="md")
    wrap = BooleanProperty(default=True)
    alignment = StringProperty(default="start")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "stack_direction": self.direction,
            "gap": self.gap,
            "wrap": "wrap" if self.wrap else "nowrap",
            "alignment": self.alignment,
        })
        return ctx