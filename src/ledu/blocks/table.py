"""
table.py
========

Converts Markdown tables into Notion `table`, `table_row` blocks.

Implementation suggestion
-------------------------
markdown-it emits a nested sequence of `thead` / `tbody` / `tr` / `td_open`
tokens – iterate until the matching `_close` while building row children.

Start small: **headerless 2×2 table** fixture first, then add alignment.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.utils.typing import JSONDict


class TableConverter(BlockConverter):
    token_types = ("table_open",)

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        """
        TODO – implement real table conversion.
        """
        return []
