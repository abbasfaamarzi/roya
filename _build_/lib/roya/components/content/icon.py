"""Icon component."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.content.icon")


class Icon(Component):
    name = "icon"
    template_name = "roya/components/content/icon.html"

    icon = StringProperty(default="")
    size = StringProperty(default="md")
    color = StringProperty(default="on_surface")
    rotate = StringProperty(default="0")
    flip = StringProperty(default="")
    source = StringProperty(default="")
    decorative = BooleanProperty(default=False)

    on_load = Event("icon:load")
    on_error = Event("icon:error")