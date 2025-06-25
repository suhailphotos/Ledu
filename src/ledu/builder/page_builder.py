"""
High-level orchestration: Markdown string → List[Notion block dicts].

You will revisit this module when:

* nested list depth handling needs tweaks
* you add support for column / synced scopes
* performance becomes an issue (large documents)

For now, keep it *simple & readable*.
"""
from typing import List
from ledu.parser.markdown_parser import MarkdownParser
from ledu.blocks.base import ConversionContext
from ledu.config import BLOCK_REGISTRY


class PageBuilder:
    """
    Public façade used by CLI and tests.

    Methods
    -------
    convert(markdown: str) -> list[dict]
        Run full pipeline; no network calls.
    """

    def __init__(self, parser: MarkdownParser | None = None) -> None:
        self.parser = parser or MarkdownParser()

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #

    def convert(self, markdown: str) -> List[dict]:
        """
        Parse Markdown and yield Notion block list.

        TODO → deepen list/column handling once basic converters work.
        """
        tokens = self.parser.parse(markdown)
        context = ConversionContext()
        blocks: List[dict] = []
        idx = 0

        while idx < len(tokens):
            tok = tokens[idx]
            converter_cls = BLOCK_REGISTRY.get(tok.type)
            if converter_cls is None:
                # Unknown token — skip quietly for now (later: log warning)
                idx += 1
                continue

            converter = converter_cls()
            new_blocks = converter.to_notion(tok, tokens, idx, context)
            blocks.extend(new_blocks)
            idx += 1  # subclasses may require smarter increment later

        return blocks
