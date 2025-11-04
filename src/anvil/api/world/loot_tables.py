import os
from typing import Union, overload

from anvil.api.vanilla.effects import MinecraftPotionEffectTypes
from anvil.lib.config import CONFIG
from anvil.lib.enums import ExplorationMapDestinations, LootPoolType, RawTextConstructor
from anvil.lib.lib import clamp
from anvil.lib.schemas import (
    AddonObject,
    BlockDescriptor,
    EntityDescriptor,
    ItemDescriptor,
    JsonSchemes,
)
from anvil.lib.types import Identifier

__all__ = ["LootTable"]


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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_book_for_trading-trade-table-only
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_random_gear
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_randomly
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#enchant_with_levels
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#set_potion
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#specific_enchants
        """
        ...

    def SpecificEnchants(self, enchants):
        """Apply specific enchantments to an item.

        Parameters:
            enchants (tuple[str, ...] | tuple[tuple[str, int], ...]): Either a tuple of enchantment names
                for default levels, or a tuple of (enchantment_name, level) pairs for custom levels.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/enchantingtables?view=minecraft-bedrock-stable#specific_enchants
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#looting_enchant-loot-table-only
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_aux_value
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_block_state
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#random_dye
        """
        self._function.append(
            {
                "function": "random_dye",
            }
        )
        return self

    def SetActorId(self, actor: EntityDescriptor | Identifier | None):
        """Sets the entity ID of a spawn egg. Only works with spawn eggs.

        When actor is None, inherits the entity ID from the associated entity
        (e.g., rabbit drops rabbit spawn egg). Be careful with chest loot tables -
        omitting ID with player interaction creates unusable player spawn eggs.

        Parameters:
            actor (EntityDescriptor | Identifier | None): The entity identifier for the spawn egg,
                or None to inherit from the associated entity.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_actor_id
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_banner_details
        """
        self._function.append(
            {
                "function": "set_banner_details",
                "type": 1,
            }
        )
        return self

    def SetBookContent(
        self, author: str, title: str, pages: list[str | RawTextConstructor]
    ):
        """Sets the contents of a book including author, title, and pages.

        Can use rawtext for localization on pages only (not author/title).
        Remember to escape special characters like quotes and backslashes in rawtext.

        Parameters:
            author (str): The author of the book.
            title (str): The title of the book.
            pages (list[str | RawTextConstructor]): List of page contents as strings or rawtext.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_book_contents
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
    def SetCount(self, count: int):
        """Sets the quantity of items returned to an exact number.

        Parameters:
            count (int): Exact number of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    @overload
    def SetCount(self, count: tuple[int, int]):
        """Sets the quantity of items returned to a random number within a range.

        Parameters:
            count (tuple[int, int]): Min/max range of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.
        """
        ...

    def SetCount(self, count):
        """Sets the quantity of items returned.

        Parameters:
            count (int | tuple[int, int]): Exact number or min/max range of items to return.

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_count
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_damage
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_data
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_data_from_color_index
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_lore
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/itemmodtables?view=minecraft-bedrock-stable#set_name
        """
        self._function.append(
            {
                "function": "set_name",
                "name": name,
            }
        )
        return self

    # Miscellaneous Functions
    def ExplorationMap(self, destination: ExplorationMapDestinations):
        """Transforms a normal map into a treasure map marking the location of structures.

        Parameters:
            destination (ExplorationMapDestinations): The type of structure to mark
                (buriedtreasure, endcity, fortress, mansion, mineshaft, monument,
                pillageroutpost, ruins, shipwreck, stronghold, temple, village).

        Returns:
            _LootPoolEntryFunctions: Self for method chaining.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#exploration_map
        """
        self._function.append(
            {
                "function": "exploration_map",
                "destination": destination,
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#fill_container
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#furnace_smelt-loot-table-only
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

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitions/miscellaneoustables?view=minecraft-bedrock-stable#trader_material_type
        """
        self._function.append(
            {
                "function": "trader_material_type",
            }
        )
        return self

    def _export(self):
        """Export the list of functions for JSON serialization.

        Returns:
            list: List of function dictionaries.
        """
        return self._function


class _LootPoolEntry:
    """Represents a single entry in a loot pool with its associated properties and functions.

    Each entry can be an item, block, another loot table, or empty, and can have functions
    applied to modify the resulting loot.
    """

    def __init__(
        self,
        entry: Union[BlockDescriptor, ItemDescriptor, Identifier, "LootTable", None],
        count: int = 1,
        weight: int = 1,
    ) -> None:
        """Initialize a loot pool entry.

        Parameters:
            entry (BlockDescriptor | ItemDescriptor | Identifier | LootTable | None):
                The entry content (item, block, loot table, or None for empty).
            count (int, optional): Base count of items. Defaults to 1.
            weight (int, optional): Selection weight in the pool. Defaults to 1.
        """
        self._functions: _LootPoolEntryFunctions = None
        self._LootPoolEntry = {
            "name": str(entry),
            "count": count,
            "weight": weight,
            "functions": [],
        }

        if entry is None:
            self._LootPoolEntry["type"] = LootPoolType.Empty
        elif isinstance(entry, (BlockDescriptor, ItemDescriptor, Identifier)):
            self._LootPoolEntry["type"] = LootPoolType.Item
        elif isinstance(entry, "LootTable"):
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
        self._functions = _LootPoolEntryFunctions()
        return self._functions

    def _export(self):
        """Export the entry data for JSON serialization.

        Returns:
            dict: Entry data including functions.
        """
        if self._functions:
            self._LootPoolEntry["functions"] = self._functions._export()
        return self._LootPoolEntry


class _LootPool:
    """Represents a loot pool containing multiple entries with roll mechanics and tier bonuses.

    A loot pool groups related loot entries together and determines how many times
    the pool is rolled to select entries based on their weights.
    """

    def __init__(
        self,
        rolls: int | list[int, int] = 1,
    ):
        """Initialize a loot pool with the specified number of rolls.

        Parameters:
            rolls (int | list[int, int]): Number of times to roll this pool.
                Can be exact number or [min, max] range. Defaults to 1.
        """
        self._pool = {}
        self._entries: list[_LootPoolEntry] = []
        if isinstance(rolls, int):
            self._pool["rolls"] = rolls
        elif isinstance(rolls, tuple):
            self._pool["rolls"] = {"min": min(rolls), "max": max(rolls)}

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
        entry: Union[BlockDescriptor, ItemDescriptor, Identifier, "LootTable", None],
        count: int = 1,
        weight: int = 1,
    ):
        """Add an entry to this loot pool.

        Parameters:
            entry (BlockDescriptor | ItemDescriptor | Identifier | LootTable | None):
                The item, block, loot table, or None (for empty entry) to add.
            count (int, optional): Base count of this entry. Defaults to 1.
            weight (int, optional): Selection weight (higher = more likely). Defaults to 1.

        Returns:
            _LootPoolEntry: The created entry for further configuration.
        """
        pool_entry = _LootPoolEntry(entry, count, weight)
        self._entries.append(pool_entry)
        return pool_entry

    def _export(self):
        """Export the pool data for JSON serialization.

        Returns:
            dict: Pool data including all entries.
        """
        for entry in self._entries:
            if "entries" not in self._pool:
                self._pool.update({"entries": []})
            self._pool["entries"].append(entry._export())
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

    ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/loottablereference/examples/loottabledefinitionlist?view=minecraft-bedrock-stable
    """

    _extension = ".loot_table.json"
    _path = os.path.join(CONFIG.BP_PATH, "loot_tables", CONFIG.NAMESPACE)
    _object_type = "Loot Table"

    def __init__(self, name: str):
        """Initialize a LootTable instance.

        Parameters:
            name (str): The name of the loot table (used for filename and referencing).
        """
        super().__init__(name)
        self._content = JsonSchemes.loot_table()
        self._pools: list[_LootPool] = []

    def pool(
        self,
        rolls: int | list[int, int] = 1,
    ):
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
    def table_path(self):
        """Get the relative path of this loot table for referencing.

        Returns:
            str: Relative path from behavior pack root.
        """
        return os.path.join(
            "loot_tables",
            CONFIG.NAMESPACE,
            self._name + self._extension,
        )

    def queue(self):
        """Queue this loot table for generation in the behavior pack.

        Exports all pools and their entries to JSON format and adds the
        loot table file to the generation queue.

        Returns:
            LootTable: Self for method chaining.
        """
        for pool in self._pools:
            self._content["pools"].append(pool._export())
        self.content(self._content)
        return super().queue()
