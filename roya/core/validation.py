"""Reusable validators."""
import re
from typing import Any, Callable, Iterable


def required(value: Any) -> bool:
    return value is not None and value != ""


def length_between(min_len: int, max_len: int) -> Callable[[Any], bool]:
    def _v(value):
        return min_len <= len(value) <= max_len
    return _v


def matches(pattern: str) -> Callable[[Any], bool]:
    compiled = re.compile(pattern)
    return lambda value: bool(compiled.match(str(value)))


def one_of(options: Iterable) -> Callable[[Any], bool]:
    options = set(options)
    return lambda value: value in options


def numeric_range(min_v: float = None, max_v: float = None) -> Callable[[Any], bool]:
    def _v(value):
        if min_v is not None and value < min_v:
            return False
        if max_v is not None and value > max_v:
            return False
        return True
    return _v


def all_of(*validators: Callable[[Any], bool]) -> Callable[[Any], bool]:
    return lambda value: all(v(value) for v in validators)


def any_of(*validators: Callable[[Any], bool]) -> Callable[[Any], bool]:
    return lambda value: any(v(value) for v in validators)