"""RelativeContainer - position children relative to parent."""
import logging

from roya.core.component import Component
from roya.core.properties import IntegerProperty, StringProperty

logger = logging.getLogger("roya.components.layout.relative")


class RelativeContainer(Component):
    name = "relative_container"
    template_name = "roya/components/layout/relative.html"

    top = StringProperty(default="auto")
    right = StringProperty(default="auto")
    bottom = StringProperty(default="auto")
    left = StringProperty(default="auto")
    z_index = IntegerProperty(default=0)

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "top": self.top, "right": self.right,
            "bottom": self.bottom, "left": self.left,
            "z_index": self.z_index,
        })
        return ctx