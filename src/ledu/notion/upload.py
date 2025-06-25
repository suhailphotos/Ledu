"""
Higher-level convenience functions for multi-step uploads.

Example use-case
----------------
`upload_markdown(md_str, parent_id=\"...\")` that internally calls PageBuilder
and then NotionClient.create_page.

This stub is optional; flesh out once basic conversion works.
"""
from __future__ import annotations

from typing import List
from ledu.builder.page_builder import PageBuilder
from ledu.notion.client import NotionClient
from ledu.config import settings


def upload_markdown(markdown: str, parent_id: str, *, title: str | None = None) -> str:
    """
    Render *markdown* and create a new Notion page.

    Returns
    -------
    str
        ID of the newly-created page.
    """
    blocks = PageBuilder().convert(markdown)

    client = NotionClient(settings.notion_api_token)
    page = client.create_page({"page_id": parent_id}, blocks)

    return page["id"]
