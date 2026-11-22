"""Base Behavior - composable capability for components."""
import logging

from roya.core.logging import LogMixin
from roya.core.state import StateStore

logger = logging.getLogger("roya.behaviors.base")


class Behavior(LogMixin):
    """Base class for all Roya behaviors."""

    name = "behavior"

    def __init__(self, component=None, **options):
        self.component = component
        self.options = options
        self.state = StateStore(options)

    def attach(self, component):
        self.component = component
        self.on_attach()
        return self

    def detach(self):
        self.on_detach()
        self.component = None

    def on_attach(self):
        pass

    def on_detach(self):
        pass