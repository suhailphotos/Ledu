"""
ledu.blocks
===========

Package that hosts one *BlockConverter* subclass per Notion block type.

Side-effect import
------------------
Importing *this package* automatically brings all individual converter modules
into memory so their subclasses register themselves in `config.BLOCK_REGISTRY`.
You may comment-out imports that you are not ready to implement yet.

When you add a new converter file, **remember to list it here**.
"""
# Keep alphabetic order so merge conflicts stay small
from .paragraph import ParagraphConverter  # noqa: F401
from .heading import HeadingConverter      # noqa: F401
from .list_item import ListItemConverter   # noqa: F401
from .code import CodeBlockConverter       # noqa: F401
from .table import TableConverter          # noqa: F401
from .media import MediaConverter          # noqa: F401
from .advanced import AdvancedBlockConverter  # noqa: F401

__all__ = [
    "ParagraphConverter",
    "HeadingConverter",
    "ListItemConverter",
    "CodeBlockConverter",
    "TableConverter",
    "MediaConverter",
    "AdvancedBlockConverter",
]
