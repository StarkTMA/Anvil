import os
from typing import Union, overload

from anvil.api.core.enums import ExplorationMapDestinations, LootPoolType
from anvil.api.core.types import Identifier
from anvil.api.vanilla.effects import MinecraftPotionEffectTypes
from anvil.api.world.structures import JigsawStructureSet
from anvil.lib.config import CONFIG
from anvil.lib.lib import clamp
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
    MinecraftBlockDescriptor,
    MinecraftEntityDescriptor,
    MinecraftItemDescriptor,
)

__all__ = ["LootTable", "LootConditions"]


class _LootPoolEntryFunctions:
    """Provides function modifiers that can be applied to loot table entries to customize their behavior.

    This class contains methods for applying various functions to loot table entries, including
    enchantment functions, item modification functions, and miscellaneous utility functions.
    All functions return self to enable method chaining.
    """

    def __init__(self):
        """Initialize the functions list."""
        self._function = []

    # Enchantment Functions
    def EnchantBookForTrading(
        self,
        base_cost: int,
        base_random_cost: int,
        per_level_random_cost: int,
        per_level_cost: int,
    ):
        """Enchants a book using the algorithm for enchanting items sold by villagers.

        Only works in trade tables. The total cost is calculated as:
        base_cost + (base_random_cost + enchantmentLevel * per_level_random_cost) + enchantmentLevel * per_level_cost

        Parameters:
            base_cost (int): The base cost of the enchantment.
            base_random_cost (int): The base random cost component.
            per_level_random_cost (int): Random cost multiplied by enchantment level.
            per_level_cost (int): Fixed cost multiplied by enchantment level.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_book_for_trading-trade-table-only)
        """
        self._function.append(
            {
                "function": "enchant_book_for_trading",
                "base_cost": base_cost,
                "base_random_cost": base_random_cost,
                "per_level_random_cost": per_level_random_cost,
                "per_level_cost": per_level_cost,
            }
        )
        return self

    def EnchantRandomGear(self, chance: float):
        """Enchants an item using the same algorithm used for vanilla mob equipment.

        The chance is modified based on difficulty: 0% on Peaceful/Easy, ~67% of specified chance
        on Normal, and 100% of specified chance on Hard difficulty. Values > 1.0 can bypass
        Normal difficulty reduction.

        Parameters:
            chance (float): Enchantment chance modifier (0.0-1.0, values >1.0 allowed for difficulty bypass).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_random_gear)
        """
        self._function.append(
            {
                "function": "enchant_random_gear",
                "chance": clamp(chance, 0.0, 1.0),
            }
        )
        return self

    def EnchantRandomly(self, treasure: bool = False):
        """Generates a random enchantment compatible with the item.

        Parameters:
            treasure (bool, optional): Allow treasure enchantments (Frost Walker, Mending,
                Soul Speed, Curse of Binding, Curse of Vanishing). Defaults to False.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_randomly)
        """
        self._function.append({"function": "enchant_randomly", "treasure": treasure})
        return self

    def EnchantWithLevels(self, levels: tuple[int, int], treasure: bool = False):
        """Applies enchantments as if using an enchanting table with specified XP levels.

        Parameters:
            levels (tuple[int, int]): Minimum and maximum XP levels for enchanting.
            treasure (bool, optional): Allow treasure-only enchantments. Defaults to False.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_with_levels)
        """
        self._function.append(
            {
                "function": "enchant_with_levels",
                "levels": {"min": min(levels), "max": max(levels)},
                "treasure": treasure,
            }
        )
        return self

    def SetPotion(self, id: MinecraftPotionEffectTypes):
        """Sets the potion type of compatible items (potions, splash potions, lingering potions).

        Parameters:
            id (MinecraftPotionEffectTypes): The potion effect identifier.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#set_potion)
        """
        self._function.append({"function": "set_potion", "id": id})
        return self

    @overload
    def SpecificEnchants(self, enchants: tuple[str, ...]) -> "_LootPoolEntryFunctions":
        """Apply specific enchantments to an item by name only (default levels).

        Parameters:
            enchants (tuple[str, ...]): Tuple of enchantment names.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    @overload
    def SpecificEnchants(
        self, enchants: tuple[tuple[str, int], ...]
    ) -> "_LootPoolEntryFunctions":
        """Apply specific enchantments to an item with custom levels.

        Note: Maximum enchantment levels are hard-coded and cannot be overridden.
        Can apply enchantments to items that wouldn't normally be enchantable.

        Parameters:
            enchants (tuple[tuple[str, int], ...]): Tuple of (enchantment_name, level) pairs.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#specific_enchants)
        """
        ...

    def SpecificEnchants(
        self, enchants: Union[tuple[str, ...], tuple[tuple[str, int], ...]]
    ) -> "_LootPoolEntryFunctions":
        """Apply specific enchantments to an item.

        Parameters:
            enchants (tuple[str, ...] | tuple[tuple[str, int], ...]): Either a tuple of enchantment names
                for default levels, or a tuple of (enchantment_name, level) pairs for custom levels.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#specific_enchants)
        """
        if enchants and isinstance(enchants[0], str):
            # Simple enchantment names only
            self._function.append(
                {
                    "function": "specific_enchants",
                    "enchants": enchants,
                }
            )
        else:
            # Enchantment name and level pairs
            self._function.append(
                {
                    "function": "specific_enchants",
                    "enchants": [
                        {"id": enchant[0], "level": enchant[1]} for enchant in enchants
                    ],
                }
            )
        return self

    # Item Mod Functions
    def LootingEnchant(self, levels: tuple[int, int]):
        """Modifies the count of items returned when an entity is killed by a looting-enchanted weapon.

        Note: Only works with loot tables called by entity death, not in villager trades or chests.

        Parameters:
            levels (tuple[int, int]): Min and max additional items per looting level.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#looting_enchant-loot-table-only)
        """
        self._function.append(
            {
                "function": "looting_enchant",
                "levels": {"min": min(levels), "max": max(levels)},
            }
        )
        return self

    def RandomAuxValue(self, range: tuple[int, int]):
        """Picks a random auxiliary value for an item (e.g., for randomly colored dyes).

        Parameters:
            range (tuple[int, int]): Min and max values for the auxiliary data.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_aux_value)
        """
        self._function.append(
            {
                "function": "random_aux_value",
                "range": {"min": min(range), "max": max(range)},
            }
        )
        return self

    def RandomBlockState(self, range: tuple[int, int]):
        """Randomizes the block state of the resulting item (e.g., for colored wool from shepherd trades).

        Parameters:
            range (tuple[int, int]): Min and max values for the block state.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_block_state)
        """
        self._function.append(
            {
                "function": "random_block_state",
                "range": {"min": min(range), "max": max(range)},
            }
        )
        return self

    def RandomDye(self):
        """Affects the colors of random leather items (used by leather workers for random coloring).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_dye)
        """
        self._function.append(
            {
                "function": "random_dye",
            }
        )
        return self

    def SetActorId(self, actor: MinecraftEntityDescriptor | Identifier | None):
        """Sets the entity ID of a spawn egg. Only works with spawn eggs.

        When actor is None, inherits the entity ID from the associated entity
        (e.g., rabbit drops rabbit spawn egg). Be careful with chest loot tables -
        omitting ID with player interaction creates unusable player spawn eggs.

        Parameters:
            actor (MinecraftEntityDescriptor | Identifier | None): The entity identifier for the spawn egg,
                or None to inherit from the associated entity.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_actor_id)
        """
        self._function.append(
            {
                "function": "set_actor_id",
                "id": str(actor) if actor is not None else None,
            }
        )
        return self

    def SetBannerDetails(self, type: int = 1):
        """Sets banner details. Only works on banners and currently only supports type 1 (villager banner).

        Parameters:
            type (int, optional): Banner type. Only type 1 (villager banner) is supported. Defaults to 1.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_banner_details)
        """
        self._function.append(
            {
                "function": "set_banner_details",
                "type": 1,
            }
        )
        return self

    def SetBookContent(self, author: str, title: str, pages: list[str]):
        """Sets the contents of a book including author, title, and pages.

        Can use rawtext for localization on pages only (not author/title).
        Remember to escape special characters like quotes and backslashes in rawtext.

        Parameters:
            author (str): The author of the book.
            title (str): The title of the book.
            pages (list[str]): List of page contents as strings.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_book_contents)
        """
        self._function.append(
            {
                "function": "set_book_contents",
                "author": author,
                "title": title,
                "pages": [str(p) for p in pages],
            }
        )
        return self

    @overload
    def SetCount(self, count: int) -> "_LootPoolEntryFunctions":
        """Sets the quantity of items returned to an exact number.

        Parameters:
            count (int): Exact number of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    @overload
    def SetCount(self, count: tuple[int, int]) -> "_LootPoolEntryFunctions":
        """Sets the quantity of items returned to a random number within a range.

        Parameters:
            count (tuple[int, int]): Min/max range of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    def SetCount(self, count) -> "_LootPoolEntryFunctions":
        """Sets the quantity of items returned.

        Parameters:
            count (int | tuple[int, int]): Exact number or min/max range of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_count)
        """
        if isinstance(count, int):
            self._function.append(
                {
                    "function": "set_count",
                    "count": count,
                }
            )
        elif isinstance(count, (list, tuple)):
            self._function.append(
                {
                    "function": "set_count",
                    "count": {"min": min(count), "max": max(count)},
                }
            )
        return self

    @overload
    def SetDamage(self, damage: float):
        """Sets the percentage of durability remaining for items with durability to an exact value.

        Parameters:
            damage (float): Durability percentage (1.0 = 100% undamaged, 0.0 = no durability).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    @overload
    def SetDamage(self, damage: tuple[float, float]):
        """Sets the percentage of durability remaining for items with durability to a random value within a range.

        Parameters:
            damage (tuple[float, float]): Min/max range of durability percentages (0.0-1.0).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    def SetDamage(self, damage):
        """Sets the percentage of durability remaining for items with durability.

        Parameters:
            damage (float | tuple[float, float]): Durability percentage (1.0 = 100% undamaged, 0.0 = no durability)
                or min/max range of durability percentages (0.0-1.0).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_damage)
        """
        if isinstance(damage, (int, float)):
            self._function.append(
                {
                    "function": "set_damage",
                    "damage": clamp(damage, 0, 1),
                }
            )
        elif isinstance(damage, tuple):
            self._function.append(
                {
                    "function": "set_damage",
                    "damage": {
                        "min": clamp(min(damage), 0, 1),
                        "max": clamp(max(damage), 0, 1),
                    },
                }
            )
        return self

    def SetData(self, data: int):
        """Sets the data value of a block or item to a specific ID (e.g., specific potion variant).

        Parameters:
            data (int): The data/variant value to set.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_data)
        """
        self._function.append(
            {
                "function": "set_data",
                "data": data,
            }
        )
        return self

    def SetDataFromColorIndex(self):
        """Inherits the data value from the associated entity's color index.

        For example, a pink sheep drops pink wool. If the entity has no color index
        or used in chest loot tables, always yields data value 0.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_data_from_color_index)
        """
        self._function.append(
            {
                "function": "set_data_from_color_index",
            }
        )
        return self

    def SetLore(self, lore: tuple[str]):
        """Sets the lore text of an item. Each string represents a single line of lore.

        Note: Currently no support for rawtext in lore.

        Parameters:
            lore (tuple[str]): Tuple of lore lines to display on the item.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_lore)
        """
        self._function.append(
            {
                "function": "set_lore",
                "lore": lore,
            }
        )
        return self

    def SetName(self, name: str):
        """Sets the custom name of an item.

        Note: Currently no support for rawtext in item names.

        Parameters:
            name (str): The custom name to give the item.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_name)
        """
        self._function.append(
            {
                "function": "set_name",
                "name": name,
            }
        )
        return self

    # Miscellaneous Functions
    def ExplorationMap(
        self, destination: ExplorationMapDestinations | JigsawStructureSet | Identifier
    ):
        """Transforms a normal map into a treasure map marking the location of structures.

        Parameters:
            destination (ExplorationMapDestinations): The type of structure to mark
                (buriedtreasure, endcity, fortress, mansion, mineshaft, monument,
                pillageroutpost, ruins, shipwreck, stronghold, temple, village).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#exploration_map)
        """
        self._function.append(
            {
                "function": "exploration_map",
                "destination": (
                    destination if isinstance(destination, str) else str(destination)
                ),
            }
        )
        return self

    def FillContainer(self, lootTable: "LootTable"):
        """Defines the loot table for a chest. Contents are generated when opened/broken.

        Tip: Use SetName() to distinguish filled chests from empty ones in inventory.

        Parameters:
            lootTable (LootTable): The loot table to use for filling the container.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#fill_container)
        """
        self._function.append(
            {
                "function": "fill_container",
                "loot_table": str(lootTable),
            }
        )
        return self

    def FurnaceSmelt(self):
        """Returns the cooked version of dropped loot when the entity dies from fire damage.

        Only works with entity loot tables, not villager trades or chests.
        Commonly used with fire aspect enchantments.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#furnace_smelt-loot-table-only)
        """
        self._function.append(
            {
                "function": "furnace_smelt",
                "conditions": [
                    {
                        "condition": "entity_properties",
                        "entity": "this",
                        "properties": {"on_fire": True},
                    }
                ],
            }
        )
        return self

    def TraderMaterialType(self):
        """Affects the type of items a fisherman wants to trade (e.g., different boat types).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#trader_material_type)
        """
        self._function.append(
            {
                "function": "trader_material_type",
            }
        )
        return self

    def __export__(self):
        """Export the list of functions for JSON serialization.

        Returns:
            list: List of function dictionaries.
        """
        return self._function


class _LootConditions:
    """Provides condition modifiers that can be applied to loot pools or entries.

    Conditions are requirements that must be met before a pool can be rolled
    or an individual entry can be selected. Each condition runs in sequence;
    if any condition fails, the pool or entry is skipped.

    All methods return self to enable method chaining.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable)
    """

    def __init__(self):
        """Initialize the conditions list."""
        self._conditions = []

    def add(self, condition: dict) -> "_LootConditions":
        """Add a raw condition dictionary.

        Parameters:
            condition (dict): Condition dictionary to append.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self._conditions.append(condition)
        return self

    def match_tool(
        self,
        item: Union[MinecraftItemDescriptor, Identifier, str, None] = None,
        enchantments: Union[
            str,
            tuple[str, ...],
            list[str],
            dict,
            list[dict],
            tuple[dict, ...],
            None,
        ] = None,
        count: Union[int, tuple[int, int], None] = None,
        durability: Union[int, tuple[int, int], None] = None,
        filter_any: Union[list[str], tuple[str, ...], None] = None,
        filter_all: Union[list[str], tuple[str, ...], None] = None,
        filter_none: Union[list[str], tuple[str, ...], None] = None,
    ) -> "_LootConditions":
        """Matches the tool used to break the block or make the loot drop.

        Parameters:
            item (MinecraftItemDescriptor | Identifier | str, optional): The item identifier (e.g. "minecraft:shears").
            enchantments (str | list | dict, optional): Enchantment name (e.g. "silk_touch") or list of enchantment specifications.
            count (int | tuple[int, int], optional): Tool count or [min, max] range.
            durability (int | tuple[int, int], optional): Tool durability requirement.
            filter_any (list[str], optional): Tool must match at least one of these item tags (minecraft:match_tool_filter_any).
            filter_all (list[str], optional): Tool must match all of these item tags (minecraft:match_tool_filter_all).
            filter_none (list[str], optional): Tool must not match any of these item tags (minecraft:match_tool_filter_none).

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#match_tool)
        """
        cond: dict = {"condition": "match_tool"}
        if item is not None:
            cond["item"] = str(item)
        if count is not None:
            if isinstance(count, int):
                cond["count"] = count
            elif isinstance(count, (tuple, list)):
                cond["count"] = {"range_min": min(count), "range_max": max(count)}
        if durability is not None:
            if isinstance(durability, int):
                cond["durability"] = {"range_min": durability}
            elif isinstance(durability, (tuple, list)):
                cond["durability"] = {
                    "range_min": min(durability),
                    "range_max": max(durability),
                }
        if enchantments is not None:
            if isinstance(enchantments, str):
                cond["enchantments"] = [
                    {"enchantment": enchantments, "levels": {"range_min": 1}}
                ]
            elif isinstance(enchantments, dict):
                cond["enchantments"] = [enchantments]
            elif isinstance(enchantments, (list, tuple)):
                ench_list = []
                for e in enchantments:
                    if isinstance(e, str):
                        ench_list.append({"enchantment": e, "levels": {"range_min": 1}})
                    elif isinstance(e, dict):
                        ench_list.append(e)
                    elif isinstance(e, (tuple, list)) and len(e) >= 2:
                        ench_list.append(
                            {"enchantment": str(e[0]), "levels": {"range_min": e[1]}}
                        )
                cond["enchantments"] = ench_list
        if filter_any:
            cond["minecraft:match_tool_filter_any"] = list(filter_any)
        if filter_all:
            cond["minecraft:match_tool_filter_all"] = list(filter_all)
        if filter_none:
            cond["minecraft:match_tool_filter_none"] = list(filter_none)
        self._conditions.append(cond)
        return self

    def random_chance(self, chance: float) -> "_LootConditions":
        """Applies a probability chance that loot will drop.

        Parameters:
            chance (float): Drop chance between 0.0 and 1.0.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#random_chance)
        """
        self._conditions.append(
            {
                "condition": "random_chance",
                "chance": clamp(chance, 0.0, 1.0),
            }
        )
        return self

    def random_chance_with_looting(
        self, chance: float, looting_multiplier: float
    ) -> "_LootConditions":
        """Applies a probability chance modified by the looting enchantment level.

        Parameters:
            chance (float): Base drop chance between 0.0 and 1.0.
            looting_multiplier (float): Multiplier added per level of looting.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#random_chance_with_looting)
        """
        self._conditions.append(
            {
                "condition": "random_chance_with_looting",
                "chance": clamp(chance, 0.0, 1.0),
                "looting_multiplier": looting_multiplier,
            }
        )
        return self

    def random_difficulty_chance(
        self,
        default_chance: float,
        peaceful: float | None = None,
        easy: float | None = None,
        normal: float | None = None,
        hard: float | None = None,
    ) -> "_LootConditions":
        """Controls loot drop probability depending on world difficulty.

        Parameters:
            default_chance (float): Default drop chance.
            peaceful (float, optional): Drop chance on Peaceful difficulty.
            easy (float, optional): Drop chance on Easy difficulty.
            normal (float, optional): Drop chance on Normal difficulty.
            hard (float, optional): Drop chance on Hard difficulty.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#random_difficulty_chance)
        """
        payload: dict = {
            "condition": "random_difficulty_chance",
            "default_chance": clamp(default_chance, 0.0, 1.0),
        }
        if peaceful is not None:
            payload["peaceful"] = clamp(peaceful, 0.0, 1.0)
        if easy is not None:
            payload["easy"] = clamp(easy, 0.0, 1.0)
        if normal is not None:
            payload["normal"] = clamp(normal, 0.0, 1.0)
        if hard is not None:
            payload["hard"] = clamp(hard, 0.0, 1.0)
        self._conditions.append(payload)
        return self

    def random_regional_difficulty_chance(self, max_chance: float) -> "_LootConditions":
        """Determines loot probability according to regional difficulty.

        Parameters:
            max_chance (float): Maximum drop chance.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#random_regional_difficulty_chance)
        """
        self._conditions.append(
            {
                "condition": "random_regional_difficulty_chance",
                "max_chance": clamp(max_chance, 0.0, 1.0),
            }
        )
        return self

    def killed_by_player(self) -> "_LootConditions":
        """Requires the entity to have been killed directly by a player.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#killed_by_player_or_pets)
        """
        self._conditions.append({"condition": "killed_by_player"})
        return self

    def killed_by_player_or_pets(self) -> "_LootConditions":
        """Requires the entity to have been killed by a player or one of their tamed pets.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#killed_by_player_or_pets)
        """
        self._conditions.append({"condition": "killed_by_player_or_pets"})
        return self

    def killed_by_entity(self, entity_type: str) -> "_LootConditions":
        """Requires the entity to have been killed by an entity of the specified type.

        Parameters:
            entity_type (str): Identifier of the killing entity type (e.g. "minecraft:skeleton").

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#pool-conditions)
        """
        self._conditions.append(
            {
                "condition": "killed_by_entity",
                "entity_type": str(entity_type),
            }
        )
        return self

    def entity_killed(self, entity_type: str) -> "_LootConditions":
        """Requires the victim entity to be of the specified type.

        Parameters:
            entity_type (str): Identifier of the victim entity type (e.g. "minecraft:magma_cube").

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#has_variant)
        """
        self._conditions.append(
            {
                "condition": "entity_killed",
                "entity_type": str(entity_type),
            }
        )
        return self

    def has_variant(self, value: int) -> "_LootConditions":
        """Specifies that the entity must have the given variant value.

        Parameters:
            value (int): Variant number.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#has_variant)
        """
        self._conditions.append(
            {
                "condition": "has_variant",
                "value": int(value),
            }
        )
        return self

    def has_mark_variant(self, value: int) -> "_LootConditions":
        """Specifies that the entity must have the given mark variant value.

        Parameters:
            value (int): Mark variant number.

        Returns:
            _LootConditions: Self for method chaining.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable#has_mark_variant)
        """
        self._conditions.append(
            {
                "condition": "has_mark_variant",
                "value": int(value),
            }
        )
        return self

    def entity_properties(
        self, entity: str = "this", properties: dict | None = None
    ) -> "_LootConditions":
        """Requires the target entity to have specific properties (e.g. on_fire).

        Parameters:
            entity (str, optional): Target entity ("this", "killer", etc.). Defaults to "this".
            properties (dict, optional): Entity properties dictionary. Defaults to None.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self._conditions.append(
            {
                "condition": "entity_properties",
                "entity": entity,
                "properties": properties if properties is not None else {},
            }
        )
        return self

    # PascalCase aliases for backwards compatibility
    MatchTool = match_tool
    RandomChance = random_chance
    RandomChanceWithLooting = random_chance_with_looting
    RandomDifficultyChance = random_difficulty_chance
    RandomRegionalDifficultyChance = random_regional_difficulty_chance
    KilledByPlayer = killed_by_player
    KilledByPlayerOrPets = killed_by_player_or_pets
    KilledByEntity = killed_by_entity
    EntityKilled = entity_killed
    HasVariant = has_variant
    HasMarkVariant = has_mark_variant
    EntityProperties = entity_properties

    def __export__(self) -> list[dict]:
        """Export the conditions list for JSON serialization.

        Returns:
            list[dict]: List of condition dictionaries.
        """
        return self._conditions


LootConditions = _LootConditions


class _LootPoolEntry:
    """Represents a single entry in a loot pool with its associated properties and functions.

    Each entry can be an item, block, another loot table, or empty, and can have functions
    applied to modify the resulting loot.
    """

    def __init__(
        self,
        entry: Union[
            MinecraftBlockDescriptor,
            MinecraftItemDescriptor,
            Identifier,
            "LootTable",
            None,
        ],
        count: int = 1,
        weight: int = 1,
    ) -> None:
        """Initialize a loot pool entry.

        Parameters:
            entry (MinecraftBlockDescriptor | MinecraftItemDescriptor | Identifier | LootTable | None):
                The entry content (item, block, loot table, or None for empty).
            count (int, optional): Base count of items. Defaults to 1.
            weight (int, optional): Selection weight in the pool. Defaults to 1.
        """
        self._functions: _LootPoolEntryFunctions | None = None
        self._conditions: _LootConditions | None = None
        self._LootPoolEntry = {
            "name": str(entry),
            "count": count,
            "weight": weight,
            "functions": [],
        }

        if entry is None:
            self._LootPoolEntry["type"] = LootPoolType.Empty
        elif isinstance(
            entry, (MinecraftBlockDescriptor, MinecraftItemDescriptor, str)
        ):
            self._LootPoolEntry["type"] = LootPoolType.Item
        elif isinstance(entry, LootTable):
            self._LootPoolEntry["type"] = LootPoolType.LootTable

    def quality(self, quality: int):
        """Sets the quality value for this entry.

        Parameters:
            quality (int): The quality value to assign.

        Returns:
            _LootPoolEntry: Self for method chaining.
        """
        self._LootPoolEntry["quality"] = quality
        return self

    @property
    def functions(self):
        """Access the functions that can be applied to this loot entry.

        Returns:
            _LootPoolEntryFunctions: Functions interface for modifying this entry.
        """
        if self._functions is None:
            self._functions = _LootPoolEntryFunctions()
        return self._functions

    @property
    def conditions(self) -> "_LootConditions":
        """Access the conditions that must be met for this entry to be selected.

        Returns:
            _LootConditions: Conditions interface for configuring this entry.
        """
        if self._conditions is None:
            self._conditions = _LootConditions()
        return self._conditions

    def __export__(self):
        """Export the entry data for JSON serialization.

        Returns:
            dict: Entry data including functions and conditions.
        """
        if self._functions:
            self._LootPoolEntry["functions"] = self._functions.__export__()
        if self._conditions and self._conditions.__export__():
            self._LootPoolEntry["conditions"] = self._conditions.__export__()
        return self._LootPoolEntry


class _LootPool:
    """Represents a loot pool containing multiple entries with roll mechanics and tier bonuses.

    A loot pool groups related loot entries together and determines how many times
    the pool is rolled to select entries based on their weights.
    """

    def __init__(
        self,
        rolls: int | tuple[int, int] = 1,
    ):
        """Initialize a loot pool with the specified number of rolls.

        Parameters:
            rolls (int | tuple[int, int]): Number of times to roll this pool.
                Can be exact number or [min, max] range. Defaults to 1.
        """
        self._pool = {}
        self._entries: list[_LootPoolEntry] = []
        self._conditions: _LootConditions | None = None
        if isinstance(rolls, int):
            self._pool["rolls"] = rolls
        elif isinstance(rolls, (tuple, list)):
            self._pool["rolls"] = {"min": min(rolls), "max": max(rolls)}

    @property
    def conditions(self) -> "_LootConditions":
        """Access the conditions that must be met for this pool to be rolled.

        Returns:
            _LootConditions: Conditions interface for configuring this pool.
        """
        if self._conditions is None:
            self._conditions = _LootConditions()
        return self._conditions

    def tiers(
        self, bonus_chance: float = 0.0, bonus_rolls: int = 0, initial_range: int = 0
    ):
        """Configure tier-based bonus mechanics for this pool.

        Parameters:
            bonus_chance (float, optional): Chance for bonus tier effects (0.0-1.0). Defaults to 0.0.
            bonus_rolls (int, optional): Additional rolls from tier bonuses. Defaults to 0.
            initial_range (int, optional): Initial range for tier calculations. Defaults to 0.

        Returns:
            _LootPool: Self for method chaining.
        """
        self._pool.update({"tiers": {}})
        if bonus_chance != 0.0:
            self._pool["tiers"].update({"bonus_chance": clamp(bonus_chance, 0.0, 1.0)})
        if bonus_rolls != 0:
            self._pool["tiers"].update({"bonus_rolls": bonus_rolls})
        if initial_range != 0:
            self._pool["tiers"].update({"initial_range": initial_range})
        return self

    def entry(
        self,
        entry: Union[
            MinecraftBlockDescriptor,
            MinecraftItemDescriptor,
            Identifier,
            "LootTable",
            None,
        ],
        count: int = 1,
        weight: int = 1,
    ):
        """Add an entry to this loot pool.

        Parameters:
            entry (MinecraftBlockDescriptor | MinecraftItemDescriptor | Identifier | LootTable | None):
                The item, block, loot table, or None (for empty entry) to add.
            count (int, optional): Base count of this entry. Defaults to 1.
            weight (int, optional): Selection weight (higher = more likely). Defaults to 1.

        Returns:
            _LootPoolEntry: The created entry for further configuration.
        """
        pool_entry = _LootPoolEntry(entry, count, weight)
        self._entries.append(pool_entry)
        return pool_entry

    def __export__(self):
        """Export the pool data for JSON serialization.

        Returns:
            dict: Pool data including all entries and pool-level conditions.
        """
        for entry in self._entries:
            if "entries" not in self._pool:
                self._pool.update({"entries": []})
            self._pool["entries"].append(entry.__export__())
        if self._conditions and self._conditions.__export__():
            self._pool["conditions"] = self._conditions.__export__()
        return self._pool


class LootTable(AddonObject):
    """A Minecraft Bedrock loot table for defining random item/block drops and rewards.

    Loot tables are used throughout Minecraft to define what items drop when:
    - Entities die
    - Blocks are broken
    - Chests generate
    - Fishing occurs
    - Trading with villagers

    Each loot table contains one or more pools, and each pool contains weighted entries
    that can have functions applied to modify the resulting items.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitionlist?view=minecraft-bedrock-stable)
    """

    _extension = ".loot_table.json"
    _path = os.path.join(CONFIG.BP_PATH, "loot_tables", CONFIG.NAMESPACE)
    _object_type = "Loot Table"

    def __init__(self, name: str) -> None:
        """Initialize a LootTable instance.

        Parameters:
            name (str): The name of the loot table (used for filename and referencing).
        """
        super().__init__(name)
        self._content = JsonSchemes.loot_table()
        self._pools: list[_LootPool] = []

    def pool(
        self,
        rolls: int | tuple[int, int] = 1,
    ) -> "_LootPool":
        """Create a new loot pool in this loot table.

        Pools are rolled independently, so multiple pools allow for multiple
        categories of loot with different roll counts and mechanics.

        Parameters:
            rolls (int | list[int, int]): Number of times to roll this pool.
                Can be exact number or [min, max] range. Defaults to 1.

        Returns:
            _LootPool: The created pool for adding entries and configuration.
        """
        pool = _LootPool(rolls)
        self._pools.append(pool)
        return pool

    @property
    def table_path(self) -> str:
        """Get the relative path of this loot table for referencing.

        Returns:
            str: Relative path from behavior pack root.
        """
        return os.path.join(
            "loot_tables",
            CONFIG.NAMESPACE,
            self._name + self._extension,
        )

    def queue(self) -> "LootTable":
        """Queue this loot table for generation in the behavior pack.

        Exports all pools and their entries to JSON format and adds the
        loot table file to the generation queue.

        Returns:
            LootTable: Self for method chaining.
        """
        for pool in self._pools:
            self._content["pools"].append(pool.__export__())
        self.content(self._content)
        return super().queue()
