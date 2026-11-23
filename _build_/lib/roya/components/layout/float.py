"""FloatContainer - free positioning container."""
import logging

from roya.core.component import Component
from roya.core.properties import StringProperty

logger = logging.getLogger("roya.components.layout.float")


class FloatContainer(Component):
    name = "float_container"
    template_name = "roya/components/layout/float.html"

    anchor_x = StringProperty(default="left")
    anchor_y = StringProperty(default="top")
    inset = StringProperty(default="0")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "anchor_x": self.anchor_x,
            "anchor_y": self.anchor_y,
            "inset": self.inset,
        })
        return ctx