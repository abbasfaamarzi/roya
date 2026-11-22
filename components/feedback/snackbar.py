"""Snackbar - transient message bar."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.feedback.snackbar")


class Snackbar(Component):
    name = "snackbar"
    template_name = "roya/components/feedback/snackbar.html"

    message = StringProperty(default="")
    supporting_text = StringProperty(default="")
    duration = IntegerProperty(default=4000)
    position = Property(type=str, default="bottom", choices=["top", "bottom"])
    action_label = StringProperty(default="")
    dismissible = BooleanProperty(default=True)
    close_button = BooleanProperty(default=True)
    variant = StringProperty(default="default")

    on_show = Event("snackbar:show")
    on_hide = Event("snackbar:hide")
    on_action = Event("snackbar:action")
    on_timeout = Event("snackbar:timeout")
    on_dismiss = Event("snackbar:dismiss")

    def show(self):
        self.on_show.emit()

    def hide(self):
        self.on_hide.emit()