"""The dimension components, added to `DimensionConfiguration.components`."""

from typing import Annotated, Literal

from anvil.lib.jsonmodel import InRange, JsonComponent, json_field

__all__ = [
    "DimensionComponent",
    "DimensionClouds",
    "DimensionDefaultBiome",
    "DimensionGeneration",
    "DimensionHeight",
]


class DimensionComponent(JsonComponent, abstract=True):
    """Base class of the dimension components, added to `DimensionConfiguration.components`."""


class DimensionGeneration(DimensionComponent):
    """Sets how the terrain of the dimension is generated. Only the void generator exists.

    Args:
        generator_type (Literal["void"]): The world generator.
    """

    identifier = "minecraft:generation"

    generator_type: Literal["void"] = json_field()


class DimensionHeight(DimensionComponent):
    """Sets the vertical bounds of the dimension. Already generated terrain is not reshaped,
    only cut off at the new bounds.

    Args:
        min_y (int): The lowest block height, from -512 to 512. Game default -64.
        height_range (int): The total height, a multiple of 16 from 16 to 1024. Game default 384.
    """

    identifier = "minecraft:dimension_height"

    min_y: Annotated[int, InRange(-512, 512)] = json_field()
    height_range: Annotated[int, InRange(16, 1024)] = json_field()

    def __validate__(self) -> None:
        if self.height_range % 16 != 0:
            raise ValueError(
                f"Dimension height_range must be a multiple of 16, got {self.height_range}."
            )


class DimensionDefaultBiome(DimensionComponent):
    """Sets the biome used throughout the dimension.

    Args:
        biome (str): The namespaced identifier of the biome. Game default minecraft:ocean.
    """

    identifier = "minecraft:default_biome"

    biome: str = json_field()


class DimensionClouds(DimensionComponent):
    """Sets the cloud height of the dimension.

    Args:
        height (int): The Y coordinate of the clouds, from -512 to 512. Game default 128.
    """

    identifier = "minecraft:clouds"

    height: Annotated[int, InRange(-512, 512)] = json_field()
