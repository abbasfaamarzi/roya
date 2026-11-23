"""Badge component."""
import logging

from roya.core.component import Component
from roya.core.properties import BooleanProperty, IntegerProperty, Property, StringProperty

logger = logging.getLogger("roya.components.feedback.badge")


class Badge(Component):
    name = "badge"
    template_name = "roya/components/feedback/badge.html"

    value = StringProperty(default="")
    max_value = IntegerProperty(default=99)
    visible = BooleanProperty(default=True)
    color = StringProperty(default="error")
    size = Property(type=str, default="medium",
                    choices=["small", "medium", "large"])
    position = Property(type=str, default="top-end",
                        choices=["top-start", "top-end", "bottom-start", "bottom-end"])
    dot = BooleanProperty(default=False)
    show_zero = BooleanProperty(default=False)
    bg_color = StringProperty(default="0.9,0.2,0.2,1")
    overlap = BooleanProperty(default=True)