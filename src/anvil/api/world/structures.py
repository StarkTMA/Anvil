from __future__ import annotations

from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Annotated, ClassVar, Literal

from anvil.api.core.core import ANVIL
from anvil.api.core.filters import Filter
from anvil.api.features.feature import Feature
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import JIGSAW_VERSION
from anvil.lib.jsonmodel import (
    AtLeastOne,
    BlockSpecifier,
    Chance,
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    NonNegative,
    Wrapped,
    json_field,
)
from anvil.lib.lib import Directory, salt_from_str
from anvil.lib.schemas import MinecraftBlockDescriptor

if TYPE_CHECKING:
    from anvil.api.world.loot_tables import LootTable

__all__ = [
    "Structure",
    "JigsawStructureTemplatePool",
    "JigsawStructureSet",
]


def _block_name(block: MinecraftBlockDescriptor | str) -> str:
    return block if isinstance(block, str) else block.identifier


# region Processors


class _UniformLimit(JsonObject):
    """A random limit, picked uniformly from `min_inclusive` to `max_inclusive`."""

    type: Literal["uniform"] = json_field(default="uniform", init=False)
    min_inclusive: Annotated[int, NonNegative] = json_field()
    max_inclusive: Annotated[int, NonNegative] = json_field()

    def __validate__(self) -> None:
        if self.max_inclusive <= self.min_inclusive:
            raise ValueError(
                "A uniform limit's maximum must be greater than its minimum."
            )


class _BlockPredicate(JsonObject):
    """A test on a block: the structure's block (`input_predicate`) or the world block it
    replaces (`location_predicate`). Each builder sets the test and only its fields."""

    __required__: ClassVar[tuple[str, ...]] = ("predicate_type",)

    predicate_type: (
        Literal[
            "minecraft:always_true",
            "minecraft:block_match",
            "minecraft:random_block_match",
            "minecraft:blockstate_match",
            "minecraft:random_blockstate_match",
            "minecraft:tag_match",
        ]
        | None
    ) = None
    block: str | None = None
    block_state: Annotated[MinecraftBlockDescriptor | str, BlockSpecifier] | None = None
    probability: Annotated[float, Chance] | None = None
    tag: str | None = None

    def _clear(self) -> None:
        self.block = None
        self.block_state = None
        self.probability = None
        self.tag = None

    def always_true(self) -> None:
        """Always matches."""
        self._clear()
        self.predicate_type = "minecraft:always_true"

    def block_match(self, block: MinecraftBlockDescriptor | str) -> None:
        """Matches the block, whatever its states.

        Args:
            block (MinecraftBlockDescriptor | str): The block identifier.
        """
        self._clear()
        self.predicate_type = "minecraft:block_match"
        self.block = _block_name(block)

    def random_block_match(
        self, block: MinecraftBlockDescriptor | str, probability: float
    ) -> None:
        """Matches the block, whatever its states, with a chance.

        Args:
            block (MinecraftBlockDescriptor | str): The block identifier.
            probability (float): The chance to match, from 0 to 1.
        """
        self._clear()
        self.predicate_type = "minecraft:random_block_match"
        self.block = _block_name(block)
        self.probability = probability

    def block_state_match(self, block: MinecraftBlockDescriptor | str) -> None:
        """Matches the block and the states of its descriptor.

        Args:
            block (MinecraftBlockDescriptor | str): The block, with the states to match.
        """
        self._clear()
        self.predicate_type = "minecraft:blockstate_match"
        self.block_state = block

    def random_block_state_match(
        self, block: MinecraftBlockDescriptor | str, probability: float
    ) -> None:
        """Matches the block and the states of its descriptor, with a chance.

        Args:
            block (MinecraftBlockDescriptor | str): The block, with the states to match.
            probability (float): The chance to match, from 0 to 1.
        """
        self._clear()
        self.predicate_type = "minecraft:random_blockstate_match"
        self.block_state = block
        self.probability = probability

    def tag_match(self, tag: str) -> None:
        """Matches blocks with the block tag.

        Args:
            tag (str): The block tag.
        """
        self._clear()
        self.predicate_type = "minecraft:tag_match"
        self.tag = tag

    def __validate__(self) -> None:
        if self.predicate_type is None:
            return
        needs = {
            "minecraft:block_match": ("block",),
            "minecraft:random_block_match": ("block", "probability"),
            "minecraft:blockstate_match": ("block_state",),
            "minecraft:random_blockstate_match": ("block_state", "probability"),
            "minecraft:tag_match": ("tag",),
        }.get(self.predicate_type, ())
        for name in needs:
            if getattr(self, name) is None:
                raise ValueError(f"A {self.predicate_type} predicate needs {name}.")


class _PositionPredicate(JsonObject):
    """A test on the distance between the world block and the structure's origin."""

    __required__: ClassVar[tuple[str, ...]] = ("predicate_type",)

    predicate_type: (
        Literal["minecraft:always_true", "minecraft:axis_aligned_linear_pos"] | None
    ) = None
    min_chance: Annotated[float, InRange(0, 1, max_exclusive=True)] | None = None
    max_chance: Annotated[float, InRange(0, 1, max_exclusive=True)] | None = None
    min_dist: Annotated[int, NonNegative] | None = None
    max_dist: Annotated[int, NonNegative] | None = None
    axis: Literal["x", "y", "z"] | None = None

    def always_true(self) -> None:
        """Always matches."""
        self.min_chance = self.max_chance = None
        self.min_dist = self.max_dist = None
        self.axis = None
        self.predicate_type = "minecraft:always_true"

    def axis_aligned_linear_pos(
        self,
        min_chance: float,
        max_chance: float,
        min_distance: int,
        max_distance: int,
        axis: Literal["x", "y", "z"],
    ) -> None:
        """Matches with a chance that goes from `min_chance` at `min_distance` to `max_chance`
        at `max_distance` along the axis.

        Args:
            min_chance (float): The chance at the minimum distance, from 0 up to 1 (excluded).
            max_chance (float): The chance at the maximum distance, greater than `min_chance`
                and below 1.
            min_distance (int): The distance from the origin where the chance starts.
            max_distance (int): The distance from the origin where the chance ends.
            axis (Literal["x", "y", "z"]): The axis the distance is measured along.
        """
        self.predicate_type = "minecraft:axis_aligned_linear_pos"
        self.min_chance = min_chance
        self.max_chance = max_chance
        self.min_dist = min_distance
        self.max_dist = max_distance
        self.axis = axis

    def __validate__(self) -> None:
        if self.predicate_type != "minecraft:axis_aligned_linear_pos":
            return
        if self.max_chance <= self.min_chance:
            raise ValueError("max_chance must be greater than min_chance.")


class _BlockEntityModifier(JsonObject):
    """What happens to the placed block's block entity, such as a chest's loot."""

    __required__: ClassVar[tuple[str, ...]] = ("type",)

    type: (
        Literal["minecraft:passthrough", "minecraft:append_loot", "minecraft:clear"]
        | None
    ) = None
    loot_table: str | None = None

    def passthrough(self) -> None:
        """Leaves the block entity as it is."""
        self.loot_table = None
        self.type = "minecraft:passthrough"

    def append_loot(self, loot_table: LootTable | str) -> None:
        """Gives the block entity a loot table.

        Args:
            loot_table (LootTable | str): The loot table, or its path from the pack root.
        """
        from anvil.api.world.loot_tables import LootTable

        self.type = "minecraft:append_loot"
        self.loot_table = (
            loot_table.table_path
            if isinstance(loot_table, LootTable)
            else str(loot_table)
        )

    def clear(self) -> None:
        """Clears the block entity's data."""
        self.loot_table = None
        self.type = "minecraft:clear"

    def __validate__(self) -> None:
        if self.type == "minecraft:append_loot" and self.loot_table is None:
            raise ValueError("An append_loot modifier needs a loot table.")


class _ProcessorRule(JsonObject):
    """A rule: when its predicates match, the block becomes `output_state`."""

    __required__: ClassVar[tuple[str, ...]] = ("output_state",)

    input_predicate: _BlockPredicate = json_field(default_factory=_BlockPredicate)
    location_predicate: _BlockPredicate = json_field(default_factory=_BlockPredicate)
    position_predicate: _PositionPredicate = json_field(
        default_factory=_PositionPredicate
    )
    output_state: Annotated[MinecraftBlockDescriptor | str, BlockSpecifier] | None = (
        None
    )
    block_entity_modifier: _BlockEntityModifier = json_field(
        default_factory=_BlockEntityModifier
    )

    def set_output_state(self, block: MinecraftBlockDescriptor | str) -> None:
        """Sets the block placed when the rule matches.

        Args:
            block (MinecraftBlockDescriptor | str): The block, with its states.
        """
        self.output_state = block

    def __validate__(self) -> None:
        if self.output_state is None:
            raise ValueError("A block rule needs an output state.")


class _BlockIgnoreProcessor(JsonObject):
    """Leaves the listed blocks out of the placed structure."""

    processor_type: Literal["minecraft:block_ignore"] = json_field(
        default="minecraft:block_ignore", init=False
    )
    blocks: list[str] = json_field(default_factory=list)

    def add_block(self, block: MinecraftBlockDescriptor | str) -> None:
        """Adds a block to leave out."""
        self.blocks.append(_block_name(block))


class _ProtectedBlocksProcessor(JsonObject):
    """Keeps the world blocks with a block tag from being replaced."""

    __required__: ClassVar[tuple[str, ...]] = ("value",)

    processor_type: Literal["minecraft:protected_blocks"] = json_field(
        default="minecraft:protected_blocks", init=False
    )
    value: str | None = None

    def set_value(self, block_tag: str) -> None:
        """Sets the block tag of the protected blocks."""
        self.value = block_tag

    def __validate__(self) -> None:
        if self.value is None:
            raise ValueError("A protected_blocks processor needs a block tag.")


class _RuleProcessor(JsonObject):
    """Runs block rules: on each block, the first rule that matches applies."""

    processor_type: Literal["minecraft:rule"] = json_field(
        default="minecraft:rule", init=False
    )
    rules: list[_ProcessorRule] = json_field(default_factory=list)

    def add_rule(self) -> _ProcessorRule:
        """Adds a rule and returns it."""
        rule = _ProcessorRule()
        self.rules.append(rule)
        return rule


class _ProcessorBuilder:
    """The builders shared by a processor list and a capped processor's delegate."""

    __slots__ = ()

    def _add_processor(self, processor: JsonObject) -> None:
        raise NotImplementedError

    def _rule_processor(self) -> _RuleProcessor | None:
        raise NotImplementedError

    def add_block_ignore_processor(
        self, blocks: list[MinecraftBlockDescriptor | str]
    ) -> None:
        """Leaves the blocks out of the placed structure, keeping the world blocks there.

        Args:
            blocks (list[MinecraftBlockDescriptor | str]): The blocks to leave out.
        """
        processor = _BlockIgnoreProcessor()
        for block in blocks:
            processor.add_block(block)
        self._add_processor(processor)

    def add_protected_blocks_processor(self, block_tag: str) -> None:
        """Keeps the world blocks with the block tag from being replaced.

        Args:
            block_tag (str): The block tag.
        """
        processor = _ProtectedBlocksProcessor()
        processor.set_value(block_tag)
        self._add_processor(processor)

    def add_block_rule(self) -> _ProcessorRule:
        """Adds a block rule. Rules are checked in order, and the first one that matches
        applies. Set its predicates with `rule.input_predicate.block_match(...)` and its
        result with `rule.set_output_state(...)`."""
        processor = self._rule_processor()
        if processor is None:
            processor = _RuleProcessor()
            self._add_processor(processor)
        return processor.add_rule()


class _CappedProcessor(JsonObject, _ProcessorBuilder):
    """Runs one delegate processor on a limited number of random blocks."""

    __required__: ClassVar[tuple[str, ...]] = ("delegate", "limit")

    processor_type: Literal["minecraft:capped"] = json_field(
        default="minecraft:capped", init=False
    )
    delegate: (
        _BlockIgnoreProcessor | _ProtectedBlocksProcessor | _RuleProcessor | None
    ) = None
    limit: Annotated[int, NonNegative] | _UniformLimit | None = None

    def set_limit(self, limit: int | tuple[int, int]) -> None:
        """Sets the most blocks the delegate runs on.

        Args:
            limit (int | tuple[int, int]): A number, or a minimum and a maximum to pick from.
        """
        if isinstance(limit, tuple):
            minimum, maximum = limit
            self.limit = _UniformLimit(min_inclusive=minimum, max_inclusive=maximum)
        else:
            self.limit = limit

    def _add_processor(self, processor: JsonObject) -> None:
        if self.delegate is not None:
            raise ValueError("A capped processor runs a single delegate processor.")
        self.delegate = processor

    def _rule_processor(self) -> _RuleProcessor | None:
        if self.delegate is None or isinstance(self.delegate, _RuleProcessor):
            return self.delegate
        raise ValueError("A capped processor runs a single delegate processor.")

    def __validate__(self) -> None:
        if self.delegate is None:
            raise ValueError("A capped processor needs a delegate processor.")
        if self.limit is None:
            raise ValueError("A capped processor needs a limit.")


class _ProcessorList(JsonObject, _ProcessorBuilder):
    """The `minecraft:processor_list` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    processors: list[
        _BlockIgnoreProcessor
        | _ProtectedBlocksProcessor
        | _CappedProcessor
        | _RuleProcessor
    ] = json_field(default_factory=list)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`."""
        self.description = identifier

    def add_capped_processor(self, limit: int | tuple[int, int]) -> _CappedProcessor:
        """Adds a processor that runs on a limited number of random blocks.

        Args:
            limit (int | tuple[int, int]): The most blocks it runs on: a number, or a minimum
                and a maximum to pick from.

        Returns:
            _CappedProcessor: Give it its one processor with its `add_` builders.
        """
        processor = _CappedProcessor()
        processor.set_limit(limit)
        self.processors.append(processor)
        return processor

    def _add_processor(self, processor: JsonObject) -> None:
        self.processors.append(processor)

    def _rule_processor(self) -> _RuleProcessor | None:
        return next((p for p in self.processors if isinstance(p, _RuleProcessor)), None)

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The processor list has no identifier.")


class _ProcessorListFile(JsonObject):
    """The content of `worldgen/processors/<name>.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:processor_list",
    )

    format_version: str = json_field(default=JIGSAW_VERSION, init=False)
    processor_list: _ProcessorList = json_field(
        key="minecraft:processor_list", default_factory=_ProcessorList
    )


# endregion

# region Jigsaw structure


class _VerticalAnchor(JsonObject):
    """A height: absolute, above the bottom or below the top of the dimension, or from sea
    level. Exactly one is set."""

    absolute: int | None = None
    above_bottom: Annotated[int, NonNegative] | None = None
    below_top: Annotated[int, NonNegative] | None = None
    from_sea: int | None = None

    def set_absolute(self, absolute: int) -> None:
        """Sets an absolute height."""
        self.absolute = absolute

    def set_above_bottom(self, above_bottom: int) -> None:
        """Sets a height above the bottom of the dimension."""
        self.above_bottom = above_bottom

    def set_below_top(self, below_top: int) -> None:
        """Sets a height below the top of the dimension."""
        self.below_top = below_top

    def set_from_sea(self, from_sea: int) -> None:
        """Sets a height from the dimension's sea level."""
        self.from_sea = from_sea

    def __validate__(self) -> None:
        anchors = (self.absolute, self.above_bottom, self.below_top, self.from_sea)
        if sum(anchor is not None for anchor in anchors) != 1:
            raise ValueError("A vertical anchor sets exactly one height.")


class _ConstantHeight(JsonObject):
    """A start height at one anchor."""

    type: Literal["constant"] = json_field(default="constant", init=False)
    value: _VerticalAnchor = json_field(default_factory=_VerticalAnchor)


class _UniformHeight(JsonObject):
    """A start height picked uniformly between two anchors."""

    type: Literal["uniform"] = json_field(default="uniform", init=False)
    min: _VerticalAnchor = json_field(default_factory=_VerticalAnchor)
    max: _VerticalAnchor = json_field(default_factory=_VerticalAnchor)


class _DimensionPadding(JsonObject):
    """Blocks at the bottom and top of the dimension the structure keeps out of."""

    bottom: Annotated[int, NonNegative] | None = None
    top: Annotated[int, NonNegative] | None = None

    def set_bottom(self, bottom: int) -> None:
        """Sets the padding at the bottom of the dimension."""
        self.bottom = bottom

    def set_top(self, top: int) -> None:
        """Sets the padding at the top of the dimension."""
        self.top = top


class _MaxDistanceFromCenter(JsonObject):
    """How far the structure's pieces may be from its start."""

    __required__: ClassVar[tuple[str, ...]] = ("horizontal",)

    horizontal: Annotated[int, InRange(1, 128)] | None = None
    vertical: Annotated[int, AtLeastOne] | None = None

    def set_horizontal(self, horizontal: int) -> None:
        """Sets the horizontal distance, from 1 to 128."""
        self.horizontal = horizontal

    def set_vertical(self, vertical: int) -> None:
        """Sets the vertical distance, at least 1."""
        self.vertical = vertical

    def __validate__(self) -> None:
        if self.horizontal is None:
            raise ValueError("max_distance_from_center needs a horizontal distance.")


class _DirectPoolAlias(JsonObject):
    """Replaces a template pool with another one."""

    type: Literal["direct"] = json_field(default="direct", init=False)
    alias: str = json_field()
    target: str = json_field()


class _PoolAliasTarget(JsonObject):
    """A template pool a random pool alias can pick."""

    data: str = json_field()
    weight: Annotated[int, AtLeastOne] = json_field()


class _RandomPoolAlias(JsonObject):
    """Replaces a template pool with one picked at random from its targets."""

    type: Literal["random"] = json_field(default="random", init=False)
    alias: str = json_field()
    targets: list[_PoolAliasTarget] = json_field(default_factory=list)

    def add_target(self, target: str, weight: int) -> None:
        """Adds a template pool to pick.

        Args:
            target (str): The template pool identifier.
            weight (int): Its weight against the other targets, at least 1.
        """
        self.targets.append(_PoolAliasTarget(data=target, weight=weight))


class _PoolAliasGroup(JsonObject):
    """A group of pool aliases a random group alias can pick."""

    data: list[_DirectPoolAlias | _RandomPoolAlias] = json_field(default_factory=list)
    weight: Annotated[int, AtLeastOne] = json_field()

    def add_direct_pool_alias(self, alias: str, target: str) -> None:
        """Adds an alias that replaces the `alias` template pool with `target`."""
        self.data.append(_DirectPoolAlias(alias=alias, target=target))

    def add_random_pool_alias(self, alias: str) -> _RandomPoolAlias:
        """Adds an alias that replaces the `alias` template pool with a random target.
        Add the targets on the returned alias."""
        pool_alias = _RandomPoolAlias(alias=alias)
        self.data.append(pool_alias)
        return pool_alias


class _RandomGroupPoolAlias(JsonObject):
    """Applies one group of pool aliases, picked at random."""

    type: Literal["random_group"] = json_field(default="random_group", init=False)
    groups: list[_PoolAliasGroup] = json_field(default_factory=list)

    def add_group(self, weight: int) -> _PoolAliasGroup:
        """Adds a group of aliases and returns it.

        Args:
            weight (int): Its weight against the other groups, at least 1.
        """
        group = _PoolAliasGroup(weight=weight)
        self.groups.append(group)
        return group


class _Jigsaw(JsonObject):
    """The `minecraft:jigsaw` object."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "step",
        "start_pool",
        "max_depth",
        "start_height",
    )

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    biome_filters: list[Filter] = json_field(default_factory=list)
    step: (
        Literal[
            "raw_generation",
            "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ]
        | None
    ) = None
    terrain_adaptation: (
        Literal["none", "bury", "beard_thin", "beard_box", "encapsulate"] | None
    ) = None
    start_pool: str | None = None
    start_jigsaw_name: str | None = None
    max_depth: Annotated[int, InRange(0, 20)] | None = None
    start_height: _ConstantHeight | _UniformHeight | None = None
    heightmap_projection: Literal["none", "world_surface", "ocean_floor"] | None = None
    dimension_padding: _DimensionPadding | None = None
    max_distance_from_center: _MaxDistanceFromCenter | None = None
    pool_aliases: list[_DirectPoolAlias | _RandomPoolAlias | _RandomGroupPoolAlias] = (
        json_field(default_factory=list)
    )
    liquid_settings: Literal["apply_waterlogging", "ignore_waterlogging"] | None = None

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`."""
        self.description = identifier

    def add_biome_filter(self, filter: Filter) -> None:
        """Adds a filter on the biomes the structure generates in."""
        self.biome_filters.append(filter)

    def set_step(
        self,
        step: Literal[
            "raw_generation",
            "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ],
    ) -> None:
        """Sets the world generation step the structure generates in."""
        self.step = step

    def set_terrain_adaptation(
        self,
        terrain_adaptation: Literal[
            "none", "bury", "beard_thin", "beard_box", "encapsulate"
        ],
    ) -> None:
        """Sets how the terrain adapts around the structure."""
        self.terrain_adaptation = terrain_adaptation

    def set_start_pool(self, start_pool: str) -> None:
        """Sets the identifier of the first template pool."""
        self.start_pool = start_pool

    def set_start_jigsaw_name(self, start_jigsaw_name: str) -> None:
        """Sets the name of the jigsaw block of the start pool placed first."""
        self.start_jigsaw_name = start_jigsaw_name

    def set_max_depth(self, max_depth: int) -> None:
        """Sets the most pieces from the start piece, from 0 to 20."""
        self.max_depth = max_depth

    def set_start_height(
        self, start_height: int | tuple[int, int], from_sea: bool = False
    ) -> None:
        """Sets the height the start pool is placed at.

        Args:
            start_height (int | tuple[int, int]): A height, absolute or from sea level, or two
                heights: the lower one above the bottom and the higher one below the top of
                the dimension, the height picked between them.
            from_sea (bool, optional): A single height is from sea level. Defaults to False.
        """
        if isinstance(start_height, tuple):
            height = _UniformHeight()
            height.min.set_above_bottom(min(start_height))
            height.max.set_below_top(max(start_height))
        else:
            height = _ConstantHeight()
            if from_sea:
                height.value.set_from_sea(start_height)
            else:
                height.value.set_absolute(start_height)
        self.start_height = height

    def set_heightmap_projection(
        self, heightmap_projection: Literal["none", "world_surface", "ocean_floor"]
    ) -> None:
        """Sets the heightmap the start height is measured from."""
        self.heightmap_projection = heightmap_projection

    def set_dimension_padding(self, bottom: int = 0, top: int = 0) -> None:
        """Sets the blocks at the bottom and top of the dimension the structure keeps out of."""
        self.dimension_padding = _DimensionPadding()
        self.dimension_padding.set_bottom(bottom)
        self.dimension_padding.set_top(top)

    def set_max_distance_from_center(
        self, horizontal: int, vertical: int | None = None
    ) -> None:
        """Sets how far the pieces may be from the start, horizontally and vertically."""
        self.max_distance_from_center = _MaxDistanceFromCenter()
        self.max_distance_from_center.set_horizontal(horizontal)
        if vertical is not None:
            self.max_distance_from_center.set_vertical(vertical)

    def add_direct_pool_alias(self, alias: str, target: str) -> None:
        """Adds an alias that replaces the `alias` template pool with `target`."""
        self.pool_aliases.append(_DirectPoolAlias(alias=alias, target=target))

    def add_random_pool_alias(self, alias: str) -> _RandomPoolAlias:
        """Adds an alias that replaces the `alias` template pool with a random target.
        Add the targets on the returned alias."""
        pool_alias = _RandomPoolAlias(alias=alias)
        self.pool_aliases.append(pool_alias)
        return pool_alias

    def add_random_group_pool_alias(self) -> _RandomGroupPoolAlias:
        """Adds an alias that applies one group of aliases, picked at random. Add the groups
        on the returned alias."""
        pool_alias = _RandomGroupPoolAlias()
        self.pool_aliases.append(pool_alias)
        return pool_alias

    def set_liquid_settings(
        self, liquid_settings: Literal["apply_waterlogging", "ignore_waterlogging"]
    ) -> None:
        """Sets whether waterloggable blocks in liquid get waterlogged."""
        self.liquid_settings = liquid_settings

    def __validate__(self) -> None:
        for name in self.__required__:
            if getattr(self, name) is None:
                raise ValueError(f"The jigsaw structure has no {name}.")


class _JigsawFile(JsonObject):
    """The content of `worldgen/structures/<name>.json`."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:jigsaw")

    format_version: str = json_field(default=JIGSAW_VERSION, init=False)
    jigsaw: _Jigsaw = json_field(key="minecraft:jigsaw", default_factory=_Jigsaw)


# endregion

# region Template pool


class _SinglePoolElement(JsonObject):
    """Places a structure template."""

    element_type: Literal["minecraft:single_pool_element"] = json_field(
        default="minecraft:single_pool_element", init=False
    )
    location: str = json_field()
    processors: str | None = None
    projection: Literal["rigid", "terrain_matching"] | None = None


class _FeaturePoolElement(JsonObject):
    """Places a feature."""

    element_type: Literal["minecraft:feature_pool_element"] = json_field(
        default="minecraft:feature_pool_element", init=False
    )
    feature: str = json_field()


class _EmptyPoolElement(JsonObject):
    """Places nothing."""

    element_type: Literal["minecraft:empty_pool_element"] = json_field(
        default="minecraft:empty_pool_element", init=False
    )


class _PoolElementEntry(JsonObject):
    """An element of the pool and its weight."""

    element: _SinglePoolElement | _FeaturePoolElement | _EmptyPoolElement = json_field()
    weight: Annotated[int, InRange(1, 200)] = json_field(default=1)


class _TemplatePool(JsonObject):
    """The `minecraft:template_pool` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    elements: list[_PoolElementEntry] = json_field(default_factory=list)
    fallback: str | None = None

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`."""
        self.description = identifier

    def add_single_element(
        self,
        location: str,
        processors: str | None = None,
        projection: Literal["rigid", "terrain_matching"] | None = None,
        weight: int = 1,
    ) -> None:
        """Adds a structure template.

        Args:
            location (str): The template's path in the `structures` folder, without its
                extension.
            processors (str, optional): The identifier of the processor list to run on it.
            projection (Literal["rigid", "terrain_matching"], optional): How it follows the
                terrain.
            weight (int, optional): Its weight, from 1 to 200. Defaults to 1.
        """
        element = _SinglePoolElement(
            location=location, processors=processors, projection=projection
        )
        self.elements.append(_PoolElementEntry(element=element, weight=weight))

    def add_feature_element(self, feature: str, weight: int = 1) -> None:
        """Adds a feature.

        Args:
            feature (str): The feature identifier.
            weight (int, optional): Its weight, from 1 to 200. Defaults to 1.
        """
        element = _FeaturePoolElement(feature=feature)
        self.elements.append(_PoolElementEntry(element=element, weight=weight))

    def add_empty_element(self, weight: int = 1) -> None:
        """Adds an element that places nothing.

        Args:
            weight (int, optional): Its weight, from 1 to 200. Defaults to 1.
        """
        self.elements.append(
            _PoolElementEntry(element=_EmptyPoolElement(), weight=weight)
        )

    def set_fallback(self, fallback: str) -> None:
        """Sets the template pool used when no element of this one fits."""
        self.fallback = fallback

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The template pool has no identifier.")


class _TemplatePoolFile(JsonObject):
    """The content of `worldgen/template_pools/<name>.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:template_pool",
    )

    format_version: str = json_field(default=JIGSAW_VERSION, init=False)
    template_pool: _TemplatePool = json_field(
        key="minecraft:template_pool", default_factory=_TemplatePool
    )


# endregion

# region Structure set


class _RandomSpreadPlacement(JsonObject):
    """Places the set's structures at a random spot in each cell of a grid."""

    __required__: ClassVar[tuple[str, ...]] = ("salt", "separation", "spacing")

    type: Literal["minecraft:random_spread"] = json_field(
        default="minecraft:random_spread", init=False
    )
    salt: int | None = None
    separation: Annotated[int, NonNegative] | None = None
    spacing: Annotated[int, AtLeastOne] | None = None
    spread_type: Literal["linear", "triangular"] | None = None

    def set_salt(self, salt: int) -> None:
        """Sets the seed that makes this set's pattern differ from other sets'."""
        self.salt = salt

    def set_separation(self, separation: int) -> None:
        """Sets the padding, in chunks, inside each cell."""
        self.separation = separation

    def set_spacing(self, spacing: int) -> None:
        """Sets the size of a cell, in chunks."""
        self.spacing = spacing

    def set_spread_type(self, spread_type: Literal["linear", "triangular"]) -> None:
        """Sets how the spot is picked in each cell."""
        self.spread_type = spread_type

    def __validate__(self) -> None:
        if self.salt is None or self.separation is None or self.spacing is None:
            raise ValueError(
                "A random spread placement needs salt, separation and spacing."
            )
        if self.separation >= self.spacing / 2:
            raise ValueError("Value 'separation' must be less than half of 'spacing'.")


class _StructureSetEntry(JsonObject):
    """A jigsaw structure of the set and its weight."""

    structure: str = json_field()
    weight: Annotated[int, AtLeastOne] = json_field(default=1)


class _StructureSet(JsonObject):
    """The `minecraft:structure_set` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description", "placement")

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    placement: _RandomSpreadPlacement = json_field(
        default_factory=_RandomSpreadPlacement
    )
    structures: list[_StructureSetEntry] = json_field(default_factory=list)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`."""
        self.description = identifier

    def add_structure(self, structure: str, weight: int = 1) -> None:
        """Adds a jigsaw structure.

        Args:
            structure (str): The jigsaw structure identifier.
            weight (int, optional): Its weight, at least 1. Defaults to 1.
        """
        self.structures.append(_StructureSetEntry(structure=structure, weight=weight))

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The structure set has no identifier.")


class _StructureSetFile(JsonObject):
    """The content of `worldgen/structure_sets/<name>.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:structure_set",
    )

    format_version: str = json_field(default=JIGSAW_VERSION, init=False)
    structure_set: _StructureSet = json_field(
        key="minecraft:structure_set", default_factory=_StructureSet
    )


# endregion


class Structure:
    """A structure template (`.mcstructure`) from `assets/structures`, copied to the
    behavior pack's `structures/<namespace>` folder."""

    def __init__(self, structure_name: str):
        """Initializes a Structure instance.

        Args:
            structure_name (str): The structure's path in `assets/structures`, without its
                extension, such as `village/house`.
        """
        self._relative = PurePosixPath(structure_name)
        self._source = Path("assets", "structures", *self._relative.parent.parts)
        self._file_name = f"{self._relative.name}.mcstructure"
        if not (self._source / self._file_name).exists():
            raise FileNotFoundError(
                f"{self._file_name} not found in {self._source}. Please ensure the file exists."
            )

    def queue(self):
        """Queues the structure to be exported."""
        ANVIL.__queue__(self)

    @property
    def identifier(self) -> str:
        """Returns the identifier of the structure."""
        return f"{CONFIG.NAMESPACE}:{self._relative.name}"

    @property
    def reference(self) -> str:
        """The structure's path in the behavior pack's `structures` folder, without its
        extension, as template pools reference it."""
        return (PurePosixPath(CONFIG.NAMESPACE) / self._relative).as_posix()

    def __export__(self):
        """Exports the structure to the file system."""
        Directory.copy_files(
            self._source,
            Path(
                CONFIG.BP_PATH,
                "structures",
                CONFIG.NAMESPACE,
                *self._relative.parent.parts,
            ),
            self._file_name,
        )


class _JigsawStructureProcess(JsonFile):
    """A processor list: rules that change the blocks of a structure template as it is
    placed, such as leaving out air or filling chests with loot.

    ```python
    processor = _JigsawStructureProcess("ruins_processor")
    processor.add_block_ignore_processor([MinecraftBlockTypes.Air()])
    rule = processor.add_block_rule()
    rule.input_predicate.random_block_match(MinecraftBlockTypes.Cobblestone(), 0.3)
    rule.set_output_state(MinecraftBlockTypes.MossyCobblestone())
    ```

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/worldgenreference/examples/jigsawprocessors)
    """

    _document = _ProcessorListFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = Path("worldgen", "processors")
    _object_type = "Jigsaw Structure Process"

    def __init__(self, name: str) -> None:
        """Initializes a processor list.

        Args:
            name (str): The processor list name.
        """
        super().__init__(name)
        self._content.processor_list.set_description(self.identifier)

    def add_block_ignore_processor(
        self, blocks: list[MinecraftBlockDescriptor | str]
    ) -> "_JigsawStructureProcess":
        """Leaves the blocks out of the placed structure, keeping the world blocks there.

        Args:
            blocks (list[MinecraftBlockDescriptor | str]): The blocks to leave out.
        """
        self._content.processor_list.add_block_ignore_processor(blocks)
        return self

    def add_protected_blocks_processor(
        self, block_tag: str
    ) -> "_JigsawStructureProcess":
        """Keeps the world blocks with the block tag from being replaced.

        Args:
            block_tag (str): The block tag.
        """
        self._content.processor_list.add_protected_blocks_processor(block_tag)
        return self

    def add_capped_processor(self, limit: int | tuple[int, int]) -> _CappedProcessor:
        """Adds a processor that runs on a limited number of random blocks.

        Args:
            limit (int | tuple[int, int]): The most blocks it runs on: a number, or a minimum
                and a maximum to pick from.

        Returns:
            _CappedProcessor: Give it its one processor with `add_block_rule()`,
                `add_block_ignore_processor(...)` or `add_protected_blocks_processor(...)`.
        """
        return self._content.processor_list.add_capped_processor(limit)

    def add_block_rule(self) -> _ProcessorRule:
        """Adds a block rule. Rules are checked in order, and the first one that matches
        applies.

        Returns:
            _ProcessorRule: Set its tests with `rule.input_predicate`, `rule.location_predicate`
                and `rule.position_predicate`, its result with `rule.set_output_state(...)`
                and a loot table with `rule.block_entity_modifier.append_loot(...)`.
        """
        return self._content.processor_list.add_block_rule()


class _JigsawStructure(JsonFile):
    """A jigsaw structure: where and how its pieces generate, from its start pool.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/worldgenreference/examples/jigsawjigsawstructures)
    """

    _document = _JigsawFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = Path("worldgen", "structures")
    _object_type = "Jigsaw Structure"

    def __init__(
        self,
        name: str,
        start_pool: "JigsawStructureTemplatePool",
        max_depth: int,
        start_height: tuple[int, int] | int,
        placement_step: Literal[
            "raw_generation",
            "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ],
        start_jigsaw_name: str | None = None,
        liquid_settings: Literal[
            "apply_waterlogging", "ignore_waterlogging"
        ] = "apply_waterlogging",
        start_height_from_sea: bool = False,
    ) -> None:
        """Initializes a jigsaw structure.

        Args:
            name (str): The name of the jigsaw structure.
            start_pool (JigsawStructureTemplatePool): The first template pool.
            max_depth (int): The most pieces from the start piece, from 0 to 20.
            start_height (tuple[int, int] | int): The height of the start piece: one height,
                or two heights, the lower one above the bottom and the higher one below the
                top of the dimension.
            placement_step (Literal[...]): The world generation step it generates in.
            start_jigsaw_name (str, optional): The jigsaw block of the start pool placed first.
            liquid_settings (Literal["apply_waterlogging", "ignore_waterlogging"], optional):
                Whether waterloggable blocks in liquid get waterlogged.
            start_height_from_sea (bool, optional): A single start height is from sea level.
        """
        super().__init__(name)
        if not isinstance(start_pool, JigsawStructureTemplatePool):
            raise TypeError(
                "start_pool must be an instance of JigsawStructureTemplatePool"
            )
        jigsaw = self._content.jigsaw
        jigsaw.set_description(self.identifier)
        jigsaw.set_step(placement_step)
        jigsaw.set_start_pool(start_pool.identifier)
        if start_jigsaw_name is not None:
            jigsaw.set_start_jigsaw_name(start_jigsaw_name)
        jigsaw.set_max_depth(max_depth)
        jigsaw.set_start_height(start_height, start_height_from_sea)
        jigsaw.set_liquid_settings(liquid_settings)
        self._start_pool = start_pool

    def add_biome_filters(self, filter: Filter) -> "_JigsawStructure":
        """Adds a filter on the biomes the structure generates in.

        Args:
            filter (Filter): The biome filter.
        """
        self._content.jigsaw.add_biome_filter(filter)
        return self

    def terrain_adaptation(
        self,
        terrain_adaptation: Literal[
            "none", "bury", "beard_thin", "beard_box", "encapsulate"
        ],
    ) -> "_JigsawStructure":
        """Sets how the terrain adapts around the structure.

        Args:
            terrain_adaptation (Literal["none", "bury", "beard_thin", "beard_box", "encapsulate"]):
                - "none" Do not adjust ambient block density.
                - "bury" Adds density to all pieces, only within the Y bounds of the start piece.
                - "beard_thin" Adds density below the structure and removes it just above the ground.
                - "beard_box" Adds density below the structure and removes it in its whole box.
                - "encapsulate" Adds density all around every piece.
        """
        self._content.jigsaw.set_terrain_adaptation(terrain_adaptation)
        return self

    def heightmap_projection(
        self, heightmap_projection: Literal["none", "world_surface", "ocean_floor"]
    ) -> "_JigsawStructure":
        """Sets the heightmap the start height is measured from.

        Args:
            heightmap_projection (Literal["none", "world_surface", "ocean_floor"]): The heightmap.
        """
        self._content.jigsaw.set_heightmap_projection(heightmap_projection)
        return self

    def dimension_padding(self, bottom: int = 0, top: int = 0) -> "_JigsawStructure":
        """Keeps the structure out of blocks at the bottom and top of the dimension.

        Args:
            bottom (int, optional): Blocks kept free at the bottom. Defaults to 0.
            top (int, optional): Blocks kept free at the top. Defaults to 0.
        """
        self._content.jigsaw.set_dimension_padding(bottom, top)
        return self

    def max_distance_from_center(
        self, horizontal: int, vertical: int | None = None
    ) -> "_JigsawStructure":
        """Sets how far the pieces may be from the start piece.

        Args:
            horizontal (int): The horizontal distance, from 1 to 128.
            vertical (int, optional): The vertical distance, at least 1.
        """
        self._content.jigsaw.set_max_distance_from_center(horizontal, vertical)
        return self

    def add_direct_pool_alias(self, alias: str, target: str) -> "_JigsawStructure":
        """Replaces the `alias` template pool with `target` in this structure.

        Args:
            alias (str): The template pool identifier to replace.
            target (str): The template pool identifier used instead.
        """
        self._content.jigsaw.add_direct_pool_alias(alias, target)
        return self

    def add_random_pool_alias(self, alias: str) -> _RandomPoolAlias:
        """Replaces the `alias` template pool with a random target in this structure.

        Args:
            alias (str): The template pool identifier to replace.

        Returns:
            _RandomPoolAlias: Add its targets with `add_target(target, weight)`.
        """
        return self._content.jigsaw.add_random_pool_alias(alias)

    def add_random_group_pool_alias(self) -> _RandomGroupPoolAlias:
        """Applies one group of pool aliases, picked at random.

        Returns:
            _RandomGroupPoolAlias: Add groups with `add_group(weight)`, then aliases to each
                group with `add_direct_pool_alias` and `add_random_pool_alias`.
        """
        return self._content.jigsaw.add_random_group_pool_alias()

    def queue(self) -> "_JigsawStructure":
        return super().queue()


class JigsawStructureTemplatePool(JsonFile):
    """A template pool: structure templates, features or nothing, picked by weight when a
    jigsaw block asks for this pool.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/worldgenreference/examples/jigsawtemplatepools)
    """

    _document = _TemplatePoolFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = Path("worldgen", "template_pools")
    _object_type = "Jigsaw Structure Template Pool"

    def __init__(self, name: str, fallback: str | None = None) -> None:
        """Initializes a JigsawStructureTemplatePool instance.

        Args:
            name (str): The name of the template pool.
            fallback (str, optional): The identifier of the template pool used when no
                element of this one fits. Defaults to None.
        """
        super().__init__(name)
        self._content.template_pool.set_description(self.identifier)
        if fallback is not None:
            self._content.template_pool.set_fallback(fallback)
        self._structures: list[Structure] = []
        self._features: list[Feature] = []
        self._processors: list[_JigsawStructureProcess] = []

    def add_structure_element(
        self,
        structure: Structure | Feature | str | None,
        processors: str | _JigsawStructureProcess | None = None,
        weight: int = 1,
        projection: Literal["rigid", "terrain_matching"] = "rigid",
    ) -> _JigsawStructureProcess | None:
        """Adds an element to the template pool.

        Args:
            structure (Structure | Feature | str | None): The structure template (a path in
                `assets/structures` is turned into a `Structure`), a feature, or None for an
                element that places nothing.
            processors (str | _JigsawStructureProcess, optional): The processor list run on a
                structure template. A name creates the processor list. Defaults to None.
            weight (int, optional): The element's weight, from 1 to 200. Defaults to 1.
            projection (Literal["rigid", "terrain_matching"], optional): How a structure
                template follows the terrain. Defaults to "rigid".

        Returns:
            _JigsawStructureProcess | None: The processor list, queued with the pool.
        """
        if not isinstance(structure, (Structure, Feature, str, type(None))):
            raise TypeError(
                "structure must be an instance of Structure, Feature, or str"
            )
        if not isinstance(processors, (str, _JigsawStructureProcess, type(None))):
            raise TypeError(
                "processors must be an instance of str or JigsawStructureProcess"
            )

        if isinstance(processors, str):
            processors = _JigsawStructureProcess(processors)
        if processors is not None:
            self._processors.append(processors)

        pool = self._content.template_pool
        if isinstance(structure, str):
            structure = Structure(structure)
        if isinstance(structure, Structure):
            self._structures.append(structure)
            pool.add_single_element(
                structure.reference,
                processors.identifier if processors else None,
                projection,
                weight,
            )
        elif isinstance(structure, Feature):
            self._features.append(structure)
            pool.add_feature_element(structure.identifier, weight)
        else:
            pool.add_empty_element(weight)

        return processors

    def queue(self) -> "JigsawStructureTemplatePool":
        for processor in self._processors:
            processor.queue()
        for structure in self._structures:
            structure.queue()
        for feature in self._features:
            feature.queue()
        return super().queue()


class JigsawStructureSet(JsonFile):
    """A structure set: jigsaw structures, picked by weight, and how they spread in the
    world relative to other structures of the same set.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/worldgenreference/examples/jigsawstructuresets)
    """

    _document = _StructureSetFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = Path("worldgen", "structure_sets")
    _object_type = "Jigsaw Structure Set"

    def __init__(
        self,
        name: str,
        separation: int,
        spacing: int,
        spread_type: Literal["linear", "triangular"] = "linear",
        placement_type: Literal["minecraft:random_spread"] = "minecraft:random_spread",
    ) -> None:
        """Initializes a JigsawStructureSet instance.

        Args:
            name (str): The name of the structure set.
            separation (int): Padding (in chunks) within each grid cell. Structures will not
                generate within the padded area. Must be less than half of `spacing`.
            spacing (int): Grid cell size (in chunks). Structures will attempt to generate at a
                random position within each cell.
            spread_type (Literal["linear", "triangular"], optional): How the position is picked
                in each cell. Defaults to "linear".
            placement_type (Literal["minecraft:random_spread"], optional): Where structures in
                the set spawn relative to one another. Defaults to "minecraft:random_spread".
        """
        super().__init__(name)
        structure_set = self._content.structure_set
        structure_set.set_description(self.identifier)
        structure_set.placement.set_salt(salt_from_str(self.identifier))
        structure_set.placement.set_separation(separation)
        structure_set.placement.set_spacing(spacing)
        structure_set.placement.set_spread_type(spread_type)
        self._structures: list[_JigsawStructure] = []

    def add_jigsaw_structure(
        self,
        structure_name: str,
        start_pool: "JigsawStructureTemplatePool",
        max_depth: int,
        start_height: tuple[int, int] | int,
        placement_step: Literal[
            "raw_generation",
            "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ],
        weight: int = 1,
        start_jigsaw_name: str | None = None,
        liquid_settings: Literal[
            "apply_waterlogging", "ignore_waterlogging"
        ] = "apply_waterlogging",
        start_height_from_sea: bool = False,
    ) -> "_JigsawStructure":
        """Adds a jigsaw structure to the set. The arguments are the jigsaw structure's,
        see `_JigsawStructure`.

        Args:
            structure_name (str): The name of the jigsaw structure.
            weight (int, optional): Its weight in the set, at least 1. Defaults to 1.

        Returns:
            _JigsawStructure: The jigsaw structure, queued with the set.
        """
        structure = _JigsawStructure(
            structure_name,
            start_pool,
            max_depth,
            start_height,
            placement_step,
            start_jigsaw_name,
            liquid_settings,
            start_height_from_sea,
        )
        self._structures.append(structure)
        self._content.structure_set.add_structure(structure.identifier, weight)
        return structure

    def queue(self) -> "JigsawStructureSet":
        for structure in self._structures:
            structure.queue()
        return super().queue()
