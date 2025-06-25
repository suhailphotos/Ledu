"""
Abstract base classes for block converters.

Every concrete converter subclass **must**:

* list the markdown-it token types it consumes (`token_types` tuple)
* implement `.to_notion(...)` returning **List[JSONDict]**
* rely on `ConversionContext` for shared state (list depth, numbering, …)

You rarely need to modify this file after initial implementation.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from ledu.utils.typing import JSONDict


class ConversionContext:
    """
    Mutable context carried throughout the PageBuilder walk.

    Attributes
    ----------
    depth : int
        Current list / column depth.
    number_stack : list[int]
        Keeps track of numbering for ordered lists at each depth.
    """

    def __init__(self) -> None:
        self.depth: int = 0
        self.number_stack: list[int] = []


class BlockConverter(ABC):
    """
    Strategy base class — one subclass per Notion block type.

    Subclasses register themselves into the global `BLOCK_REGISTRY` via
    `__init_subclass__`.
    """

    #: markdown-it token types handled by this converter
    token_types: tuple[str, ...] = ()

    # --------------------------  Meta hooks  --------------------------- #

    def __init_subclass__(cls) -> None:  # noqa: D401  (simple docstring ok)
        """Auto-register subclasses so PageBuilder can dispatch quickly."""
        from ledu.config import BLOCK_REGISTRY  # local import, no cycles
        for t in cls.token_types:
            BLOCK_REGISTRY[t] = cls

    # -------------------------  Main method  --------------------------- #

    @abstractmethod
    def to_notion(self, token, tokens, idx: int,
                  context: ConversionContext) -> List[JSONDict]:
        """
        Convert *token* (and possibly its siblings/children) into Notion blocks.

        Parameters
        ----------
        token : markdown_it.token.Token
            The current token PageBuilder is examining.
        tokens : list[Token]
            Full token list (you may need look-ahead).
        idx : int
            Index of *token* inside *tokens*.
        context : ConversionContext
            Shared mutable state for nested structures.

        Returns
        -------
        list[JSONDict]
            One or more Notion block dicts ready for upload.

        Side effects
        ------------
        Subclass **may** advance `context.depth` or mutate `context.number_stack`.
        PageBuilder takes care of advancing *idx* after return.
        """
        raise NotImplementedError  # implemented by subclass
