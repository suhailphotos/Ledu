"""
Placeholder test: verifies ParagraphConverter currently *drops nothing*
once implemented.

Replace with real fixtures as you flesh out the converter.
"""
import pytest
from ledu.builder import PageBuilder


def test_empty_result_before_implementation() -> None:
    md = "Hello world"
    blocks = PageBuilder().convert(md)
    # ParagraphConverter not yet implemented, so list is empty for now
    assert blocks == []
