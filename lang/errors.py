"""Errors raised while parsing or compiling .roya files."""

class RoyaLanguageError(Exception):
    """Base exception for Roya Language errors."""


class RoyaSyntaxError(RoyaLanguageError):
    """Invalid .roya syntax, with source location when available."""

    def __init__(self, message, line=None):
        self.line = line
        prefix = f"Line {line}: " if line is not None else ""
        super().__init__(prefix + message)


class RoyaExpressionError(RoyaLanguageError):
    """An expression uses an unsupported or unavailable operation."""
