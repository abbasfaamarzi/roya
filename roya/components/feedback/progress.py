"""Progress indicator."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.feedback.progress")


class Progress(Component):
    name = "progress"
    template_name = "roya/components/feedback/progress.html"

    value = IntegerProperty(default=0)
    min = IntegerProperty(default=0)
    max = IntegerProperty(default=100)
    indeterminate = BooleanProperty(default=False)
    buffer = IntegerProperty(default=0)
    thickness = StringProperty(default="4px")
    variant = Property(type=str, default="linear", choices=["linear", "circular"])
    color = StringProperty(default="primary")

    on_change = Event("progress:change")
    on_complete = Event("progress:complete")
    on_start = Event("progress:start")