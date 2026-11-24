"""Small AST model for the first Roya Language release."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Node:
    kind: str
    name: str = ""
    properties: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=dict)
    events: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    children: List["Node"] = field(default_factory=list)
    variable: str = ""
    expression: str = ""
    key_expression: str = ""
    line: Optional[int] = None


@dataclass
class StyleRule:
    name: str
    base: str
    properties: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=dict)
    line: Optional[int] = None


@dataclass
class Document:
    root: Node
    rules: Dict[str, StyleRule] = field(default_factory=dict)
    logic_modules: List[str] = field(default_factory=list)
    includes: List[str] = field(default_factory=list)
    version: str = "1.0"
