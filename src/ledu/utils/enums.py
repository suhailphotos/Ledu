"""
Enumerations shared across modules; keep *tiny* to avoid dependency bloat.
"""
from enum import Enum


class Color(str, Enum):
    """Subset of Notion colour names."""
    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
