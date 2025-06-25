"""
paragraph.py
============

First concrete BlockConverter you should implement — easiest to test.

Steps to implement
------------------
1. Collect inline tokens until you hit `paragraph_close`.
2. Concatenate their `.content` into a raw string.
3. Pass raw string to `RichTextSegmenter.segment`.
4. Build a single Notion **paragraph block**.

Unit test
---------
Input  :  \"Hello **world**!\"\n
Expect :  paragraph.block.rich_text == [\"Hello \", \"world\"(bold), \"!\"]

Once this file is stable, use it as a template for headings & list items.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.parser.rich_text import RichTextSegmenter
from ledu.utils.typing import JSONDict


class ParagraphConverter(BlockConverter):
    """Handles `paragraph_open` → Notion *paragraph* block."""

    token_types = ("paragraph_open",)

    def to_notion(self, token, tokens, idx: int,
                  context: ConversionContext) -> List[JSONDict]:
        """
        Convert a markdown paragraph into one Notion paragraph block.

        TODO → Real implementation.  Current placeholder returns empty list
        so PageBuilder will effectively drop paragraphs until you write code.
        """
        return []
