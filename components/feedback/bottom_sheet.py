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
