import os
from collections.abc import Sequence
from dataclasses import dataclass
from math import inf
from typing import Any, Literal, overload

from anvil.api.core.enums import BlockFaceValues
from anvil.api.core.types import Identifier, Vector3DInt
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilFormatter, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftBlockDescriptor


@dataclass
class CoordinateRange:
    distribution: str
    extent: tuple[int, int]
    grid_offset: int | None = None
    step_size: int | None = None

    @overload
    def __init__(
        self,
        distribution: Literal["uniform", "gaussian", "inverse_gaussian", "triangle"],
        extent: tuple[int, int],
    ): ...

    @overload
    def __init__(
        self,
        distribution: Literal["fixed_grid", "jittered_grid"],
        extent: tuple[int, int],
        grid_offset: int | None = None,
        step_size: int | None = None,
    ): ...

    def __init__(
        self,
        distribution: str,
        extent: tuple[int, int],
        grid_offset: int | None = None,
        step_size: int | None = None,
    ):
        if distribution not in {
            "uniform",
            "gaussian",
            "inverse_gaussian",
            "triangle",
            "fixed_grid",
            "jittered_grid",
        }:
            raise ValueError("Invalid distribution type for CoordinateRange")

        if distribution not in {"fixed_grid", "jittered_grid"} and (
            grid_offset is not None or step_size is not None
        ):
            raise ValueError(
                "grid_offset and step_size should not be provided for non-grid distributions"
            )

        if len(extent) != 2:
            raise ValueError("extent must contain exactly 2 values")

        self.distribution = distribution
        self.extent = extent
        self.grid_offset = grid_offset
        self.step_size = step_size

    def _get_coordinate_range_dict(self) -> dict[str, Any]:
        range_dict = {
            "distribution": self.distribution,
            "extent": self.extent,
        }
        if self.distribution in {"fixed_grid", "jittered_grid"}:
            if self.grid_offset is not None:
                range_dict["grid_offset"] = self.grid_offset
            if self.step_size is not None:
                range_dict["step_size"] = self.step_size

        return range_dict


class DistributionMixin:
    def _distribution_target(self) -> dict[str, Any]:
        raise NotImplementedError()

    def distribution(
        self,
        iteration: int | Molang,
        scatter_chance: float | tuple[int, int],
        x: int | Molang | CoordinateRange,
        y: int | Molang | CoordinateRange,
        z: int | Molang | CoordinateRange,
        coordinate_eval_order: Literal["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"],
    ):
        if coordinate_eval_order not in {"xyz", "xzy", "yxz", "yzx", "zxy", "zyx"}:
            raise ValueError(
                "coordinate_eval_order must be one of 'xyz', 'xzy', 'yxz', 'yzx', 'zxy', or 'zyx'"
            )

        if isinstance(scatter_chance, tuple):
            if len(scatter_chance) != 2:
                raise ValueError("scatter_chance tuple must have exactly 2 elements")
            if scatter_chance[1] <= 0:
                raise ValueError("scatter_chance denominator must be greater than 0")
            scatter_chance = {
                "numerator": scatter_chance[0],
                "denominator": scatter_chance[1],
            }

        distribution = {
            "iterations": iteration,
            "scatter_chance": scatter_chance,
            "coordinate_eval_order": coordinate_eval_order,
            "x": (
                x._get_coordinate_range_dict() if isinstance(x, CoordinateRange) else x
            ),
            "y": (
                y._get_coordinate_range_dict() if isinstance(y, CoordinateRange) else y
            ),
            "z": (
                z._get_coordinate_range_dict() if isinstance(z, CoordinateRange) else z
            ),
        }

        self._distribution_target()["distribution"] = distribution
        return self


class Feature(AddonObject):
    """Base class for Bedrock worldgen feature definitions."""

    _object_type = "Feature"
    _extension = ".json"
    _template_name = "feature_base"
    _path = os.path.join(
        CONFIG.BP_PATH,
        "features",
    )

    def __init__(self, name) -> None:
        """Initializes the base feature definition content.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
        """
        super().__init__(name, False)
        self.content(JsonSchemes.worldgen_feature(self._template_name, self.identifier))

    def queue(self) -> "Feature":
        """Queues the feature definition for export."""
        return super().queue()


class AggregateFeature(Feature):
    """Places a collection of features in an arbitrary order. All features in the collection use the same input position. Features should not depend on each other, as there is no guarantee in which order the features will be placed.
    - Succeeds if At least one feature is placed successfully.
    - Fails if All features fail to be placed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftaggregate_feature)
    """

    _template_name = "feature_aggregate"
    _feature_name = "minecraft:aggregate_feature"

    def __init__(self, name) -> None:
        """Places a collection of features in an arbitrary order.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftaggregate_feature)
        """
        super().__init__(name)

    def features(self, feature_list: list[Feature | Identifier]) -> "AggregateFeature":
        """Sets the collection of features to be placed one by one.

        No guarantee of order. All features use the same input position.
        """
        self._content[self._feature_name].setdefault("features", []).extend(
            [str(feature) for feature in feature_list]
        )
        return self

    def early_out(
        self, early_out: Literal["none", "first_failure", "first_success"]
    ) -> "AggregateFeature":
        """Do not continue placing features once either the first success or first failure has occurred."""
        self._content[self._feature_name]["early_out"] = early_out
        return self


class CaveCarverFeature(Feature):
    """Carves caves through the world during pregeneration.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftcave_carver_feature)
    """

    _template_name = "feature_cave_carver"
    _feature_name = "minecraft:cave_carver_feature"

    def __init__(
        self,
        name,
        fill_with: MinecraftBlockDescriptor | Identifier | None = None,
        width_modifier: Molang | float | int | None = None,
        skip_carve_chance: int | None = None,
        height_limit: int | None = None,
        y_scale: float | tuple[float, float] | None = None,
        horizontal_radius_multiplier: float | tuple[float, float] | None = None,
        vertical_radius_multiplier: float | tuple[float, float] | None = None,
        floor_level: float | tuple[float, float] | None = None,
    ) -> None:
        """Carves caves through the world during pregeneration.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            fill_with (MinecraftBlockDescriptor | Identifier | None): Reference
                to the block to fill the cave with.
            width_modifier (Molang | float | int | None): How many blocks to
                increase the cave radius by, from the center point of the cave.
            skip_carve_chance (int | None): The chance to skip doing the carve
                (1 / value).
            height_limit (int | None): The height limit where we attempt to
                carve.
            y_scale (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                The scaling in y.
            horizontal_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Horizontal radius multiplier.
            vertical_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Vertical radius multiplier.
            floor_level (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Floor Level.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftcave_carver_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]

        if fill_with is not None:
            feature_content["fill_with"] = fill_with

        if width_modifier is not None:
            feature_content["width_modifier"] = str(width_modifier)

        if skip_carve_chance is not None:
            feature_content["skip_carve_chance"] = clamp(skip_carve_chance, 1, inf)

        if height_limit is not None:
            feature_content["height_limit"] = height_limit

        if y_scale is not None:
            feature_content["y_scale"] = AnvilFormatter.range_min_max_dict(y_scale)

        if horizontal_radius_multiplier is not None:
            feature_content["horizontal_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(horizontal_radius_multiplier)
            )

        if vertical_radius_multiplier is not None:
            feature_content["vertical_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(vertical_radius_multiplier)
            )

        if floor_level is not None:
            feature_content["floor_level"] = AnvilFormatter.range_min_max_dict(
                floor_level
            )


class FossilFeature(Feature):
    """Generates a fossil structure with a configurable ore block.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftfossil_feature)
    """

    _template_name = "feature_fossil"
    _feature_name = "minecraft:fossil_feature"

    def __init__(
        self,
        name,
        ore_block: MinecraftBlockDescriptor | Identifier,
        max_empty_corners: int,
    ) -> None:
        """Generates a fossil structure with a configurable ore block.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            ore_block (MinecraftBlockDescriptor | Identifier): Ore block used by
                the fossil feature.
            max_empty_corners (int): Maximum number of empty corners allowed.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftfossil_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["ore_block"] = ore_block
        feature_content["max_empty_corners"] = clamp(max_empty_corners, 0, inf)


class GeodeFeature(Feature):
    """Generates a geode with configurable shell layers, point distribution, and crack behavior.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftgeode_feature)
    """

    _template_name = "feature_geode"
    _feature_name = "minecraft:geode_feature"

    def __init__(
        self,
        name,
        *,
        filler: MinecraftBlockDescriptor | Identifier,
        inner_layer: MinecraftBlockDescriptor | Identifier,
        alternate_inner_layer: MinecraftBlockDescriptor | Identifier,
        middle_layer: MinecraftBlockDescriptor | Identifier,
        outer_layer: MinecraftBlockDescriptor | Identifier,
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
        inner_placements: list[MinecraftBlockDescriptor | Identifier] | None = None,
    ) -> None:
        """Generates a geode with configurable shell layers, point distribution, and crack behavior.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            filler (MinecraftBlockDescriptor | Identifier): The block to fill
                the inside of the geode.
            inner_layer (MinecraftBlockDescriptor | Identifier): The block that
                forms the inside layer of the geode shell.
            alternate_inner_layer (MinecraftBlockDescriptor | Identifier): The
                block that has a chance of generating instead of inner_layer.
            middle_layer (MinecraftBlockDescriptor | Identifier): The block
                that forms the middle layer of the geode shell.
            outer_layer (MinecraftBlockDescriptor | Identifier): The block that
                forms the outer shell of the geode.
            min_outer_wall_distance (int): The minimum distance each
                distribution point must be from the outer wall.
            max_outer_wall_distance (int): The maximum distance each
                distribution point can be from the outer wall.
            min_distribution_points (int): The minimum number of points inside
                the distance field that can get generated.
            max_distribution_points (int): The maximum number of points inside
                the distance field that can get generated.
            min_point_offset (int): The lowest possible value of random offset
                applied to the position of each distribution point.
            max_point_offset (int): The highest possible value of random offset
                applied to the position of each distribution point.
            max_radius (int): The maximum possible radius of the geode
                generated.
            crack_point_offset (float): An offset applied to each distribution
                point that forms the geode crack opening.
            generate_crack_chance (float): The likelihood of a geode generating
                with a crack in its shell.
            base_crack_size (float): How large the crack opening of the geode
                should be when generated.
            noise_multiplier (float): A multiplier applied to the noise that is
                applied to the distribution points within the geode. Higher =
                more noisy.
            use_potential_placements_chance (float): The likelihood that a
                special block will be placed on the inside of the geode.
            use_alternate_layer0_chance (float): The likelihood that a block in
                the innermost layer of the geode will be replaced with an
                alternate option.
            placements_require_layer0_alternate (bool): If true, the potential
                placement block will only be placed on the alternate layer0
                blocks that get placed.
            invalid_blocks_threshold (int): The threshold of invalid blocks for
                a geode to have a distribution point in before it aborts
                generation entirely.
            inner_placements (list[MinecraftBlockDescriptor | Identifier] | None):
                A list of blocks that may be replaced during placement. Omit
                this field to allow any block to be replaced.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftgeode_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["filler"] = filler
        feature_content["inner_layer"] = inner_layer
        feature_content["alternate_inner_layer"] = alternate_inner_layer
        feature_content["middle_layer"] = middle_layer
        feature_content["outer_layer"] = outer_layer
        feature_content["min_outer_wall_distance"] = clamp(
            min_outer_wall_distance, 1, 10
        )
        feature_content["max_outer_wall_distance"] = clamp(
            max_outer_wall_distance, 1, 20
        )
        feature_content["min_distribution_points"] = clamp(
            min_distribution_points, 1, 10
        )
        feature_content["max_distribution_points"] = clamp(
            max_distribution_points, 1, 20
        )
        feature_content["min_point_offset"] = clamp(min_point_offset, 0, 10)
        feature_content["max_point_offset"] = clamp(max_point_offset, 0, 10)
        feature_content["max_radius"] = clamp(max_radius, 0, inf)
        feature_content["crack_point_offset"] = clamp(crack_point_offset, 0.0, 10.0)
        feature_content["generate_crack_chance"] = clamp(
            generate_crack_chance, 0.0, 1.0
        )
        feature_content["base_crack_size"] = clamp(base_crack_size, 0.0, 5.0)
        feature_content["noise_multiplier"] = noise_multiplier
        feature_content["use_potential_placements_chance"] = clamp(
            use_potential_placements_chance, 0.0, 1.0
        )
        feature_content["use_alternate_layer0_chance"] = clamp(
            use_alternate_layer0_chance, 0.0, 1.0
        )
        feature_content["placements_require_layer0_alternate"] = (
            placements_require_layer0_alternate
        )
        feature_content["invalid_blocks_threshold"] = clamp(
            invalid_blocks_threshold, 0, inf
        )

        if inner_placements is not None:
            self.inner_placements(inner_placements)

    def inner_placements(self, blocks: list[MinecraftBlockDescriptor | Identifier]):
        """Sets a list of blocks that may be replaced during placement.

        Omit this field to allow any block to be replaced.
        """
        self._content[self._feature_name]["inner_placements"] = list(blocks)


class GrowingPlantFeature(Feature):
    """Places a growing plant column with weighted height, body, and head blocks.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftgrowing_plant_feature)
    """

    _template_name = "feature_growing_plant"
    _feature_name = "minecraft:growing_plant_feature"

    def __init__(
        self,
        name,
        growth_direction: Literal["UP", "DOWN"],
        age: float | tuple[float, float] | None = None,
        allow_water: bool = False,
    ) -> None:
        """Places a growing plant in the world.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            growth_direction (Literal["UP", "DOWN"]): Direction that the plant grows
                towards.
            age (int | tuple[int, int] | list[int] | Mapping[str, int] | None):
                Age of the head of the plant.
            allow_water (bool): Plant blocks can be placed in water.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftgrowing_plant_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["growth_direction"] = growth_direction
        feature_content["allow_water"] = allow_water

        if age is not None:
            self.age(age)

    def add_height(
        self,
        height: float | tuple[float, float],
        weight: float = 1.0,
    ):
        """Adds a height_distribution entry with plant height and weight used in random selection."""
        self._content[self._feature_name].setdefault("height_distribution", []).append(
            [
                AnvilFormatter.range_min_max_dict(height),
                clamp(weight, 0, inf),
            ]
        )

    def height_distribution(
        self,
        heights: list[tuple[float | tuple[float, float], float]],
    ):
        """Adds multiple height_distribution entries with plant height and weight values."""
        for height, weight in heights:
            self.add_height(height, weight)

    def age(self, age: float | tuple[float, float]):
        """Sets the age of the head of the plant."""
        self._content[self._feature_name]["age"] = AnvilFormatter.range_min_max_dict(
            age
        )

    def add_body_block(
        self, block: MinecraftBlockDescriptor | Identifier, weight: float = 1.0
    ):
        """Adds a body_blocks entry with a plant body block and weight."""
        self._content[self._feature_name].setdefault("body_blocks", []).append(
            [block, clamp(weight, 0, inf)]
        )

    def body_blocks(
        self, blocks: list[tuple[MinecraftBlockDescriptor | Identifier, float]]
    ):
        """Adds multiple body_blocks entries with plant body blocks and weights."""
        for block, weight in blocks:
            self.add_body_block(block, weight)

    def add_head_block(
        self, block: MinecraftBlockDescriptor | Identifier, weight: float = 1.0
    ):
        """Adds a head_blocks entry with a plant head block and weight."""
        self._content[self._feature_name].setdefault("head_blocks", []).append(
            [block, clamp(weight, 0, inf)]
        )

    def head_blocks(
        self, blocks: list[tuple[MinecraftBlockDescriptor | Identifier, float]]
    ):
        """Adds multiple head_blocks entries with plant head blocks and weights."""
        for block, weight in blocks:
            self.add_head_block(block, weight)


class MultifaceFeature(Feature):
    """Places multiface blocks on floors, walls, and ceilings.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftmultiface_feature)
    """

    _template_name = "feature_multiface"
    _feature_name = "minecraft:multiface_feature"

    def __init__(
        self,
        name,
        places_block: MinecraftBlockDescriptor | Identifier,
        search_range: int,
        can_place_on_floor: bool,
        can_place_on_ceiling: bool,
        can_place_on_wall: bool,
        chance_of_spreading: float,
        can_place_on: list[MinecraftBlockDescriptor | Identifier] | None = None,
    ) -> None:
        """Places one or a few multiface blocks on floors, walls, and ceilings.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            places_block (MinecraftBlockDescriptor | Identifier): Reference to
                the block to be placed.
            search_range (int): How far, in blocks, this feature can search for
                a valid position to place.
            can_place_on_floor (bool): Whether placement on floors is allowed.
            can_place_on_ceiling (bool): Whether placement on ceilings is
                allowed.
            can_place_on_wall (bool): Whether placement on walls is allowed.
            chance_of_spreading (float): For each block placed by this feature,
                how likely that block is to spread to another.
            can_place_on (list[MinecraftBlockDescriptor | Identifier] | None):
                Optional block reference array limiting valid support blocks.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftmultiface_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["places_block"] = places_block
        feature_content["search_range"] = clamp(search_range, 1, 64)
        feature_content["can_place_on_floor"] = can_place_on_floor
        feature_content["can_place_on_ceiling"] = can_place_on_ceiling
        feature_content["can_place_on_wall"] = can_place_on_wall
        feature_content["chance_of_spreading"] = clamp(chance_of_spreading, 0.0, 1.0)

        if can_place_on is not None:
            self.can_place_on(can_place_on)

    def can_place_on(self, blocks: list[MinecraftBlockDescriptor | Identifier]):
        """Sets the can_place_on block reference array."""
        self._content[self._feature_name]["can_place_on"] = list(blocks)


class MultiBlockFeature(Feature):
    """Places a multi-block in the world as a biome decoration feature.

    A multi-block must be defined with the ``minecraft:multi_block`` trait.
    The required ``places_block`` field must reference the first part of a
    multi-block (i.e. its ``minecraft:multi_block_part`` state must equal 0).

    - The optional ``may_replace`` allowlist specifies which blocks each part
      of the multi-block may replace. If omitted, multi-block parts can be
      placed anywhere except on top of other multi-block parts.
    - The optional ``randomize_rotation`` field randomizes the multi-block's
      cardinal orientation. Requires the block to have a cardinal direction
      state.
    - The optional ``enforce_placement_rules`` field checks whether each part
      of the multi-block may be placed on top of existing blocks, optionally
      consulting the block's ``minecraft:placement_filter`` component.

    Note:
        Requires ``format_version`` of at least ``1.26.50``.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_multi_block_feature)
    """

    _template_name = "feature_multi_block"
    _feature_name = "minecraft:multi_block_feature"

    def __init__(
        self,
        name: str,
        places_block: MinecraftBlockDescriptor | Identifier,
        randomize_rotation: bool = False,
        enforce_placement_rules: bool = False,
    ) -> None:
        """Places a multi-block in the world as a biome decoration feature.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            places_block (MinecraftBlockDescriptor | Identifier): Reference to the multi-block to be
                placed. Must be the identifier of the first part of a
                multi-block (``minecraft:multi_block_part`` state == 0).
            randomize_rotation (bool): If True, randomizes the multi-block's
                cardinal orientation. The multi-block must have a cardinal
                direction state.
            enforce_placement_rules (bool): If True, checks each part of the
                multi-block against the block's canPlace rules, optionally
                including its ``minecraft:placement_filter`` component.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_multi_block_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["places_block"] = str(places_block)

        if randomize_rotation:
            feature_content["randomize_rotation"] = randomize_rotation

        if enforce_placement_rules:
            feature_content["enforce_placement_rules"] = enforce_placement_rules

    def may_replace(self, blocks: "list[MinecraftBlockDescriptor | Identifier]"):
        """Sets the may_replace allowlist.

        Specifies which blocks each part of the multi-block may replace.
        Other multi-blocks can never be replaced regardless of this list.

        Parameters:
            blocks (list[MinecraftBlockDescriptor | Identifier]): List of
                blocks that the multi-block parts are allowed to replace.
        """
        self._content[self._feature_name]["may_replace"] = list(blocks)


class NetherCaveCarverFeature(Feature):
    """Carves cave systems through the Nether using the cave carver schema.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftnether_cave_carver_feature)
    """

    _template_name = "feature_nether_cave_carver"
    _feature_name = "minecraft:nether_cave_carver_feature"

    def __init__(
        self,
        name,
        fill_with: MinecraftBlockDescriptor | Identifier | None = None,
        width_modifier: Molang | float | int | None = None,
        skip_carve_chance: int | None = None,
        height_limit: int | None = None,
        y_scale: float | tuple[float, float] | None = None,
        horizontal_radius_multiplier: float | tuple[float, float] | None = None,
        vertical_radius_multiplier: float | tuple[float, float] | None = None,
        floor_level: float | tuple[float, float] | None = None,
    ) -> None:
        """Carves cave systems through the Nether.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            fill_with (MinecraftBlockDescriptor | Identifier | None): Reference
                to the block to fill the cave with.
            width_modifier (Molang | float | int | None): How many blocks to
                increase the cave radius by, from the center point of the cave.
            skip_carve_chance (int | None): The chance to skip doing the carve
                (1 / value).
            height_limit (int | None): The height limit where we attempt to
                carve.
            y_scale (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                The scaling in y.
            horizontal_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Horizontal radius multiplier.
            vertical_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Vertical radius multiplier.
            floor_level (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Floor Level.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftnether_cave_carver_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]

        if fill_with is not None:
            feature_content["fill_with"] = fill_with

        if width_modifier is not None:
            feature_content["width_modifier"] = str(width_modifier)

        if skip_carve_chance is not None:
            feature_content["skip_carve_chance"] = clamp(skip_carve_chance, 1, inf)

        if height_limit is not None:
            feature_content["height_limit"] = height_limit

        if y_scale is not None:
            feature_content["y_scale"] = AnvilFormatter.range_min_max_dict(y_scale)

        if horizontal_radius_multiplier is not None:
            feature_content["horizontal_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(horizontal_radius_multiplier)
            )

        if vertical_radius_multiplier is not None:
            feature_content["vertical_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(vertical_radius_multiplier)
            )

        if floor_level is not None:
            feature_content["floor_level"] = AnvilFormatter.range_min_max_dict(
                floor_level
            )


class OreFeature(Feature):
    """Places a vein of blocks using ordered replacement rules.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftore_feature)
    """

    _template_name = "feature_ore"
    _feature_name = "minecraft:ore_feature"

    def __init__(
        self,
        name,
        count: int,
        discard_chance_on_air_exposure: float | None = None,
    ) -> None:
        """Places a vein of blocks to simulate ore deposits.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            count (int): The number of blocks to be placed.
            discard_chance_on_air_exposure (float | None): Optional discard
                chance applied when ore is exposed to air.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftore_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["count"] = clamp(count, 1, inf)

        if discard_chance_on_air_exposure is not None:
            feature_content["discard_chance_on_air_exposure"] = clamp(
                discard_chance_on_air_exposure, 0.0, 1.0
            )

    def add_replace_rule(
        self,
        places_block: MinecraftBlockDescriptor | Identifier,
        may_replace: list[MinecraftBlockDescriptor | Identifier] | None = None,
    ):
        """Adds a replace_rules entry with places_block and an optional may_replace array."""
        rule = {"places_block": places_block}
        if may_replace is not None:
            rule["may_replace"] = may_replace

        self._content[self._feature_name].setdefault("replace_rules", []).append(rule)


class PartiallyExposedBlobFeature(Feature):
    """Generates a blob where one face may remain exposed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftpartially_exposed_blob_feature)
    """

    _template_name = "feature_partially_exposed_blob"
    _feature_name = "minecraft:partially_exposed_blob_feature"

    def __init__(
        self,
        name,
        places_block: MinecraftBlockDescriptor | Identifier,
        placement_radius_around_floor: int,
        placement_probability_per_valid_position: float,
        exposed_face: BlockFaceValues | None = BlockFaceValues.Up,
    ) -> None:
        """Generates a blob where one face may remain exposed.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            places_block (MinecraftBlockDescriptor | Identifier): Block placed
                by the blob feature.
            placement_radius_around_floor (int): Radius around the floor used
                for placement.
            placement_probability_per_valid_position (float): Probability per
                valid position.
            exposed_face (BlockFaceValues | None): Defines a block face allowed to
                be exposed.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftpartially_exposed_blob_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["places_block"] = places_block
        feature_content["placement_radius_around_floor"] = clamp(
            placement_radius_around_floor, 1, 8
        )
        feature_content["placement_probability_per_valid_position"] = clamp(
            placement_probability_per_valid_position, 0.0, 1.0
        )

        if exposed_face is not None:
            feature_content["exposed_face"] = str(exposed_face)


class ScatterFeature(Feature, DistributionMixin):
    """Places a referenced feature using scatter distribution parameters.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftscatter_feature)
    """

    _template_name = "feature_scatter"
    _feature_name = "minecraft:scatter_feature"

    def __init__(
        self,
        name,
        places_feature: Feature | Identifier,
        project_input_to_floor: bool = False,
    ) -> None:
        """Scatters a feature throughout a chunk.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            places_feature (Feature | Identifier): Named reference to the feature
                being scattered.
            project_input_to_floor (bool): Whether the input position should be
                projected to the floor before placement.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftscatter_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["places_feature"] = str(places_feature)
        feature_content["project_input_to_floor"] = project_input_to_floor

    def _distribution_target(self) -> dict[str, Any]:
        return self._content[self._feature_name]


class SearchFeature(Feature):
    """Searches a volume along an axis for valid positions before placing another feature.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsearch_feature)
    """

    _template_name = "feature_search"
    _feature_name = "minecraft:search_feature"

    def __init__(
        self,
        name,
        places_feature: Feature | Identifier,
        search_axis: Literal["-x", "+x", "-y", "+y", "-z", "+z"],
        min_position: Sequence[int],
        max_position: Sequence[int],
        required_successes: int = None,
    ) -> None:
        """Sweeps a volume searching for a valid placement location for its referenced feature.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            places_feature (Feature | Identifier): Named reference to the feature
                placed after a successful search.
            search_axis (Literal["-x", "+x", "-y", "+y", "-z", "+z"]): Axis used to sweep the search volume.
            min_position (Sequence[int]): Minimum coordinates of the
                search_volume object.
            max_position (Sequence[int]): Maximum coordinates of the
                search_volume object.
            required_successes (int | None): Optional number of successful
                placements required.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsearch_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["places_feature"] = str(places_feature)
        feature_content["search_axis"] = search_axis
        self.search_volume(min_position, max_position)
        if required_successes is not None:
            feature_content["required_successes"] = clamp(required_successes, 1, inf)

    def search_volume(self, min_position: Vector3DInt, max_position: Vector3DInt):
        """Sets the search_volume object with min and max coordinates."""
        if len(min_position) != 3:
            raise ValueError("min_position must contain exactly 3 coordinates.")
        if len(max_position) != 3:
            raise ValueError("max_position must contain exactly 3 coordinates.")

        self._content[self._feature_name]["search_volume"] = {
            "min": list(min_position),
            "max": list(max_position),
        }

    def _distribution_target(self) -> dict[str, Any]:
        return self._content[self._feature_name]


class SculkPatchFeature(Feature):
    """Places a sculk patch with cursor spread settings and an optional central block.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsculk_patch_feature)
    """

    _template_name = "feature_sculk_patch"
    _feature_name = "minecraft:sculk_patch_feature"

    def __init__(
        self,
        name,
        can_place_sculk_patch_on: list[MinecraftBlockDescriptor | Identifier],
        cursor_count: int,
        charge_amount: int,
        spread_attempts: int,
        growth_rounds: int,
        spread_rounds: int,
        central_block: MinecraftBlockDescriptor | Identifier | None = None,
        central_block_placement_chance: float | None = None,
        extra_growth_chance: float | tuple[float, float] | None = None,
    ) -> None:
        """Places a sculk patch with cursor spread settings and an optional central block.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            can_place_sculk_patch_on (list[MinecraftBlockDescriptor | Identifier]):
                Blocks that the sculk patch can be placed on.
            cursor_count (int): Number of cursors used during spread.
            charge_amount (int): Amount of charge assigned to the patch.
            spread_attempts (int): Number of spread attempts to perform.
            growth_rounds (int): Number of growth rounds to perform.
            spread_rounds (int): Number of spread rounds to perform.
            central_block (MinecraftBlockDescriptor | Identifier | None):
                Optional central block placed with the patch.
            central_block_placement_chance (float | None): Optional chance to
                place the central block.
            extra_growth_chance (int | tuple[int, int] | list[int] | Mapping[str, int] | None):
                Optional extra growth chance value or range.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsculk_patch_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["can_place_sculk_patch_on"] = list(can_place_sculk_patch_on)
        feature_content["cursor_count"] = clamp(cursor_count, 0, 32)
        feature_content["charge_amount"] = clamp(charge_amount, 1, 1000)
        feature_content["spread_attempts"] = clamp(spread_attempts, 1, 64)
        feature_content["growth_rounds"] = clamp(growth_rounds, 0, 8)
        feature_content["spread_rounds"] = clamp(spread_rounds, 0, 8)

        if central_block is not None:
            feature_content["central_block"] = central_block

        if central_block_placement_chance is not None:
            feature_content["central_block_placement_chance"] = clamp(
                central_block_placement_chance, 0.0, 1.0
            )

        if extra_growth_chance is not None:
            feature_content["extra_growth_chance"] = AnvilFormatter.range_min_max_dict(
                extra_growth_chance
            )

    def can_place_sculk_patch_on(
        self, blocks: list[MinecraftBlockDescriptor | Identifier]
    ):
        """Sets the can_place_sculk_patch_on block reference array."""
        self._content[self._feature_name]["can_place_sculk_patch_on"] = list(blocks)

    def central_block(
        self,
        block: MinecraftBlockDescriptor | Identifier,
        placement_chance: float | None = None,
    ):
        """Sets the optional central_block and central_block_placement_chance values."""
        feature_content = self._content[self._feature_name]
        feature_content["central_block"] = block
        if placement_chance is not None:
            feature_content["central_block_placement_chance"] = clamp(
                placement_chance, 0.0, 1.0
            )


class SequenceFeature(Feature):
    """Places a collection of features sequentially, in the order they are defined.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsequence_feature)
    """

    _template_name = "feature_sequence"
    _feature_name = "minecraft:sequence_feature"

    def features(self, feature_list: list[Feature | Identifier]) -> "SequenceFeature":
        """Sets the ordered feature_reference array for the sequence."""
        self._content[self._feature_name].setdefault("features", []).extend(
            [str(feature) for feature in feature_list]
        )
        return self


class SingleBlockFeature(Feature):
    """Places a single block in the world. The places_block field supports a
    single block or a list of weighted blocks, where the weight defines how
    likely it is for that block to be selected. The may_attach_to and may_replace
    fields are allowlists which specify where the block can be placed.
    If these fields are omitted, the block can be placed anywhere.
    The may_not_attach_to field is a denylist that specifies what blocks can't be
    close to the placement location. The randomize_rotation field will randomize
    the block's cardinal orientation. The block's internal survivability and
    placement rules can optionally be enforced with the enforce_survivability_rules
    and enforce_placement_rules fields. These rules are specified per-block and are
    typically designed to produce high quality gameplay or natural behavior.
    However, enabling this enforcement may make it harder to debug placement failures.

    - Succeeds if: The block is successfully placed in the world.
    - Fails if: The block fails to be placed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsingle_block_feature)
    """

    _template_name = "feature_single_block"
    _feature_name = "minecraft:single_block_feature"

    def __init__(
        self,
        name,
        enforce_placement_rules: bool = False,
        enforce_survivability_rules: bool = False,
        randomize_rotation: bool = False,
    ) -> None:
        """Places a single block in the world.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            enforce_placement_rules (bool): Whether block-specific placement
                rules are enforced.
            enforce_survivability_rules (bool): Whether block survivability
                rules are enforced.
            randomize_rotation (bool): Whether the block's cardinal rotation
                should be randomized.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsingle_block_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["enforce_placement_rules"] = enforce_placement_rules
        feature_content["enforce_survivability_rules"] = enforce_survivability_rules
        feature_content["randomize_rotation"] = randomize_rotation

    def place_block(
        self, block: MinecraftBlockDescriptor | Identifier, weight: float = 1.0
    ):
        """Adds a places_block entry with a block reference and weight."""

        feature_content = self._content[self._feature_name]
        feature_content.setdefault("places_block", []).append(
            {"block": block, "weight": clamp(weight, 0, inf)}
        )

    def may_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: list[MinecraftBlockDescriptor | Identifier],
        min_sides_must_attach: int = 1,
        auto_rotate: bool = False,
    ):
        """Sets the may_attach_to object.

        The object supports min_sides_must_attach, auto_rotate, and face-based
        block reference arrays such as top, bottom, sides, all, or diagonal.
        """

        if not 1 <= min_sides_must_attach <= 4:
            raise ValueError("min_sides_must_attach must be between 1 and 4")

        face = (
            "top"
            if face == BlockFaceValues.Up
            else "bottom" if face == BlockFaceValues.Down else face
        )

        attachment = {
            "auto_rotate": auto_rotate,
            "min_sides_must_attach": min_sides_must_attach,
            face: blocks,
        }
        feature_content = self._content[self._feature_name]
        feature_content["may_attach_to"] = attachment

    def may_not_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: list[MinecraftBlockDescriptor | Identifier],
        min_sides_must_attach: int = 1,
        auto_rotate: bool = False,
    ):
        """Sets the may_not_attach_to denylist.

        This has the same structure as may_attach_to, including min_sides_must_attach,
        auto_rotate, and face-based block reference arrays.
        """

        if not 1 <= min_sides_must_attach <= 4:
            raise ValueError("min_sides_must_attach must be between 1 and 4")

        face = (
            "top"
            if face == BlockFaceValues.Up
            else "bottom" if face == BlockFaceValues.Down else face
        )

        attachment = {
            "auto_rotate": auto_rotate,
            "min_sides_must_attach": min_sides_must_attach,
            face: blocks,
        }
        feature_content = self._content[self._feature_name]
        feature_content["may_not_attach_to"] = attachment

    def may_replace(self, blocks: list[MinecraftBlockDescriptor | Identifier]):
        """Sets the may_replace block reference array."""
        feature_content = self._content[self._feature_name]
        feature_content["may_replace"] = blocks


class SnapToSurfaceFeature(Feature):
    """Snaps a referenced feature to a floor, ceiling, wall, or random horizontal surface.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsnap_to_surface_feature)
    """

    _template_name = "feature_snap_to_surface"
    _feature_name = "minecraft:snap_to_surface_feature"

    def __init__(
        self,
        name,
        feature_to_snap: Feature | Identifier,
        search_range: int,
        surface: Literal["ceiling", "floor", "random_horizontal", "wall"] = "floor",
        allow_air_placement: bool = True,
        allow_non_air_placement: bool = False,
        allow_underwater_placement: bool = False,
        allowed_surface_blocks: (
            list[MinecraftBlockDescriptor | Identifier] | None
        ) = None,
        embed_in_surface: bool = False,
    ) -> None:
        """Snaps the y-value of a feature placement position to a surface within the provided search range.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            feature_to_snap (Feature | Identifier): Named reference to the feature
                that will be snapped to a surface.
            search_range (int): Distance searched for a valid surface.
            surface (Literal["ceiling", "floor", "random_horizontal", "wall"]): Surface type to snap to.
            allow_air_placement (bool): Whether placement in air is allowed.
            allow_non_air_placement (bool): Whether the feature can snap through
                non-air blocks. Only used if the snap starts in a block that is
                neither water nor air.
            allow_underwater_placement (bool): Whether underwater placement is
                allowed.
            allowed_surface_blocks (list[MinecraftBlockDescriptor | Identifier] | None):
                Optional block reference array limiting valid surfaces.
            embed_in_surface (bool): Allows specifying whether the snapped feature should be embedded in the located surface

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsnap_to_surface_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["feature_to_snap"] = str(feature_to_snap)
        feature_content["search_range"] = search_range
        feature_content["surface"] = surface
        feature_content["allow_air_placement"] = allow_air_placement
        feature_content["allow_non_air_placement"] = allow_non_air_placement
        feature_content["allow_underwater_placement"] = allow_underwater_placement

        if allowed_surface_blocks is not None:
            self.allowed_surface_blocks(allowed_surface_blocks)

        if embed_in_surface:
            feature_content["embed_in_surface"] = embed_in_surface

    def allowed_surface_blocks(
        self, blocks: list[MinecraftBlockDescriptor | Identifier]
    ):
        """Sets the allowed_surface_blocks block reference array."""
        self._content[self._feature_name]["allowed_surface_blocks"] = list(blocks)


class StructureTemplateFeature(Feature):
    """Places a saved structure template with optional facing and constraints.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftstructure_template_feature)
    """

    _template_name = "feature_structure_template"
    _feature_name = "minecraft:structure_template_feature"

    def __init__(
        self,
        name,
        structure_name: Identifier,
        adjustment_radius: int | None = None,
        facing_direction: (
            Literal["north", "south", "east", "west", "random"] | None
        ) = None,
        rotate_around_center: bool = False,
    ) -> None:
        """Places a structure in the world.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            structure_name (Identifier): Structure reference stored as a
                .mcstructure file in the behavior pack structures directory.
            adjustment_radius (int | None): Optional radius used to adjust
                placement.
            facing_direction (Literal["north", "south", "east", "west", "random"] | None): Optional facing
                direction for the structure.
            rotate_around_center (bool, optional): If true, the structure will be rotated around its center. Defaults to False.
        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftstructure_template_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["structure_name"] = str(structure_name)

        if adjustment_radius is not None:
            feature_content["adjustment_radius"] = clamp(adjustment_radius, 0, 16)

        if facing_direction is not None:
            feature_content["facing_direction"] = facing_direction

        if rotate_around_center:
            feature_content["rotate_around_center"] = rotate_around_center

    def grounded(self):
        """Adds the grounded constraint object."""
        self._content[self._feature_name].setdefault("constraints", {})["grounded"] = {}

    def unburied(self):
        """Adds the unburied constraint object."""
        self._content[self._feature_name].setdefault("constraints", {})["unburied"] = {}

    def block_allowlist(self, blocks: list[MinecraftBlockDescriptor | Identifier]):
        """Sets the block_allowlist array used by the block_intersection constraint."""
        self._content[self._feature_name].setdefault("constraints", {}).setdefault(
            "block_intersection", {}
        )["block_allowlist"] = list(blocks)


class SurfaceRelativeThresholdFeature(Feature):
    """Places a referenced feature only when the position is below the estimated surface.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsurface_relative_threshold_feature)
    """

    _template_name = "feature_surface_relative_threshold"
    _feature_name = "minecraft:surface_relative_threshold_feature"

    def __init__(
        self,
        name,
        feature_to_place: Feature | Identifier,
        minimum_distance_below_surface: int = 0,
    ) -> None:
        """Determines whether the provided position is below the estimated surface level of the world and places a feature if so.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            feature_to_place (Feature | Identifier): Named reference to the feature
                placed when the threshold passes.
            minimum_distance_below_surface (int): Minimum distance below the
                estimated surface required for placement.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftsurface_relative_threshold_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["feature_to_place"] = str(feature_to_place)
        feature_content["minimum_distance_below_surface"] = clamp(
            minimum_distance_below_surface, 0, inf
        )


class TreeFeature(Feature):
    """Builds a tree feature with optional base data, trunk, canopy, and mangrove roots.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecrafttree_feature)
    """

    _template_name = "feature_tree"
    _feature_name = "minecraft:tree_feature"

    def _sync_branch_canopy(
        self, canopy_type: str, canopy_dict: dict[str, Any]
    ) -> None:
        target = self._content[self._feature_name]
        for trunk_type in ("acacia_trunk", "cherry_trunk"):
            if trunk_type in target and "branches" in target[trunk_type]:
                target[trunk_type]["branches"].setdefault("branch_canopy", {})[
                    canopy_type
                ] = canopy_dict

    def base_block(
        self,
        blocks: (
            MinecraftBlockDescriptor
            | Identifier
            | list[MinecraftBlockDescriptor | Identifier]
        ),
    ) -> "TreeFeature":
        """Sets the single block or array of blocks for the base."""
        self._content[self._feature_name]["base_block"] = (
            list(blocks) if isinstance(blocks, list) else blocks
        )
        return self

    def base_cluster(
        self,
        num_clusters: int = 1,
        cluster_radius: int = 0,
        may_replace: list[MinecraftBlockDescriptor | Identifier] | None = None,
    ) -> "TreeFeature":
        """Sets the base_cluster object with num_clusters, cluster_radius, and may_replace."""
        cluster: dict[str, Any] = {
            "num_clusters": clamp(num_clusters, 1, inf),
            "cluster_radius": clamp(cluster_radius, 0, inf),
        }
        if may_replace is not None:
            cluster["may_replace"] = list(may_replace)
        self._content[self._feature_name]["base_cluster"] = cluster
        return self

    def may_grow_on(
        self, blocks: list[MinecraftBlockDescriptor | Identifier]
    ) -> "TreeFeature":
        """Sets the may_grow_on block reference array."""
        self._content[self._feature_name]["may_grow_on"] = list(blocks)
        return self

    def may_replace(
        self, blocks: list[MinecraftBlockDescriptor | Identifier]
    ) -> "TreeFeature":
        """Sets the may_replace block reference array."""
        self._content[self._feature_name]["may_replace"] = list(blocks)
        return self

    def may_grow_through(
        self, blocks: list[MinecraftBlockDescriptor | Identifier]
    ) -> "TreeFeature":
        """Sets the may_grow_through block reference array."""
        self._content[self._feature_name]["may_grow_through"] = list(blocks)
        return self

    # -------------------------------------------------------------------------
    # Trunk builder methods
    # -------------------------------------------------------------------------

    def cherry_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        base_height: int = 7,
        height_intervals: list[int] | tuple[int, ...] | None = None,
        one_branch_weight: int = 10,
        two_branches_weight: int = 10,
        two_branches_and_trunk_weight: int = 10,
        branch_horizontal_length: tuple[int, int] | int = (2, 4),
        branch_start_offset_from_top: tuple[int, int] | int = (-4, -3),
        branch_end_offset_from_top: tuple[int, int] | int = (-1, 0),
    ) -> "TreeFeature":
        """Sets the cherry_trunk configuration using strictly typed plain arguments."""
        trunk_height: dict[str, Any] = {"base": clamp(base_height, 2, inf)}
        if height_intervals is not None:
            trunk_height["intervals"] = [int(i) for i in height_intervals]

        branches: dict[str, Any] = {
            "tree_type_weights": {
                "one_branch": clamp(one_branch_weight, 0, inf),
                "two_branches": clamp(two_branches_weight, 0, inf),
                "two_branches_and_trunk": clamp(two_branches_and_trunk_weight, 0, inf),
            },
            "branch_horizontal_length": AnvilFormatter.range_min_max_dict(
                branch_horizontal_length, "branch_horizontal_length"
            ),
            "branch_start_offset_from_top": AnvilFormatter.range_min_max_dict(
                branch_start_offset_from_top, "branch_start_offset_from_top"
            ),
            "branch_end_offset_from_top": AnvilFormatter.range_min_max_dict(
                branch_end_offset_from_top, "branch_end_offset_from_top"
            ),
        }

        existing_branch_canopy = (
            self._content[self._feature_name]
            .get("cherry_trunk", {})
            .get("branches", {})
            .get("branch_canopy")
        )
        if existing_branch_canopy:
            branches["branch_canopy"] = existing_branch_canopy

        self._content[self._feature_name]["cherry_trunk"] = {
            "trunk_block": trunk_block,
            "trunk_height": trunk_height,
            "branches": branches,
        }
        return self

    def acacia_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        trunk_width: int = 1,
        base_height: int = 5,
        height_intervals: list[int] | tuple[int, ...] | None = None,
        min_height_for_canopy: int | None = None,
        allow_diagonal_growth: bool = True,
        lean_height: tuple[int, int] | int = (1, 5),
        lean_steps: tuple[int, int] | int = (1, 4),
        lean_length: tuple[int, int] | int | None = None,
        branch_chance: float = 0.0,
        branch_length: tuple[int, int] | int = (1, 4),
        branch_position: tuple[int, int] | int = (1, 3),
    ) -> "TreeFeature":
        """Sets the acacia_trunk configuration using strictly typed plain arguments."""
        trunk_height: dict[str, Any] = {"base": clamp(base_height, 1, inf)}
        if height_intervals is not None:
            trunk_height["intervals"] = [int(i) for i in height_intervals]
        if min_height_for_canopy is not None:
            trunk_height["min_height_for_canopy"] = min_height_for_canopy

        trunk_lean: dict[str, Any] = {
            "allow_diagonal_growth": allow_diagonal_growth,
            "lean_height": AnvilFormatter.range_min_max_dict(
                lean_height, "lean_height"
            ),
            "lean_steps": AnvilFormatter.range_min_max_dict(lean_steps, "lean_steps"),
        }
        if lean_length is not None:
            trunk_lean["lean_length"] = AnvilFormatter.range_min_max_dict(
                lean_length, "lean_length"
            )

        branches: dict[str, Any] = {
            "branch_chance": branch_chance,
            "branch_length": AnvilFormatter.range_min_max_dict(
                branch_length, "branch_length"
            ),
            "branch_position": AnvilFormatter.range_min_max_dict(
                branch_position, "branch_position"
            ),
        }

        existing_branch_canopy = (
            self._content[self._feature_name]
            .get("acacia_trunk", {})
            .get("branches", {})
            .get("branch_canopy")
        )
        if existing_branch_canopy:
            branches["branch_canopy"] = existing_branch_canopy

        self._content[self._feature_name]["acacia_trunk"] = {
            "trunk_block": trunk_block,
            "trunk_width": clamp(trunk_width, 1, inf),
            "trunk_height": trunk_height,
            "trunk_lean": trunk_lean,
            "branches": branches,
        }
        return self

    def trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        trunk_height: tuple[int, int] | int = (4, 7),
        height_modifier: tuple[int, int] | int | None = None,
        can_be_submerged: bool | int | None = None,
    ) -> "TreeFeature":
        """Sets the standard trunk configuration using strictly typed plain arguments."""
        config: dict[str, Any] = {
            "trunk_block": trunk_block,
            "trunk_height": (
                AnvilFormatter.range_min_max_dict(trunk_height, "trunk_height")
                if isinstance(trunk_height, (tuple, list))
                else trunk_height
            ),
        }
        if height_modifier is not None:
            config["height_modifier"] = AnvilFormatter.range_min_max_dict(
                height_modifier, "height_modifier"
            )
        if can_be_submerged is not None:
            if isinstance(can_be_submerged, bool):
                config["can_be_submerged"] = can_be_submerged
            else:
                config["can_be_submerged"] = {
                    "max_depth": clamp(can_be_submerged, 1, inf)
                }
        self._content[self._feature_name]["trunk"] = config
        return self

    def fancy_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
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
        """Sets the fancy_trunk configuration using strictly typed plain arguments."""
        self._content[self._feature_name]["fancy_trunk"] = {
            "trunk_block": trunk_block,
            "trunk_width": clamp(trunk_width, 1, inf),
            "trunk_height": {
                "base": clamp(base_height, 1, inf),
                "variance": clamp(height_variance, 1, inf),
                "scale": clamp(height_scale, 0.0, 1.0),
            },
            "branches": {
                "slope": branch_slope,
                "density": branch_density,
                "min_altitude_factor": clamp(branch_min_altitude_factor, 0.0, 1.0),
            },
            "width_scale": clamp(width_scale, 0.0, inf),
            "foliage_altitude_factor": clamp(foliage_altitude_factor, 0.0, 1.0),
        }
        return self

    def mega_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        trunk_width: int = 2,
        base_height: int = 15,
        height_intervals: list[int] | tuple[int, ...] | None = None,
        height_modifier: tuple[int, int] | int | None = None,
        branch_length: int | None = None,
        branch_slope: float | None = None,
        branch_interval: int | None = None,
        branch_altitude_factor: float | None = None,
    ) -> "TreeFeature":
        """Sets the mega_trunk configuration using strictly typed plain arguments."""
        trunk_height: dict[str, Any] = {"base": clamp(base_height, 1, inf)}
        if height_intervals is not None:
            trunk_height["intervals"] = [int(i) for i in height_intervals]

        config: dict[str, Any] = {
            "trunk_block": trunk_block,
            "trunk_width": clamp(trunk_width, 1, inf),
            "trunk_height": trunk_height,
        }
        if height_modifier is not None:
            config["height_modifier"] = AnvilFormatter.range_min_max_dict(
                height_modifier, "height_modifier"
            )

        branches: dict[str, Any] = {}
        if branch_length is not None:
            branches["branch_length"] = branch_length
        if branch_slope is not None:
            branches["branch_slope"] = branch_slope
        if branch_interval is not None:
            branches["branch_interval"] = branch_interval
        if branch_altitude_factor is not None:
            branches["branch_altitude_factor"] = branch_altitude_factor
        if branches:
            config["branches"] = branches

        self._content[self._feature_name]["mega_trunk"] = config
        return self

    def poplar_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        trunk_height: tuple[int, int] | int = (5, 8),
        remaining_trunk_height_above_branches: tuple[int, int] | int | None = None,
        amount_of_foliage_support_branches: int | None = None,
        height_modifier: tuple[int, int] | int | None = None,
    ) -> "TreeFeature":
        """Sets the poplar_trunk configuration using strictly typed plain arguments."""
        config: dict[str, Any] = {
            "trunk_block": trunk_block,
            "trunk_height": AnvilFormatter.range_min_max_dict(
                trunk_height, "trunk_height"
            ),
        }
        if remaining_trunk_height_above_branches is not None:
            config["remaining_trunk_height_above_branches"] = (
                AnvilFormatter.range_min_max_dict(
                    remaining_trunk_height_above_branches,
                    "remaining_trunk_height_above_branches",
                )
            )
        if amount_of_foliage_support_branches is not None:
            config["amount_of_foliage_support_branches"] = (
                amount_of_foliage_support_branches
            )
        if height_modifier is not None:
            config["height_modifier"] = AnvilFormatter.range_min_max_dict(
                height_modifier, "height_modifier"
            )
        self._content[self._feature_name]["poplar_trunk"] = config
        return self

    def mangrove_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        trunk_width: int = 1,
        base_height: int = 5,
        height_rand_a: int = 1,
        height_rand_b: int = 1,
        branch_length: tuple[int, int] | int = (2, 4),
        branch_steps: tuple[int, int] | int = (1, 3),
        branch_chance: float = 100.0,
    ) -> "TreeFeature":
        """Sets the mangrove_trunk configuration using strictly typed plain arguments."""
        self._content[self._feature_name]["mangrove_trunk"] = {
            "trunk_block": trunk_block,
            "trunk_width": clamp(trunk_width, 1, inf),
            "trunk_height": {
                "base": clamp(base_height, 1, inf),
                "height_rand_a": clamp(height_rand_a, 1, inf),
                "height_rand_b": clamp(height_rand_b, 1, inf),
            },
            "branches": {
                "branch_length": AnvilFormatter.range_min_max_dict(
                    branch_length, "branch_length"
                ),
                "branch_steps": AnvilFormatter.range_min_max_dict(
                    branch_steps, "branch_steps"
                ),
                "branch_chance": clamp(branch_chance, 0.0, 100.0),
            },
        }
        return self

    def fallen_trunk(
        self,
        trunk_block: MinecraftBlockDescriptor | Identifier,
        log_length: tuple[int, int] | int = (4, 7),
        stump_height: tuple[int, int] | int | None = None,
        height_modifier: tuple[int, int] | int | None = None,
        log_decoration_feature: str | Identifier | None = None,
    ) -> "TreeFeature":
        """Sets the fallen_trunk configuration using strictly typed plain arguments."""
        config: dict[str, Any] = {
            "trunk_block": trunk_block,
            "log_length": AnvilFormatter.range_min_max_dict(log_length, "log_length"),
        }
        if stump_height is not None:
            config["stump_height"] = AnvilFormatter.range_min_max_dict(
                stump_height, "stump_height"
            )
        if height_modifier is not None:
            config["height_modifier"] = AnvilFormatter.range_min_max_dict(
                height_modifier, "height_modifier"
            )
        if log_decoration_feature is not None:
            config["log_decoration_feature"] = str(log_decoration_feature)
        self._content[self._feature_name]["fallen_trunk"] = config
        return self

    # -------------------------------------------------------------------------
    # Canopy builder methods
    # -------------------------------------------------------------------------

    def cherry_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        height: tuple[int, int] | int = 4,
        radius: tuple[int, int] | int = 4,
        trunk_width: int | None = None,
        wide_bottom_layer_hole_chance: float = 25.0,
        corner_hole_chance: float = 50.0,
        hanging_leaves_chance: float = 16.6666,
        hanging_leaves_extension_chance: float = 33.3333,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the cherry_canopy configuration using strictly typed plain arguments.

        Note: Bedrock schema requires height to be at least 4. Values below 4 are clamped.
        """
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "height": AnvilFormatter.range_min_max_dict(height, "height", clamp_min=4),
            "radius": AnvilFormatter.range_min_max_dict(radius, "radius"),
            "wide_bottom_layer_hole_chance": wide_bottom_layer_hole_chance,
            "corner_hole_chance": corner_hole_chance,
            "hanging_leaves_chance": hanging_leaves_chance,
            "hanging_leaves_extension_chance": hanging_leaves_extension_chance,
        }
        if trunk_width is not None:
            canopy_dict["trunk_width"] = clamp(trunk_width, 1, inf)

        self._content[self._feature_name]["cherry_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("cherry_canopy", canopy_dict)
        return self

    def fancy_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        height: int = 4,
        radius: int = 4,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the fancy_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "height": clamp(height, 1, inf),
            "radius": clamp(radius, 0, inf),
        }
        self._content[self._feature_name]["fancy_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("fancy_canopy", canopy_dict)
        return self

    def acacia_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_size: int = 3,
        simplify_canopy: bool = False,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the acacia_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_size": clamp(canopy_size, 1, inf),
        }
        if simplify_canopy:
            canopy_dict["simplify_canopy"] = True
        self._content[self._feature_name]["acacia_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("acacia_canopy", canopy_dict)
        return self

    def canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        min_width: int | None = None,
        canopy_offset_min: int | None = None,
        canopy_offset_max: int | None = None,
        slope_rise: int | None = None,
        slope_run: int | None = None,
        variation_chance: list[tuple[int, int]] | None = None,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the standard canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
        }
        if min_width is not None:
            canopy_dict["min_width"] = clamp(min_width, 0, inf)
        if canopy_offset_min is not None and canopy_offset_max is not None:
            canopy_dict["canopy_offset"] = AnvilFormatter.min_max_dict(
                (canopy_offset_min, canopy_offset_max), "canopy_offset"
            )
        if slope_rise is not None and slope_run is not None:
            canopy_dict["canopy_slope"] = {
                "rise": slope_rise,
                "run": slope_run,
            }
        if variation_chance is not None:
            canopy_dict["variation_chance"] = [
                {"numerator": item[0], "denominator": item[1]}
                for item in variation_chance
            ]
        self._content[self._feature_name]["canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("canopy", canopy_dict)
        return self

    def roofed_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_height: int = 3,
        core_width: int = 1,
        outer_radius: int = 3,
        inner_radius: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the roofed_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_height": clamp(canopy_height, 3, inf),
            "core_width": clamp(core_width, 1, inf),
            "outer_radius": clamp(outer_radius, 0, inf),
            "inner_radius": clamp(inner_radius, 0, inf),
        }
        self._content[self._feature_name]["roofed_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("roofed_canopy", canopy_dict)
        return self

    def spruce_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        lower_offset: tuple[int, int] | int = (0, 0),
        upper_offset: tuple[int, int] | int = (0, 0),
        max_radius: tuple[int, int] | int = (2, 3),
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the spruce_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "lower_offset": AnvilFormatter.range_min_max_dict(
                lower_offset, "lower_offset"
            ),
            "upper_offset": AnvilFormatter.range_min_max_dict(
                upper_offset, "upper_offset"
            ),
            "max_radius": AnvilFormatter.range_min_max_dict(max_radius, "max_radius"),
        }
        self._content[self._feature_name]["spruce_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("spruce_canopy", canopy_dict)
        return self

    def pine_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_height: tuple[int, int] | int = (4, 5),
        base_radius: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the pine_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_height": AnvilFormatter.range_min_max_dict(
                canopy_height, "canopy_height"
            ),
            "base_radius": clamp(base_radius, 1, inf),
        }
        self._content[self._feature_name]["pine_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("pine_canopy", canopy_dict)
        return self

    def mega_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_height: tuple[int, int] | int = (4, 6),
        base_radius: int = 4,
        core_width: int = 2,
        simplify_canopy: bool = False,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the mega_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_height": AnvilFormatter.range_min_max_dict(
                canopy_height, "canopy_height"
            ),
            "base_radius": clamp(base_radius, 0, inf),
            "core_width": clamp(core_width, 1, inf),
        }
        if simplify_canopy:
            canopy_dict["simplify_canopy"] = True
        self._content[self._feature_name]["mega_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("mega_canopy", canopy_dict)
        return self

    def mega_pine_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_height: tuple[int, int] | int = (8, 12),
        base_radius: int = 4,
        radius_step_modifier: float = 0.5,
        core_width: int = 2,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the mega_pine_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_height": AnvilFormatter.range_min_max_dict(
                canopy_height, "canopy_height"
            ),
            "base_radius": clamp(base_radius, 0, inf),
            "radius_step_modifier": radius_step_modifier,
            "core_width": clamp(core_width, 1, inf),
        }
        self._content[self._feature_name]["mega_pine_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("mega_pine_canopy", canopy_dict)
        return self

    def poplar_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the poplar_canopy configuration using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
        }
        self._content[self._feature_name]["poplar_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("poplar_canopy", canopy_dict)
        return self

    def mangrove_canopy(
        self,
        leaf_blocks: (
            list[tuple[MinecraftBlockDescriptor | Identifier, float]]
            | list[MinecraftBlockDescriptor | Identifier]
        ),
        canopy_height: tuple[int, int] | int = (3, 5),
        canopy_radius: tuple[int, int] | int = (3, 5),
        leaf_placement_attempts: int = 100,
        hanging_block: MinecraftBlockDescriptor | Identifier | None = None,
        hanging_block_placement_chance: float | None = None,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the mangrove_canopy configuration using strictly typed plain arguments."""
        formatted_leaves: list[list[Any]] = []
        for entry in leaf_blocks:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                formatted_leaves.append([entry[0], float(entry[1])])
            else:
                formatted_leaves.append([entry, 1.0])

        canopy_dict: dict[str, Any] = {
            "leaf_blocks": formatted_leaves,
            "canopy_height": AnvilFormatter.range_min_max_dict(
                canopy_height, "canopy_height"
            ),
            "canopy_radius": AnvilFormatter.range_min_max_dict(
                canopy_radius, "canopy_radius"
            ),
            "leaf_placement_attempts": clamp(leaf_placement_attempts, 1, inf),
        }
        if hanging_block is not None:
            canopy_dict["hanging_block"] = hanging_block
        if hanging_block_placement_chance is not None:
            canopy_dict["hanging_block_placement_chance"] = (
                hanging_block_placement_chance
            )

        self._content[self._feature_name]["mangrove_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("mangrove_canopy", canopy_dict)
        return self

    def random_spread_canopy(
        self,
        leaf_blocks: (
            list[tuple[MinecraftBlockDescriptor | Identifier, float]]
            | list[MinecraftBlockDescriptor | Identifier]
        ),
        canopy_height: tuple[int, int] | int = (3, 5),
        canopy_radius: tuple[int, int] | int = (3, 5),
        leaf_placement_attempts: int = 100,
        sync_to_branches: bool = True,
    ) -> "TreeFeature":
        """Sets the random_spread_canopy configuration using strictly typed plain arguments."""
        formatted_leaves: list[list[Any]] = []
        for entry in leaf_blocks:
            if isinstance(entry, (list, tuple)) and len(entry) == 2:
                formatted_leaves.append([entry[0], float(entry[1])])
            else:
                formatted_leaves.append([entry, 1.0])

        canopy_dict: dict[str, Any] = {
            "leaf_blocks": formatted_leaves,
            "canopy_height": AnvilFormatter.range_min_max_dict(
                canopy_height, "canopy_height"
            ),
            "canopy_radius": AnvilFormatter.range_min_max_dict(
                canopy_radius, "canopy_radius"
            ),
            "leaf_placement_attempts": clamp(leaf_placement_attempts, 1, inf),
        }
        self._content[self._feature_name]["random_spread_canopy"] = canopy_dict
        if sync_to_branches:
            self._sync_branch_canopy("random_spread_canopy", canopy_dict)
        return self

    # -------------------------------------------------------------------------
    # Branch canopy override methods
    # -------------------------------------------------------------------------

    def branch_cherry_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        height: tuple[int, int] | int = 4,
        radius: tuple[int, int] | int = 4,
        trunk_width: int | None = None,
        wide_bottom_layer_hole_chance: float = 25.0,
        corner_hole_chance: float = 50.0,
        hanging_leaves_chance: float = 16.6666,
        hanging_leaves_extension_chance: float = 33.3333,
    ) -> "TreeFeature":
        """Explicitly sets cherry_canopy for trunk branches using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "height": AnvilFormatter.range_min_max_dict(height, "height", clamp_min=4),
            "radius": AnvilFormatter.range_min_max_dict(radius, "radius"),
            "wide_bottom_layer_hole_chance": wide_bottom_layer_hole_chance,
            "corner_hole_chance": corner_hole_chance,
            "hanging_leaves_chance": hanging_leaves_chance,
            "hanging_leaves_extension_chance": hanging_leaves_extension_chance,
        }
        if trunk_width is not None:
            canopy_dict["trunk_width"] = clamp(trunk_width, 1, inf)
        self._sync_branch_canopy("cherry_canopy", canopy_dict)
        return self

    def branch_fancy_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        height: int = 4,
        radius: int = 4,
    ) -> "TreeFeature":
        """Explicitly sets fancy_canopy for trunk branches using strictly typed plain arguments."""
        canopy_dict = {
            "leaf_block": leaf_block,
            "height": clamp(height, 1, inf),
            "radius": clamp(radius, 0, inf),
        }
        self._sync_branch_canopy("fancy_canopy", canopy_dict)
        return self

    def branch_acacia_canopy(
        self,
        leaf_block: MinecraftBlockDescriptor | Identifier,
        canopy_size: int = 3,
        simplify_canopy: bool = False,
    ) -> "TreeFeature":
        """Explicitly sets acacia_canopy for trunk branches using strictly typed plain arguments."""
        canopy_dict: dict[str, Any] = {
            "leaf_block": leaf_block,
            "canopy_size": clamp(canopy_size, 1, inf),
        }
        if simplify_canopy:
            canopy_dict["simplify_canopy"] = True
        self._sync_branch_canopy("acacia_canopy", canopy_dict)
        return self

    def mangrove_roots(
        self,
        root_block: MinecraftBlockDescriptor | Identifier,
        muddy_root_block: MinecraftBlockDescriptor | Identifier | None = None,
        max_root_width: int = 5,
        max_root_length: int = 15,
        y_offset: int = 0,
        roots_may_grow_through: (
            list[MinecraftBlockDescriptor | Identifier] | None
        ) = None,
    ) -> "TreeFeature":
        """Sets the mangrove_roots configuration using strictly typed plain arguments."""
        roots: dict[str, Any] = {
            "root_block": root_block,
            "max_root_width": clamp(max_root_width, 1, inf),
            "max_root_length": clamp(max_root_length, 1, inf),
            "y_offset": y_offset,
        }
        if muddy_root_block is not None:
            roots["muddy_root_block"] = muddy_root_block
        if roots_may_grow_through is not None:
            roots["roots_may_grow_through"] = list(roots_may_grow_through)
        self._content[self._feature_name]["mangrove_roots"] = roots
        return self


class UnderwaterCaveCarverFeature(Feature):
    """Carves underwater caves below sea level during pregeneration.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftunderwater_cave_carver_feature)
    """

    _template_name = "feature_underwater_cave_carver"
    _feature_name = "minecraft:underwater_cave_carver_feature"

    def __init__(
        self,
        name,
        fill_with: MinecraftBlockDescriptor | Identifier | None = None,
        width_modifier: Molang | float | int | None = None,
        skip_carve_chance: int | None = None,
        height_limit: int | None = None,
        y_scale: float | tuple[float, float] | None = None,
        horizontal_radius_multiplier: float | tuple[float, float] | None = None,
        vertical_radius_multiplier: float | tuple[float, float] | None = None,
        floor_level: float | tuple[float, float] | None = None,
        replace_air_with: MinecraftBlockDescriptor | Identifier | None = None,
    ) -> None:
        """Carves underwater caves below sea level during pregeneration.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            fill_with (MinecraftBlockDescriptor | Identifier | None): Reference
                to the block to fill the cave with.
            width_modifier (Molang | float | int | None): How many blocks to
                increase the cave radius by, from the center point of the cave.
            skip_carve_chance (int | None): The chance to skip doing the carve
                (1 / value).
            height_limit (int | None): The height limit where we attempt to
                carve.
            y_scale (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                The scaling in y.
            horizontal_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Horizontal radius multiplier.
            vertical_radius_multiplier (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Vertical radius multiplier.
            floor_level (int | float | tuple[int | float, int | float] | list[int | float] | Mapping[str, int | float] | None):
                Floor Level.
            replace_air_with (MinecraftBlockDescriptor | Identifier | None):
                Optional block used to replace carved air.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftunderwater_cave_carver_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]

        if fill_with is not None:
            feature_content["fill_with"] = fill_with

        if width_modifier is not None:
            feature_content["width_modifier"] = str(width_modifier)

        if skip_carve_chance is not None:
            feature_content["skip_carve_chance"] = clamp(skip_carve_chance, 1, inf)

        if height_limit is not None:
            feature_content["height_limit"] = height_limit

        if y_scale is not None:
            feature_content["y_scale"] = AnvilFormatter.range_min_max_dict(y_scale)

        if horizontal_radius_multiplier is not None:
            feature_content["horizontal_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(horizontal_radius_multiplier)
            )

        if vertical_radius_multiplier is not None:
            feature_content["vertical_radius_multiplier"] = (
                AnvilFormatter.range_min_max_dict(vertical_radius_multiplier)
            )

        if floor_level is not None:
            feature_content["floor_level"] = AnvilFormatter.range_min_max_dict(
                floor_level
            )

        if replace_air_with is not None:
            feature_content["replace_air_with"] = replace_air_with


class VegetationPatchFeature(Feature):
    """Creates a patch of ground blocks and scatters a vegetation feature over it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftvegetation_patch_feature)
    """

    _template_name = "feature_vegetation_patch"
    _feature_name = "minecraft:vegetation_patch_feature"

    def __init__(
        self,
        name,
        ground_block: MinecraftBlockDescriptor | Identifier,
        vegetation_feature: Feature | Identifier,
        depth: float | tuple[float, float],
        vertical_range: int,
        horizontal_radius: float | tuple[float, float],
        surface: Literal["floor", "ceiling"] = "floor",
        extra_deep_block_chance: float | None = None,
        vegetation_chance: float | None = None,
        extra_edge_column_chance: float | None = None,
        waterlogged: bool = False,
    ) -> None:
        """Creates a patch of ground blocks and scatters a vegetation feature over it.

        Parameters:
            name (str): The name of this feature. The resulting identifier uses
                the format 'namespace_name:feature_name'. 'feature_name' must
                match the filename.
            ground_block (MinecraftBlockDescriptor | Identifier): Block used
                for the generated ground patch.
            vegetation_feature (Feature | Identifier): Named reference to the
                vegetation feature scattered over the patch.
            depth (int | tuple[int, int] | list[int] | Mapping[str, int]):
                Patch depth value or range.
            vertical_range (int): Vertical placement range.
            horizontal_radius (int | tuple[int, int] | list[int] | Mapping[str, int]):
                Horizontal radius value or range.
            surface (Literal["floor", "ceiling"]): Surface type used for placement.
            extra_deep_block_chance (float | None): Optional chance to place
                extra deep blocks.
            vegetation_chance (float | None): Optional chance to place
                vegetation.
            extra_edge_column_chance (float | None): Optional chance to add
                extra edge columns.
            waterlogged (bool): Whether generated blocks should be waterlogged.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftvegetation_patch_feature)
        """
        super().__init__(name)
        feature_content = self._content[self._feature_name]
        feature_content["ground_block"] = ground_block
        feature_content["vegetation_feature"] = str(vegetation_feature)
        feature_content["surface"] = surface
        feature_content["depth"] = AnvilFormatter.range_min_max_dict(depth)
        feature_content["vertical_range"] = vertical_range
        feature_content["horizontal_radius"] = AnvilFormatter.range_min_max_dict(
            horizontal_radius
        )
        feature_content["waterlogged"] = waterlogged

        if extra_deep_block_chance is not None:
            feature_content["extra_deep_block_chance"] = clamp(
                extra_deep_block_chance, 0.0, 1.0
            )

        if vegetation_chance is not None:
            feature_content["vegetation_chance"] = clamp(vegetation_chance, 0.0, 1.0)

        if extra_edge_column_chance is not None:
            feature_content["extra_edge_column_chance"] = max(
                0.0, extra_edge_column_chance
            )

    def replaceable_blocks(self, blocks: list[MinecraftBlockDescriptor | Identifier]):
        """Sets the replaceable_blocks block reference array."""
        self._content[self._feature_name]["replaceable_blocks"] = list(blocks)


class WeightedRandomFeature(Feature):
    """Places one feature chosen from a weighted list of feature references.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraftweighted_random_feature)
    """

    _template_name = "feature_weighted_random"
    _feature_name = "minecraft:weighted_random_feature"

    def add_feature(self, feature: Feature | Identifier, weight: float = 1.0):
        """Adds a weighted feature entry with a named reference to a feature and a weight."""
        self._content[self._feature_name].setdefault("features", []).append(
            [str(feature), clamp(weight, 0, inf)]
        )

    def features(
        self, feature_list: list[tuple[Feature | Identifier, float]]
    ) -> "WeightedRandomFeature":
        """Adds multiple weighted feature entries with feature references and weights."""
        for feature, weight in feature_list:
            self.add_feature(feature, weight)
        return self
