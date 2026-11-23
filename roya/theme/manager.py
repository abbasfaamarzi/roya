"""ThemeManager - central theme engine for Roya."""
import logging
from typing import Dict

from roya.core.events import Event
from roya.core.logging import LogMixin
from roya.core.properties import StringProperty
from roya.foundation import ColorPalette, ColorUtil, Elevation, Shape, Spacing, Typography
from .tokens import DesignTokens

logger = logging.getLogger("roya.theme.manager")


class ThemeManager(LogMixin):
    """Global theme engine for the application."""

    name = "theme_manager"

    on_change = Event("theme:change")
    on_mode_change = Event("theme:mode-change")
    on_colors_change = Event("theme:colors-change")
    on_loaded = Event("theme:loaded")
    on_error = Event("theme:error")

    theme_mode = StringProperty(default="light")
    direction = StringProperty(default="auto")

    def __init__(self):
        self.tokens = DesignTokens()
        self._themes: Dict[str, dict] = {}
        self._load_defaults()

    def register_theme(self, name: str, theme: dict):
        self._themes[name] = theme
        logger.info("Registered theme: %s", name)

    def unregister_theme(self, name: str):
        self._themes.pop(name, None)

    def set_theme(self, name: str):
        if name not in self._themes:
            self.on_error.emit(detail={"theme": name, "reason": "not found"})
            raise KeyError(f"Theme '{name}' not registered")
        self._apply_theme(self._themes[name])
        self.on_change.emit(detail={"theme": name})
        self.on_loaded.emit(detail={"theme": name})

    def switch_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self.on_mode_change.emit(detail={"mode": self.theme_mode})
        self._load_defaults()

    def update_colors(self, colors: dict):
        self.tokens.colors.update(colors)
        self.on_colors_change.emit(detail={"colors": colors})

    def generate_palette(self, source_color: str) -> dict:
        base = ColorUtil.hex_to_rgb(source_color)
        logger.debug("Generating palette from %s", source_color)
        return {
            "primary": source_color,
            "secondary": self._shade(base, 0.2),
            "tertiary": self._shade(base, -0.2),
            "surface": ColorPalette.SURFACE,
            "on_surface": ColorPalette.ON_SURFACE,
        }

    def get_token(self, name: str):
        return self.tokens.to_dict().get(name)

    def resolve_color(self, name: str) -> str:
        return self.tokens.resolve_color(name)

    def resolve_spacing(self, name: str) -> str:
        return self.tokens.resolve_spacing(name)

    def _shade(self, rgb, amount: float) -> str:
        if amount >= 0:
            r, g, b = [int(c + (255 - c) * amount) for c in rgb]
        else:
            r, g, b = [int(c * (1 + amount)) for c in rgb]
        return f"#{r:02X}{g:02X}{b:02X}"

    def _apply_theme(self, theme: dict):
        self.tokens.colors.update(theme.get("colors", {}))
        self.tokens.typography.update(theme.get("typography", {}))
        self.tokens.spacing.update(theme.get("spacing", {}))
        self.tokens.radius.update(theme.get("radius", {}))
        self.tokens.elevation.update(theme.get("elevation", {}))

    def _load_defaults(self):
        if self.theme_mode == "dark":
            colors = {
                "primary": "#D0BCFF", "on_primary": "#381E72",
                "surface": "#1C1B1F", "on_surface": "#E6E1E5",
            }
        else:
            colors = {
                "primary": ColorPalette.PRIMARY,
                "on_primary": ColorPalette.ON_PRIMARY,
                "surface": ColorPalette.SURFACE,
                "on_surface": ColorPalette.ON_SURFACE,
            }
        self.tokens.colors.update(colors)
        self.tokens.typography.update({
            "body": Typography.BODY_MEDIUM,
            "label": Typography.LABEL_MEDIUM,
            "title": Typography.TITLE_LARGE,
        })
        self.tokens.spacing.update(Spacing.SCALE)
        self.tokens.radius.update(Shape.SCALE)
        self.tokens.elevation.update(Elevation.LEVELS)


theme_manager = ThemeManager()