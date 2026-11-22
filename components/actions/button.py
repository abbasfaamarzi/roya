"""Button - Material Design 3 button with all variants."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, Property, StringProperty

logger = logging.getLogger("roya.components.actions.button")


class Button(Component):
    """Material Design 3 Button with all standard variants."""

    name = "button"
    template_name = "roya/components/actions/button.html"

    label = StringProperty(default="")
    variant = Property(type=str, default="filled",
                       choices=["filled", "elevated", "outlined", "text", "tonal"])
    size = Property(type=str, default="medium",
                    choices=["small", "medium", "large"])
    color = StringProperty(default="primary")
    icon = StringProperty(default="")
    icon_position = Property(type=str, default="start", choices=["start", "end"])
    icon_only = BooleanProperty(default=False)
    full_width = BooleanProperty(default=False)
    href = StringProperty(default="")
    target = StringProperty(default="")
    type = Property(type=str, default="button",
                    choices=["button", "submit", "reset"])
    ripple = BooleanProperty(default=True)
    elevation = Property(type=int, default=0)
    rounded = BooleanProperty(default=True)

    on_click = Event("button:click", cancelable=True)
    on_press = Event("button:press")
    on_release = Event("button:release")
    on_focus = Event("button:focus")
    on_blur = Event("button:blur")

    def click(self):
        payload = self.on_click.emit()
        logger.debug("Button clicked: %s", self.id)
        return payload

    def set_loading(self, value: bool = True):
        self.loading = value

    def get_context(self):
        ctx = super().get_context()
        classes = [
            "roya-button", f"roya-button--{self.variant}",
            f"roya-button--{self.size}",
        ]
        if self.full_width:
            classes.append("roya-button--full-width")
        if self.icon_only:
            classes.append("roya-button--icon-only")
        if self.rounded:
            classes.append("roya-button--rounded")
        ctx["classes"] = " ".join(classes)
        return ctx