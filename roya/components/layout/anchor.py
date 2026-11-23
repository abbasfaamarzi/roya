"""AnchorContainer - place child relative to parent anchors."""
import logging

from roya.core.component import Component
from roya.core.properties import StringProperty

logger = logging.getLogger("roya.components.layout.anchor")


class AnchorContainer(Component):
    name = "anchor_container"
    template_name = "roya/components/layout/anchor.html"

    horizontal_anchor = StringProperty(default="center")
    vertical_anchor = StringProperty(default="center")
    offset_x = StringProperty(default="0")
    offset_y = StringProperty(default="0")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "ha": self.horizontal_anchor,
            "va": self.vertical_anchor,
            "ox": self.offset_x,
            "oy": self.offset_y,
        })
        return ctx