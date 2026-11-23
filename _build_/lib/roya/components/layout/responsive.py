"""AdaptiveContainer - responsive layout switching."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.layout.responsive")


class AdaptiveContainer(Component):
    name = "adaptive_container"
    template_name = "roya/components/layout/responsive.html"

    mobile_layout = StringProperty(default="column")
    tablet_layout = StringProperty(default="row")
    desktop_layout = StringProperty(default="row")
    auto_switch = BooleanProperty(default=True)

    on_breakpoint_change = Event("breakpoint:change")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "mobile": self.mobile_layout,
            "tablet": self.tablet_layout,
            "desktop": self.desktop_layout,
        })
        return ctx