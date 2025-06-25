"""
Lightweight shared typing helpers.

Expand cautiously to avoid circular imports.
"""
from typing import Dict, Any, TypedDict

JSONDict = Dict[str, Any]


class RichTextDict(TypedDict, total=False):
    type: str
    text: Dict[str, str]
    annotations: Dict[str, bool]
    href: str | None
    equation: Dict[str, str] | None
