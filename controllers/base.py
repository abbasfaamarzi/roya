"""BaseController - shared lifecycle for all controllers."""
import logging

from roya.core.logging import LogMixin
from roya.core.state import StateStore

logger = logging.getLogger("roya.controllers.base")


class BaseController(LogMixin):
    name = "controller"

    def __init__(self, **options):
        self.state = StateStore(options)
        self._started = False

    def start(self):
        if not self._started:
            self._started = True
            self.on_start()

    def stop(self):
        if self._started:
            self._started = False
            self.on_stop()

    def on_start(self):
        pass

    def on_stop(self):
        pass