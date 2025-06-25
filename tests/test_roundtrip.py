"""
Integration test scaffold — fill once conversion produces real blocks.
"""
import pytest
from ledu.builder import PageBuilder


@pytest.mark.skip(reason="round-trip tests need working converters")
def test_full_roundtrip() -> None:
    md = "# Heading\\n\\nParagraph"
    blocks = PageBuilder().convert(md)
    assert blocks  # expect non-empty once implemented
