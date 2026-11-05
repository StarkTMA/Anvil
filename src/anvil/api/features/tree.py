"""The tree feature: a trunk, an optional canopy and, for mangroves, roots.

A tree has one trunk type and at most one canopy type, each set with its own method of
:class:`TreeFeature`. Trunks with branches (acacia, cherry and mega trunks) also grow a
canopy at the end of each branch: a canopy set with `sync_to_branches` (the default) is
used there too, and the `branch_*_canopy` methods set a different one.

Example:
    ```python
    tree = TreeFeature("palm_tree")
    tree.trunk("minecraft:jungle_log", trunk_height=(5, 8))
    tree.canopy("minecraft:jungle_leaves", canopy_offset_min=-2, canopy_offset_max=0)
    tree.may_grow_on(["minecraft:sand"])
    ```

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_tree_feature)
"""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    AtLeastOne,
    BlockId,
    Bounds,
    Chance,
    ExactRangeMinMax,
    Fraction,
    InRange,
    JsonObject,
    NonNegative,
    RangeMinMax,
    json_field,
)

_ExactMinMax = Bounds("min", "max", exact=True)

# region Decorations


class _TreeDecoration(JsonObject):
    """A `trunk_decoration`, `canopy_decoration` or `root_decoration`: blocks spread from
    the trunk, the canopy or the roots."""

    decoration_chance: Annotated[float | tuple[int, int], Fraction] = json_field()
    decoration_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    num_steps: Annotated[int, NonNegative] | None = None
    step_direction: Literal["down", "up", "out", "away"] | None = None


def _decoration(
    decoration_chance: float | tuple[int, int],
    decoration_block: str | Block | BlockDescriptor | None,
    num_steps: int | None,
    step_direction: Literal["down", "up", "out", "away"] | None,
) -> _TreeDecoration:
    return _TreeDecoration(
        decoration_chance=decoration_chance,
        decoration_block=decoration_block,
        num_steps=num_steps,
        step_direction=step_direction,
    )


# endregion

# region Canopies


class _AcaciaCanopy(JsonObject):
    """An `acacia_canopy`."""

    canopy_size: Annotated[int, AtLeastOne] = json_field()
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    simplify_canopy: bool | None = None


class _CanopySlope(JsonObject):
    """The `canopy_slope` of a canopy: `rise` over `run`."""

    rise: Annotated[int, AtLeastOne] | None = None
    run: Annotated[int, AtLeastOne] | None = None


class _Canopy(JsonObject):
    """A `canopy`."""

    canopy_offset: Annotated[tuple[int, int], _ExactMinMax] | None = None
    min_width: Annotated[int, NonNegative] | None = None
    canopy_slope: _CanopySlope | None = None
    variation_chance: (
        list[Annotated[float | tuple[int, int], Fraction]]
        | Annotated[float | tuple[int, int], Fraction]
        | None
    ) = None
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    canopy_decoration: _TreeDecoration | None = None

    def set_canopy_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the canopy."""
        self.canopy_decoration = decoration


class _CherryCanopy(JsonObject):
    """A `cherry_canopy`."""

    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    radius: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    trunk_width: Annotated[int, AtLeastOne] | None = None
    wide_bottom_layer_hole_chance: Annotated[float | tuple[int, int], Fraction] = (
        json_field()
    )
    corner_hole_chance: Annotated[float | tuple[int, int], Fraction] = json_field()
    hanging_leaves_chance: Annotated[float | tuple[int, int], Fraction] = json_field()
    hanging_leaves_extension_chance: Annotated[float | tuple[int, int], Fraction] = (
        json_field()
    )


class _FancyCanopy(JsonObject):
    """A `fancy_canopy`."""

    height: Annotated[int, AtLeastOne] = json_field()
    radius: Annotated[int, NonNegative] = json_field()
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _MangroveCanopy(JsonObject):
    """A `mangrove_canopy`."""

    canopy_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    canopy_radius: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    leaf_placement_attempts: Annotated[int, AtLeastOne] = json_field()
    leaf_blocks: list[
        tuple[
            Annotated[str | Block | BlockDescriptor, BlockId],
            Annotated[float, NonNegative],
        ]
    ] = json_field()
    canopy_decoration: _TreeDecoration | None = None
    hanging_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    hanging_block_placement_chance: (
        Annotated[float | tuple[int, int], Fraction] | None
    ) = None

    def set_canopy_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the canopy."""
        self.canopy_decoration = decoration


class _MegaCanopy(JsonObject):
    """A `mega_canopy`."""

    canopy_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    base_radius: Annotated[int, NonNegative] = json_field()
    core_width: Annotated[int, AtLeastOne] | None = None
    simplify_canopy: bool | None = None
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _MegaPineCanopy(JsonObject):
    """A `mega_pine_canopy`."""

    canopy_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    base_radius: Annotated[int, NonNegative] = json_field()
    radius_step_modifier: Annotated[float, NonNegative] = json_field()
    core_width: Annotated[int, AtLeastOne] | None = None
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _PineCanopy(JsonObject):
    """A `pine_canopy`."""

    canopy_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    base_radius: Annotated[int, AtLeastOne] = json_field()
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _PoplarRadius(JsonObject):
    """A radius a poplar canopy can have, with its weight."""

    value: Annotated[int, NonNegative] = json_field()
    weight: Annotated[int, NonNegative] = json_field()


class _PoplarCanopy(JsonObject):
    """A `poplar_canopy`."""

    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    radius: list[_PoplarRadius] | None = None
    trunk_width: Annotated[int, AtLeastOne] | None = None


class _RandomSpreadCanopy(JsonObject):
    """A `random_spread_canopy`."""

    canopy_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    canopy_radius: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    leaf_placement_attempts: Annotated[int, AtLeastOne] = json_field()
    leaf_blocks: list[
        tuple[
            Annotated[str | Block | BlockDescriptor, BlockId],
            Annotated[float, NonNegative],
        ]
    ] = json_field()


class _RoofedCanopy(JsonObject):
    """A `roofed_canopy`."""

    canopy_height: Annotated[int, InRange(minimum=3)] = json_field()
    core_width: Annotated[int, AtLeastOne] = json_field()
    outer_radius: Annotated[int, NonNegative] = json_field()
    inner_radius: Annotated[int, NonNegative] = json_field()
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _SpruceCanopy(JsonObject):
    """A `spruce_canopy`."""

    lower_offset: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    upper_offset: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    max_radius: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    leaf_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()


class _BranchCanopy(JsonObject):
    """The `branch_canopy` of a trunk's branches: the canopy at the end of each branch."""

    acacia_canopy: _AcaciaCanopy | None = None
    canopy: _Canopy | None = None
    cherry_canopy: _CherryCanopy | None = None
    fancy_canopy: _FancyCanopy | None = None
    mangrove_canopy: _MangroveCanopy | None = None
    mega_canopy: _MegaCanopy | None = None
    mega_pine_canopy: _MegaPineCanopy | None = None
    pine_canopy: _PineCanopy | None = None
    roofed_canopy: _RoofedCanopy | None = None
    spruce_canopy: _SpruceCanopy | None = None


_BRANCH_CANOPIES = frozenset(
    name for name in _BranchCanopy.__dataclass_fields__ if name.endswith("canopy")
)

# endregion

# region Trunks


class _TrunkHeight(JsonObject):
    """The `trunk_height` of an acacia, cherry or mega trunk: a base height plus a random
    number below each interval."""

    base: Annotated[int, AtLeastOne] = json_field()
    intervals: list[Annotated[int, AtLeastOne]] | None = None
    min_height_for_canopy: Annotated[int, AtLeastOne] | None = None


class _TrunkLean(JsonObject):
    """The `trunk_lean` of an acacia trunk: its diagonal growth."""

    allow_diagonal_growth: bool = json_field()
    lean_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    lean_steps: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    lean_length: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None


class _AcaciaBranches(JsonObject):
    """The `branches` of an acacia trunk."""

    branch_length: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    branch_position: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    branch_chance: Annotated[float | tuple[int, int], Fraction] = json_field()
    branch_canopy: _BranchCanopy | None = None

    def set_branch_canopy(self, canopy: _BranchCanopy | None) -> None:
        """Sets the canopy at the end of each branch."""
        self.branch_canopy = canopy


class _AcaciaTrunk(JsonObject):
    """An `acacia_trunk`."""

    trunk_width: Annotated[int, AtLeastOne] = json_field()
    trunk_height: _TrunkHeight = json_field()
    trunk_lean: _TrunkLean = json_field()
    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    branches: _AcaciaBranches | None = None
    trunk_decoration: _TreeDecoration | None = None

    def set_trunk_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the trunk."""
        self.trunk_decoration = decoration


class _TreeTypeWeights(JsonObject):
    """The `tree_type_weights` of a cherry trunk: how likely each tree shape is."""

    one_branch: Annotated[int, NonNegative] = json_field()
    two_branches: Annotated[int, NonNegative] = json_field()
    two_branches_and_trunk: Annotated[int, NonNegative] = json_field()


class _CherryBranches(JsonObject):
    """The `branches` of a cherry trunk."""

    tree_type_weights: _TreeTypeWeights | None = None
    branch_horizontal_length: Annotated[int | tuple[int, int], ExactRangeMinMax] = (
        json_field()
    )
    branch_start_offset_from_top: Annotated[int | tuple[int, int], ExactRangeMinMax] = (
        json_field()
    )
    branch_end_offset_from_top: Annotated[int | tuple[int, int], ExactRangeMinMax] = (
        json_field()
    )
    branch_canopy: _BranchCanopy | None = None

    def set_branch_canopy(self, canopy: _BranchCanopy | None) -> None:
        """Sets the canopy at the end of each branch."""
        self.branch_canopy = canopy


class _CherryTrunk(JsonObject):
    """A `cherry_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_height: _TrunkHeight = json_field()
    branches: _CherryBranches = json_field()

    def __validate__(self) -> None:
        if self.trunk_height.base < 2:
            raise ValueError(
                f"A cherry trunk's base height must be at least 2, got {self.trunk_height.base}."
            )


class _FallenTrunk(JsonObject):
    """A `fallen_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    log_length: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    stump_height: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None
    height_modifier: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None
    log_decoration_feature: str | None = None
    trunk_decoration: _TreeDecoration | None = None

    def set_trunk_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the trunk."""
        self.trunk_decoration = decoration


class _FancyTrunkHeight(JsonObject):
    """The `trunk_height` of a fancy trunk."""

    base: Annotated[int, AtLeastOne] = json_field()
    variance: Annotated[int, AtLeastOne] = json_field()
    scale: Annotated[float, Chance] = json_field()


class _FancyBranches(JsonObject):
    """The `branches` of a fancy trunk."""

    slope: float = json_field()
    density: float = json_field()
    min_altitude_factor: Annotated[float, Chance] = json_field()


class _FancyTrunk(JsonObject):
    """A `fancy_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_width: Annotated[int, AtLeastOne] = json_field()
    trunk_height: _FancyTrunkHeight = json_field()
    branches: _FancyBranches = json_field()
    width_scale: Annotated[float, NonNegative] = json_field()
    foliage_altitude_factor: Annotated[float, Chance] = json_field()


class _MangroveTrunkHeight(JsonObject):
    """The `trunk_height` of a mangrove trunk."""

    base: Annotated[int, AtLeastOne] = json_field()
    height_rand_a: Annotated[int, AtLeastOne] = json_field()
    height_rand_b: Annotated[int, AtLeastOne] = json_field()


class _MangroveBranches(JsonObject):
    """The `branches` of a mangrove trunk."""

    branch_length: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    branch_steps: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    branch_chance: Annotated[float | tuple[int, int], Fraction] = json_field()


class _MangroveTrunk(JsonObject):
    """A `mangrove_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_width: Annotated[int, AtLeastOne] = json_field()
    trunk_height: _MangroveTrunkHeight = json_field()
    branches: _MangroveBranches | None = None
    trunk_decoration: _TreeDecoration | None = None

    def set_trunk_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the trunk."""
        self.trunk_decoration = decoration


class _MegaBranches(JsonObject):
    """The `branches` of a mega trunk."""

    branch_length: Annotated[int, AtLeastOne] | None = None
    branch_slope: float | None = None
    branch_interval: Annotated[int | tuple[int, int], RangeMinMax] | None = None
    branch_altitude_factor: (
        Annotated[float | tuple[float, float], Chance, _ExactMinMax] | None
    ) = None
    branch_canopy: _BranchCanopy | None = None

    def set_branch_canopy(self, canopy: _BranchCanopy | None) -> None:
        """Sets the canopy at the end of each branch."""
        self.branch_canopy = canopy


class _MegaTrunk(JsonObject):
    """A `mega_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_width: Annotated[int, AtLeastOne] = json_field()
    trunk_height: _TrunkHeight = json_field()
    height_modifier: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None
    branches: _MegaBranches | None = None
    trunk_decoration: _TreeDecoration | None = None

    def set_trunk_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the trunk."""
        self.trunk_decoration = decoration


class _PoplarTrunk(JsonObject):
    """A `poplar_trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_height: Annotated[int | tuple[int, int], ExactRangeMinMax] = json_field()
    remaining_trunk_height_above_branches: (
        Annotated[int | tuple[int, int], ExactRangeMinMax] | None
    ) = None
    amount_of_foliage_support_branches: Annotated[int, NonNegative] | None = None
    height_modifier: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None


class _SubmergedDepth(JsonObject):
    """The `can_be_submerged` of a trunk as its greatest depth."""

    max_depth: Annotated[int, AtLeastOne] = json_field()


class _Trunk(JsonObject):
    """A `trunk`."""

    trunk_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    trunk_height: Annotated[int | tuple[int, int], RangeMinMax] = json_field()
    height_modifier: Annotated[int | tuple[int, int], ExactRangeMinMax] | None = None
    can_be_submerged: bool | _SubmergedDepth | None = None
    trunk_decoration: _TreeDecoration | None = None

    def set_trunk_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the trunk."""
        self.trunk_decoration = decoration


# endregion

# region Tree


class _BaseCluster(JsonObject):
    """The `base_cluster` of a tree: clusters of the base block around its base."""

    may_replace: list[Annotated[str | Block | BlockDescriptor, BlockId]] = json_field()
    num_clusters: Annotated[int, AtLeastOne] = json_field()
    cluster_radius: Annotated[int, NonNegative] = json_field()


class _AboveRoot(JsonObject):
    """The `above_root` of mangrove roots: blocks on top of the roots."""

    above_root_chance: Annotated[float | tuple[int, int], Fraction] | None = None
    above_root_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None


class _MangroveRoots(JsonObject):
    """The `mangrove_roots` of a tree."""

    max_root_width: Annotated[int, AtLeastOne] = json_field()
    max_root_length: Annotated[int, AtLeastOne] = json_field()
    root_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    above_root: _AboveRoot | None = None
    muddy_root_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    mud_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    y_offset: int = json_field()
    roots_may_grow_through: (
        list[Annotated[str | Block | BlockDescriptor, BlockId]] | None
    ) = None
    root_decoration: _TreeDecoration | None = None

    def set_root_decoration(self, decoration: _TreeDecoration) -> None:
        """Sets the blocks spread from the roots."""
        self.root_decoration = decoration


_TRUNKS = (
    "acacia_trunk",
    "cherry_trunk",
    "fallen_trunk",
    "fancy_trunk",
    "mangrove_trunk",
    "mega_trunk",
    "poplar_trunk",
    "trunk",
)
_CANOPIES = (
    "acacia_canopy",
    "canopy",
    "cherry_canopy",
    "fancy_canopy",
    "mangrove_canopy",
    "mega_canopy",
    "mega_pine_canopy",
    "pine_canopy",
    "poplar_canopy",
    "random_spread_canopy",
    "roofed_canopy",
    "spruce_canopy",
)


class _TreeFeature(_Feature):
    """The `minecraft:tree_feature` body."""

    base_block: (
        Annotated[str | Block | BlockDescriptor, BlockId]
        | list[Annotated[str | Block | BlockDescriptor, BlockId]]
        | None
    ) = None
    base_cluster: _BaseCluster | None = None
    may_grow_on: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    may_replace: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    may_grow_through: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = (
        None
    )
    acacia_trunk: _AcaciaTrunk | None = None
    cherry_trunk: _CherryTrunk | None = None
    fallen_trunk: _FallenTrunk | None = None
    fancy_trunk: _FancyTrunk | None = None
    mangrove_trunk: _MangroveTrunk | None = None
    mega_trunk: _MegaTrunk | None = None
    poplar_trunk: _PoplarTrunk | None = None
    trunk: _Trunk | None = None
    acacia_canopy: _AcaciaCanopy | None = None
    canopy: _Canopy | None = None
    cherry_canopy: _CherryCanopy | None = None
    fancy_canopy: _FancyCanopy | None = None
    mangrove_canopy: _MangroveCanopy | None = None
    mega_canopy: _MegaCanopy | None = None
    mega_pine_canopy: _MegaPineCanopy | None = None
    pine_canopy: _PineCanopy | None = None
    poplar_canopy: _PoplarCanopy | None = None
    random_spread_canopy: _RandomSpreadCanopy | None = None
    roofed_canopy: _RoofedCanopy | None = None
    spruce_canopy: _SpruceCanopy | None = None
    mangrove_roots: _MangroveRoots | None = None

    def set_base_block(
        self,
        blocks: str | Block | BlockDescriptor | Sequence[str | Block | BlockDescriptor],
    ) -> None:
        """Sets the block, or blocks, at the base of the tree."""
        self.base_block = (
            blocks
            if isinstance(blocks, (str, Block, BlockDescriptor))
            else list(blocks)
        )

    def set_base_cluster(self, cluster: _BaseCluster) -> None:
        """Sets the clusters of the base block around the base."""
        self.base_cluster = cluster

    def set_may_grow_on(self, blocks: Sequence[str | Block | BlockDescriptor]) -> None:
        """Sets the blocks the tree can grow on."""
        self.may_grow_on = _blocks(blocks)

    def set_may_replace(self, blocks: Sequence[str | Block | BlockDescriptor]) -> None:
        """Sets the blocks the tree may replace."""
        self.may_replace = _blocks(blocks)

    def set_may_grow_through(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> None:
        """Sets the blocks the tree can grow through."""
        self.may_grow_through = _blocks(blocks)

    def set_trunk(self, kind: str, trunk: JsonObject) -> None:
        """Sets the trunk, replacing a trunk of another kind."""
        for name in _TRUNKS:
            setattr(self, name, trunk if name == kind else None)

    def set_canopy(self, kind: str, canopy: JsonObject) -> None:
        """Sets the canopy, replacing a canopy of another kind."""
        for name in _CANOPIES:
            setattr(self, name, canopy if name == kind else None)

    def set_mangrove_roots(self, roots: _MangroveRoots) -> None:
        """Sets the roots of a mangrove tree."""
        self.mangrove_roots = roots

    def current_trunk(self) -> JsonObject | None:
        """The trunk, whatever its kind."""
        return next(
            (getattr(self, name) for name in _TRUNKS if getattr(self, name)), None
        )

    def current_canopy(self) -> JsonObject | None:
        """The canopy, whatever its kind."""
        return next(
            (getattr(self, name) for name in _CANOPIES if getattr(self, name)), None
        )

    def __validate__(self) -> None:
        if self.current_trunk() is None:
            raise ValueError("A tree feature needs a trunk.")


class _TreeFeatureFile(JsonObject):
    """The content of a tree feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:tree_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _TreeFeature = json_field(
        key="minecraft:tree_feature", default_factory=_TreeFeature
    )


def _leaves(
    leaf_blocks: Sequence[
        tuple[str | Block | BlockDescriptor, float] | str | Block | BlockDescriptor
    ],
) -> list[tuple[str | Block | BlockDescriptor, float]]:
    """Leaf blocks with their weight, 1 for a block given alone."""
    return [
        (entry[0], float(entry[1])) if isinstance(entry, tuple) else (entry, 1.0)
        for entry in leaf_blocks
    ]


class TreeFeature(Feature[_TreeFeatureFile]):
    """Places a tree: a trunk anchored to a base block, and a canopy around its top.

    Set one trunk and at most one canopy. Setting another trunk, or another canopy,
    replaces it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_tree_feature)
    """

    def __init__(self, name: str) -> None:
        """Creates a tree feature. Set its trunk and canopy next.

        Args:
            name (str): The name of the feature, also its file name.
        """
        super().__init__(name)
        self._branch_canopies: dict[str, JsonObject] = {}

    # region Base

    def base_block(
        self,
        blocks: str | Block | BlockDescriptor | Sequence[str | Block | BlockDescriptor],
    ) -> "TreeFeature":
        """Sets the block at the base of the tree.

        Args:
            blocks (str | Block | BlockDescriptor | Sequence[str | Block | BlockDescriptor]):
                The block, or blocks.
        """
        self._feature.set_base_block(blocks)
        return self

    def base_cluster(
        self,
        num_clusters: int = 1,
        cluster_radius: int = 0,
        may_replace: Sequence[str | Block | BlockDescriptor] | None = None,
    ) -> "TreeFeature":
        """Sets clusters of the base block, placed at random around the base of the tree.

        Args:
            num_clusters (int, optional): The number of clusters. At least 1. Defaults to 1.
            cluster_radius (int, optional): The radius of each cluster. At least 0.
                Defaults to 0.
            may_replace (Sequence[str | Block | BlockDescriptor], optional): The blocks a
                cluster may replace.
        """
        self._feature.set_base_cluster(
            _BaseCluster(
                may_replace=_blocks(may_replace or []),
                num_clusters=num_clusters,
                cluster_radius=cluster_radius,
            )
        )
        return self

    def may_grow_on(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "TreeFeature":
        """Sets the blocks the tree can grow on.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_may_grow_on(blocks)
        return self

    def may_replace(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "TreeFeature":
        """Sets the blocks the tree may replace.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_may_replace(blocks)
        return self

    def may_grow_through(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "TreeFeature":
        """Sets the blocks the tree can grow through.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_may_grow_through(blocks)
        return self

    # endregion

    # region Trunks

    def _set_trunk(self, kind: str, trunk: JsonObject) -> "TreeFeature":
        self._feature.set_trunk(kind, trunk)
        self._sync_branch_canopies()
        return self

    def trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_height: int | tuple[int, int] = (4, 7),
        height_modifier: int | tuple[int, int] | None = None,
        can_be_submerged: bool | int | None = None,
    ) -> "TreeFeature":
        """Sets a straight trunk.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_height (int | tuple[int, int], optional): The height, or a range it is
                picked from. Defaults to (4, 7).
            height_modifier (int | tuple[int, int], optional): Added to the height, or a
                range it is picked from.
            can_be_submerged (bool | int, optional): Whether the trunk can grow under water;
                a number is the greatest depth, at least 1.
        """
        submerged = (
            _SubmergedDepth(max_depth=can_be_submerged)
            if isinstance(can_be_submerged, int)
            and not isinstance(can_be_submerged, bool)
            else can_be_submerged
        )
        return self._set_trunk(
            "trunk",
            _Trunk(
                trunk_block=trunk_block,
                trunk_height=trunk_height,
                height_modifier=height_modifier,
                can_be_submerged=submerged,
            ),
        )

    def acacia_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_width: int = 1,
        base_height: int = 5,
        height_intervals: Sequence[int] | None = None,
        min_height_for_canopy: int | None = None,
        allow_diagonal_growth: bool = True,
        lean_height: int | tuple[int, int] = (1, 5),
        lean_steps: int | tuple[int, int] = (1, 4),
        lean_length: int | tuple[int, int] | None = None,
        branch_chance: float | tuple[int, int] = 0.0,
        branch_length: int | tuple[int, int] = (1, 4),
        branch_position: int | tuple[int, int] = (1, 3),
    ) -> "TreeFeature":
        """Sets a trunk that can lean, with branches, like an acacia.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_width (int, optional): The width of the trunk. At least 1. Defaults to 1.
            base_height (int, optional): The least height. At least 1. Defaults to 5.
            height_intervals (Sequence[int], optional): Each adds a random number below it
                to the height.
            min_height_for_canopy (int, optional): The least height the canopy is placed at.
            allow_diagonal_growth (bool, optional): The trunk can lean. Defaults to True.
            lean_height (int | tuple[int, int], optional): How far below the top the lean
                starts, or a range it is picked from. Defaults to (1, 5).
            lean_steps (int | tuple[int, int], optional): How many blocks the trunk moves
                sideways, or a range. Defaults to (1, 4).
            lean_length (int | tuple[int, int], optional): How long the lean is along y, or
                a range.
            branch_chance (float | tuple[int, int], optional): The chance of a branch: a
                number or a `(numerator, denominator)` fraction. Defaults to 0.
            branch_length (int | tuple[int, int], optional): The length of a branch along y,
                or a range. Defaults to (1, 4).
            branch_position (int | tuple[int, int], optional): Where a branch starts along
                y, or a range. Defaults to (1, 3).
        """
        return self._set_trunk(
            "acacia_trunk",
            _AcaciaTrunk(
                trunk_block=trunk_block,
                trunk_width=trunk_width,
                trunk_height=_TrunkHeight(
                    base=base_height,
                    intervals=(
                        None if height_intervals is None else list(height_intervals)
                    ),
                    min_height_for_canopy=min_height_for_canopy,
                ),
                trunk_lean=_TrunkLean(
                    allow_diagonal_growth=allow_diagonal_growth,
                    lean_height=lean_height,
                    lean_steps=lean_steps,
                    lean_length=lean_length,
                ),
                branches=_AcaciaBranches(
                    branch_chance=branch_chance,
                    branch_length=branch_length,
                    branch_position=branch_position,
                ),
            ),
        )

    def cherry_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        base_height: int = 7,
        height_intervals: Sequence[int] | None = None,
        one_branch_weight: int = 10,
        two_branches_weight: int = 10,
        two_branches_and_trunk_weight: int = 10,
        branch_horizontal_length: int | tuple[int, int] = (2, 4),
        branch_start_offset_from_top: int | tuple[int, int] = (-4, -3),
        branch_end_offset_from_top: int | tuple[int, int] = (-1, 0),
    ) -> "TreeFeature":
        """Sets a trunk with one or two long branches, like a cherry tree.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            base_height (int, optional): The least height. At least 2. Defaults to 7.
            height_intervals (Sequence[int], optional): Each adds a random number below it
                to the height.
            one_branch_weight (int, optional): The weight of a tree with one branch.
                Defaults to 10.
            two_branches_weight (int, optional): The weight of a tree with two branches.
                Defaults to 10.
            two_branches_and_trunk_weight (int, optional): The weight of a tree with two
                branches and the trunk going on. Defaults to 10.
            branch_horizontal_length (int | tuple[int, int], optional): The length of a
                branch along x and z, or a range. Defaults to (2, 4).
            branch_start_offset_from_top (int | tuple[int, int], optional): Where a branch
                starts, from the top of the tree, or a range. Defaults to (-4, -3).
            branch_end_offset_from_top (int | tuple[int, int], optional): Where a branch
                ends, from the top of the tree, or a range. Defaults to (-1, 0).
        """
        return self._set_trunk(
            "cherry_trunk",
            _CherryTrunk(
                trunk_block=trunk_block,
                trunk_height=_TrunkHeight(
                    base=base_height,
                    intervals=(
                        None if height_intervals is None else list(height_intervals)
                    ),
                ),
                branches=_CherryBranches(
                    tree_type_weights=_TreeTypeWeights(
                        one_branch=one_branch_weight,
                        two_branches=two_branches_weight,
                        two_branches_and_trunk=two_branches_and_trunk_weight,
                    ),
                    branch_horizontal_length=branch_horizontal_length,
                    branch_start_offset_from_top=branch_start_offset_from_top,
                    branch_end_offset_from_top=branch_end_offset_from_top,
                ),
            ),
        )

    def fallen_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        log_length: int | tuple[int, int] = (4, 7),
        stump_height: int | tuple[int, int] | None = None,
        height_modifier: int | tuple[int, int] | None = None,
        log_decoration_feature: "Feature | str | None" = None,
    ) -> "TreeFeature":
        """Sets a fallen log, with an optional stump.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the log.
            log_length (int | tuple[int, int], optional): The length of the log, or a range.
                Defaults to (4, 7).
            stump_height (int | tuple[int, int], optional): The height of the stump, or a
                range.
            height_modifier (int | tuple[int, int], optional): Added to the length, or a
                range.
            log_decoration_feature (Feature | str, optional): A feature that decorates the
                log.
        """
        return self._set_trunk(
            "fallen_trunk",
            _FallenTrunk(
                trunk_block=trunk_block,
                log_length=log_length,
                stump_height=stump_height,
                height_modifier=height_modifier,
                log_decoration_feature=(
                    None
                    if log_decoration_feature is None
                    else str(log_decoration_feature)
                ),
            ),
        )

    def fancy_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_width: int = 1,
        base_height: int = 5,
        height_variance: int = 12,
        height_scale: float = 0.618,
        branch_slope: float = 0.381,
        branch_density: float = 1.0,
        branch_min_altitude_factor: float = 0.2,
        width_scale: float = 1.0,
        foliage_altitude_factor: float = 0.3,
    ) -> "TreeFeature":
        """Sets a tall trunk with many branches, like a fancy oak.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_width (int, optional): The width of the trunk. At least 1. Defaults to 1.
            base_height (int, optional): The least height. At least 1. Defaults to 5.
            height_variance (int, optional): Added to the height at random. At least 1.
                Defaults to 12.
            height_scale (float, optional): The height is multiplied by this, from 0 to 1.
                Defaults to 0.618.
            branch_slope (float, optional): The slope of a branch: 0 is flat, 1 vertical.
                Defaults to 0.381.
            branch_density (float, optional): How dense the foliage is. Defaults to 1.
            branch_min_altitude_factor (float, optional): The lowest branch, as a share of
                the height, from 0 to 1. Defaults to 0.2.
            width_scale (float, optional): Scales the radius of the tree. At least 0.
                Defaults to 1.
            foliage_altitude_factor (float, optional): The lowest foliage, as a share of the
                height, from 0 to 1. Defaults to 0.3.
        """
        return self._set_trunk(
            "fancy_trunk",
            _FancyTrunk(
                trunk_block=trunk_block,
                trunk_width=trunk_width,
                trunk_height=_FancyTrunkHeight(
                    base=base_height, variance=height_variance, scale=height_scale
                ),
                branches=_FancyBranches(
                    slope=branch_slope,
                    density=branch_density,
                    min_altitude_factor=branch_min_altitude_factor,
                ),
                width_scale=width_scale,
                foliage_altitude_factor=foliage_altitude_factor,
            ),
        )

    def mangrove_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_width: int = 1,
        base_height: int = 5,
        height_rand_a: int = 1,
        height_rand_b: int = 1,
        branch_length: int | tuple[int, int] = (2, 4),
        branch_steps: int | tuple[int, int] = (1, 3),
        branch_chance: float | tuple[int, int] = 100.0,
    ) -> "TreeFeature":
        """Sets a trunk with branches, like a mangrove. Add roots with `mangrove_roots()`.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_width (int, optional): The width of the trunk. At least 1. Defaults to 1.
            base_height (int, optional): The least height. At least 1. Defaults to 5.
            height_rand_a (int, optional): The first height modifier. At least 1. Defaults
                to 1.
            height_rand_b (int, optional): The second height modifier. At least 1. Defaults
                to 1.
            branch_length (int | tuple[int, int], optional): The length of a branch along y,
                or a range. Defaults to (2, 4).
            branch_steps (int | tuple[int, int], optional): The number of branches, or a
                range. Defaults to (1, 3).
            branch_chance (float | tuple[int, int], optional): The chance of a branch: a
                number or a `(numerator, denominator)` fraction. Defaults to 100.
        """
        return self._set_trunk(
            "mangrove_trunk",
            _MangroveTrunk(
                trunk_block=trunk_block,
                trunk_width=trunk_width,
                trunk_height=_MangroveTrunkHeight(
                    base=base_height,
                    height_rand_a=height_rand_a,
                    height_rand_b=height_rand_b,
                ),
                branches=_MangroveBranches(
                    branch_length=branch_length,
                    branch_steps=branch_steps,
                    branch_chance=branch_chance,
                ),
            ),
        )

    def mega_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_width: int = 2,
        base_height: int = 15,
        height_intervals: Sequence[int] | None = None,
        height_modifier: int | tuple[int, int] | None = None,
        branch_length: int | None = None,
        branch_slope: float | None = None,
        branch_interval: int | tuple[int, int] | None = None,
        branch_altitude_factor: float | tuple[float, float] | None = None,
    ) -> "TreeFeature":
        """Sets a wide trunk, like a mega jungle tree or a dark oak.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_width (int, optional): The width of the trunk. At least 1. Defaults to 2.
            base_height (int, optional): The least height. At least 1. Defaults to 15.
            height_intervals (Sequence[int], optional): Each adds a random number below it
                to the height.
            height_modifier (int | tuple[int, int], optional): Added to the height, or a
                range.
            branch_length (int, optional): The length of a branch. At least 1.
            branch_slope (float, optional): The slope of a branch: 0 is flat, 1 vertical.
            branch_interval (int | tuple[int, int], optional): The distance between two
                branches, or a range.
            branch_altitude_factor (float | tuple[float, float], optional): Where branches
                grow, as a share of the height from 0 to 1, or a range.
        """
        options = {
            "branch_length": branch_length,
            "branch_slope": branch_slope,
            "branch_interval": branch_interval,
            "branch_altitude_factor": branch_altitude_factor,
        }
        branches = (
            _MegaBranches(**options)
            if any(value is not None for value in options.values())
            else None
        )
        return self._set_trunk(
            "mega_trunk",
            _MegaTrunk(
                trunk_block=trunk_block,
                trunk_width=trunk_width,
                trunk_height=_TrunkHeight(
                    base=base_height,
                    intervals=(
                        None if height_intervals is None else list(height_intervals)
                    ),
                ),
                height_modifier=height_modifier,
                branches=branches,
            ),
        )

    def poplar_trunk(
        self,
        trunk_block: str | Block | BlockDescriptor,
        trunk_height: int | tuple[int, int] = (5, 8),
        remaining_trunk_height_above_branches: int | tuple[int, int] | None = None,
        amount_of_foliage_support_branches: int | None = None,
        height_modifier: int | tuple[int, int] | None = None,
    ) -> "TreeFeature":
        """Sets a tall, thin trunk, like a poplar.

        Args:
            trunk_block (str | Block | BlockDescriptor): The block of the trunk.
            trunk_height (int | tuple[int, int], optional): The height, or a range.
                Defaults to (5, 8).
            remaining_trunk_height_above_branches (int | tuple[int, int], optional): The
                height of the trunk above the branches, or a range.
            amount_of_foliage_support_branches (int, optional): The number of branches that
                hold the foliage.
            height_modifier (int | tuple[int, int], optional): Added to the height, or a
                range.
        """
        return self._set_trunk(
            "poplar_trunk",
            _PoplarTrunk(
                trunk_block=trunk_block,
                trunk_height=trunk_height,
                remaining_trunk_height_above_branches=remaining_trunk_height_above_branches,
                amount_of_foliage_support_branches=amount_of_foliage_support_branches,
                height_modifier=height_modifier,
            ),
        )

    def trunk_decoration(
        self,
        decoration_chance: float | tuple[int, int],
        decoration_block: str | Block | BlockDescriptor | None = None,
        num_steps: int | None = None,
        step_direction: Literal["down", "up", "out", "away"] | None = None,
    ) -> "TreeFeature":
        """Spreads blocks from the trunk, such as vines. Set the trunk first.

        Args:
            decoration_chance (float | tuple[int, int]): The chance of a decoration: a
                number or a `(numerator, denominator)` fraction.
            decoration_block (str | Block | BlockDescriptor, optional): The block placed.
            num_steps (int, optional): How many blocks are placed.
            step_direction (Literal["down", "up", "out", "away"], optional): The direction
                the blocks spread in.

        Raises:
            ValueError: When the tree has no trunk, or its trunk has no decorations (cherry,
                fancy and poplar trunks).
        """
        trunk = self._feature.current_trunk()
        if not hasattr(trunk, "set_trunk_decoration"):
            raise ValueError(
                f"Tree '{self.identifier}' has no trunk that takes a decoration."
            )
        trunk.set_trunk_decoration(
            _decoration(decoration_chance, decoration_block, num_steps, step_direction)
        )
        return self

    # endregion

    # region Canopies

    def _set_canopy(
        self, kind: str, canopy: JsonObject, sync_to_branches: bool
    ) -> "TreeFeature":
        self._feature.set_canopy(kind, canopy)
        if sync_to_branches and kind in _BRANCH_CANOPIES:
            self._set_branch_canopy(kind, canopy)
        return self

    def _set_branch_canopy(self, kind: str, canopy: JsonObject) -> "TreeFeature":
        self._branch_canopies[kind] = canopy
        self._sync_branch_canopies()
        return self

    def _sync_branch_canopies(self) -> None:
        """Gives every trunk with branches the branch canopies set so far."""
        canopy = (
            _BranchCanopy(**self._branch_canopies) if self._branch_canopies else None
        )
        for kind in ("acacia_trunk", "cherry_trunk", "mega_trunk"):
            trunk = getattr(self._feature, kind)
            if trunk is not None and trunk.branches is not None:
                trunk.branches.set_branch_canopy(canopy)

    def acacia_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_size: int = 3,
        simplify_canopy: bool = False,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets a flat canopy, like an acacia.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            canopy_size (int, optional): The size of the canopy. At least 1. Defaults to 3.
            simplify_canopy (bool, optional): Use a simpler pattern. Defaults to False.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "acacia_canopy",
            _AcaciaCanopy(
                leaf_block=leaf_block,
                canopy_size=canopy_size,
                simplify_canopy=simplify_canopy or None,
            ),
            sync_to_branches,
        )

    def canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        min_width: int | None = None,
        canopy_offset_min: int | None = None,
        canopy_offset_max: int | None = None,
        slope_rise: int | None = None,
        slope_run: int | None = None,
        variation_chance: Sequence[float | tuple[int, int]] | None = None,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets a layered canopy, like an oak or a birch.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            min_width (int, optional): The least width of the canopy. At least 0.
            canopy_offset_min (int, optional): The lowest layer, from the block above the
                trunk. Set with `canopy_offset_max`.
            canopy_offset_max (int, optional): The highest layer, from the block above the
                trunk.
            slope_rise (int, optional): The rise of the canopy's slope. At least 1.
            slope_run (int, optional): The run of the canopy's slope. At least 1.
            variation_chance (Sequence[float | tuple[int, int]], optional): For each layer,
                the chance of each leaf: a number or a `(numerator, denominator)` fraction.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        offset = (
            (canopy_offset_min, canopy_offset_max)
            if canopy_offset_min is not None and canopy_offset_max is not None
            else None
        )
        slope = (
            _CanopySlope(rise=slope_rise, run=slope_run)
            if slope_rise is not None or slope_run is not None
            else None
        )
        return self._set_canopy(
            "canopy",
            _Canopy(
                leaf_block=leaf_block,
                min_width=min_width,
                canopy_offset=offset,
                canopy_slope=slope,
                variation_chance=(
                    None if variation_chance is None else list(variation_chance)
                ),
            ),
            sync_to_branches,
        )

    def cherry_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        height: int | tuple[int, int] = 4,
        radius: int | tuple[int, int] = 4,
        trunk_width: int | None = None,
        wide_bottom_layer_hole_chance: float | tuple[int, int] = 25.0,
        corner_hole_chance: float | tuple[int, int] = 50.0,
        hanging_leaves_chance: float | tuple[int, int] = 16.6666,
        hanging_leaves_extension_chance: float | tuple[int, int] = 33.3333,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets a round canopy with hanging leaves, like a cherry tree.

        Chances are percentages, or `(numerator, denominator)` fractions.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            height (int | tuple[int, int], optional): The number of layers, or a range.
                Defaults to 4.
            radius (int | tuple[int, int], optional): The radius, or a range. Defaults to 4.
            trunk_width (int, optional): The width of the trunk. At least 1.
            wide_bottom_layer_hole_chance (float | tuple[int, int], optional): The chance
                of a hole in the bottom layer. Defaults to 25.
            corner_hole_chance (float | tuple[int, int], optional): The chance of a hole in
                a corner. Defaults to 50.
            hanging_leaves_chance (float | tuple[int, int], optional): The chance of hanging
                leaves. Defaults to 16.6666.
            hanging_leaves_extension_chance (float | tuple[int, int], optional): The chance
                hanging leaves go one further. Defaults to 33.3333.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "cherry_canopy",
            _CherryCanopy(
                leaf_block=leaf_block,
                height=height,
                radius=radius,
                trunk_width=trunk_width,
                wide_bottom_layer_hole_chance=wide_bottom_layer_hole_chance,
                corner_hole_chance=corner_hole_chance,
                hanging_leaves_chance=hanging_leaves_chance,
                hanging_leaves_extension_chance=hanging_leaves_extension_chance,
            ),
            sync_to_branches,
        )

    def fancy_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        height: int = 4,
        radius: int = 4,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the round canopy of a fancy oak.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            height (int, optional): The number of layers. At least 1. Defaults to 4.
            radius (int, optional): The radius. At least 0. Defaults to 4.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "fancy_canopy",
            _FancyCanopy(leaf_block=leaf_block, height=height, radius=radius),
            sync_to_branches,
        )

    def mangrove_canopy(
        self,
        leaf_blocks: Sequence[
            tuple[str | Block | BlockDescriptor, float]
            | str
            | str
            | Block
            | BlockDescriptor
        ],
        canopy_height: int | tuple[int, int] = (3, 5),
        canopy_radius: int | tuple[int, int] = (3, 5),
        leaf_placement_attempts: int = 100,
        hanging_block: str | Block | BlockDescriptor | None = None,
        hanging_block_placement_chance: float | tuple[int, int] | None = None,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets a canopy of leaves placed at random, with hanging blocks, like a mangrove.

        Args:
            leaf_blocks (Sequence[tuple[str | Block | BlockDescriptor, float] | str | Block | BlockDescriptor]):
                The leaf blocks, with their weight; 1 for a block given alone.
            canopy_height (int | tuple[int, int], optional): The number of layers, or a
                range. Defaults to (3, 5).
            canopy_radius (int | tuple[int, int], optional): The radius, or a range.
                Defaults to (3, 5).
            leaf_placement_attempts (int, optional): How many times a leaf is tried. At
                least 1. Defaults to 100.
            hanging_block (str | Block | BlockDescriptor, optional): The block hanging
                under the leaves.
            hanging_block_placement_chance (float | tuple[int, int], optional): The chance
                of a hanging block: a number or a `(numerator, denominator)` fraction.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "mangrove_canopy",
            _MangroveCanopy(
                leaf_blocks=_leaves(leaf_blocks),
                canopy_height=canopy_height,
                canopy_radius=canopy_radius,
                leaf_placement_attempts=leaf_placement_attempts,
                hanging_block=hanging_block,
                hanging_block_placement_chance=hanging_block_placement_chance,
            ),
            sync_to_branches,
        )

    def mega_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_height: int | tuple[int, int] = (4, 6),
        base_radius: int = 4,
        core_width: int = 2,
        simplify_canopy: bool = False,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the wide canopy of a mega tree.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            canopy_height (int | tuple[int, int], optional): The number of layers, or a
                range. Defaults to (4, 6).
            base_radius (int, optional): The radius. At least 0. Defaults to 4.
            core_width (int, optional): The width of the trunk. At least 1. Defaults to 2.
            simplify_canopy (bool, optional): Use a simpler pattern. Defaults to False.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "mega_canopy",
            _MegaCanopy(
                leaf_block=leaf_block,
                canopy_height=canopy_height,
                base_radius=base_radius,
                core_width=core_width,
                simplify_canopy=simplify_canopy or None,
            ),
            sync_to_branches,
        )

    def mega_pine_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_height: int | tuple[int, int] = (8, 12),
        base_radius: int = 4,
        radius_step_modifier: float = 0.5,
        core_width: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the canopy of a mega spruce.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            canopy_height (int | tuple[int, int], optional): The number of layers, or a
                range. Defaults to (8, 12).
            base_radius (int, optional): The radius. At least 0. Defaults to 4.
            radius_step_modifier (float, optional): Changes the radius from layer to layer.
                At least 0. Defaults to 0.5.
            core_width (int, optional): The width of the trunk. At least 1. Defaults to 2.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "mega_pine_canopy",
            _MegaPineCanopy(
                leaf_block=leaf_block,
                canopy_height=canopy_height,
                base_radius=base_radius,
                radius_step_modifier=radius_step_modifier,
                core_width=core_width,
            ),
            sync_to_branches,
        )

    def pine_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_height: int | tuple[int, int] = (4, 5),
        base_radius: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the canopy of a pine.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            canopy_height (int | tuple[int, int], optional): The number of layers, or a
                range. Defaults to (4, 5).
            base_radius (int, optional): The radius. At least 1. Defaults to 2.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "pine_canopy",
            _PineCanopy(
                leaf_block=leaf_block,
                canopy_height=canopy_height,
                base_radius=base_radius,
            ),
            sync_to_branches,
        )

    def poplar_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        radius: Sequence[tuple[int, int]] | None = None,
        trunk_width: int | None = None,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the canopy of a poplar.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            radius (Sequence[tuple[int, int]], optional): `(radius, weight)` pairs the
                radius is picked from.
            trunk_width (int, optional): The width of the trunk. At least 1.
            sync_to_branches (bool, optional): Kept for symmetry: a poplar canopy cannot
                grow on branches. Defaults to True.
        """
        return self._set_canopy(
            "poplar_canopy",
            _PoplarCanopy(
                leaf_block=leaf_block,
                radius=(
                    None
                    if radius is None
                    else [
                        _PoplarRadius(value=value, weight=weight)
                        for value, weight in radius
                    ]
                ),
                trunk_width=trunk_width,
            ),
            sync_to_branches,
        )

    def random_spread_canopy(
        self,
        leaf_blocks: Sequence[
            tuple[str | Block | BlockDescriptor, float]
            | str
            | str
            | Block
            | BlockDescriptor
        ],
        canopy_height: int | tuple[int, int] = (3, 5),
        canopy_radius: int | tuple[int, int] = (3, 5),
        leaf_placement_attempts: int = 100,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets a canopy of leaves placed at random, like an azalea.

        Args:
            leaf_blocks (Sequence[tuple[str | Block | BlockDescriptor, float] | str | Block | BlockDescriptor]):
                The leaf blocks, with their weight; 1 for a block given alone.
            canopy_height (int | tuple[int, int], optional): The number of layers, or a
                range. Defaults to (3, 5).
            canopy_radius (int | tuple[int, int], optional): The radius, or a range.
                Defaults to (3, 5).
            leaf_placement_attempts (int, optional): How many times a leaf is tried. At
                least 1. Defaults to 100.
            sync_to_branches (bool, optional): Kept for symmetry: a random spread canopy
                cannot grow on branches. Defaults to True.
        """
        return self._set_canopy(
            "random_spread_canopy",
            _RandomSpreadCanopy(
                leaf_blocks=_leaves(leaf_blocks),
                canopy_height=canopy_height,
                canopy_radius=canopy_radius,
                leaf_placement_attempts=leaf_placement_attempts,
            ),
            sync_to_branches,
        )

    def roofed_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_height: int = 3,
        core_width: int = 1,
        outer_radius: int = 3,
        inner_radius: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the flat, wide canopy of a dark oak.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            canopy_height (int, optional): The number of middle layers. At least 3.
                Defaults to 3.
            core_width (int, optional): The width of the trunk. At least 1. Defaults to 1.
            outer_radius (int, optional): The radius of the base and top layers. At least 0.
                Defaults to 3.
            inner_radius (int, optional): The radius of the middle layers. At least 0.
                Defaults to 2.
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "roofed_canopy",
            _RoofedCanopy(
                leaf_block=leaf_block,
                canopy_height=canopy_height,
                core_width=core_width,
                outer_radius=outer_radius,
                inner_radius=inner_radius,
            ),
            sync_to_branches,
        )

    def spruce_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        lower_offset: int | tuple[int, int] = (0, 0),
        upper_offset: int | tuple[int, int] = (0, 0),
        max_radius: int | tuple[int, int] = (2, 3),
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the canopy of a spruce.

        Args:
            leaf_block (str | Block | BlockDescriptor): The block of the canopy.
            lower_offset (int | tuple[int, int], optional): The lowest layer, or a range.
                Defaults to (0, 0).
            upper_offset (int | tuple[int, int], optional): The highest layer, or a range.
                Defaults to (0, 0).
            max_radius (int | tuple[int, int], optional): The largest radius, or a range.
                Defaults to (2, 3).
            sync_to_branches (bool, optional): Also grow it at the end of the trunk's
                branches. Defaults to True.
        """
        return self._set_canopy(
            "spruce_canopy",
            _SpruceCanopy(
                leaf_block=leaf_block,
                lower_offset=lower_offset,
                upper_offset=upper_offset,
                max_radius=max_radius,
            ),
            sync_to_branches,
        )

    def canopy_decoration(
        self,
        decoration_chance: float | tuple[int, int],
        decoration_block: str | Block | BlockDescriptor | None = None,
        num_steps: int | None = None,
        step_direction: Literal["down", "up", "out", "away"] | None = None,
    ) -> "TreeFeature":
        """Spreads blocks from the canopy, such as vines. Set a canopy or a mangrove canopy
        first.

        Args:
            decoration_chance (float | tuple[int, int]): The chance of a decoration: a
                number or a `(numerator, denominator)` fraction.
            decoration_block (str | Block | BlockDescriptor, optional): The block placed.
            num_steps (int, optional): How many blocks are placed.
            step_direction (Literal["down", "up", "out", "away"], optional): The direction
                the blocks spread in.

        Raises:
            ValueError: When the tree has no canopy that takes a decoration.
        """
        canopy = self._feature.current_canopy()
        if not hasattr(canopy, "set_canopy_decoration"):
            raise ValueError(
                f"Tree '{self.identifier}' has no canopy that takes a decoration: use canopy() or mangrove_canopy()."
            )
        canopy.set_canopy_decoration(
            _decoration(decoration_chance, decoration_block, num_steps, step_direction)
        )
        return self

    # endregion

    # region Branch canopies

    def branch_cherry_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        height: int | tuple[int, int] = 4,
        radius: int | tuple[int, int] = 4,
        trunk_width: int | None = None,
        wide_bottom_layer_hole_chance: float | tuple[int, int] = 25.0,
        corner_hole_chance: float | tuple[int, int] = 50.0,
        hanging_leaves_chance: float | tuple[int, int] = 16.6666,
        hanging_leaves_extension_chance: float | tuple[int, int] = 33.3333,
    ) -> "TreeFeature":
        """Grows a cherry canopy at the end of the trunk's branches. The arguments are the
        ones of `cherry_canopy()`."""
        return self._set_branch_canopy(
            "cherry_canopy",
            _CherryCanopy(
                leaf_block=leaf_block,
                height=height,
                radius=radius,
                trunk_width=trunk_width,
                wide_bottom_layer_hole_chance=wide_bottom_layer_hole_chance,
                corner_hole_chance=corner_hole_chance,
                hanging_leaves_chance=hanging_leaves_chance,
                hanging_leaves_extension_chance=hanging_leaves_extension_chance,
            ),
        )

    def branch_fancy_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        height: int = 4,
        radius: int = 4,
    ) -> "TreeFeature":
        """Grows a fancy canopy at the end of the trunk's branches. The arguments are the
        ones of `fancy_canopy()`."""
        return self._set_branch_canopy(
            "fancy_canopy",
            _FancyCanopy(leaf_block=leaf_block, height=height, radius=radius),
        )

    def branch_acacia_canopy(
        self,
        leaf_block: str | Block | BlockDescriptor,
        canopy_size: int = 3,
        simplify_canopy: bool = False,
    ) -> "TreeFeature":
        """Grows an acacia canopy at the end of the trunk's branches. The arguments are the
        ones of `acacia_canopy()`."""
        return self._set_branch_canopy(
            "acacia_canopy",
            _AcaciaCanopy(
                leaf_block=leaf_block,
                canopy_size=canopy_size,
                simplify_canopy=simplify_canopy or None,
            ),
        )

    # endregion

    def mangrove_roots(
        self,
        root_block: str | Block | BlockDescriptor,
        muddy_root_block: str | Block | BlockDescriptor | None = None,
        max_root_width: int = 5,
        max_root_length: int = 15,
        y_offset: int = 0,
        roots_may_grow_through: Sequence[str | Block | BlockDescriptor] | None = None,
        mud_block: str | Block | BlockDescriptor | None = None,
        above_root_block: str | Block | BlockDescriptor | None = None,
        above_root_chance: float | tuple[int, int] | None = None,
    ) -> "TreeFeature":
        """Sets the roots of a mangrove.

        Args:
            root_block (str | Block | BlockDescriptor): The block of the roots.
            muddy_root_block (str | Block | BlockDescriptor, optional): The block of the
                roots in mud.
            max_root_width (int, optional): The widest the roots get, growing down. At
                least 1. Defaults to 5.
            max_root_length (int, optional): The longest a root gets. At least 1. Defaults
                to 15.
            y_offset (int, optional): The offset of the roots from the trunk. Defaults to 0.
            roots_may_grow_through (Sequence[str | Block | BlockDescriptor], optional): The
                blocks roots can grow through.
            mud_block (str | Block | BlockDescriptor, optional): The block where a muddy
                root is placed.
            above_root_block (str | Block | BlockDescriptor, optional): A block placed on
                top of the roots.
            above_root_chance (float | tuple[int, int], optional): The chance of that block:
                a number or a `(numerator, denominator)` fraction.
        """
        above = (
            _AboveRoot(
                above_root_chance=above_root_chance, above_root_block=above_root_block
            )
            if above_root_block is not None or above_root_chance is not None
            else None
        )
        self._feature.set_mangrove_roots(
            _MangroveRoots(
                root_block=root_block,
                max_root_width=max_root_width,
                max_root_length=max_root_length,
                y_offset=y_offset,
                muddy_root_block=muddy_root_block,
                mud_block=mud_block,
                above_root=above,
                roots_may_grow_through=(
                    None
                    if roots_may_grow_through is None
                    else _blocks(roots_may_grow_through)
                ),
            )
        )
        return self

    def root_decoration(
        self,
        decoration_chance: float | tuple[int, int],
        decoration_block: str | Block | BlockDescriptor | None = None,
        num_steps: int | None = None,
        step_direction: Literal["down", "up", "out", "away"] | None = None,
    ) -> "TreeFeature":
        """Spreads blocks from the mangrove roots. Set the roots first.

        Args:
            decoration_chance (float | tuple[int, int]): The chance of a decoration: a
                number or a `(numerator, denominator)` fraction.
            decoration_block (str | Block | BlockDescriptor, optional): The block placed.
            num_steps (int, optional): How many blocks are placed.
            step_direction (Literal["down", "up", "out", "away"], optional): The direction
                the blocks spread in.

        Raises:
            ValueError: When the tree has no mangrove roots.
        """
        if self._feature.mangrove_roots is None:
            raise ValueError(f"Tree '{self.identifier}' has no mangrove roots.")
        self._feature.mangrove_roots.set_root_decoration(
            _decoration(decoration_chance, decoration_block, num_steps, step_direction)
        )
        return self


# endregion
