"""Centralized logging helpers."""
import logging

LOGGER_NAMESPACES = [
    "roya", "roya.core", "roya.foundation", "roya.theme",
    "roya.components", "roya.behaviors", "roya.controllers",
    "roya.effects", "roya.templatetags",
]


def get_logger(name: str = "roya") -> logging.Logger:
    if not name.startswith("roya"):
        name = f"roya.{name}"
    return logging.getLogger(name)


def configure(level: int = logging.INFO, handler: logging.Handler = None) -> None:
    for ns in LOGGER_NAMESPACES:
        logger = logging.getLogger(ns)
        logger.setLevel(level)
        if handler and handler not in logger.handlers:
            logger.addHandler(handler)


class LogMixin:
    """Mixin exposing a class-scoped logger."""

    @property
    def logger(self) -> logging.Logger:
        return get_logger(self.__class__.__module__)