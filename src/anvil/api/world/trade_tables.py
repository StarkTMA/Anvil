import os
from typing import List, Optional, Union

from anvil.api.core.types import Identifier
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, MinecraftItemDescriptor

from .loot_tables import _LootPoolEntryFunctions

__all__ = ["TradeTable"]


class _TradeItemWants:
    """Represents an item that a trader wants."""

    def __init__(
        self, item: Union[MinecraftItemDescriptor, Identifier, str], quantity: int = 1, price_multiplier: float = 0.05
    ):
        self.item = item
        self.quantity = quantity
        self.price_multiplier = price_multiplier

    def to_json(self):
        return {"item": str(self.item), "quantity": self.quantity, "price_multiplier": self.price_multiplier}


class _TradeItemGives(_LootPoolEntryFunctions):
    """Represents an item that a trader gives, supporting functions like enchantments."""

    def __init__(self, item: Union[MinecraftItemDescriptor, Identifier, str], quantity: int = 1):
        super().__init__()
        self.item = item
        self.quantity = quantity
        # self._function is initialized by super().__init__()

    def to_json(self):
        data = {"item": str(self.item), "quantity": self.quantity}
        if self._function:
            data["functions"] = self._function
        return data


class _Trade:
    """Represents a single trade definition."""

    def __init__(self, max_uses: int = 7, reward_exp: bool = True, trader_exp: int = 1):
        self.wants_list: List[_TradeItemWants] = []
        self.gives_list: List[_TradeItemGives] = []
        self.max_uses = max_uses
        self.reward_exp = reward_exp
        self.trader_exp = trader_exp

    def wants(
        self, item: Union[MinecraftItemDescriptor, Identifier, str], quantity: int = 1, price_multiplier: float = 0.05
    ):
        """Adds an item cost to this trade.

        Args:
            item: The item identifier or descriptor.
            quantity: Amount required. Defaults to 1.
            price_multiplier: Impact on price when demand is high/low. Defaults to 0.05.

        Returns:
            _Trade: Self for chaining (e.g. .wants(...).wants(...)).
        """
        obj = _TradeItemWants(item, quantity, price_multiplier)
        self.wants_list.append(obj)
        return self

    def gives(self, item: Union[MinecraftItemDescriptor, Identifier, str], quantity: int = 1):
        """Adds an item reward to this trade.

        Args:
            item: The item identifier or descriptor.
            quantity: Amount given. Defaults to 1.

        Returns:
            _TradeItemGives: The created item object, to allow adding functions (e.g. .gives(...).Enchant(...)).
        """
        obj = _TradeItemGives(item, quantity)
        self.gives_list.append(obj)
        return obj

    def to_json(self):
        return {
            "wants": [w.to_json() for w in self.wants_list],
            "gives": [g.to_json() for g in self.gives_list],
            "trader_exp": self.trader_exp,
            "max_uses": self.max_uses,
            "reward_exp": self.reward_exp,
        }


class _TradeGroup:
    """Represents a group of trades from which a selection is made."""

    def __init__(self, num_to_select: int = 1):
        self.num_to_select = num_to_select
        self.trades_list: List[_Trade] = []

    def trade(self, max_uses: int = 7, reward_exp: bool = True, trader_exp: int = 1):
        """Adds a new trade option to this group.

        Args:
            max_uses: Maximum times this trade can be used before locking. Defaults to 7.
            reward_exp: Whether the player gets XP. Defaults to True.
            trader_exp: Experience gained by the villager. Defaults to 1.

        Returns:
            _Trade: The created trade object.
        """
        t = _Trade(max_uses, reward_exp, trader_exp)
        self.trades_list.append(t)
        return t

    def to_json(self):
        return {"num_to_select": self.num_to_select, "trades": [t.to_json() for t in self.trades_list]}


class _TradeTier:
    """Represents a trading tier (level) for a villager."""

    def __init__(self, total_exp_required: int):
        self.total_exp_required = total_exp_required
        self.groups_list: List[_TradeGroup] = []

    def group(self, num_to_select: int = 1):
        """Adds a group of trades to this tier.

        Args:
            num_to_select: How many trades from this group will be unlocked. Defaults to 1.

        Returns:
            _TradeGroup: The created trade group.
        """
        g = _TradeGroup(num_to_select)
        self.groups_list.append(g)
        return g

    def to_json(self):
        return {"total_exp_required": self.total_exp_required, "groups": [g.to_json() for g in self.groups_list]}


class TradeTable(AddonObject):
    """A Minecraft Bedrock trade table for defining villager trades.

    Used to customize the trades available from villagers and wandering traders.
    Supports tiers, groups, and randomized trade selections.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "trading", CONFIG.NAMESPACE)
    _object_type = "Trade Table"

    def __init__(self, name: str):
        super().__init__(name)
        self.tiers_list: List[_TradeTier] = []
        self._content = {"tiers": []}

    def tier(self, total_exp_required: int):
        """Adds a new level/tier of trades.

        Args:
            total_exp_required: Experience required for the villager to unlock this tier.

        Returns:
            _TradeTier: The created tier object.
        """
        t = _TradeTier(total_exp_required)
        self.tiers_list.append(t)
        return t

    @property
    def table_path(self):
        """Get the relative path of this loot table for referencing.

        Returns:
            str: Relative path from behavior pack root.
        """
        return os.path.join(
            "trading",
            CONFIG.NAMESPACE,
            self._name + self._extension,
        )

    def queue(self):
        """Queue this trade table for generation.

        Constructs the final JSON structure and registers it for export.
        """
        self._content["tiers"] = [t.to_json() for t in self.tiers_list]
        self.content(self._content)
        return super().queue()
