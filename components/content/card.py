"""Card - Material Design container."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.content.card")


class Card(Component):
    name = "card"
    template_name = "roya/components/content/card.html"

    variant = Property(type=str, default="elevated",
                       choices=["elevated", "filled", "outlined", "swipeable"])
    elevation = IntegerProperty(default=1)
    radius = StringProperty(default="md")
    padding = StringProperty(default="md")
    clickable = BooleanProperty(default=False)
    selected = BooleanProperty(default=False)
    swipeable = BooleanProperty(default=False)
    swipe_direction = StringProperty(default="end")

    on_click = Event("card:click")
    on_select = Event("card:select")
    on_swipe = Event("card:swipe")

    def get_context(self):
        ctx = super().get_context()
        classes = ["roya-card", f"roya-card--{self.variant}"]
        if self.clickable:
            classes.append("roya-card--clickable")
        if self.selected:
            classes.append("roya-card--selected")
        ctx["classes"] = " ".join(classes)
        return ctx