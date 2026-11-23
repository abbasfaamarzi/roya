"""Label - text display component."""
import logging

from roya.core.component import Component
from roya.core.properties import BooleanProperty, IntegerProperty, StringProperty

logger = logging.getLogger("roya.components.content.label")


class Label(Component):
    name = "label"
    template_name = "roya/components/content/label.html"

    text = StringProperty(default="")
    color = StringProperty(default="on_surface")
    font_family = StringProperty(default="")
    font_size = StringProperty(default="")
    font_weight = StringProperty(default="")
    line_height = StringProperty(default="")
    letter_spacing = StringProperty(default="")
    text_align = StringProperty(default="start")
    text_transform = StringProperty(default="none")
    text_decoration = StringProperty(default="none")
    max_lines = IntegerProperty(default=0)
    overflow = StringProperty(default="visible")
    selectable = BooleanProperty(default=True)
    typography = StringProperty(default="body")

    def get_context(self):
        ctx = super().get_context()
        ctx.update({"label_text": self.text, "typo": self.typography})
        return ctx