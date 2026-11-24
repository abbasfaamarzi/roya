"""Explicit allow-list registry for browser-triggered Python actions."""
import re

_ACTION_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+$")


class ActionRegistry:
    def __init__(self):
        self._actions = {}

    def register(self, name, function):
        if not isinstance(name, str) or not _ACTION_NAME.fullmatch(name):
            raise ValueError("Action names must use dotted identifiers, e.g. 'shop.add_to_cart'.")
        if not callable(function):
            raise TypeError("Registered actions must be callable.")
        self._actions[name] = function
        return function

    def get(self, name):
        return self._actions.get(name)

    def names(self):
        return tuple(sorted(self._actions))


action_registry = ActionRegistry()


def action(name):
    """Register a named action. Usage: @action('instagram.toggle_like')."""
    def decorator(function):
        action_registry.register(name, function)
        return function
    return decorator
