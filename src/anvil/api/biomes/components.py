from typing import Annotated, Literal
from warnings import deprecated

from anvil.api.core.enums import Dimension, MusicCategory
from anvil.api.core.types import (
    RGB,
    RGB255,
    RGBA,
    RGBA255,
    BiomeClimateCategory,
    BiomeNoiseGradientBuilderType,
    BiomeNoiseType,
    BiomeVillageTypes,
    FoliageColorMap,
    GrassColorMap,
    HexRGB,
    HexRGBA,
)
from anvil.api.vanilla.biomes import MinecraftBiomeTags, MinecraftBiomeTypes
from anvil.lib.jsonmodel import (
    AsString,
    Chance,
    ColorMap,
    Hex,
    InRange,
    JsonComponent,
    JsonObject,
    Length,
    MinMax,
    json_field,
)
from anvil.lib.schemas import MinecraftBlockDescriptor

from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.color_grading import ColorGradingSettings
from anvil.api.pbr.cubemap import CubeMapSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.lighting import LightingSettings
from anvil.api.pbr.water import WaterSettings


# region Parts: objects nested inside components


class NoiseDescriptor(JsonObject):
    """The noise a noise gradient surface builder samples.

    Args:
        name (str): The name of the noise.
        first_octave (int): The first octave of the noise.
        amplitudes (list[float]): The amplitude of each octave, at least 1.
    """

    name: str = json_field()
    first_octave: int = json_field()
    amplitudes: Annotated[list[float], Length(minimum=1)] = json_field()


class NoiseBlockSpecifier(JsonObject):
    """A block placed where the noise is above a threshold, or inside a range.

    Args:
        block (MinecraftBlockDescriptor): The block placed.
        noise (str, optional): The noise sampled. Defaults to the builder's noise.
        threshold (float, optional): The block is placed where the noise is above this value. Set this or `range`.
        range (tuple[float, float], optional): The block is placed where the noise is inside this `(min, max)` range, each in [-1, 1]. Set this or `threshold`.
    """

    noise: str | None = json_field(default=None)
    threshold: float | None = json_field(default=None)
    range: Annotated[tuple[float, float], InRange(-1.0, 1.0), MinMax] | None = (
        json_field(default=None)
    )
    block: MinecraftBlockDescriptor = json_field()

    def __validate__(self) -> None:
        if self.threshold is None and self.range is None:
            raise ValueError("NoiseBlockSpecifier needs `threshold` or `range`.")


class Surface(JsonObject, abstract=True):
    """Base of the surface builder variants. Each variant fixes its own `type`."""

    type: str = json_field(init=False)


class OverworldSurface(Surface):
    """Controls the blocks used for the default Minecraft Overworld terrain generation.

    Args:
        foundation_material (MinecraftBlockDescriptor): The block used deep underground.
        mid_material (MinecraftBlockDescriptor): The block used in a layer below the surface.
        sea_floor_material (MinecraftBlockDescriptor): The block used as the floor of bodies of water.
        sea_material (MinecraftBlockDescriptor): The block used in bodies of water.
        top_material (MinecraftBlockDescriptor): The block used for the surface.
        sea_floor_depth (int, optional): How deep the sea floor material goes, up to 127.
    """

    type: str = json_field(default="minecraft:overworld", init=False)
    foundation_material: MinecraftBlockDescriptor = json_field()
    mid_material: MinecraftBlockDescriptor = json_field()
    top_material: MinecraftBlockDescriptor = json_field()
    sea_floor_material: MinecraftBlockDescriptor = json_field()
    sea_material: MinecraftBlockDescriptor = json_field()
    sea_floor_depth: Annotated[int, InRange(maximum=127)] | None = json_field(
        default=None
    )


class FrozenOceanSurface(OverworldSurface):
    """Similar to the overworld surface. Adds icebergs."""

    type: str = json_field(default="minecraft:frozen_ocean", init=False)


class MesaSurface(OverworldSurface):
    """Similar to the overworld surface. Adds colored strata and optional pillars.

    Args:
        clay_material (MinecraftBlockDescriptor): The base clay block.
        hard_clay_material (MinecraftBlockDescriptor): The hardened clay block.
        bryce_pillars (bool, optional): Whether to add Bryce pillars.
        has_forest (bool, optional): Whether to add a forest on top.
    """

    type: str = json_field(default="minecraft:mesa", init=False)
    clay_material: MinecraftBlockDescriptor = json_field()
    hard_clay_material: MinecraftBlockDescriptor = json_field()
    bryce_pillars: bool | None = json_field(default=None)
    has_forest: bool | None = json_field(default=None)


class SwampSurface(OverworldSurface):
    """Used to add decoration to the surface of swamp biomes such as water lilies.

    Args:
        max_puddle_depth_below_sea_level (int, optional): How deep puddles may go, up to 127.
    """

    type: str = json_field(default="minecraft:swamp", init=False)
    max_puddle_depth_below_sea_level: Annotated[int, InRange(maximum=127)] | None = (
        json_field(default=None)
    )


class CappedSurface(Surface):
    """Generates surface on blocks with non-solid blocks above or below.

    Args:
        beach_material (MinecraftBlockDescriptor): The block used for beaches.
        ceiling_materials (list[MinecraftBlockDescriptor]): Blocks used for ceilings, at least 1.
        floor_materials (list[MinecraftBlockDescriptor]): Blocks used for floors, at least 1.
        foundation_material (MinecraftBlockDescriptor): The block used deep underground.
        sea_material (MinecraftBlockDescriptor): The block used in bodies of water.
    """

    type: str = json_field(default="minecraft:capped", init=False)
    foundation_material: MinecraftBlockDescriptor = json_field()
    sea_material: MinecraftBlockDescriptor = json_field()
    beach_material: MinecraftBlockDescriptor = json_field()
    ceiling_materials: Annotated[list[MinecraftBlockDescriptor], Length(minimum=1)] = (
        json_field()
    )
    floor_materials: Annotated[list[MinecraftBlockDescriptor], Length(minimum=1)] = (
        json_field()
    )


class TheEndSurface(Surface):
    """Use default Minecraft End terrain generation."""

    type: str = json_field(default="minecraft:the_end", init=False)


class NoiseGradientSurface(Surface):
    """Places continuous bands of blocks according to a noise distribution.

    Args:
        noise_descriptor (NoiseDescriptor): The noise used by the surface builder.
        noise_block_specifiers (list[NoiseBlockSpecifier]): Which noise ranges map to which blocks, at least 1.
        non_replaceable_blocks (list[MinecraftBlockDescriptor], optional): Blocks the builder may not replace.
    """

    type: str = json_field(default="minecraft:noise_gradient", init=False)
    noise_descriptor: NoiseDescriptor = json_field()
    noise_block_specifiers: Annotated[list[NoiseBlockSpecifier], Length(minimum=1)] = (
        json_field()
    )
    non_replaceable_blocks: list[MinecraftBlockDescriptor] | None = json_field(
        default=None
    )


class SteepMaterialAdjustment(JsonObject):
    """Surface material for steep slopes.

    Args:
        material (MinecraftBlockDescriptor): The block used on steep slopes.
        north_slopes (bool, optional): Enable for north-facing slopes. Defaults to None.
        south_slopes (bool, optional): Enable for south-facing slopes. Defaults to None.
        east_slopes (bool, optional): Enable for east-facing slopes. Defaults to None.
        west_slopes (bool, optional): Enable for west-facing slopes. Defaults to None.
    """

    material: MinecraftBlockDescriptor = json_field()
    north_slopes: bool | None = json_field(default=None)
    south_slopes: bool | None = json_field(default=None)
    east_slopes: bool | None = json_field(default=None)
    west_slopes: bool | None = json_field(default=None)


class TopSlide(JsonObject):
    """Controls the top slide of mountain terrain.

    Args:
        enabled (bool): Whether top slide generation is enabled.
    """

    enabled: bool = json_field()


class BiomeReplacement(JsonObject):
    """One biome replacement.

    Args:
        targets (list[MinecraftBiomeTypes | str]): Biomes that are going to be replaced by the overriding biome. Target biomes must not contain namespaces.
        amount (float): Noise value used to determine whether or not the replacement is attempted, similar to a percentage. Must be in the range (0.0, 1.0].
        noise_frequency_scale (float): Scaling value used to alter the frequency of replacement attempts. A lower frequency will mean a bigger contiguous biome area that occurs less often. A higher frequency will mean smaller contiguous biome areas that occur more often. Must be in the range (0.0, 100.0].
        dimension (Dimension, optional): Dimension in which this replacement can happen: 'minecraft:overworld' or 'minecraft:nether'. Defaults to "minecraft:overworld".
    """

    targets: Annotated[list[MinecraftBiomeTypes | str], Length(minimum=1)] = (
        json_field()
    )
    amount: Annotated[float, InRange(0.0, 1.0, min_exclusive=True)] = json_field()
    noise_frequency_scale: Annotated[float, InRange(0.0, 100.0, min_exclusive=True)] = (
        json_field()
    )
    dimension: Literal[Dimension.Overworld, Dimension.Nether] = json_field(
        default=Dimension.Overworld
    )


class SurfaceAdjustmentMaterials(JsonObject):
    """The blocks a surface material adjustment uses while it is active.

    Args:
        foundation_material (MinecraftBlockDescriptor, optional): The block used deep underground.
        mid_material (MinecraftBlockDescriptor, optional): The block used in a layer below the surface.
        sea_floor_material (MinecraftBlockDescriptor, optional): The block used as the floor of bodies of water.
        sea_material (MinecraftBlockDescriptor, optional): The block used in bodies of water.
        top_material (MinecraftBlockDescriptor, optional): The block used for the surface.
    """

    foundation_material: MinecraftBlockDescriptor | None = json_field(default=None)
    mid_material: MinecraftBlockDescriptor | None = json_field(default=None)
    sea_floor_material: MinecraftBlockDescriptor | None = json_field(default=None)
    sea_material: MinecraftBlockDescriptor | None = json_field(default=None)
    top_material: MinecraftBlockDescriptor | None = json_field(default=None)


class GrassTint(JsonObject):
    """The color grass is tinted by on the map, for `BiomeMapTints`.

    Args:
        tint (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The tint color. Written as a hex color.
    """

    tint: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] = (
        json_field()
    )


class SurfaceMaterialAdjustment(JsonObject):
    """An adjustment to generated terrain, replacing blocks based on the specified settings.

    Args:
        height_range (tuple[float | str, float | str], optional): The range of heights [min, max] for which this adjustment applies. Each bound is a number or a Molang expression.
        noise_frequency_scale (float, optional): The scale to multiply by the position when accessing the noise value for the material adjustments.
        noise_range (tuple[float, float], optional): The range of noise values [min, max] for which this adjustment applies.
        materials (SurfaceAdjustmentMaterials): The blocks used while this adjustment is active.
    """

    height_range: tuple[float | str, float | str] | None = json_field(default=None)
    noise_frequency_scale: float | None = json_field(default=None)
    noise_range: tuple[float, float] | None = json_field(default=None)
    materials: SurfaceAdjustmentMaterials = json_field(
        default_factory=SurfaceAdjustmentMaterials
    )


# endregion

# region Components


class _BaseBiomeSurfaceBuilder(JsonComponent, abstract=True):
    """Shared fields and builders of the surface and subsurface builder components.

    Args:
        builder (Surface, optional): The surface builder to use. Set it directly or
            with one of the `set_*_builder` methods.
    """

    builder: Surface | None = json_field(default=None)

    def set_overworld_builder(
        self,
        *,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int | None = None,
    ):
        """Controls the blocks used for the default Minecraft Overworld terrain generation."""
        self.builder = OverworldSurface(
            foundation_material=foundation_material,
            mid_material=mid_material,
            sea_floor_material=sea_floor_material,
            sea_material=sea_material,
            top_material=top_material,
            sea_floor_depth=sea_floor_depth,
        )
        return self

    def set_frozen_ocean_builder(
        self,
        *,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int | None = None,
    ):
        """Similar to overworld_surface. Adds icebergs."""
        self.builder = FrozenOceanSurface(
            foundation_material=foundation_material,
            mid_material=mid_material,
            sea_floor_material=sea_floor_material,
            sea_material=sea_material,
            top_material=top_material,
            sea_floor_depth=sea_floor_depth,
        )
        return self

    def set_mesa_builder(
        self,
        *,
        clay_material: MinecraftBlockDescriptor,
        foundation_material: MinecraftBlockDescriptor,
        hard_clay_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        bryce_pillars: bool | None = None,
        has_forest: bool | None = None,
        sea_floor_depth: int | None = None,
    ):
        """Similar to overworld_surface. Adds colored strata and optional pillars."""
        self.builder = MesaSurface(
            clay_material=clay_material,
            foundation_material=foundation_material,
            hard_clay_material=hard_clay_material,
            mid_material=mid_material,
            sea_floor_material=sea_floor_material,
            sea_material=sea_material,
            top_material=top_material,
            bryce_pillars=bryce_pillars,
            has_forest=has_forest,
            sea_floor_depth=sea_floor_depth,
        )
        return self

    def set_swamp_builder(
        self,
        *,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int | None = None,
        max_puddle_depth_below_sea_level: int | None = None,
    ):
        """Used to add decoration to the surface of swamp biomes such as water lilies."""
        self.builder = SwampSurface(
            foundation_material=foundation_material,
            mid_material=mid_material,
            sea_floor_material=sea_floor_material,
            sea_material=sea_material,
            top_material=top_material,
            sea_floor_depth=sea_floor_depth,
            max_puddle_depth_below_sea_level=max_puddle_depth_below_sea_level,
        )
        return self

    def set_capped_builder(
        self,
        *,
        beach_material: MinecraftBlockDescriptor,
        ceiling_materials: list[MinecraftBlockDescriptor],
        floor_materials: list[MinecraftBlockDescriptor],
        foundation_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
    ):
        """Generates surface on blocks with non-solid blocks above or below."""
        self.builder = CappedSurface(
            beach_material=beach_material,
            ceiling_materials=ceiling_materials,
            floor_materials=floor_materials,
            foundation_material=foundation_material,
            sea_material=sea_material,
        )
        return self

    def set_end_builder(self):
        """Use default Minecraft End terrain generation."""
        self.builder = TheEndSurface()
        return self

    def set_noise_gradient_builder(
        self,
        *,
        noise_descriptor: NoiseDescriptor,
        noise_block_specifiers: list[NoiseBlockSpecifier],
        non_replaceable_blocks: list[MinecraftBlockDescriptor] | None = None,
    ):
        """Places continuous bands of blocks according to a noise distribution.

        Args:
            noise_descriptor (NoiseDescriptor): The NoiseDescriptor used by the surface builder.
            noise_block_specifiers (list[NoiseBlockSpecifier]): The noise block specifiers defining which ranges
                of noise are associated with which blocks.
            non_replaceable_blocks (list[MinecraftBlockDescriptor], optional): Blocks that the
                surface builder is not allowed to replace. Defaults to None.
        """
        self.builder = NoiseGradientSurface(
            noise_descriptor=noise_descriptor,
            noise_block_specifiers=noise_block_specifiers,
            non_replaceable_blocks=non_replaceable_blocks,
        )
        return self


class BiomeClimate(JsonComponent):
    """Sets the climate properties of the biome.

    Args:
        temperature (float, optional): Temperature affects a variety of visual and behavioral things, including snow and ice placement, sponge drying, and sky color. Between -50.0 and 50.0. Defaults to None.
        downfall (float, optional): Amount that precipitation affects colors and block changes. Setting to 0 will stop rain from falling in the biome. Between 0.0 and 1.0. Defaults to None.
        snow_accumulation (list[float], optional): Minimum and maximum snow level, each multiple of 0.125 is another snow layer. Exactly 2 values between 0.0 and 1.0. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_climate)
    """

    identifier = "minecraft:climate"

    temperature: Annotated[float, InRange(-50.0, 50.0)] | None = json_field(
        default=None
    )
    downfall: Annotated[float, Chance] | None = json_field(default=None)
    snow_accumulation: Annotated[list[float], Length(2, 2), Chance] | None = json_field(
        default=None
    )


class BiomeCreatureSpawnProbability(JsonComponent):
    """Sets the probability that creatures will spawn within the biome when a chunk is generated.

    Args:
        probability (float, optional): Probability between 0.0 and 0.75 of creatures spawning within the biome on chunk generation. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_creature_spawn_probability)
    """

    identifier = "minecraft:creature_spawn_probability"

    probability: Annotated[float, InRange(0.0, 0.75)] | None = json_field(default=None)


class BiomeHumidity(JsonComponent):
    """Forces a biome to either always be humid or never humid. Humidity affects the spread chance and spread rate of fire in the biome.

    Args:
        is_humid (bool, optional): Whether the biome is humid or not. Affects fire spread mechanics. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_humidity)
    """

    identifier = "minecraft:humidity"

    is_humid: bool | None = json_field(default=None)


class BiomeMapTints(JsonComponent):
    """Sets the color grass and foliage will be tinted by in this biome on the map.

    Args:
        foliage (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): Sets the color foliage will be tinted by in this biome on the map. Written as a hex color. Defaults to None.
        grass (GrassTint, optional): The color grass is tinted by in this biome on the map. Defaults to None. Set it with `set_grass`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_map_tints)
    """

    identifier = "minecraft:map_tints"

    foliage: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None = (
        json_field(default=None)
    )
    grass: GrassTint | None = json_field(default=None)

    def set_grass(
        self,
        *,
        tint: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
    ) -> "BiomeMapTints":
        """Sets the color grass is tinted by on the map. See `GrassTint` for the parameters."""
        self.grass = GrassTint(
            tint=tint,
        )
        return self


class BiomeMountainParameters(JsonComponent):
    """Noise parameters used to drive mountain terrain generation in Overworld.

    Args:
        steep_material_adjustment (SteepMaterialAdjustment, optional): Surface material for steep slopes. Defaults to None.
        top_slide (TopSlide, optional): Top slide settings. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_mountain_parameters)
    """

    identifier = "minecraft:mountain_parameters"

    steep_material_adjustment: SteepMaterialAdjustment | None = json_field(default=None)
    top_slide: TopSlide | None = json_field(default=None)

    def set_steep_material_adjustment(
        self,
        *,
        material: MinecraftBlockDescriptor,
        north_slopes: bool | None = None,
        south_slopes: bool | None = None,
        east_slopes: bool | None = None,
        west_slopes: bool | None = None,
    ):
        """Defines surface material for steep slopes."""
        self.steep_material_adjustment = SteepMaterialAdjustment(
            material=material,
            north_slopes=north_slopes,
            south_slopes=south_slopes,
            east_slopes=east_slopes,
            west_slopes=west_slopes,
        )
        return self

    def set_top_slide(self, *, enabled: bool):
        """Enable or disable top slide generation."""
        self.top_slide = TopSlide(enabled=enabled)
        return self


@deprecated("This is a pre-Caves and Cliffs component and is unused for custom biomes.")
class BiomeMultiNoiseGenerationRules(JsonComponent):
    """Controls how this biome is instantiated (and then potentially modified) during world generation of the nether.

    Args:
        target_altitude (float, optional): Altitude with which this biome should be generated, relative to other biomes. Defaults to None.
        target_humidity (float, optional): Humidity with which this biome should be generated, relative to other biomes. Defaults to None.
        target_temperature (float, optional): Temperature with which this biome should be generated, relative to other biomes. Defaults to None.
        target_weirdness (float, optional): Weirdness with which this biome should be generated, relative to other biomes. Defaults to None.
        weight (float, optional): Weight with which this biome should be generated, relative to other biomes. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_multinoise_generation_rules)
    """

    identifier = "minecraft:multinoise_generation_rules"

    target_altitude: float | None = json_field(default=None)
    target_humidity: float | None = json_field(default=None)
    target_temperature: float | None = json_field(default=None)
    target_weirdness: float | None = json_field(default=None)
    weight: float | None = json_field(default=None)


class BiomeNoiseGradient(JsonComponent):
    """Places continuous bands of blocks according to a noise distribution.
    This surface builder's processing has been implemented with sub-terrain height ranges in mind.

    Args:
        type (BiomeNoiseGradientBuilderType, optional): The builder type. Defaults to None.
        noise_descriptor (NoiseDescriptor, optional): The specification for the noise used by the surface builder. Defaults to None.
        noise_block_specifiers (list[NoiseBlockSpecifier], optional): Which ranges of noise are associated with which blocks.
        non_replaceable_blocks (list[MinecraftBlockDescriptor], optional): Blocks the surface builder may not replace. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_noise_gradient)
    """

    identifier = "minecraft:noise_gradient"

    type: BiomeNoiseGradientBuilderType | None = json_field(default=None)
    noise_descriptor: NoiseDescriptor | None = json_field(default=None)
    noise_block_specifiers: list[NoiseBlockSpecifier] = json_field(
        default_factory=list, omit_default=True
    )
    non_replaceable_blocks: list[MinecraftBlockDescriptor] | None = json_field(
        default=None
    )

    def set_type(self, *, builder_type: BiomeNoiseGradientBuilderType):
        """Sets the builder type for this noise gradient component."""
        self.type = builder_type
        return self

    def set_noise_descriptor(self, *, noise_descriptor: NoiseDescriptor):
        """Sets the noise descriptor specification for the surface builder."""
        self.noise_descriptor = noise_descriptor
        return self

    def set_noise_block_specifiers(self, *, specifiers: list[NoiseBlockSpecifier]):
        """Sets the noise block specifiers, replacing any already added. At least 1."""
        self.noise_block_specifiers = list(specifiers)
        return self

    def add_noise_block_specifier(self, *, specifier: NoiseBlockSpecifier):
        """Adds a noise block specifier associating a noise range or threshold with a block."""
        self.noise_block_specifiers.append(specifier)
        return self

    def set_non_replaceable_blocks(self, *, blocks: list[MinecraftBlockDescriptor]):
        """Sets the list of blocks that the surface builder is not allowed to replace."""
        self.non_replaceable_blocks = list(blocks)
        return self


@deprecated("This is a pre-Caves and Cliffs component and is unused for custom biomes.")
class BiomeOverworldGenerationRules(JsonComponent):
    """Controls how this biome is instantiated (and then potentially modified) during world generation of the overworld.

    Args:
        generate_for_climates (list[tuple[BiomeClimateCategory, int]], optional): The climate categories this biome can spawn for, as `[climate, weight]` pairs. Defaults to None.
        hills_transformation (str | list[tuple[str, int]], optional): What biome to switch to when converting to a hilly biome. Defaults to None.
        mutate_transformation (str | list[tuple[str, int]], optional): What biome to switch to when converting to a mutated biome. Defaults to None.
        river_transformation (str | list[tuple[str, int]], optional): What biome to switch to when converting to a river biome (if not the Vanilla 'river' biome). Defaults to None.
        shore_transformation (str | list[tuple[str, int]], optional): What biome to switch to when adjacent to an ocean biome. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_generation_rules)
    """

    identifier = "minecraft:overworld_generation_rules"

    generate_for_climates: list[tuple[BiomeClimateCategory, int]] | None = json_field(
        default=None
    )
    hills_transformation: str | list[tuple[str, int]] | None = json_field(default=None)
    mutate_transformation: str | list[tuple[str, int]] | None = json_field(default=None)
    river_transformation: str | list[tuple[str, int]] | None = json_field(default=None)
    shore_transformation: str | list[tuple[str, int]] | None = json_field(default=None)


@deprecated(
    "This is a pre-Caves and Cliffs component. It does not change overworld height, and currently only affects map item rendering."
)
class BiomeOverworldHeight(JsonComponent):
    """Noise parameters used to drive terrain height in the Overworld. Set either `noise_params` or `noise_type`.

    Args:
        noise_params (tuple[float, float], optional): First value is depth - more negative means deeper underwater, while more positive means higher. Second value is scale, which affects how much noise changes as it moves from the surface. Defaults to None.
        noise_type (BiomeNoiseType, optional): Specifies a preset based on a built-in setting rather than manually using noise_params. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_height)
    """

    identifier = "minecraft:overworld_height"

    noise_params: tuple[float, float] | None = json_field(default=None)
    noise_type: BiomeNoiseType | None = json_field(default=None)

    def __validate__(self) -> None:
        if self.noise_params is not None and self.noise_type is not None:
            raise ValueError("Set either noise_params or noise_type, not both.")


class BiomePartiallyFrozen(JsonComponent):
    """Impacts the temperature in a frozen biome, causing some areas to not be frozen. For example patchy ice or patchy snow.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_partially_frozen)
    """

    identifier = "minecraft:partially_frozen"


class BiomeReplaceBiomes(JsonComponent):
    """Replaces a specified portion of one or more Minecraft biomes.

    Args:
        replacements (list[BiomeReplacement], optional): The replacements. Set them directly or add them with `add_replacement`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_replace_biomes)
    """

    identifier = "minecraft:replace_biomes"

    replacements: list[BiomeReplacement] = json_field(
        default_factory=list, omit_default=True
    )

    def add_replacement(
        self,
        *,
        targets: list[MinecraftBiomeTypes | str],
        amount: float,
        noise_frequency_scale: float,
        dimension: Dimension = Dimension.Overworld,
    ):
        """Add a biome replacement configuration. See `BiomeReplacement` for the parameters.

        Returns:
            BiomeReplaceBiomes: Self for method chaining.
        """
        self.replacements.append(
            BiomeReplacement(
                targets=targets,
                amount=amount,
                noise_frequency_scale=noise_frequency_scale,
                dimension=dimension,
            )
        )
        return self


class BiomeSubSurfaceBuilder(_BaseBiomeSurfaceBuilder):
    """Allow specifying a minecraft:surface_builder to be applied to biomes located underneath regular terrain surface.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_subsurface_builder)
    """

    identifier = "minecraft:subsurface_builder"


class BiomeSurfaceBuilder(_BaseBiomeSurfaceBuilder):
    """Controls the materials used for terrain generation.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_builder)
    """

    identifier = "minecraft:surface_builder"


class BiomeSurfaceMaterialAdjustments(JsonComponent):
    """Specify fine-detail changes to blocks used in terrain generation (based on a noise function).

    Args:
        adjustments (list[SurfaceMaterialAdjustment], optional): The adjustments. Set them directly or add them with `add_adjustment`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_material_adjustments)
    """

    identifier = "minecraft:surface_material_adjustments"

    adjustments: list[SurfaceMaterialAdjustment] = json_field(
        default_factory=list, omit_default=True
    )

    def add_adjustment(
        self,
        *,
        height_range: tuple[float | str, float | str] | None = None,
        noise_frequency_scale: float | None = None,
        noise_range: tuple[float, float] | None = None,
        foundation_material: MinecraftBlockDescriptor | None = None,
        mid_material: MinecraftBlockDescriptor | None = None,
        sea_floor_material: MinecraftBlockDescriptor | None = None,
        sea_material: MinecraftBlockDescriptor | None = None,
        top_material: MinecraftBlockDescriptor | None = None,
    ):
        """Adds an adjustment. See `SurfaceMaterialAdjustment` and `SurfaceAdjustmentMaterials` for the parameters."""
        self.adjustments.append(
            SurfaceMaterialAdjustment(
                height_range=height_range,
                noise_frequency_scale=noise_frequency_scale,
                noise_range=noise_range,
                materials=SurfaceAdjustmentMaterials(
                    foundation_material=foundation_material,
                    mid_material=mid_material,
                    sea_floor_material=sea_floor_material,
                    sea_material=sea_material,
                    top_material=top_material,
                ),
            )
        )
        return self


class BiomeTags(JsonComponent):
    """Attach arbitrary string tags to this biome. Most biome tags are referenced by JSON settings, but some meanings of tags are directly implemented in the game's code.

    Args:
        tags (list[str | MinecraftBiomeTags], optional): Array of string tags used by other systems such as entity spawning. Common tags include: birch, cold, deep, desert, extreme_hills, flower_forest, forest, forest_generation, frozen, ice, ice_plains, jungle, hills, meadow, mesa, mountain, mutated, no_legacy_worldgen, ocean, pale_garden, plains, rare, swamp, taiga. Defaults to None.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_tags)
    """

    identifier = "minecraft:tags"

    tags: list[str | MinecraftBiomeTags] | None = json_field(default=None)


class BiomeVillageType(JsonComponent):
    """Determines the type of village for the Biome.

    Args:
        type (BiomeVillageTypes): The village type for this biome. Must be one of: "default", "desert", "ice", "savanna", "taiga".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_village_type)
    """

    identifier = "minecraft:village_type"

    type: BiomeVillageTypes = json_field()


# endregion

# region Client components


class BiomeClientComponent(JsonComponent, abstract=True):
    """Base class of the client biome components, written to the client biome file.
    `BiomeClient` takes only these and `BiomeServer` refuses them.
    """


class BiomeClientAmbientSounds(BiomeClientComponent):
    """Sets the ambient sounds of the biome. The sounds must be individual named sounds in
    `sounds.json`; `BiomeClient.ambient_sounds` adds the component and registers them.

    Args:
        addition (str, optional): Named sound that occasionally plays at the listener position.
        loop (str, optional): Named sound that loops while the listener is inside the biome.
        mood (str, optional): Named sound that rarely plays at a nearby air block when the light
            level is low. Without it, the biome uses `ambient.cave`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_ambient_sounds)
    """

    identifier = "minecraft:ambient_sounds"

    addition: str | None = json_field(default=None)
    loop: str | None = json_field(default=None)
    mood: str | None = json_field(default=None)


class BiomeClientAtmosphereIdentifier(BiomeClientComponent):
    """Sets the atmospherics used in Vibrant Visuals mode.

    Args:
        atmosphere_identifier (AtmosphericSettings | str): The atmospherics definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_atmosphere_identifier)
    """

    identifier = "minecraft:atmosphere_identifier"

    atmosphere_identifier: Annotated[AtmosphericSettings | str, AsString] = (
        json_field()
    )


class BiomeClientMusic(BiomeClientComponent):
    """Sets the music played in the biome. `BiomeClient.biome_music` adds the component and
    registers the music definitions.

    Args:
        music_definition (MusicCategory | str, optional): Music played in the biome. Without it
            the dimension decides; an empty string plays no music.
        underwater_music (MusicCategory | str, optional): Music played underwater in the biome.
        volume_multiplier (float, optional): Applied gradually to the music volume, from 0 to 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_biome_music)
    """

    identifier = "minecraft:biome_music"

    music_definition: MusicCategory | str | None = json_field(default=None)
    underwater_music: MusicCategory | str | None = json_field(default=None)
    volume_multiplier: Annotated[float, Chance] | None = json_field(default=None)


class BiomeClientColorGradingIdentifier(BiomeClientComponent):
    """Sets the color grading used in Vibrant Visuals mode.

    Args:
        color_grading_identifier (ColorGradingSettings | str): The color grading definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_color_grading_identifier)
    """

    identifier = "minecraft:color_grading_identifier"

    color_grading_identifier: Annotated[ColorGradingSettings | str, AsString] = (
        json_field()
    )


class BiomeClientCubemapIdentifier(BiomeClientComponent):
    """Sets the cubemap used for the Vibrant Visuals skybox lighting.

    Args:
        cubemap_identifier (CubeMapSettings | str): The cubemap definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_cubemap_identifier)
    """

    identifier = "minecraft:cubemap_identifier"

    cubemap_identifier: Annotated[CubeMapSettings | str, AsString] = json_field()


class BiomeClientDryFoliageColor(BiomeClientComponent):
    """Sets the dry foliage color.

    Args:
        color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The dry foliage color. Written as a hex color.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_dry_foliage_color)
    """

    identifier = "minecraft:dry_foliage_color"

    color: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] = (
        json_field()
    )


class BiomeClientFogAppearance(BiomeClientComponent):
    """Sets the fog used during rendering.

    Args:
        fog_identifier (FogSettings | str): The fog definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_fog_appearance)
    """

    identifier = "minecraft:fog_appearance"

    fog_identifier: Annotated[FogSettings | str, AsString] = json_field()


class BiomeClientFoliageAppearance(BiomeClientComponent):
    """Sets the foliage color or color map.

    Args:
        color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | FoliageColorMap): A color, written as hex, or a color map name, written
            as `{"color_map": name}`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_foliage_appearance)
    """

    identifier = "minecraft:foliage_appearance"

    color: (
        Annotated[FoliageColorMap, ColorMap]
        | Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex]
    ) = json_field()


class BiomeClientGrassAppearance(BiomeClientComponent):
    """Sets the grass color or color map.

    Args:
        color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | GrassColorMap): A color, written as hex, or a color map name, written
            as `{"color_map": name}`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_grass_appearance)
    """

    identifier = "minecraft:grass_appearance"

    color: (
        Annotated[GrassColorMap, ColorMap]
        | Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex]
    ) = json_field()


class BiomeClientLightingIdentifier(BiomeClientComponent):
    """Sets the lighting used in Vibrant Visuals mode.

    Args:
        lighting_identifier (LightingSettings | str): The lighting definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_lighting_identifier)
    """

    identifier = "minecraft:lighting_identifier"

    lighting_identifier: Annotated[LightingSettings | str, AsString] = json_field()


class BiomeClientPrecipitation(BiomeClientComponent):
    """Sets the precipitation visuals. Set at most one of them.

    Args:
        ash (float, optional): Density of ash, as in the soul sand valley.
        blue_spores (float, optional): Density of blue spores, as in the warped forest.
        red_spores (float, optional): Density of red spores, as in the crimson forest.
        white_ash (float, optional): Density of white ash, as in the basalt deltas.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_precipitation)
    """

    identifier = "minecraft:precipitation"

    ash: float | None = json_field(default=None)
    blue_spores: float | None = json_field(default=None)
    red_spores: float | None = json_field(default=None)
    white_ash: float | None = json_field(default=None)

    def __validate__(self) -> None:
        values = (self.ash, self.blue_spores, self.red_spores, self.white_ash)
        if sum(value is not None for value in values) > 1:
            raise ValueError(
                "BiomeClientPrecipitation takes at most one precipitation type."
            )


class BiomeClientSkyColor(BiomeClientComponent):
    """Sets the sky color.

    Args:
        sky_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The sky color. Written as a hex color.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_sky_color)
    """

    identifier = "minecraft:sky_color"

    sky_color: Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] = (
        json_field()
    )


class BiomeClientWaterAppearance(BiomeClientComponent):
    """Sets the water surface color.

    Args:
        surface_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): The water surface color. Written as a hex color.
        surface_opacity (float, optional): From 0, invisible, to 1, opaque.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_appearance)
    """

    identifier = "minecraft:water_appearance"

    surface_color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None
    ) = json_field(default=None)
    surface_opacity: Annotated[float, Chance] | None = json_field(default=None)


class BiomeClientWaterIdentifier(BiomeClientComponent):
    """Sets the water rendering used in Vibrant Visuals mode.

    Args:
        water_identifier (WaterSettings | str): The water definition.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_identifier)
    """

    identifier = "minecraft:water_identifier"

    water_identifier: Annotated[WaterSettings | str, AsString] = json_field()


# endregion
