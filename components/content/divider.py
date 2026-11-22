"""Divider component."""
import logging

from roya.core.component import Component
from roya.core.properties import StringProperty

logger = logging.getLogger("roya.components.content.divider")


class Divider(Component):
    name = "divider"
    template_name = "roya/components/content/divider.html"

    orientation = StringProperty(default="horizontal")
    color = StringProperty(default="outline")
    thickness = StringProperty(default="1px")
    spacing = StringProperty(default="0")
    inset = StringProperty(default="0")
    variant = StringProperty(default="full-width")