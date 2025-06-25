"""
Global configuration and registries.

You will rarely *import* this module elsewhere; instead, other parts of the
package interact with the singletons defined here.

Things to implement later
-------------------------
* A `Settings.load_from_env()` helper so the CLI can honour NOTION_TOKEN.
* Mutability safeguards (e.g. freeze `settings` once `.lock()` is called).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Type
from ledu.blocks.base import BlockConverter


@dataclass
class Settings:
    """
    Runtime-configurable options.

    TODO → implement validation & persistence if you need a config file.
    """
    notion_api_token: str = ""
    default_color: str = "default"
    enable_equation_blocks: bool = True


#: singleton instance imported everywhere
settings = Settings()

#: Registry mapping *markdown-it token type* → *BlockConverter subclass*.
#   Filled automatically by BlockConverter.__init_subclass__.
BLOCK_REGISTRY: Dict[str, Type[BlockConverter]] = {}
