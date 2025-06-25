"""
code.py
=======

Handles fenced code blocks & inline code spans.

Notion quirks
-------------
* The *language* field must be lower-case (\"python\", \"bash\", …).
* Captions: Notion API supports `caption` (rich-text array) – leave blank first.

Implementation plan
-------------------
* Check `token.info` for language after stripping trailing metadata.
* Inline code is handled entirely by `RichTextSegmenter` (annotation.code=True).
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.utils.typing import JSONDict


class CodeBlockConverter(BlockConverter):
    """`fence` → Notion `code` block."""

    token_types = ("fence",)

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        """
        TODO – parse `token.content` & `token.info`, build code block.
        """
        return []
