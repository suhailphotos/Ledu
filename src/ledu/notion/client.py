"""
Thin wrapper around the official `notion_client.Client`.

Goals
-----
* Keep the rest of Ledu completely decoupled from HTTP details.
* Allow dependency injection / mocking during unit tests.

Future improvements
-------------------
* Back-off & retry logic using `tenacity`.
* Request batching for >100 block uploads.
"""
from __future__ import annotations

from typing import List, Any
from notion_client import Client


class NotionClient:
    """Wraps the Notion Python SDK with just the endpoints we need."""

    def __init__(self, token: str, **kwargs: Any) -> None:
        #: underlying SDK instance (private)
        self._client = Client(auth=token, **kwargs)

    # --------------------------  Pages  ------------------------------- #

    def create_page(self, parent: dict, blocks: List[dict]) -> dict:
        """
        Create a new Notion page populated with *blocks*.

        Parameters
        ----------
        parent : dict
            Parent spec, e.g. `{\"page_id\": \"...\"}` or `{\"database_id\": ...}`.
        blocks : list[dict]
            Children blocks in API format.

        Returns
        -------
        dict
            Raw response from Notion HTTP API.
        """
        return self._client.pages.create(parent=parent, children=blocks)

    # --------------------------  Blocks  ------------------------------ #

    def append_blocks(self, block_id: str, blocks: List[dict]) -> dict:
        """Append *blocks* to an existing block or page."""
        return self._client.blocks.children.append(block_id, children=blocks)
