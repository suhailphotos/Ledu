"""
heading.py
==========

Handles Markdown ATX headings (`#`, `##`, `###`) and maps them to Notion
`heading_1 | heading_2 | heading_3`.

Implementation notes
--------------------
* markdown-it emits **three tokens** per heading:
    1. `heading_open` (tag = h1/h2/h3)
    2. `inline`
    3. `heading_close`
* You only need to look at `token.tag` on the *open* token to determine level.

Unit tests to write first
-------------------------
* `# H1` → `heading_1`
* `## Policy ($\\pi$)` → mixed inline rich-text.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.parser.rich_text import RichTextSegmenter
from ledu.utils.typing import JSONDict


class HeadingConverter(BlockConverter):
    """`heading_open` → Notion heading blocks."""

    token_types = ("heading_open",)

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        """
        Build a single Notion heading block.

        TODO – real implementation; placeholder returns [].
        """
        return []
