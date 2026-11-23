"""ThemeController - proxies theme changes."""
import logging

from roya.core.events import Event
from roya.theme.manager import theme_manager
from .base import BaseController

logger = logging.getLogger("roya.controllers.theme")


class ThemeController(BaseController):
    name = "theme"

    on_change = Event("theme:change")
    on_loaded = Event("theme:loaded")
    on_error = Event("theme:error")

    def __init__(self, **options):
        super().__init__(**options)
        self.manager = theme_manager

    def switch(self):
        self.manager.switch_theme()
        self.on_change.emit(detail={"mode": self.manager.theme_mode})