"""
media.py
========

Unifies *image*, *video*, *audio*, *file*, *bookmark* conversion.

For images/videos/audio:
    token.type == 'inline' with a nested child of type 'image'.
For bookmark/file:
    Accept custom Markdown syntax or HTML fallback, e.g. `[bookmark](url)`.

For now, create **one stub class** that does nothing but keep API symmetry.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.utils.typing import JSONDict


class MediaConverter(BlockConverter):
    """Placeholder; real implementation will register multiple token types."""
    token_types = ("image",)  # extend later

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        return []
