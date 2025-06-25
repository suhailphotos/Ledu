"""
Command-line entry point.

Usage examples
--------------
$ ledu README.md --dry                 # print JSON to stdout
$ ledu README.md --parent-id=<page>    # upload new page
$ ledu -h                              # help

Integration steps
-----------------
1. Add `[tool.poetry.scripts] ledu = "ledu.cli:main"` in *pyproject.toml*.
2. Run `poetry install`, then `ledu -h` should work.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from ledu.builder.page_builder import PageBuilder
from ledu.notion.client import NotionClient
from ledu.config import settings


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Ledu – Markdown ➜ Notion converter")
    p.add_argument("file", type=pathlib.Path, help="Markdown file to convert")
    p.add_argument("--parent-id", help="Notion parent page/database ID")
    p.add_argument("--dry", action="store_true", help="Print JSON instead of uploading")
    return p


def main(argv: list[str] | None = None) -> None:
    """
    Main entry; designed so that it can be called programmatically.

    TODO → Add `--token` option to override config.notion_api_token.
    """
    args = _build_arg_parser().parse_args(argv)

    markdown = args.file.read_text(encoding="utf8")
    blocks = PageBuilder().convert(markdown)

    if args.dry:
        print(json.dumps(blocks, indent=2))
        return

    client = NotionClient(settings.notion_api_token)
    client.create_page({"page_id": args.parent_id}, blocks)
