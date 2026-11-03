"""The cave carvers: `minecraft:cave_carver_feature`, `minecraft:nether_cave_carver_feature`
and `minecraft:underwater_cave_carver_feature`."""

from typing import Annotated, Any, ClassVar

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import AtLeastOne, ExactRangeMinMax, JsonObject, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor


class _CaveCarverFeature(_Feature):
    """The body of a cave carver feature."""

    fill_with: str | MinecraftBlockDescriptor | None = None
    width_modifier: float | str | None = None
    skip_carve_chance: Annotated[int, AtLeastOne] | None = None
    height_limit: int | None = None
    y_scale: Annotated[float | tuple[float, float], ExactRangeMinMax] | None = None
    horizontal_radius_multiplier: (
        Annotated[float | tuple[float, float], ExactRangeMinMax] | None
    ) = None
    vertical_radius_multiplier: (
        Annotated[float | tuple[float, float], ExactRangeMinMax] | None
    ) = None
    floor_level: Annotated[float | tuple[float, float], ExactRangeMinMax] | None = None

    def set_carver(self, **options: Any) -> None:
        """Sets the carver options given, leaving the others as they are."""
        for name, value in options.items():
            if value is not None:
                setattr(self, name, value)


class _UnderwaterCaveCarverFeature(_CaveCarverFeature):
    """The `minecraft:underwater_cave_carver_feature` body."""

    replace_air_with: str | MinecraftBlockDescriptor | None = None


class _CaveCarverFeatureFile(JsonObject):
    """The content of a cave carver feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:cave_carver_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _CaveCarverFeature = json_field(
        key="minecraft:cave_carver_feature", default_factory=_CaveCarverFeature
    )


class _NetherCaveCarverFeatureFile(JsonObject):
    """The content of a nether cave carver feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:nether_cave_carver_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _CaveCarverFeature = json_field(
        key="minecraft:nether_cave_carver_feature", default_factory=_CaveCarverFeature
    )


class _UnderwaterCaveCarverFeatureFile(JsonObject):
    """The content of an underwater cave carver feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:underwater_cave_carver_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _UnderwaterCaveCarverFeature = json_field(
        key="minecraft:underwater_cave_carver_feature",
        default_factory=_UnderwaterCaveCarverFeature,
    )


class CaveCarverFeature(Feature):
    """Carves a cave through the current chunk and the chunks around it. Only works when its
    feature rule places it in the `pregeneration_pass`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_cave_carver_feature)
    """

    _document = _CaveCarverFeatureFile

    def __init__(
        self,
        name: str,
        fill_with: str | MinecraftBlockDescriptor | None = None,
        width_modifier: float | str | None = None,
        skip_carve_chance: int | None = None,
        height_limit: int | None = None,
        y_scale: float | tuple[float, float] | None = None,
        horizontal_radius_multiplier: float | tuple[float, float] | None = None,
        vertical_radius_multiplier: float | tuple[float, float] | None = None,
        floor_level: float | tuple[float, float] | None = None,
    ) -> None:
        """Creates a cave carver feature.

        Args:
            name (str): The name of the feature, also its file name.
            fill_with (str | MinecraftBlockDescriptor, optional): The block the cave is
                filled with.
            width_modifier (float | str, optional): How many blocks the cave radius grows
                by, from its centre: a number or a Molang expression.
            skip_carve_chance (int, optional): The chance to skip the carve, as 1 in this
                value. At least 1.
            height_limit (int, optional): The height limit of the carve.
            y_scale (float | tuple[float, float], optional): The scale along y, or a range
                it is picked from.
            horizontal_radius_multiplier (float | tuple[float, float], optional): The
                horizontal radius multiplier, or a range it is picked from.
            vertical_radius_multiplier (float | tuple[float, float], optional): The vertical
                radius multiplier, or a range it is picked from.
            floor_level (float | tuple[float, float], optional): The floor level, or a range
                it is picked from.
        """
        super().__init__(name)
        self._feature.set_carver(
            fill_with=fill_with,
            width_modifier=width_modifier,
            skip_carve_chance=skip_carve_chance,
            height_limit=height_limit,
            y_scale=y_scale,
            horizontal_radius_multiplier=horizontal_radius_multiplier,
            vertical_radius_multiplier=vertical_radius_multiplier,
            floor_level=floor_level,
        )


class NetherCaveCarverFeature(CaveCarverFeature):
    """Carves a cave through the Nether in the current chunk and the chunks around it. Only
    works when its feature rule places it in the `pregeneration_pass`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_nether_cave_carver_feature)
    """

    _document = _NetherCaveCarverFeatureFile


class UnderwaterCaveCarverFeature(CaveCarverFeature):
    """Carves a cave below sea level through the current chunk and the chunks around it.
    Only works when its feature rule places it in the `pregeneration_pass`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_underwater_cave_carver_feature)
    """

    _document = _UnderwaterCaveCarverFeatureFile

    def __init__(
        self,
        name: str,
        fill_with: str | MinecraftBlockDescriptor | None = None,
        width_modifier: float | str | None = None,
        skip_carve_chance: int | None = None,
        height_limit: int | None = None,
        y_scale: float | tuple[float, float] | None = None,
        horizontal_radius_multiplier: float | tuple[float, float] | None = None,
        vertical_radius_multiplier: float | tuple[float, float] | None = None,
        floor_level: float | tuple[float, float] | None = None,
        replace_air_with: str | MinecraftBlockDescriptor | None = None,
    ) -> None:
        """Creates an underwater cave carver feature.

        Args:
            name (str): The name of the feature, also its file name.
            fill_with (str | MinecraftBlockDescriptor, optional): The block the cave is
                filled with.
            width_modifier (float | str, optional): How many blocks the cave radius grows
                by, from its centre: a number or a Molang expression.
            skip_carve_chance (int, optional): The chance to skip the carve, as 1 in this
                value. At least 1.
            height_limit (int, optional): The height limit of the carve.
            y_scale (float | tuple[float, float], optional): The scale along y, or a range
                it is picked from.
            horizontal_radius_multiplier (float | tuple[float, float], optional): The
                horizontal radius multiplier, or a range it is picked from.
            vertical_radius_multiplier (float | tuple[float, float], optional): The vertical
                radius multiplier, or a range it is picked from.
            floor_level (float | tuple[float, float], optional): The floor level, or a range
                it is picked from.
            replace_air_with (str | MinecraftBlockDescriptor, optional): The block air is
                replaced with.
        """
        super().__init__(
            name,
            fill_with,
            width_modifier,
            skip_carve_chance,
            height_limit,
            y_scale,
            horizontal_radius_multiplier,
            vertical_radius_multiplier,
            floor_level,
        )
        self._feature.set_carver(replace_air_with=replace_air_with)
