"""Image - responsive image with lazy loading."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, StringProperty

logger = logging.getLogger("roya.components.content.image")


class Image(Component):
    name = "image"
    template_name = "roya/components/content/image.html"

    src = StringProperty(default="")
    alt = StringProperty(default="")
    width = StringProperty(default="auto")
    height = StringProperty(default="auto")
    object_fit = StringProperty(default="cover")
    object_position = StringProperty(default="center")
    lazy = BooleanProperty(default=True)
    decoding = StringProperty(default="async")
    radius = StringProperty(default="md")
    fallback = StringProperty(default="")

    on_load = Event("image:load")
    on_error = Event("image:error")