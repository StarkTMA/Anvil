"""The `minecraft:vegetation_patch_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    Chance,
    ExactRangeMinMax,
    JsonObject,
    NonNegative,
    json_field,
)


class _VegetationPatchFeature(_Feature):
    """The `minecraft:vegetation_patch_feature` body."""

    replaceable_blocks: (
        list[Annotated[str | Block | BlockDescriptor, BlockId]] | None
    ) = None
    ground_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    vegetation_feature: str = json_field()
    surface: Literal["floor", "ceiling"] | None = None
    depth: Annotated[float | tuple[float, float], ExactRangeMinMax] = json_field()
    extra_deep_block_chance: Annotated[float, Chance] | None = None
    vertical_range: int = json_field()
    vegetation_chance: Annotated[float, Chance] | None = None
    horizontal_radius: Annotated[float | tuple[float, float], ExactRangeMinMax] = (
        json_field()
    )
    extra_edge_column_chance: Annotated[float, NonNegative] | None = None
    waterlogged: bool | None = None

    def set_replaceable_blocks(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> None:
        """Sets the blocks the ground block may replace."""
        self.replaceable_blocks = _blocks(blocks)


class _VegetationPatchFeatureFile(JsonObject):
    """The content of a vegetation patch feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:vegetation_patch_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _VegetationPatchFeature | None = json_field(
        key="minecraft:vegetation_patch_feature", default=None
    )

    def set_feature(self, feature: _VegetationPatchFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class VegetationPatchFeature(Feature[_VegetationPatchFeatureFile]):
    """Places a patch of ground blocks and a vegetation feature on it, such as moss.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_vegetation_patch_feature)
    """

    def __init__(
        self,
        name: str,
        ground_block: str | Block | BlockDescriptor,
        vegetation_feature: "Feature | str",
        depth: float | tuple[float, float],
        vertical_range: int,
        horizontal_radius: float | tuple[float, float],
        surface: Literal["floor", "ceiling"] = "floor",
        extra_deep_block_chance: float | None = None,
        vegetation_chance: float | None = None,
        extra_edge_column_chance: float | None = None,
        waterlogged: bool = False,
    ) -> None:
        """Creates a vegetation patch feature.

        Args:
            name (str): The name of the feature, also its file name.
            ground_block (str | Block | BlockDescriptor): The block the patch is made of.
            vegetation_feature (Feature | str): The feature placed on the patch.
            depth (float | tuple[float, float]): How deep the ground blocks go, or a range
                it is picked from.
            vertical_range (int): How far up or down a surface is searched for.
            horizontal_radius (float | tuple[float, float]): The radius of the patch, or a
                range it is picked from.
            surface (Literal["floor", "ceiling"], optional): Whether the patch grows on the
                floor or the ceiling. Defaults to "floor".
            extra_deep_block_chance (float, optional): The chance the ground goes one block
                deeper, from 0 to 1.
            vegetation_chance (float, optional): The chance vegetation is placed on a
                ground block, from 0 to 1.
            extra_edge_column_chance (float, optional): The chance vegetation is placed on
                the edge of the patch. At least 0.
            waterlogged (bool, optional): Waterlog the positions of the ground blocks.
                Defaults to False.
        """
        super().__init__(name)
        self._document.set_feature(
            _VegetationPatchFeature(
                description=self._description(),
                ground_block=ground_block,
                vegetation_feature=str(vegetation_feature),
                surface=surface,
                depth=depth,
                vertical_range=vertical_range,
                horizontal_radius=horizontal_radius,
                waterlogged=waterlogged,
                extra_deep_block_chance=extra_deep_block_chance,
                vegetation_chance=vegetation_chance,
                extra_edge_column_chance=extra_edge_column_chance,
            )
        )

    def replaceable_blocks(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "VegetationPatchFeature":
        """Sets the blocks the ground blocks may replace.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_replaceable_blocks(blocks)
        return self
