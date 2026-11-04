"""The `minecraft:snap_to_surface_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import BlockId, JsonObject, json_field


class _SnapToSurfaceFeature(_Feature):
    """The `minecraft:snap_to_surface_feature` body."""

    feature_to_snap: str = json_field()
    search_range: int = json_field()
    surface: Literal["ceiling", "floor", "random_horizontal", "wall"] | None = None
    allow_air_placement: bool | None = None
    allow_non_air_placement: bool | None = None
    allow_underwater_placement: bool | None = None
    allowed_surface_blocks: (
        list[Annotated[str | Block | BlockDescriptor, BlockId]] | None
    ) = None
    embed_in_surface: bool | None = None

    def set_allowed_surface_blocks(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> None:
        """Sets the blocks the feature may snap to."""
        self.allowed_surface_blocks = _blocks(blocks)


class _SnapToSurfaceFeatureFile(JsonObject):
    """The content of a snap to surface feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:snap_to_surface_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SnapToSurfaceFeature | None = json_field(
        key="minecraft:snap_to_surface_feature", default=None
    )

    def set_feature(self, feature: _SnapToSurfaceFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class SnapToSurfaceFeature(Feature):
    """Places a feature on the floor, the ceiling or a wall found within a range above or
    below its position. Fails if the surface is in another biome.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_snap_to_surface_feature)
    """

    _document = _SnapToSurfaceFeatureFile

    def __init__(
        self,
        name: str,
        feature_to_snap: "Feature | str",
        search_range: int,
        surface: Literal["ceiling", "floor", "random_horizontal", "wall"] = "floor",
        allow_air_placement: bool = True,
        allow_non_air_placement: bool = False,
        allow_underwater_placement: bool = False,
        allowed_surface_blocks: Sequence[str | Block | BlockDescriptor] | None = None,
        embed_in_surface: bool = False,
    ) -> None:
        """Creates a snap to surface feature.

        Args:
            name (str): The name of the feature, also its file name.
            feature_to_snap (Feature | str): The feature placed on the surface.
            search_range (int): How far a surface is searched for.
            surface (Literal["ceiling", "floor", "random_horizontal", "wall"], optional):
                The surface snapped to. Defaults to "floor".
            allow_air_placement (bool, optional): The search goes through air. Defaults to
                True.
            allow_non_air_placement (bool, optional): The search goes through blocks other
                than air and water, when it starts in one. Defaults to False.
            allow_underwater_placement (bool, optional): The search goes through water.
                Defaults to False.
            allowed_surface_blocks (Sequence[str | Block | BlockDescriptor], optional): The
                blocks it may snap to. Any block that supports the face when left out.
            embed_in_surface (bool, optional): Place the feature in the surface block rather
                than on it. Defaults to False.
        """
        super().__init__(name)
        self._content.set_feature(
            _SnapToSurfaceFeature(
                description=self._description(),
                feature_to_snap=str(feature_to_snap),
                search_range=search_range,
                surface=surface,
                allow_air_placement=allow_air_placement,
                allow_non_air_placement=allow_non_air_placement,
                allow_underwater_placement=allow_underwater_placement,
                embed_in_surface=embed_in_surface or None,
            )
        )
        if allowed_surface_blocks is not None:
            self.allowed_surface_blocks(allowed_surface_blocks)

    def allowed_surface_blocks(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "SnapToSurfaceFeature":
        """Sets the blocks the feature may snap to.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_allowed_surface_blocks(blocks)
        return self
