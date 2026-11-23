"""NavigationController - route history and navigation."""
import logging

from roya.core.events import Event
from .base import BaseController

logger = logging.getLogger("roya.controllers.navigation")


class NavigationController(BaseController):
    name = "navigation"

    on_route_change = Event("route:change")
    on_route_before_change = Event("route:before-change")
    on_route_error = Event("route:error")

    def __init__(self, **options):
        super().__init__(**options)
        self.current_route = None
        self.history = []

    def navigate(self, route: str):
        self.on_route_before_change.emit(detail={"route": route})
        if self.current_route:
            self.history.append(self.current_route)
        self.current_route = route
        self.on_route_change.emit(detail={"route": route})

    def back(self):
        if self.history:
            self.current_route = self.history.pop()
            self.on_route_change.emit(detail={"route": self.current_route})