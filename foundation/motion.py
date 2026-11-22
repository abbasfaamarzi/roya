"""MD3 motion and easing tokens."""


class Motion:
    DURATION_SHORT1 = "50ms"
    DURATION_SHORT2 = "100ms"
    DURATION_SHORT3 = "150ms"
    DURATION_SHORT4 = "200ms"
    DURATION_MEDIUM1 = "250ms"
    DURATION_MEDIUM2 = "300ms"
    DURATION_MEDIUM3 = "350ms"
    DURATION_MEDIUM4 = "400ms"
    DURATION_LONG1 = "450ms"
    DURATION_LONG2 = "500ms"

    EASING_STANDARD = "cubic-bezier(0.2, 0.0, 0, 1.0)"
    EASING_EMPHASIZED = "cubic-bezier(0.05, 0.7, 0.1, 1.0)"
    EASING_DECELERATE = "cubic-bezier(0.0, 0.0, 0, 1.0)"
    EASING_ACCELERATE = "cubic-bezier(0.3, 0.0, 1.0, 1.0)"
    EASING_LINEAR = "linear"

    @classmethod
    def duration(cls, name: str) -> str:
        return getattr(cls, f"DURATION_{name.upper()}", cls.DURATION_MEDIUM2)

    @classmethod
    def easing(cls, name: str) -> str:
        return getattr(cls, f"EASING_{name.upper()}", cls.EASING_STANDARD)