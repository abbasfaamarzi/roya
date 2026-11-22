"""Design token resolver."""


class DesignTokens:
    """Unified resolver for color, typography, spacing, radius, elevation."""

    def __init__(self):
        self.colors = {}
        self.typography = {}
        self.spacing = {}
        self.radius = {}
        self.elevation = {}
        self.motion = {}

    def resolve_color(self, name: str, fallback: str = "#6750A4") -> str:
        return self.colors.get(name, fallback)

    def resolve_typography(self, name: str) -> dict:
        return self.typography.get(name, {"size": "14px", "line": "20px", "weight": 400})

    def resolve_spacing(self, name: str) -> str:
        return self.spacing.get(name, "16px")

    def resolve_radius(self, name: str) -> str:
        return self.radius.get(name, "12px")

    def resolve_elevation(self, level: int) -> str:
        return self.elevation.get(level, "none")

    def to_dict(self) -> dict:
        return {
            "colors": self.colors,
            "typography": self.typography,
            "spacing": self.spacing,
            "radius": self.radius,
            "elevation": self.elevation,
            "motion": self.motion,
        }