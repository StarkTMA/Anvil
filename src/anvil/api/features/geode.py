"""The `minecraft:geode_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    Chance,
    InRange,
    JsonObject,
    Length,
    NonNegative,
    json_field,
)


class _GeodeFeature(_Feature):
    """The `minecraft:geode_feature` body."""

    filler: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    inner_layer: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    alternate_inner_layer: Annotated[str | Block | BlockDescriptor, BlockId] = (
        json_field()
    )
    middle_layer: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    outer_layer: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    inner_placements: (
        Annotated[
            list[Annotated[str | Block | BlockDescriptor, BlockId]], Length(minimum=1)
        ]
        | None
    ) = None
    min_outer_wall_distance: Annotated[int, InRange(1, 10)] = json_field()
    max_outer_wall_distance: Annotated[int, InRange(1, 20)] = json_field()
    min_distribution_points: Annotated[int, InRange(1, 10)] = json_field()
    max_distribution_points: Annotated[int, InRange(1, 20)] = json_field()
    min_point_offset: Annotated[int, InRange(0, 10)] = json_field()
    max_point_offset: Annotated[int, InRange(0, 10)] = json_field()
    max_radius: int = json_field()
    crack_point_offset: Annotated[float, InRange(0, 10)] = json_field()
    generate_crack_chance: Annotated[float, Chance] = json_field()
    base_crack_size: Annotated[float, InRange(0, 5)] = json_field()
    noise_multiplier: float = json_field()
    use_potential_placements_chance: Annotated[float, Chance] = json_field()
    use_alternate_layer0_chance: Annotated[float, Chance] = json_field()
    placements_require_layer0_alternate: bool = json_field()
    invalid_blocks_threshold: Annotated[int, NonNegative] = json_field()

    def set_inner_placements(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> None:
        """Sets the blocks that may be placed on the inside of the geode."""
        self.inner_placements = _blocks(blocks)


class _GeodeFeatureFile(JsonObject):
    """The content of a geode feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:geode_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _GeodeFeature | None = json_field(
        key="minecraft:geode_feature", default=None
    )

    def set_feature(self, feature: _GeodeFeature) -> None:
        """Sets the body of the geode."""
        self.feature = feature


class GeodeFeature(Feature):
    """Places a rock formation like a geode: layers of shell around a filler, with
    optional blocks growing inside and a crack.

    - Succeeds if at least one block of the geode is placed.
    - Fails if every block fails to be placed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_geode_feature)
    """

    _document = _GeodeFeatureFile

    def __init__(
        self,
        name: str,
        *,
        filler: str | Block | BlockDescriptor,
        inner_layer: str | Block | BlockDescriptor,
        alternate_inner_layer: str | Block | BlockDescriptor,
        middle_layer: str | Block | BlockDescriptor,
        outer_layer: str | Block | BlockDescriptor,
        min_outer_wall_distance: int,
        max_outer_wall_distance: int,
        min_distribution_points: int,
        max_distribution_points: int,
        min_point_offset: int,
        max_point_offset: int,
        max_radius: int,
        crack_point_offset: float,
        generate_crack_chance: float,
        base_crack_size: float,
        noise_multiplier: float,
        use_potential_placements_chance: float,
        use_alternate_layer0_chance: float,
        placements_require_layer0_alternate: bool,
        invalid_blocks_threshold: int,
        inner_placements: Sequence[str | Block | BlockDescriptor] | None = None,
    ) -> None:
        """Creates a geode feature.

        Args:
            name (str): The name of the feature, also its file name.
            filler (str | Block | BlockDescriptor): The block inside the geode.
            inner_layer (str | Block | BlockDescriptor): The inside layer of the shell.
            alternate_inner_layer (str | Block | BlockDescriptor): The block that may
                replace a block of the inside layer.
            middle_layer (str | Block | BlockDescriptor): The middle layer of the shell.
            outer_layer (str | Block | BlockDescriptor): The outer layer of the shell.
            min_outer_wall_distance (int): The least distance from a distribution point to
                the outer wall, from 1 to 10.
            max_outer_wall_distance (int): The greatest distance from a distribution point
                to the outer wall, from 1 to 20.
            min_distribution_points (int): The fewest distribution points, from 1 to 10.
            max_distribution_points (int): The most distribution points, from 1 to 20.
            min_point_offset (int): The lowest random offset of a distribution point, from
                0 to 10.
            max_point_offset (int): The highest random offset of a distribution point, from
                0 to 10.
            max_radius (int): The largest radius of the geode.
            crack_point_offset (float): The offset of the points that form the crack, from
                0 to 10.
            generate_crack_chance (float): The chance the geode has a crack, from 0 to 1.
            base_crack_size (float): The size of the crack, from 0 to 5.
            noise_multiplier (float): How noisy the distribution points are.
            use_potential_placements_chance (float): The chance a block from
                `inner_placements` grows inside, from 0 to 1.
            use_alternate_layer0_chance (float): The chance a block of the inside layer is
                the alternate block, from 0 to 1.
            placements_require_layer0_alternate (bool): The inner placements only grow on
                the alternate blocks.
            invalid_blocks_threshold (int): How many invalid blocks around a distribution
                point stop the geode. At least 0.
            inner_placements (Sequence[str | Block | BlockDescriptor], optional): The
                blocks that may grow inside the geode.
        """
        super().__init__(name)
        self._content.set_feature(
            _GeodeFeature(
                description=self._description(),
                filler=filler,
                inner_layer=inner_layer,
                alternate_inner_layer=alternate_inner_layer,
                middle_layer=middle_layer,
                outer_layer=outer_layer,
                min_outer_wall_distance=min_outer_wall_distance,
                max_outer_wall_distance=max_outer_wall_distance,
                min_distribution_points=min_distribution_points,
                max_distribution_points=max_distribution_points,
                min_point_offset=min_point_offset,
                max_point_offset=max_point_offset,
                max_radius=max_radius,
                crack_point_offset=crack_point_offset,
                generate_crack_chance=generate_crack_chance,
                base_crack_size=base_crack_size,
                noise_multiplier=noise_multiplier,
                use_potential_placements_chance=use_potential_placements_chance,
                use_alternate_layer0_chance=use_alternate_layer0_chance,
                placements_require_layer0_alternate=placements_require_layer0_alternate,
                invalid_blocks_threshold=invalid_blocks_threshold,
            )
        )
        if inner_placements is not None:
            self.inner_placements(inner_placements)

    def inner_placements(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "GeodeFeature":
        """Sets the blocks that may grow inside the geode.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks. At least one.
        """
        self._feature.set_inner_placements(blocks)
        return self
