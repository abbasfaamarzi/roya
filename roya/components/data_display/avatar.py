"""Avatar component."""
import logging

from roya.core.component import Component
from roya.core.properties import Property, StringProperty

logger = logging.getLogger("roya.components.data_display.avatar")


class Avatar(Component):
    name = "avatar"
    template_name = "roya/components/data_display/avatar.html"

    src = StringProperty(default="")
    initials = StringProperty(default="")
    alt = StringProperty(default="")
    size = Property(type=str, default="medium",
                    choices=["small", "medium", "large"])
    shape = Property(type=str, default="circle", choices=["circle", "square"])