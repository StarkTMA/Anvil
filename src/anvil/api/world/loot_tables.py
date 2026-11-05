from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Annotated, ClassVar, Literal

from anvil.api.actors.entity import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.items import Item
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import (
    AtLeastOne,
    Bounds,
    Chance,
    InRange,
    JsonFile,
    JsonObject,
    JsonValue,
    Length,
    MinMax,
    NonNegative,
    RangeMinMax,
    json_field,
)
from anvil.lib.jsonmodel.enums import ExplorationMapDestinations, LootPoolType

if TYPE_CHECKING:
    from anvil.api.vanilla.effects import MinecraftPotionEffectTypes
    from anvil.api.world.structures import JigsawStructureSet

__all__ = ["LootTable", "LootConditions"]


# region Conditions


class _RandomChance(JsonObject):
    condition: Literal["random_chance"] = json_field(
        default="random_chance", init=False
    )
    chance: Annotated[float, Chance] = json_field()


class _RandomChanceWithLooting(JsonObject):
    condition: Literal["random_chance_with_looting"] = json_field(
        default="random_chance_with_looting", init=False
    )
    chance: Annotated[float, Chance] = json_field()
    looting_multiplier: float = json_field()


class _RandomDifficultyChance(JsonObject):
    condition: Literal["random_difficulty_chance"] = json_field(
        default="random_difficulty_chance", init=False
    )
    default_chance: Annotated[float, Chance] = json_field()
    peaceful: Annotated[float, Chance] | None = None
    easy: Annotated[float, Chance] | None = None
    normal: Annotated[float, Chance] | None = None
    hard: Annotated[float, Chance] | None = None


class _RandomRegionalDifficultyChance(JsonObject):
    condition: Literal["random_regional_difficulty_chance"] = json_field(
        default="random_regional_difficulty_chance", init=False
    )
    max_chance: Annotated[float, Chance] = json_field()


class _KilledByPlayer(JsonObject):
    condition: Literal["killed_by_player"] = json_field(
        default="killed_by_player", init=False
    )


class _KilledByPlayerOrPets(JsonObject):
    condition: Literal["killed_by_player_or_pets"] = json_field(
        default="killed_by_player_or_pets", init=False
    )


class _KilledByEntity(JsonObject):
    condition: Literal["killed_by_entity"] = json_field(
        default="killed_by_entity", init=False
    )
    entity_type: str = json_field()


class _EntityKilled(JsonObject):
    condition: Literal["entity_killed"] = json_field(
        default="entity_killed", init=False
    )
    entity_type: str = json_field()


class _HasVariant(JsonObject):
    condition: Literal["has_variant"] = json_field(default="has_variant", init=False)
    value: int = json_field()


class _HasMarkVariant(JsonObject):
    condition: Literal["has_mark_variant"] = json_field(
        default="has_mark_variant", init=False
    )
    value: int = json_field()


class _EntityPropertyValues(JsonObject):
    """The entity properties to match."""

    on_fire: bool | None = None

    def set_on_fire(self, on_fire: bool | None) -> None:
        """Sets whether the entity is on fire."""
        self.on_fire = on_fire


class _EntityProperties(JsonObject):
    condition: Literal["entity_properties"] = json_field(
        default="entity_properties", init=False
    )
    entity: str = json_field()
    properties: _EntityPropertyValues = json_field(
        default_factory=_EntityPropertyValues
    )


class _ToolRange(JsonObject):
    """A tool value range: `range_min`, `range_max` or both."""

    range_min: int | None = None
    range_max: int | None = None


class _ToolEnchantment(JsonObject):
    """An enchantment the tool must have, with its level range."""

    enchantment: str = json_field()
    levels: _ToolRange = json_field(default_factory=_ToolRange)


class _MatchTool(JsonObject):
    condition: Literal["match_tool"] = json_field(default="match_tool", init=False)
    item: str | None = None
    count: Annotated[int | tuple[int, int], RangeMinMax] | None = None
    durability: _ToolRange | None = None
    enchantments: list[_ToolEnchantment] | None = None
    filter_any: list[str] | None = json_field(
        key="minecraft:match_tool_filter_any", default=None
    )
    filter_all: list[str] | None = json_field(
        key="minecraft:match_tool_filter_all", default=None
    )
    filter_none: list[str] | None = json_field(
        key="minecraft:match_tool_filter_none", default=None
    )

    def set_durability(self, range_min: int, range_max: int | None = None) -> None:
        """Sets the tool's minimum durability, and its maximum."""
        self.durability = _ToolRange(range_min=range_min, range_max=range_max)

    def add_enchantment(self, enchantment: str, min_level: int) -> None:
        """Adds an enchantment the tool must have, at least at this level."""
        if self.enchantments is None:
            self.enchantments = []
        levels = _ToolRange(range_min=min_level)
        self.enchantments.append(
            _ToolEnchantment(enchantment=enchantment, levels=levels)
        )


class _LootConditions(JsonValue):
    """Requirements that must all be met before a pool is rolled or an entry is picked.
    Each method adds a condition and returns the conditions, to chain them.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/loottableconditions?view=minecraft-bedrock-stable)
    """

    conditions: list[
        _MatchTool
        | _RandomChance
        | _RandomChanceWithLooting
        | _RandomDifficultyChance
        | _RandomRegionalDifficultyChance
        | _KilledByPlayer
        | _KilledByPlayerOrPets
        | _KilledByEntity
        | _EntityKilled
        | _HasVariant
        | _HasMarkVariant
        | _EntityProperties
    ] = json_field(default_factory=list)

    def match_tool(
        self,
        item: Item | str | None = None,
        enchantments: str | list[str | tuple[str, int]] | None = None,
        count: int | tuple[int, int] | None = None,
        durability: int | tuple[int, int] | None = None,
        filter_any: list[str] | None = None,
        filter_all: list[str] | None = None,
        filter_none: list[str] | None = None,
    ) -> _LootConditions:
        """Matches the tool used to break the block or make the loot drop.

        Args:
            item (Item | str, optional): The tool's item identifier.
            enchantments (str | list[str | tuple[str, int]], optional): Enchantments the tool
                must have: a name (any level), or `(name, minimum level)` pairs.
            count (int | tuple[int, int], optional): The tool's count, or its range.
            durability (int | tuple[int, int], optional): The minimum durability, or its range.
            filter_any (list[str], optional): Item tags of which the tool has at least one.
            filter_all (list[str], optional): Item tags the tool has all of.
            filter_none (list[str], optional): Item tags the tool has none of.

        Returns:
            _LootConditions: Self for method chaining.
        """
        condition = _MatchTool(
            item=None if item is None else str(item),
            count=count,
            filter_any=list(filter_any) if filter_any else None,
            filter_all=list(filter_all) if filter_all else None,
            filter_none=list(filter_none) if filter_none else None,
        )
        if durability is not None:
            if isinstance(durability, tuple):
                condition.set_durability(min(durability), max(durability))
            else:
                condition.set_durability(durability)
        if enchantments is not None:
            for enchantment in (
                [enchantments] if isinstance(enchantments, str) else enchantments
            ):
                if isinstance(enchantment, str):
                    condition.add_enchantment(enchantment, 1)
                else:
                    condition.add_enchantment(str(enchantment[0]), enchantment[1])
        self.conditions.append(condition)
        return self

    def random_chance(self, chance: float) -> _LootConditions:
        """Applies a chance, from 0 to 1, that the loot drops.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_RandomChance(chance=chance))
        return self

    def random_chance_with_looting(
        self, chance: float, looting_multiplier: float
    ) -> _LootConditions:
        """Applies a chance, from 0 to 1, raised by `looting_multiplier` per looting level.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(
            _RandomChanceWithLooting(
                chance=chance, looting_multiplier=looting_multiplier
            )
        )
        return self

    def random_difficulty_chance(
        self,
        default_chance: float,
        peaceful: float | None = None,
        easy: float | None = None,
        normal: float | None = None,
        hard: float | None = None,
    ) -> _LootConditions:
        """Applies a chance, from 0 to 1, that depends on the world difficulty.

        Args:
            default_chance (float): The chance on difficulties not set.
            peaceful (float, optional): The chance on Peaceful.
            easy (float, optional): The chance on Easy.
            normal (float, optional): The chance on Normal.
            hard (float, optional): The chance on Hard.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(
            _RandomDifficultyChance(
                default_chance=default_chance,
                peaceful=peaceful,
                easy=easy,
                normal=normal,
                hard=hard,
            )
        )
        return self

    def random_regional_difficulty_chance(self, max_chance: float) -> _LootConditions:
        """Applies a chance, up to `max_chance`, that grows with the regional difficulty.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_RandomRegionalDifficultyChance(max_chance=max_chance))
        return self

    def killed_by_player(self) -> _LootConditions:
        """Requires the entity to have been killed by a player.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_KilledByPlayer())
        return self

    def killed_by_player_or_pets(self) -> _LootConditions:
        """Requires the entity to have been killed by a player or their tamed pets.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_KilledByPlayerOrPets())
        return self

    def killed_by_entity(self, entity_type: str) -> _LootConditions:
        """Requires the entity to have been killed by an entity of this type.

        Args:
            entity_type (str): The killer's identifier, such as `minecraft:skeleton`.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_KilledByEntity(entity_type=str(entity_type)))
        return self

    def entity_killed(self, entity_type: str) -> _LootConditions:
        """Requires the killed entity to be of this type.

        Args:
            entity_type (str): The killed entity's identifier, such as `minecraft:magma_cube`.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_EntityKilled(entity_type=str(entity_type)))
        return self

    def has_variant(self, value: int) -> _LootConditions:
        """Requires the entity to have this variant.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_HasVariant(value=value))
        return self

    def has_mark_variant(self, value: int) -> _LootConditions:
        """Requires the entity to have this mark variant.

        Returns:
            _LootConditions: Self for method chaining.
        """
        self.conditions.append(_HasMarkVariant(value=value))
        return self

    def entity_properties(
        self, entity: str = "this", on_fire: bool | None = None
    ) -> _LootConditions:
        """Requires an entity to have these properties.

        Args:
            entity (str, optional): The entity checked, such as `this`. Defaults to "this".
            on_fire (bool, optional): The entity is on fire, or not.

        Returns:
            _LootConditions: Self for method chaining.
        """
        condition = _EntityProperties(entity=entity)
        condition.properties.set_on_fire(on_fire)
        self.conditions.append(condition)
        return self

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


LootConditions = _LootConditions

# endregion

# region Functions


class _EnchantBookForTrading(JsonObject):
    function: Literal["enchant_book_for_trading"] = json_field(
        default="enchant_book_for_trading", init=False
    )
    base_cost: int = json_field()
    base_random_cost: int = json_field()
    per_level_random_cost: int = json_field()
    per_level_cost: int = json_field()


class _EnchantRandomGear(JsonObject):
    function: Literal["enchant_random_gear"] = json_field(
        default="enchant_random_gear", init=False
    )
    chance: Annotated[float, NonNegative] = json_field()


class _EnchantRandomly(JsonObject):
    function: Literal["enchant_randomly"] = json_field(
        default="enchant_randomly", init=False
    )
    treasure: bool = json_field(default=False)


class _EnchantWithLevels(JsonObject):
    function: Literal["enchant_with_levels"] = json_field(
        default="enchant_with_levels", init=False
    )
    levels: Annotated[tuple[int, int], MinMax] = json_field()
    treasure: bool = json_field(default=False)


class _SetPotion(JsonObject):
    function: Literal["set_potion"] = json_field(default="set_potion", init=False)
    id: str = json_field()


class _EnchantLevel(JsonObject):
    """An enchantment and its level."""

    id: str = json_field()
    level: Annotated[int, AtLeastOne] = json_field()


class _SpecificEnchants(JsonObject):
    function: Literal["specific_enchants"] = json_field(
        default="specific_enchants", init=False
    )
    enchants: list[str] | list[_EnchantLevel] = json_field()


class _LootingEnchant(JsonObject):
    function: Literal["looting_enchant"] = json_field(
        default="looting_enchant", init=False
    )
    count: Annotated[tuple[int, int], MinMax] = json_field()


class _RandomAuxValue(JsonObject):
    function: Literal["random_aux_value"] = json_field(
        default="random_aux_value", init=False
    )
    values: Annotated[tuple[int, int], MinMax] = json_field()


class _RandomBlockState(JsonObject):
    function: Literal["random_block_state"] = json_field(
        default="random_block_state", init=False
    )
    block_state: str = json_field()
    values: Annotated[tuple[int, int], MinMax] = json_field()


class _RandomDye(JsonObject):
    function: Literal["random_dye"] = json_field(default="random_dye", init=False)


class _SetActorId(JsonObject):
    function: Literal["set_actor_id"] = json_field(default="set_actor_id", init=False)
    id: str | None = None


class _BannerPattern(JsonObject):
    """A pattern of a banner and its color."""

    pattern: str = json_field()
    color: str = json_field()


class _SetBannerDetails(JsonObject):
    function: Literal["set_banner_details"] = json_field(
        default="set_banner_details", init=False
    )
    type: Literal[0, 1, "default", "illager_captain"] = json_field(default=1)
    base_color: str | None = None
    patterns: Annotated[list[_BannerPattern], Length(maximum=6)] | None = None

    def add_pattern(self, pattern: str, color: str) -> None:
        """Adds a pattern and its color."""
        if self.patterns is None:
            self.patterns = []
        self.patterns.append(_BannerPattern(pattern=pattern, color=color))

    def __validate__(self) -> None:
        if self.patterns and self.type not in (0, "default"):
            raise ValueError("Only default banners (type 0) can have patterns.")


class _ExplosionDecay(JsonObject):
    function: Literal["explosion_decay"] = json_field(
        default="explosion_decay", init=False
    )


class _StewEffect(JsonObject):
    """An effect a suspicious stew can have."""

    id: Annotated[int, NonNegative] = json_field()


class _SetStewEffect(JsonObject):
    function: Literal["minecraft:set_stew_effect"] = json_field(
        default="minecraft:set_stew_effect", init=False
    )
    effects: Annotated[list[_StewEffect], Length(minimum=1)] = json_field(
        default_factory=list
    )


class _SetOminousBottleAmplifier(JsonObject):
    function: Literal["set_ominous_bottle_amplifier"] = json_field(
        default="set_ominous_bottle_amplifier", init=False
    )
    amplifier: Annotated[
        int | tuple[int, int], NonNegative, Bounds("min", "max", exact=True)
    ] = json_field()


class _SetArmorTrim(JsonObject):
    function: Literal["set_armor_trim"] = json_field(
        default="set_armor_trim", init=False
    )
    material: str = json_field()
    pattern: str = json_field()


class _SetBookContents(JsonObject):
    function: Literal["set_book_contents"] = json_field(
        default="set_book_contents", init=False
    )
    author: str = json_field()
    title: str = json_field()
    pages: list[str] = json_field(default_factory=list)


class _SetCount(JsonObject):
    function: Literal["set_count"] = json_field(default="set_count", init=False)
    count: Annotated[int | tuple[int, int], MinMax] = json_field()


class _SetDamage(JsonObject):
    function: Literal["set_damage"] = json_field(default="set_damage", init=False)
    damage: Annotated[float | tuple[float, float], InRange(0, 1), MinMax] = json_field()


class _SetData(JsonObject):
    function: Literal["set_data"] = json_field(default="set_data", init=False)
    data: int = json_field()


class _SetDataFromColorIndex(JsonObject):
    function: Literal["set_data_from_color_index"] = json_field(
        default="set_data_from_color_index", init=False
    )


class _SetLore(JsonObject):
    function: Literal["set_lore"] = json_field(default="set_lore", init=False)
    lore: list[str] = json_field(default_factory=list)


class _SetName(JsonObject):
    function: Literal["set_name"] = json_field(default="set_name", init=False)
    name: str = json_field()


class _ExplorationMap(JsonObject):
    function: Literal["exploration_map"] = json_field(
        default="exploration_map", init=False
    )
    destination: str | None = None


class _FillContainer(JsonObject):
    function: Literal["fill_container"] = json_field(
        default="fill_container", init=False
    )
    loot_table: str = json_field()


class _FurnaceSmelt(JsonObject):
    function: Literal["furnace_smelt"] = json_field(default="furnace_smelt", init=False)
    conditions: _LootConditions = json_field(default_factory=_LootConditions)


class _TraderMaterialType(JsonObject):
    function: Literal["trader_material_type"] = json_field(
        default="trader_material_type", init=False
    )


class _LootFunctionBuilder:
    """The function builders shared by loot entries and trade items. Each adds a function
    and returns the builder, to chain them."""

    __slots__ = ()

    def _add_function(self, function: JsonObject) -> None:
        raise NotImplementedError

    def EnchantBookForTrading(
        self,
        base_cost: int,
        base_random_cost: int,
        per_level_random_cost: int,
        per_level_cost: int,
    ):
        """Enchants a book with the villager trade algorithm. Trade tables only.

        The cost is `base_cost + (base_random_cost + level * per_level_random_cost) +
        level * per_level_cost`.

        Args:
            base_cost (int): The base cost.
            base_random_cost (int): The base random cost.
            per_level_random_cost (int): The random cost per enchantment level.
            per_level_cost (int): The cost per enchantment level.
        """
        self._add_function(
            _EnchantBookForTrading(
                base_cost=base_cost,
                base_random_cost=base_random_cost,
                per_level_random_cost=per_level_random_cost,
                per_level_cost=per_level_cost,
            )
        )
        return self

    def EnchantRandomGear(self, chance: float):
        """Enchants the item like the equipment vanilla mobs spawn with.

        The chance drops to 0 on Peaceful and Easy and to about 2/3 on Normal. A chance
        above 1 makes up for the drop on Normal: 2.0 always enchants on Normal and Hard.

        Args:
            chance (float): The chance modifier, 0 or more.
        """
        self._add_function(_EnchantRandomGear(chance=chance))
        return self

    def EnchantRandomly(self, treasure: bool = False):
        """Adds a random enchantment compatible with the item.

        Args:
            treasure (bool, optional): Allow treasure enchantments. Defaults to False.
        """
        self._add_function(_EnchantRandomly(treasure=treasure))
        return self

    def EnchantWithLevels(self, levels: tuple[int, int], treasure: bool = False):
        """Enchants the item like an enchanting table with this many XP levels.

        Args:
            levels (tuple[int, int]): The minimum and maximum XP levels.
            treasure (bool, optional): Allow treasure enchantments. Defaults to False.
        """
        self._add_function(_EnchantWithLevels(levels=levels, treasure=treasure))
        return self

    def SetPotion(self, id: MinecraftPotionEffectTypes | str):
        """Sets the potion type of a potion, splash potion or lingering potion.

        Args:
            id (MinecraftPotionEffectTypes | str): The potion type.
        """
        self._add_function(_SetPotion(id=str(id)))
        return self

    def SpecificEnchants(self, enchants: tuple[str, ...] | tuple[tuple[str, int], ...]):
        """Adds these enchantments, even to items that can't normally have them. Maximum
        levels can't be exceeded.

        Args:
            enchants (tuple[str, ...] | tuple[tuple[str, int], ...]): Enchantment names, or
                `(name, level)` pairs.
        """
        if enchants and isinstance(enchants[0], str):
            function = _SpecificEnchants(enchants=list(enchants))
        else:
            function = _SpecificEnchants(
                enchants=[
                    _EnchantLevel(id=name, level=level) for name, level in enchants
                ]
            )
        self._add_function(function)
        return self

    def LootingEnchant(self, count: tuple[int, int]):
        """Adds items per looting level of the weapon that killed the entity. Loot tables
        of entity deaths only.

        Args:
            count (tuple[int, int]): The minimum and maximum items added per level.
        """
        self._add_function(_LootingEnchant(count=count))
        return self

    def RandomAuxValue(self, values: tuple[int, int]):
        """Picks a random auxiliary value for the item, such as a dye color.

        Args:
            values (tuple[int, int]): The minimum and maximum values.
        """
        self._add_function(_RandomAuxValue(values=values))
        return self

    def RandomBlockState(self, block_state: str, values: tuple[int, int]):
        """Picks a random value for a block state of the item, such as a wool color.

        Args:
            block_state (str): The block state, such as `color`.
            values (tuple[int, int]): The minimum and maximum values.
        """
        self._add_function(_RandomBlockState(block_state=block_state, values=values))
        return self

    def RandomDye(self):
        """Gives leather items a random color."""
        self._add_function(_RandomDye())
        return self

    def SetActorId(self, actor: str | Entity | None = None):
        """Sets the entity of a spawn egg.

        Args:
            actor (str | Entity, optional): The entity. None takes the
                entity the loot table belongs to; in a chest, that is the player who opens it.
        """
        self._add_function(_SetActorId(id=None if actor is None else str(actor)))
        return self

    def SetBannerDetails(
        self,
        type: Literal[0, 1, "default", "illager_captain"] = 1,
        base_color: str | None = None,
        patterns: list[tuple[str, str]] | None = None,
    ):
        """Sets the banner type, color and patterns. Banners only.

        Args:
            type (Literal[0, 1, "default", "illager_captain"], optional): The banner type:
                0 or "default", 1 or "illager_captain". Defaults to 1.
            base_color (str, optional): The banner color, such as `silver`.
            patterns (list[tuple[str, str]], optional): Up to 6 `(pattern, color)` pairs, such as
                `("gradient", "black")`. Default banners only.
        """
        function = _SetBannerDetails(type=type, base_color=base_color)
        for pattern, color in patterns or ():
            function.add_pattern(pattern, color)
        self._add_function(function)
        return self

    def ExplosionDecay(self):
        """When an explosion drops the loot, destroys each item with a chance of 1 in the
        explosion radius."""
        self._add_function(_ExplosionDecay())
        return self

    def SetStewEffect(self, effects: list[int]):
        """Gives a suspicious stew one of these effects, picked at random.

        Args:
            effects (list[int]): The stew effect ids.
        """
        self._add_function(
            _SetStewEffect(effects=[_StewEffect(id=effect) for effect in effects])
        )
        return self

    def SetOminousBottleAmplifier(self, amplifier: int | tuple[int, int]):
        """Sets the Bad Omen amplifier of an ominous bottle.

        Args:
            amplifier (int | tuple[int, int]): The amplifier, or the minimum and maximum.
        """
        self._add_function(_SetOminousBottleAmplifier(amplifier=amplifier))
        return self

    def SetArmorTrim(self, material: str, pattern: str):
        """Trims armor that can take a trim.

        Args:
            material (str): The trim material, such as `netherite`.
            pattern (str): The trim pattern, such as `wayfinder`.
        """
        self._add_function(_SetArmorTrim(material=material, pattern=pattern))
        return self

    def SetBookContent(self, author: str, title: str, pages: list[str]):
        """Sets the author, title and pages of a book. Pages can be `rawtext`, the author
        and title can't.

        Args:
            author (str): The author.
            title (str): The title.
            pages (list[str]): The pages.
        """
        self._add_function(
            _SetBookContents(author=author, title=title, pages=[str(p) for p in pages])
        )
        return self

    def SetCount(self, count: int | tuple[int, int]):
        """Sets how many items drop.

        Args:
            count (int | tuple[int, int]): The number, or the minimum and maximum.
        """
        self._add_function(_SetCount(count=count))
        return self

    def SetDamage(self, damage: float | tuple[float, float]):
        """Sets the durability left, from 0 (none) to 1 (undamaged).

        Args:
            damage (float | tuple[float, float]): The durability, or the minimum and maximum.
        """
        self._add_function(_SetDamage(damage=damage))
        return self

    def SetData(self, data: int):
        """Sets the data value of the item, such as a potion variant."""
        self._add_function(_SetData(data=data))
        return self

    def SetDataFromColorIndex(self):
        """Takes the data value from the entity's color index, like a pink sheep's wool."""
        self._add_function(_SetDataFromColorIndex())
        return self

    def SetLore(self, lore: tuple[str, ...]):
        """Sets the lore of the item, one line per string. No `rawtext`."""
        self._add_function(_SetLore(lore=list(lore)))
        return self

    def SetName(self, name: str):
        """Sets the name of the item. No `rawtext`."""
        self._add_function(_SetName(name=name))
        return self

    def ExplorationMap(
        self,
        destination: (
            ExplorationMapDestinations | JigsawStructureSet | str | None
        ) = None,
    ):
        """Turns a map into a treasure map to a structure.

        Args:
            destination (ExplorationMapDestinations | JigsawStructureSet | str, optional): The
                structure the map leads to.
        """
        self._add_function(
            _ExplorationMap(
                destination=None if destination is None else str(destination)
            )
        )
        return self

    def FillContainer(self, lootTable: LootTable):
        """Fills a container item, such as a chest, from a loot table when it is opened.
        Name the container with `SetName` to tell it apart from an empty one.

        Args:
            lootTable (LootTable): The loot table.
        """
        self._add_function(_FillContainer(loot_table=lootTable.table_path))
        return self

    def FurnaceSmelt(self):
        """Drops the cooked item when the entity dies on fire. Loot tables of entity deaths
        only."""
        function = _FurnaceSmelt()
        function.conditions.entity_properties("this", on_fire=True)
        self._add_function(function)
        return self

    def TraderMaterialType(self):
        """Sets the material of the item a fisherman wants, such as the boat type."""
        self._add_function(_TraderMaterialType())
        return self


class _LootFunctions(JsonValue, _LootFunctionBuilder):
    """Functions that change an entry's items. Each method adds a function and returns
    the functions, to chain them.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/lootandtradetablefunctions?view=minecraft-bedrock-stable)
    """

    functions: list[
        _EnchantBookForTrading
        | _EnchantRandomGear
        | _EnchantRandomly
        | _EnchantWithLevels
        | _SetPotion
        | _SpecificEnchants
        | _LootingEnchant
        | _RandomAuxValue
        | _RandomBlockState
        | _RandomDye
        | _SetActorId
        | _SetBannerDetails
        | _SetBookContents
        | _SetCount
        | _SetDamage
        | _SetData
        | _SetDataFromColorIndex
        | _SetLore
        | _SetName
        | _ExplorationMap
        | _FillContainer
        | _FurnaceSmelt
        | _TraderMaterialType
        | _ExplosionDecay
        | _SetStewEffect
        | _SetOminousBottleAmplifier
        | _SetArmorTrim
    ] = json_field(default_factory=list)

    def _add_function(self, function: JsonObject) -> None:
        self.functions.append(function)


# endregion

# region Loot table


class _LootPoolEntry(JsonObject):
    """An entry of a pool: an item, another loot table, or nothing."""

    type: Literal["item", "loot_table", "empty"] = json_field()
    name: str | None = None
    count: int = json_field(default=1)
    weight: Annotated[int, AtLeastOne] = json_field(default=1)
    quality: int | None = None
    functions: _LootFunctions = json_field(default_factory=_LootFunctions)
    conditions: _LootConditions = json_field(default_factory=_LootConditions)

    def set_quality(self, quality: int) -> _LootPoolEntry:
        """Sets how much the luck of the player changes the entry's weight.

        Returns:
            _LootPoolEntry: Self for method chaining.
        """
        self.quality = quality
        return self


class _LootPoolTiers(JsonObject):
    """Tiers of a pool: the entry is picked by tier rather than by weight."""

    initial_range: int | None = None
    bonus_rolls: int | None = None
    bonus_chance: Annotated[float, Chance] | None = None


class _LootPool(JsonObject):
    """A pool: rolled `rolls` times, each roll picks one of its entries by weight."""

    __required__: ClassVar[tuple[str, ...]] = ("rolls",)

    rolls: Annotated[int | tuple[int, int], MinMax] = json_field(default=1)
    tiers: _LootPoolTiers | None = None
    conditions: _LootConditions = json_field(default_factory=_LootConditions)
    entries: list[_LootPoolEntry] = json_field(default_factory=list)

    def set_tiers(
        self, bonus_chance: float = 0.0, bonus_rolls: int = 0, initial_range: int = 0
    ) -> _LootPool:
        """Picks entries by tier.

        Args:
            bonus_chance (float, optional): The chance, from 0 to 1, of a bonus roll.
            bonus_rolls (int, optional): The bonus rolls.
            initial_range (int, optional): The initial tier range.

        Returns:
            _LootPool: Self for method chaining.
        """
        self.tiers = _LootPoolTiers(
            bonus_chance=bonus_chance or None,
            bonus_rolls=bonus_rolls or None,
            initial_range=initial_range or None,
        )
        return self

    def entry(
        self,
        entry: str | Block | BlockDescriptor | Item | LootTable | None,
        count: int = 1,
        weight: int = 1,
    ) -> _LootPoolEntry:
        """Adds an entry to the pool.

        Args:
            entry (Block | BlockDescriptor | Item | str | LootTable | None):
                An item or block, another loot table, or None for an entry that drops nothing.
            count (int, optional): The entry's count. Defaults to 1.
            weight (int, optional): Its weight against the other entries, at least 1.

        Returns:
            _LootPoolEntry: The entry, to add functions and conditions to.
        """
        if entry is None:
            entry_type, name = LootPoolType.Empty, None
        elif isinstance(entry, LootTable):
            entry_type, name = LootPoolType.LootTable, entry.table_path
        else:
            entry_type, name = LootPoolType.Item, str(entry)
        pool_entry = _LootPoolEntry(
            type=entry_type, name=name, count=count, weight=weight
        )
        self.entries.append(pool_entry)
        return pool_entry


class _LootTableFile(JsonObject):
    """The content of `loot_tables/<namespace>/<name>.loot_table.json`."""

    pools: list[_LootPool] = json_field(default_factory=list)

    def add_pool(self, rolls: int | tuple[int, int] = 1) -> _LootPool:
        """Adds a pool and returns it."""
        pool = _LootPool(rolls=rolls)
        self.pools.append(pool)
        return pool


class LootTable(JsonFile[_LootTableFile]):
    """A loot table: what drops from entities, blocks, chests, fishing and other rewards.

    Each pool is rolled on its own, and each roll picks one of its entries by weight.
    Entries take functions (`entry.functions.SetCount(...)`) and conditions
    (`entry.conditions.random_chance(...)`).

    ```python
    table = LootTable("ruins_chest")
    pool = table.pool((1, 3))
    pool.entry("minecraft:emerald", weight=5).functions.SetCount((1, 4))
    pool.entry(None, weight=10)
    table.queue()
    ```

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/introductiontoloottables?view=minecraft-bedrock-stable)
    """

    _extension = ".loot_table.json"
    _pack = Pack.BP
    _object_type = "Loot Table"

    def __init__(self, name: str) -> None:
        """Initialize a LootTable instance.

        Args:
            name (str): The name of the loot table (used for filename and referencing).
        """
        super().__init__(name)
        self._folder = Path("loot_tables", CONFIG.NAMESPACE)

    def pool(self, rolls: int | tuple[int, int] = 1) -> _LootPool:
        """Adds a pool to the loot table.

        Args:
            rolls (int | tuple[int, int], optional): How many times the pool is rolled, or the
                minimum and maximum. Defaults to 1.

        Returns:
            _LootPool: The pool, to add entries, conditions and tiers to.
        """
        return self._document.add_pool(rolls)

    @property
    def table_path(self) -> str:
        """The loot table's path from the behavior pack root, as other files reference it."""
        return PurePosixPath(
            "loot_tables", CONFIG.NAMESPACE, self.identifier.name + self._extension
        ).as_posix()

    def queue(self) -> "LootTable":
        """Queues the loot table for export."""
        return super().queue()
