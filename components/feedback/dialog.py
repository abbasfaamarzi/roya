"""Dialog - modal dialog."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.feedback.dialog")


class Dialog(Component):
    name = "dialog"
    template_name = "roya/components/feedback/dialog.html"

    open = BooleanProperty(default=False)
    title = StringProperty(default="")
    message = StringProperty(default="")
    max_width = StringProperty(default="560px")
    modal = BooleanProperty(default=True)
    dismissible = BooleanProperty(default=True)
    close_on_escape = BooleanProperty(default=True)
    close_on_outside = BooleanProperty(default=True)
    scrollable = BooleanProperty(default=False)
    persistent = BooleanProperty(default=False)

    on_before_open = Event("dialog:before-open")
    on_open = Event("dialog:open")
    on_before_close = Event("dialog:before-close")
    on_close = Event("dialog:close")
    on_confirm = Event("dialog:confirm")
    on_cancel = Event("dialog:cancel")

    def show(self):
        self.on_before_open.emit()
        self.open = True
        self.on_open.emit()

    def close(self):
        if not self.open:
            return
        self.on_before_close.emit()
        self.open = False
        self.on_close.emit()

    def confirm(self):
        self.on_confirm.emit()
        self.close()

    def cancel(self):
        self.on_cancel.emit()
        self.close()