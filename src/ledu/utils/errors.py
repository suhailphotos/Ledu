"""
Project-specific exceptions — keeps error hierarchy tidy.
"""


class LeduError(Exception):
    """Base class for all custom exceptions."""


class UnsupportedTokenError(LeduError):
    """Raised when PageBuilder meets a token type with no converter."""


class ConversionFailedError(LeduError):
    """Raised by a BlockConverter when it cannot build a valid Notion block."""
