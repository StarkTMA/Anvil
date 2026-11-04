"""The `minecraft:structure_template_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    InRange,
    JsonObject,
    Kept,
    NonNegative,
    json_field,
)


class _BlockIntersection(JsonObject):
    """The `block_intersection` constraint of a structure template feature."""

    block_allowlist: list[Annotated[str | Block | BlockDescriptor, BlockId]] = (
        json_field()
    )
    only_check_intersection_for_motion_blocking_blocks: bool | None = None


class _Leveled(JsonObject):
    """The `leveled` constraint of a structure template feature."""

    max_steepness: Annotated[int, NonNegative] | None = None


class _StructureConstraints(JsonObject):
    """The `constraints` of a structure template feature."""

    grounded: Annotated[bool, Kept] | None = None
    unburied: Annotated[bool, Kept] | None = None
    leveled: Annotated[_Leveled, Kept] | None = None
    block_intersection: _BlockIntersection | None = None

    def set_grounded(self, grounded: bool = True) -> None:
        """Sets whether the ground level of the structure must touch the ground."""
        self.grounded = grounded

    def set_unburied(self, unburied: bool = True) -> None:
        """Sets whether the structure must have air above it."""
        self.unburied = unburied

    def set_leveled(self, max_steepness: int | None = None) -> None:
        """Requires mostly flat terrain under the ground level of the structure."""
        self.leveled = _Leveled(max_steepness=max_steepness)

    def set_block_intersection(
        self,
        blocks: Sequence[str | Block | BlockDescriptor],
        only_check_intersection_for_motion_blocking_blocks: bool | None = None,
    ) -> None:
        """Sets the only blocks the structure may intersect."""
        self.block_intersection = _BlockIntersection(
            block_allowlist=_blocks(blocks),
            only_check_intersection_for_motion_blocking_blocks=only_check_intersection_for_motion_blocking_blocks,
        )


class _StructureTemplateFeature(_Feature):
    """The `minecraft:structure_template_feature` body."""

    structure_name: str = json_field()
    adjustment_radius: Annotated[int, InRange(0, 16)] | None = None
    facing_direction: Literal["north", "south", "east", "west", "random"] | None = None
    ground_level: Annotated[int, NonNegative] | None = None
    rotate_around_center: bool | None = None
    constraints: _StructureConstraints = json_field(
        default_factory=_StructureConstraints
    )


class _StructureTemplateFeatureFile(JsonObject):
    """The content of a structure template feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:structure_template_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _StructureTemplateFeature | None = json_field(
        key="minecraft:structure_template_feature", default=None
    )

    def set_feature(self, feature: _StructureTemplateFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class StructureTemplateFeature(Feature):
    """Places a structure saved as a `.mcstructure` file in the `structures` folder of a
    behavior pack, any behavior pack.

    The constraints say where it may be placed. The feature searches the nearest position
    within `adjustment_radius` that satisfies them all, and places nothing when there is none.

    - Succeeds if the structure is placed.
    - Fails if it is not.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_structure_template_feature)
    """

    _document = _StructureTemplateFeatureFile

    def __init__(
        self,
        name: str,
        structure_name: str,
        adjustment_radius: int | None = None,
        facing_direction: (
            Literal["north", "south", "east", "west", "random"] | None
        ) = None,
        rotate_around_center: bool = False,
        ground_level: int | None = None,
    ) -> None:
        """Creates a structure template feature.

        Args:
            name (str): The name of the feature, also its file name.
            structure_name (str): The identifier of the structure.
            adjustment_radius (int, optional): How far the structure may move to find a
                valid position, from 0 to 16. Game default 0.
            facing_direction (Literal["north", "south", "east", "west", "random"], optional):
                The direction the structure faces. Game default "random".
            rotate_around_center (bool, optional): Rotate the structure around its centre
                rather than its corner. Defaults to False.
            ground_level (int, optional): The y of the structure's layer that is its ground
                level. Game default 0.
        """
        super().__init__(name)
        self._content.set_feature(
            _StructureTemplateFeature(
                description=self._description(),
                structure_name=str(structure_name),
                adjustment_radius=adjustment_radius,
                facing_direction=facing_direction,
                ground_level=ground_level,
                rotate_around_center=rotate_around_center or None,
            )
        )

    def grounded(self) -> "StructureTemplateFeature":
        """Requires the ground level of the structure to touch the ground."""
        self._feature.constraints.set_grounded()
        return self

    def unburied(self) -> "StructureTemplateFeature":
        """Requires air above the structure."""
        self._feature.constraints.set_unburied()
        return self

    def leveled(self, max_steepness: int | None = None) -> "StructureTemplateFeature":
        """Requires mostly flat terrain under the ground level of the structure.

        Args:
            max_steepness (int, optional): The greatest height difference between the
                position and the terrain halfway along each side. Game default 2.
        """
        self._feature.constraints.set_leveled(max_steepness)
        return self

    def block_allowlist(
        self,
        blocks: Sequence[str | Block | BlockDescriptor],
        only_check_intersection_for_motion_blocking_blocks: bool | None = None,
    ) -> "StructureTemplateFeature":
        """Requires the structure to intersect only these blocks.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
            only_check_intersection_for_motion_blocking_blocks (bool, optional): Only the
                structure's motion blocking blocks are checked, rather than all of its
                blocks but structure voids.
        """
        self._feature.constraints.set_block_intersection(
            blocks, only_check_intersection_for_motion_blocking_blocks
        )
        return self
