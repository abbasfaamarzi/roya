"""Floating Action Button."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import BooleanProperty, Property, StringProperty

logger = logging.getLogger("roya.components.actions.fab")


class FAB(Component):
    name = "fab"
    template_name = "roya/components/actions/fab.html"

    icon = StringProperty(default="add")
    label = StringProperty(default="")
    size = Property(type=str, default="regular",
                    choices=["small", "regular", "large"])
    variant = Property(type=str, default="primary",
                       choices=["primary", "secondary", "tertiary", "surface"])
    extended = BooleanProperty(default=False)
    position = Property(type=str, default="end",
                        choices=["start", "center", "end"])
    fixed = BooleanProperty(default=True)

    on_click = Event("fab:click")

    def get_context(self):
        ctx = super().get_context()
        ctx["fab_classes"] = f"roya-fab roya-fab--{self.size} roya-fab--{self.variant}"
        return ctx