"""IconButton component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, Property, StringProperty

logger = logging.getLogger("roya.components.actions.icon_button")


class IconButton(Component):
    name = "icon_button"
    template_name = "roya/components/actions/icon_button.html"

    icon = StringProperty(default="")
    aria_label = StringProperty(default="")
    variant = Property(type=str, default="standard",
                       choices=["standard", "filled", "tonal", "outlined"])
    selected = BooleanProperty(default=False)
    size = Property(type=str, default="medium",
                    choices=["small", "medium", "large"])

    on_click = Event("icon_button:click")
    on_toggle = Event("icon_button:toggle")

    def toggle(self):
        self.selected = not self.selected
        self.on_toggle.emit(detail={"selected": self.selected})