"""
advanced.py
===========

Aggregator for the \"rare\" block types: toggle, columns, synced, callout,
breadcrumb, table-of-contents, AI block, mermaid, button.

Approach
--------
* Start with **toggle** (`details` HTML or `???`) because markdown-it can emit
  a custom token via a plugin.
* Each advanced block might deserve its own helper method.

Until then this stub simply returns [] to avoid crashes.
"""
from typing import List
from ledu.blocks.base import BlockConverter, ConversionContext
from ledu.utils.typing import JSONDict


class AdvancedBlockConverter(BlockConverter):
    """Temporary catch-all; refine into per-block files later."""
    token_types = ("details_open",)  # example – plugin must emit this

    def to_notion(
        self, token, tokens, idx: int, context: ConversionContext
    ) -> List[JSONDict]:
        return []
