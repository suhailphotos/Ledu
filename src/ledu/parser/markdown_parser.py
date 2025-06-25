"""
markdown_parser.py
==================

Tokenises raw Markdown into markdown-it-py `Token` objects.

Implementation plan
-------------------
1. Instantiate a `MarkdownIt` parser with CommonMark base.
2. Enable extensions as needed (`table`, `strikethrough`, …).
3. Expose **only one public method**: `parse(markdown: str) -> list[Token]`.
4. Unit-test the token list for a simple paragraph and for a table.

Edge cases to handle later
--------------------------
* HTML disabled (security); enable via option if you truly need raw HTML.
* Custom containers (`:::columns`) — you will probably write a plugin.
"""
from typing import List
from markdown_it import MarkdownIt
from markdown_it.token import Token


class MarkdownParser:
    """Light wrapper around `markdown_it.MarkdownIt`."""

    def __init__(self, *, enable_extensions: bool = True) -> None:
        self.md = MarkdownIt("commonmark", {"html": False})
        if enable_extensions:
            # TODO → call self.md.enable("table") etc.
            pass

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #

    def parse(self, markdown: str) -> List[Token]:
        """Return a list of markdown-it tokens preserving order & nesting."""
        return self.md.parse(markdown)
