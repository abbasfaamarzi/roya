"""ScrollContainer - scrollable wrapper."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, StringProperty

logger = logging.getLogger("roya.components.layout.scroll")


class ScrollContainer(Component):
    name = "scroll_container"
    template_name = "roya/components/layout/scroll.html"

    direction = StringProperty(default="vertical")
    smooth = BooleanProperty(default=True)
    scrollbar = BooleanProperty(default=True)
    overscroll = StringProperty(default="auto")
    max_scroll = IntegerProperty(default=0)

    on_scroll = Event("scroll")
    on_scroll_start = Event("scroll:start")
    on_scroll_end = Event("scroll:end")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({
            "scroll_direction": self.direction,
            "smooth": "smooth" if self.smooth else "auto",
            "show_scrollbar": self.scrollbar,
        })
        return ctx