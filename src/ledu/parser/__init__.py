"""
ledu.parser
===========

Utility sub-package for turning Markdown into an intermediate representation.
"""
from .markdown_parser import MarkdownParser
from .rich_text import RichTextSegmenter

__all__ = ["MarkdownParser", "RichTextSegmenter"]
