"""Responsive breakpoints."""


class Breakpoints:
    XS = (0, 599)
    SM = (600, 767)
    MD = (768, 1023)
    LG = (1024, 1439)
    XL = (1440, 1919)
    XXL = (1920, None)

    ORDER = ["xs", "sm", "md", "lg", "xl", "xxl"]

    RANGES = {"xs": XS, "sm": SM, "md": MD, "lg": LG, "xl": XL, "xxl": XXL}

    @classmethod
    def for_width(cls, width: int) -> str:
        for name in cls.ORDER:
            low, high = cls.RANGES[name]
            if high is None or low <= width <= high:
                return name
        return "xxl"