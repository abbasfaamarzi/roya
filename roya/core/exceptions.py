"""Exception hierarchy for Roya."""


class RoyaError(Exception):
    """Base exception for all Roya errors."""


class ComponentError(RoyaError):
    """Component lifecycle or contract violation."""


class PropertyError(RoyaError):
    """Property contract violation."""


class ValidationError(PropertyError):
    """Property value failed validation."""


class RegistryError(RoyaError):
    """Duplicate or missing component registration."""


class LifecycleError(RoyaError):
    """Invalid lifecycle transition."""


class EventError(RoyaError):
    """Invalid event operation."""