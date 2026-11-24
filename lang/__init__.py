"""Roya declarative language (KV-inspired) public API."""
from .loader import render_roya
from .parser import parse

__all__ = ["parse", "render_roya"]
