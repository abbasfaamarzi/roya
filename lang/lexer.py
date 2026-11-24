"""Indentation-aware line lexer for .roya source files."""
from dataclasses import dataclass
from .errors import RoyaSyntaxError


@dataclass(frozen=True)
class SourceLine:
    number: int
    indent: int
    text: str


def _strip_comment(value: str) -> str:
    if value.lstrip().startswith("#:"):
        return value
    quote = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote:
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in ("'", '"'):
            quote = char
        elif char == "#":
            return value[:index]
    return value


def lex(source: str):
    result = []
    for number, raw in enumerate(source.splitlines(), 1):
        if "\t" in raw[:len(raw) - len(raw.lstrip())]:
            raise RoyaSyntaxError("Tabs are not allowed for indentation; use four spaces.", number)
        uncommented = _strip_comment(raw).rstrip()
        if not uncommented.strip():
            continue
        indent = len(uncommented) - len(uncommented.lstrip(" "))
        if indent % 4:
            raise RoyaSyntaxError("Indentation must use multiples of four spaces.", number)
        result.append(SourceLine(number, indent, uncommented.strip()))
    return result
