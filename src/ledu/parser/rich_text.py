"""
rich_text.py
============

Contains the logic to split inline Markdown tokens into Notion-compatible
**rich-text runs** (each run = contiguous segment with identical annotations).

Why isolate this?
-----------------
* All BlockConverters delegate inline splitting here — single source of truth.
* Easier to write unit tests against plain strings without worrying about
  outer blocks.

Implementation roadmap
----------------------
1. Start with bold/italic/code only → make tests pass.
2. Add inline equations (`$...$`) — be careful to escape '\\\\$' literals.
3. Introduce hyperlinks (`[text](url)`).
4. Eventually support mentions via a special pattern (`<mention:id>`).

The heavy lifting will probably be done via a small *state machine* that walks
through the raw text and yields `RichTextRun` dataclass instances.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict
from ledu.utils.typing import RichTextDict


@dataclass
class RichTextRun:
    """
    Dataclass representing a single rich-text fragment.

    Fields mirror Notion's JSON structure for easy conversion.
    """
    plain_text: str
    annotations: Dict[str, bool]
    href: str | None = None
    equation: str | None = None

    # ------------------------------------------------------------------ #
    # Conversion helpers                                                 #
    # ------------------------------------------------------------------ #

    def to_notion(self) -> RichTextDict:
        """Return a JSON-serialisable dict matching Notion API schema."""
        if self.equation:
            return {
                "type": "equation",
                "equation": {"expression": self.equation},
                "annotations": self.annotations,
            }
        return {
            "type": "text",
            "text": {"content": self.plain_text, "link": None if not self.href else {"url": self.href}},
            "annotations": self.annotations,
        }


class RichTextSegmenter:
    """Pure-function object that splits a string into `RichTextRun`s."""

    INLINE_EQ = re.compile(r"\\?\\$(.+?)\\$")  # naive first pass

    # ------------------------------------------------------------------ #
    # Public API                                                         #
    # ------------------------------------------------------------------ #

    def segment(self, text: str) -> List[RichTextRun]:
        """
        Main entry point — returns an ordered list of runs.

        TODO → replace this naïve placeholder with a real parser that respects
        overlapping Markdown tokens and escapes.
        """
        # Temporary trivial implementation: whole text, no annotations.
        return [RichTextRun(plain_text=text, annotations={})]
