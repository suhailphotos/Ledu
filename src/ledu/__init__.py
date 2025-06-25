"""
Ledu
=====

Markdown ⇨ Notion converter skeleton.

Nothing is executed at import-time except attaching the package version.
"""
from importlib.metadata import version as _v

__all__ = ["__version__"]
__version__: str = _v("ledu")  # resolved from pyproject.toml
