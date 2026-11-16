"""The `minecraft:crevasse_feature`."""

from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    ExactRangeMinMax,
    InRange,
    JsonObject,
    json_field,
)


class _CrevasseFeature(_Feature):
    """The `minecraft:crevasse_feature` body."""

    max_width: Annotated[int, InRange(2, 8)] | None = json_field(default=None)
    max_length: Annotated[int, InRange(4, 16)] | None = json_field(default=None)
    min_footprint: Annotated[int, InRange(1, 32)] | None = json_field(default=None)
    twistiness: Annotated[float, InRange(0.0, 16.0)] | None = json_field(default=None)
    carve_depth: (
        Annotated[int | tuple[int, int], InRange(4, 32), ExactRangeMinMax] | None
    ) = json_field(default=None)
    fill_depth: (
        Annotated[int | tuple[int, int], InRange(0, 32), ExactRangeMinMax] | None
    ) = json_field(default=None)
    surface_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = (
        json_field(default=None)
    )
    fill_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = json_field(
        default=None
    )


class _CrevasseFeatureFile(JsonObject):
    """The content of a crevasse feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:crevasse_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _CrevasseFeature | None = json_field(
        key="minecraft:crevasse_feature", default=None
    )

    def set_feature(self, feature: _CrevasseFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class CrevasseFeature(Feature[_CrevasseFeatureFile]):
    """[UNAVAILABLE] Carves a winding, tapered crevasse into an exposed terrain surface.

    The crevasse follows nearby terrain and extends in opposite directions from its
    placement position. Its width and depth taper toward both ends, and its lower portion
    can be filled to a consistent level. It succeeds when a suitable exposed surface and
    enough valid carve columns are found.

    Minecraft keeps this feature internal: it is not available for creator content yet, so
    using one always raises ValueError, with or without `features.experimental`.

    Example:
        >>> CrevasseFeature("ice_crevasse", carve_depth=(6, 10), fill_depth=(4, 6), surface_block="minecraft:ice", fill_block="minecraft:water")
    """

    def __init__(
        self,
        name: str,
        *,
        max_width: int | None = None,
        max_length: int | None = None,
        min_footprint: int | None = None,
        twistiness: float | None = None,
        carve_depth: int | tuple[int, int] | None = None,
        fill_depth: int | tuple[int, int] | None = None,
        surface_block: str | Block | BlockDescriptor | None = None,
        fill_block: str | Block | BlockDescriptor | None = None,
    ) -> None:
        """Creates a crevasse feature.

        Args:
            name (str): The name of the feature, also its file name.
            max_width (int, optional): The widest cross-section in blocks, from 2 to 8. Game default 4.
            max_length (int, optional): The longest end-to-end length in blocks, from 4 to 16. Game default 16.
            min_footprint (int, optional): The connected horizontal footprint needed before carving, from 1 to 32 blocks. Game default 10.
            twistiness (float, optional): How much the crevasse curves horizontally, from 0 to 16. Game default 4.
            carve_depth (int | tuple[int, int], optional): The carve depth below the terrain surface, or a `(min, max)` range, from 4 to 32 blocks. Game default (6, 10).
            fill_depth (int | tuple[int, int], optional): The fill depth below the terrain surface, or a `(min, max)` range, from 0 to 32 blocks. Game default (4, 6).
            surface_block (str | Block | BlockDescriptor, optional): The block placed over the opening. Omitted by default.
            fill_block (str | Block | BlockDescriptor, optional): The block placed at or below the fill depth. Omitted by default.

        It raises ValueError until Minecraft opens the feature to creators.
        """

        raise ValueError(
            "CrevasseFeature is unavailable: Minecraft keeps minecraft:crevasse_feature internal and does not allow it in creator content yet."
        )

        super().__init__(name)
        self._document.set_feature(
            _CrevasseFeature(
                description=self._description(),
                max_width=max_width,
                max_length=max_length,
                min_footprint=min_footprint,
                twistiness=twistiness,
                carve_depth=carve_depth,
                fill_depth=fill_depth,
                surface_block=surface_block,
                fill_block=fill_block,
            )
        )
