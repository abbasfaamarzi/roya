"""MD3 typography scale."""
import logging

logger = logging.getLogger("roya.foundation.typography")


class Typography:
    DISPLAY_LARGE = {"size": "57px", "line": "64px", "weight": 400}
    DISPLAY_MEDIUM = {"size": "45px", "line": "52px", "weight": 400}
    DISPLAY_SMALL = {"size": "36px", "line": "44px", "weight": 400}
    HEADLINE_LARGE = {"size": "32px", "line": "40px", "weight": 400}
    HEADLINE_MEDIUM = {"size": "28px", "line": "36px", "weight": 400}
    HEADLINE_SMALL = {"size": "24px", "line": "32px", "weight": 400}
    TITLE_LARGE = {"size": "22px", "line": "28px", "weight": 400}
    TITLE_MEDIUM = {"size": "16px", "line": "24px", "weight": 500}
    TITLE_SMALL = {"size": "14px", "line": "20px", "weight": 500}
    BODY_LARGE = {"size": "16px", "line": "24px", "weight": 400}
    BODY_MEDIUM = {"size": "14px", "line": "20px", "weight": 400}
    BODY_SMALL = {"size": "12px", "line": "16px", "weight": 400}
    LABEL_LARGE = {"size": "14px", "line": "20px", "weight": 500}
    LABEL_MEDIUM = {"size": "12px", "line": "16px", "weight": 500}
    LABEL_SMALL = {"size": "11px", "line": "16px", "weight": 500}

    FONT_FAMILY = "Roboto, system-ui, sans-serif"

    @classmethod
    def get(cls, style: str) -> dict:
        token = style.upper()
        if not hasattr(cls, token):
            logger.warning("Unknown typography token: %s", style)
            return cls.BODY_MEDIUM
        return getattr(cls, token)