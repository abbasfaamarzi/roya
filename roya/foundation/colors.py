"""Material Design 3 color tokens."""
import logging

logger = logging.getLogger("roya.foundation.colors")


class ColorPalette:
    """MD3 light palette."""

    PRIMARY = "#6750A4"
    ON_PRIMARY = "#FFFFFF"
    PRIMARY_CONTAINER = "#EADDFF"
    ON_PRIMARY_CONTAINER = "#21005D"
    SECONDARY = "#625B71"
    ON_SECONDARY = "#FFFFFF"
    TERTIARY = "#7D5260"
    ERROR = "#B3261E"
    ON_ERROR = "#FFFFFF"
    SURFACE = "#FEF7FF"
    ON_SURFACE = "#1D1B20"
    SURFACE_VARIANT = "#E7E0EC"
    ON_SURFACE_VARIANT = "#49454F"
    OUTLINE = "#79747E"
    BACKGROUND = "#FEF7FF"
    ON_BACKGROUND = "#1D1B20"

    @classmethod
    def get(cls, token: str, default=None):
        if not token.startswith("_"):
            return getattr(cls, token.upper(), default)
        return default


class ColorUtil:
    @staticmethod
    def hex_to_rgb(color: str):
        c = color.lstrip("#")
        return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgba(color: str, alpha: float) -> str:
        r, g, b = ColorUtil.hex_to_rgb(color)
        return f"rgba({r},{g},{b},{alpha})"