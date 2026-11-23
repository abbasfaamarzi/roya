"""Scroll effects including StiffScrollEffect."""
import logging

from roya.core.events import Event
from .base import BaseEffect

logger = logging.getLogger("roya.effects.scroll")


class StiffScrollEffect(BaseEffect):
    """Resists scroll near boundaries (KivyMD StiffScrollEffect port)."""

    name = "stiff_scroll"

    on_start = Event("effect:start")
    on_update = Event("effect:update")
    on_stop = Event("effect:stop")
    on_boundary_reached = Event("effect:boundary-reached")

    def __init__(self, target=None, drag_threshold=5, min_scroll=0,
                 max_scroll=0, max_friction=0.6, body=0.5, **options):
        super().__init__(target, **options)
        self.drag_threshold = drag_threshold
        self.min_scroll = min_scroll
        self.max_scroll = max_scroll
        self.max_friction = max_friction
        self.body = body

    def update(self, scroll: float, velocity: float = 0):
        if scroll <= self.min_scroll or scroll >= self.max_scroll:
            friction = min(abs(velocity) * self.max_friction, self.max_friction)
            self.on_boundary_reached.emit(detail={"friction": friction})
        self.on_update.emit(detail={"scroll": scroll, "velocity": velocity})


class SmoothScrollEffect(BaseEffect):
    name = "smooth_scroll"

    def update(self, scroll: float, target: float = None):
        pass


class SnapScrollEffect(BaseEffect):
    name = "snap_scroll"

    def __init__(self, target=None, snap_points=None, **options):
        super().__init__(target, **options)
        self.snap_points = snap_points or []


class OverscrollEffect(BaseEffect):
    name = "overscroll"