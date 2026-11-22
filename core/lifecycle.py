"""Component lifecycle state machine."""
import enum
import logging

from .exceptions import LifecycleError

logger = logging.getLogger("roya.core.lifecycle")


class LifecycleState(enum.Enum):
    REGISTERED = "registered"
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    RENDERED = "rendered"
    MOUNTED = "mounted"
    READY = "ready"
    UPDATED = "updated"
    DISABLED = "disabled"
    HIDDEN = "hidden"
    UNMOUNTED = "unmounted"
    DESTROYED = "destroyed"


_TRANSITIONS = {
    LifecycleState.REGISTERED: {LifecycleState.INITIALIZED},
    LifecycleState.INITIALIZED: {LifecycleState.VALIDATED},
    LifecycleState.VALIDATED: {LifecycleState.RENDERED},
    LifecycleState.RENDERED: {LifecycleState.MOUNTED},
    LifecycleState.MOUNTED: {LifecycleState.READY},
    LifecycleState.READY: {
        LifecycleState.UPDATED, LifecycleState.DISABLED,
        LifecycleState.HIDDEN, LifecycleState.UNMOUNTED,
    },
    LifecycleState.UPDATED: {LifecycleState.READY, LifecycleState.UNMOUNTED},
    LifecycleState.DISABLED: {LifecycleState.READY, LifecycleState.UNMOUNTED},
    LifecycleState.HIDDEN: {LifecycleState.READY, LifecycleState.UNMOUNTED},
    LifecycleState.UNMOUNTED: {LifecycleState.DESTROYED},
    LifecycleState.DESTROYED: set(),
}


class Lifecycle:
    """Tracks and guards state transitions for one component."""

    def __init__(self, owner):
        self.owner = owner
        self.state = LifecycleState.REGISTERED
        self.history = [self.state]

    def can_transition(self, target: LifecycleState) -> bool:
        return target in _TRANSITIONS.get(self.state, set())

    def transition(self, target: LifecycleState):
        if not self.can_transition(target):
            raise LifecycleError(
                f"{self.owner}: cannot transition {self.state.value} -> {target.value}"
            )
        logger.debug("%s: %s -> %s", self.owner, self.state.value, target.value)
        self.state = target
        self.history.append(target)

    def is_(self, *states: LifecycleState) -> bool:
        return self.state in states