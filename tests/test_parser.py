"""
Smoke-test that MarkdownParser returns a non-empty token list.
"""
import pytest
from ledu.parser import MarkdownParser


@pytest.mark.parametrize("text", ["Hello world", "# Title"])
def test_parser_returns_tokens(text: str) -> None:
    tokens = MarkdownParser().parse(text)
    assert tokens, "Parser should return at least one token"
