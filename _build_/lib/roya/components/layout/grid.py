"""GridContainer - CSS grid layout."""
import logging

from roya.core.component import Component
from roya.core.events import Event
from roya.core.properties import IntegerProperty, StringProperty

logger = logging.getLogger("roya.components.layout.grid")


class GridContainer(Component):
    name = "grid_container"
    template_name = "roya/components/layout/grid.html"

    columns = IntegerProperty(default=1)
    rows = IntegerProperty(default=0)
    column_gap = StringProperty(default="md")
    row_gap = StringProperty(default="md")
    auto_flow = StringProperty(default="row")
    alignment = StringProperty(default="start")
    justify_items = StringProperty(default="stretch")

    on_grid_change = Event("grid:change")

    def get_context(self):
        ctx = super().get_context()
        cols = self.columns if self.columns > 0 else 1
        ctx.update({
            "grid_columns": f"repeat({cols}, minmax(0, 1fr))",
            "grid_rows": f"repeat({self.rows}, minmax(0, 1fr))" if self.rows else "auto",
            "column_gap": self.column_gap,
            "row_gap": self.row_gap,
            "auto_flow": self.auto_flow,
            "justify_items": self.justify_items,
        })
        return ctx