"""
list_item.py
============

Converts both *bulleted* and *numbered* Markdown list items.  Requires tracking
depth & numbering via `ConversionContext`.

Algorithm sketch (to implement later)
-------------------------------------
1. Detect list type by inspecting `token.markup` on `list_item_open`.
2. For ordered lists maintain `context.number_stack`; bump on each new item.
3. Recursively convert child tokens (they appear between `_open` and `_close`).

Edge case: nested lists inside toggle or callout are handled higher up.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.parser.rich_text import RichTextSegmenter
from ledu.utils.typing import JSONDict


class ListItemConverter(BlockConverter):
    """`list_item_open` → bulleted/numbered list Notion blocks."""

    token_types = ("list_item_open",)

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        """
        TODO – implement list-item conversion.  For now returns empty list.
        """
        return []
