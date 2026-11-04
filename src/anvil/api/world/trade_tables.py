from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import Annotated

from anvil.api.items.items import Item
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import (
    JsonFile,
    JsonObject,
    MinMax,
    NonNegative,
    json_field,
)

from .loot_tables import _LootFunctionBuilder, _LootFunctions

__all__ = ["TradeTable"]


class _TradeItemWants(JsonObject):
    """An item the trader wants."""

    item: str = json_field()
    quantity: Annotated[int | tuple[int, int], MinMax] = json_field(default=1)
    price_multiplier: Annotated[float, NonNegative] = json_field(default=0.05)


class _TradeItemGives(JsonObject, _LootFunctionBuilder):
    """An item the trader gives. Its function builders (`EnchantWithLevels(...)`...) add
    functions to it and return it, to chain them."""

    item: str = json_field()
    quantity: Annotated[int | tuple[int, int], MinMax] = json_field(default=1)
    functions: _LootFunctions = json_field(default_factory=_LootFunctions)

    def _add_function(self, function: JsonObject) -> None:
        self.functions._add_function(function)


class _Trade(JsonObject):
    """A trade: what the trader wants and what it gives."""

    wants: list[_TradeItemWants] = json_field(default_factory=list)
    gives: list[_TradeItemGives] = json_field(default_factory=list)
    trader_exp: Annotated[int, NonNegative] = json_field(default=1)
    max_uses: Annotated[int, NonNegative] = json_field(default=7)
    reward_exp: bool = json_field(default=True)

    def add_wants(
        self,
        item: Item | str,
        quantity: int | tuple[int, int] = 1,
        price_multiplier: float = 0.05,
    ) -> _Trade:
        """Adds an item the trader wants.

        Args:
            item (Item | str): The item.
            quantity (int | tuple[int, int], optional): How many, or the minimum and maximum.
                Defaults to 1.
            price_multiplier (float, optional): How much the price moves with supply and
                demand. Defaults to 0.05.

        Returns:
            _Trade: Self, to add more items.
        """
        if item is None:
            raise ValueError("Item cannot be None.")
        self.wants.append(
            _TradeItemWants(
                item=str(item), quantity=quantity, price_multiplier=price_multiplier
            )
        )
        return self

    def add_gives(
        self, item: Item | str, quantity: int | tuple[int, int] = 1
    ) -> _TradeItemGives:
        """Adds an item the trader gives.

        Args:
            item (Item | str): The item.
            quantity (int | tuple[int, int], optional): How many, or the minimum and maximum.
                Defaults to 1.

        Returns:
            _TradeItemGives: The item, to add functions such as `EnchantWithLevels(...)`.
        """
        if item is None:
            raise ValueError("Item cannot be None.")
        given = _TradeItemGives(item=str(item), quantity=quantity)
        self.gives.append(given)
        return given


class _TradeGroup(JsonObject):
    """A group of trades, of which `num_to_select` are offered."""

    num_to_select: Annotated[int, NonNegative] = json_field(default=1)
    trades: list[_Trade] = json_field(default_factory=list)

    def trade(
        self, max_uses: int = 7, reward_exp: bool = True, trader_exp: int = 1
    ) -> _Trade:
        """Adds a trade to the group.

        Args:
            max_uses (int, optional): Uses before the trade locks until the trader restocks.
                Defaults to 7.
            reward_exp (bool, optional): The player gets experience. Defaults to True.
            trader_exp (int, optional): Experience the trader gains. Defaults to 1.

        Returns:
            _Trade: The trade, to add what it wants and gives.
        """
        trade = _Trade(max_uses=max_uses, reward_exp=reward_exp, trader_exp=trader_exp)
        self.trades.append(trade)
        return trade


class _TradeTier(JsonObject):
    """A tier of trades, unlocked once the trader has `total_exp_required` experience."""

    total_exp_required: Annotated[int, NonNegative] = json_field(default=0)
    groups: list[_TradeGroup] = json_field(default_factory=list)

    def group(self, num_to_select: int = 1) -> _TradeGroup:
        """Adds a group of trades to the tier.

        Args:
            num_to_select (int, optional): How many of its trades are offered. Defaults to 1.

        Returns:
            _TradeGroup: The group, to add trades to.
        """
        group = _TradeGroup(num_to_select=num_to_select)
        self.groups.append(group)
        return group


class _TradeTableFile(JsonObject):
    """The content of `trading/<namespace>/<name>.json`."""

    tiers: list[_TradeTier] = json_field(default_factory=list)

    def add_tier(self, total_exp_required: int) -> _TradeTier:
        """Adds a tier and returns it."""
        tier = _TradeTier(total_exp_required=total_exp_required)
        self.tiers.append(tier)
        return tier


class TradeTable(JsonFile):
    """A trade table: the trades of a villager or wandering trader, in tiers unlocked by the
    trader's experience.

    ```python
    table = TradeTable("fisher")
    trade = table.tier(0).group().trade()
    trade.wants("minecraft:emerald", 3)
    trade.gives("minecraft:fishing_rod").EnchantWithLevels((5, 19))
    table.queue()
    ```

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/createtradetable?view=minecraft-bedrock-stable)
    """

    _document = _TradeTableFile
    _extension = ".json"
    _pack = Pack.BP
    _object_type = "Trade Table"

    def __init__(self, name: str) -> None:
        """Initializes a trade table.

        Args:
            name (str): The trade table name.
        """
        super().__init__(name)
        self._folder = Path("trading", CONFIG.NAMESPACE)

    def tier(self, total_exp_required: int) -> _TradeTier:
        """Adds a tier of trades.

        Args:
            total_exp_required (int): The trader experience that unlocks the tier. The first
                tier is always unlocked.

        Returns:
            _TradeTier: The tier, to add groups of trades to.
        """
        return self._content.add_tier(total_exp_required)

    @property
    def table_path(self) -> str:
        """The trade table's path from the behavior pack root, as entities reference it."""
        return PurePosixPath(
            "trading", CONFIG.NAMESPACE, self.identifier.name + self._extension
        ).as_posix()

    def queue(self) -> "TradeTable":
        """Queues the trade table for export."""
        return super().queue()
