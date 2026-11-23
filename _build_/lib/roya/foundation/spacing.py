"""MD3 spacing tokens (4dp grid)."""


class Spacing:
    NONE = "0"
    XS = "4px"
    SM = "8px"
    MD = "16px"
    LG = "24px"
    XL = "32px"
    XXL = "48px"
    XXXL = "64px"

    SCALE = {
        "none": NONE, "xs": XS, "sm": SM, "md": MD,
        "lg": LG, "xl": XL, "xxl": XXL, "xxxl": XXXL,
    }

    @classmethod
    def get(cls, name: str, default="md") -> str:
        return cls.SCALE.get(name, cls.SCALE.get(default, "16px"))