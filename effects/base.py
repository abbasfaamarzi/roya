"""BaseEffect for scroll and transition effects."""
import logging

from roya.core.logging import LogMixin

logger = logging.getLogger("roya.effects.base")


class BaseEffect(LogMixin):
    name = "effect"

    def __init__(self, target=None, **options):
        self.target = target
        self.options = options
        self.running = False

    def start(self):
        self.running = True

    def update(self, *args, **kwargs):
        pass

    def stop(self):
        self.running = False