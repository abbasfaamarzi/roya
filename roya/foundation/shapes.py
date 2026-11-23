"""MD3 shape/radius tokens."""


class Shape:
    NONE = "0"
    EXTRA_SMALL = "4px"
    SMALL = "8px"
    MEDIUM = "12px"
    LARGE = "16px"
    EXTRA_LARGE = "28px"
    FULL = "9999px"

    SCALE = {
        "none": NONE, "xs": EXTRA_SMALL, "sm": SMALL,
        "md": MEDIUM, "lg": LARGE, "xl": EXTRA_LARGE, "full": FULL,
    }

    @classmethod
    def get(cls, name: str, default="md") -> str:
        return cls.SCALE.get(name, cls.SCALE.get(default, "12px"))