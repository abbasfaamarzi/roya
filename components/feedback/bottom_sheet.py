"""BottomSheet - dismissible modal or persistent bottom panel."""
import logging
from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.feedback.bottom_sheet")

class BottomSheet(Component):
    name = "bottom_sheet"
    template_name = "roya/components/feedback/bottom_sheet.html"
    open = BooleanProperty(default=False)
    title = StringProperty(default="")
    dismissible = BooleanProperty(default=True)
    modal = BooleanProperty(default=True)
    max_height = StringProperty(default="85vh")
    detachable = BooleanProperty(default=True)
    backdrop = BooleanProperty(default=True)
    close_on_backdrop = BooleanProperty(default=True)
    close_on_escape = BooleanProperty(default=True)
    initial_height = StringProperty(default="40%")
    expanded_height = StringProperty(default="90%")
    collapsed_height = StringProperty(default="15%")
    bg_color = StringProperty(default="")
    corner_radius = StringProperty(default="16px")
    on_open = Event("bottom-sheet:open")
    on_close = Event("bottom-sheet:close")

    def show(self):
        if not self.open:
            self.open = True
            self.on_open.emit()

    def close(self):
        if self.open and self.dismissible:
            self.open = False
            self.on_close.emit()