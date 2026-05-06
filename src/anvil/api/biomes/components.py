from typing import Literal, overload
from warnings import deprecated

from anvil.api.core.components import Component
from anvil.api.core.enums import Dimension
from anvil.api.core.types import Color, HexRGB
from anvil.api.vanilla.biomes import MinecraftBiomeTags, MinecraftBiomeTypes
from anvil.lib.format_versions import BIOME_SERVER_VERSION
from anvil.lib.lib import AnvilFormatter
from anvil.lib.schemas import MinecraftBlockDescriptor

BiomeNoiseType = Literal[
    "beach",
    "deep_ocean",
    "default",
    "default_mutated",
    "extreme",
    "highlands",
    "less_extreme",
    "lowlands",
    "mountains",
    "mushroom",
    "ocean",
    "river",
    "stone_beach",
    "swamp",
    "taiga",
]

BiomeNoiseGradientBuilderType = Literal[
    "minecraft:capped",
    "minecraft:frozen_ocean",
    "minecraft:mesa",
    "minecraft:noise_gradient",
    "minecraft:overworld",
    "minecraft:swamp",
    "minecraft:the_end",
]


class _BaseBiomeSurfaceBuilder(Component):
    def _validate_materials(self, materials: list[MinecraftBlockDescriptor]):
        for material in materials:
            if not isinstance(material, MinecraftBlockDescriptor):
                raise ValueError(
                    "All materials must be MinecraftBlockDescriptor instances"
                )

    def _validate_sea_floor_depth(self, sea_floor_depth: int = None):
        if sea_floor_depth is not None:
            if not isinstance(sea_floor_depth, int):
                raise ValueError("Sea floor depth must be an integer")
            if sea_floor_depth > 127:
                raise ValueError("Sea floor depth must be <= 127")

    def set_overworld_builder(
        self,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int = None,
    ):
        """Controls the blocks used for the default Minecraft Overworld terrain generation."""
        self._validate_materials(
            [
                foundation_material,
                mid_material,
                top_material,
                sea_floor_material,
                sea_material,
            ]
        )
        self._validate_sea_floor_depth(sea_floor_depth)

        builder = {
            "type": "minecraft:overworld",
            "foundation_material": foundation_material,
            "mid_material": mid_material,
            "top_material": top_material,
            "sea_floor_material": sea_floor_material,
            "sea_material": sea_material,
        }
        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth

        self._add_field("builder", builder)
        return self

    def set_frozen_ocean_builder(
        self,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int = None,
    ):
        """Similar to overworld_surface. Adds icebergs."""
        self._validate_materials(
            [
                foundation_material,
                mid_material,
                top_material,
                sea_floor_material,
                sea_material,
            ]
        )
        self._validate_sea_floor_depth(sea_floor_depth)

        builder = {
            "type": "minecraft:frozen_ocean",
            "foundation_material": foundation_material,
            "mid_material": mid_material,
            "top_material": top_material,
            "sea_floor_material": sea_floor_material,
            "sea_material": sea_material,
        }
        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth

        self._add_field("builder", builder)
        return self

    def set_mesa_builder(
        self,
        clay_material: MinecraftBlockDescriptor,
        foundation_material: MinecraftBlockDescriptor,
        hard_clay_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        bryce_pillars: bool = None,
        has_forest: bool = None,
        sea_floor_depth: int = None,
    ):
        """Similar to overworld_surface. Adds colored strata and optional pillars."""
        self._validate_materials(
            [
                foundation_material,
                mid_material,
                top_material,
                sea_floor_material,
                sea_material,
                clay_material,
                hard_clay_material,
            ]
        )
        self._validate_sea_floor_depth(sea_floor_depth)

        if bryce_pillars is not None and not isinstance(bryce_pillars, bool):
            raise ValueError("Bryce pillars must be a boolean")
        if has_forest is not None and not isinstance(has_forest, bool):
            raise ValueError("Has forest must be a boolean")

        builder = {
            "type": "minecraft:mesa",
            "foundation_material": foundation_material,
            "mid_material": mid_material,
            "top_material": top_material,
            "sea_floor_material": sea_floor_material,
            "sea_material": sea_material,
            "clay_material": clay_material,
            "hard_clay_material": hard_clay_material,
        }
        if bryce_pillars is not None:
            builder["bryce_pillars"] = bryce_pillars
        if has_forest is not None:
            builder["has_forest"] = has_forest
        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth

        self._add_field("builder", builder)
        return self

    def set_swamp_builder(
        self,
        foundation_material: MinecraftBlockDescriptor,
        mid_material: MinecraftBlockDescriptor,
        sea_floor_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
        top_material: MinecraftBlockDescriptor,
        sea_floor_depth: int = None,
        max_puddle_depth_below_sea_level: int = None,
    ):
        """Used to add decoration to the surface of swamp biomes such as water lilies."""
        self._validate_materials(
            [
                foundation_material,
                mid_material,
                top_material,
                sea_floor_material,
                sea_material,
            ]
        )
        self._validate_sea_floor_depth(sea_floor_depth)

        if max_puddle_depth_below_sea_level is not None:
            if not isinstance(max_puddle_depth_below_sea_level, int):
                raise ValueError("Max puddle depth below sea level must be an integer")
            if max_puddle_depth_below_sea_level > 127:
                raise ValueError("Max puddle depth below sea level must be <= 127")

        builder = {
            "type": "minecraft:swamp",
            "foundation_material": foundation_material,
            "mid_material": mid_material,
            "top_material": top_material,
            "sea_floor_material": sea_floor_material,
            "sea_material": sea_material,
        }
        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth
        if max_puddle_depth_below_sea_level is not None:
            builder["max_puddle_depth_below_sea_level"] = (
                max_puddle_depth_below_sea_level
            )

        self._add_field("builder", builder)
        return self

    def set_capped_builder(
        self,
        beach_material: MinecraftBlockDescriptor,
        ceiling_materials: list[MinecraftBlockDescriptor],
        floor_materials: list[MinecraftBlockDescriptor],
        foundation_material: MinecraftBlockDescriptor,
        sea_material: MinecraftBlockDescriptor,
    ):
        """Generates surface on blocks with non-solid blocks above or below."""
        if not isinstance(ceiling_materials, list) or len(ceiling_materials) < 1:
            raise ValueError("Ceiling materials must be a list with at least 1 item")
        if not isinstance(floor_materials, list) or len(floor_materials) < 1:
            raise ValueError("Floor materials must be a list with at least 1 item")
        self._validate_materials(
            [
                foundation_material,
                sea_material,
                beach_material,
                *ceiling_materials,
                *floor_materials,
            ]
        )

        builder = {
            "type": "minecraft:capped",
            "foundation_material": foundation_material,
            "sea_material": sea_material,
            "beach_material": beach_material,
            "ceiling_materials": [material for material in ceiling_materials],
            "floor_materials": [material for material in floor_materials],
        }
        self._add_field("builder", builder)
        return self

    def set_end_builder(self):
        """Use default Minecraft End terrain generation."""
        self._add_field("builder", {"type": "minecraft:the_end"})
        return self

    def set_noise_gradient_builder(
        self,
        noise_block_specifiers: list[dict],
        noise_descriptor: dict = None,
        non_replaceable_blocks: list[MinecraftBlockDescriptor] = None,
    ):
        """Places continuous bands of blocks according to a noise distribution.

        Parameters:
            noise_block_specifiers (list[dict]): The noise block specifiers defining which ranges
                of noise are associated with which blocks. Each dict should contain 'noise_range'
                (a [min, max] pair valid on [0, 1]) and 'block' (a MinecraftBlockDescriptor).
                Must have at least 1 item.
            noise_descriptor (dict, optional): The specification for the noise used by the
                surface builder. Defaults to None.
            non_replaceable_blocks (list[MinecraftBlockDescriptor], optional): Blocks that the
                surface builder is not allowed to replace. Defaults to None.
        """
        if (
            not isinstance(noise_block_specifiers, list)
            or len(noise_block_specifiers) < 1
        ):
            raise ValueError(
                "noise_block_specifiers must be a list with at least 1 item"
            )

        builder = {
            "type": "minecraft:noise_gradient",
            "noise_block_specifiers": noise_block_specifiers,
        }

        if noise_descriptor is not None:
            if not isinstance(noise_descriptor, dict):
                raise ValueError("noise_descriptor must be a dictionary")
            builder["noise_descriptor"] = noise_descriptor

        if non_replaceable_blocks is not None:
            if not isinstance(non_replaceable_blocks, list):
                raise ValueError("non_replaceable_blocks must be a list")
            for block in non_replaceable_blocks:
                if not isinstance(block, MinecraftBlockDescriptor):
                    raise ValueError(
                        "All non_replaceable_blocks must be MinecraftBlockDescriptor instances"
                    )
            builder["non_replaceable_blocks"] = non_replaceable_blocks

        self._add_field("builder", builder)
        return self


class BiomeClimate(Component):
    _identifier = "minecraft:climate"

    def __init__(
        self,
        temperature: float = None,
        downfall: float = None,
        snow_accumulation: list[float] = None,
    ) -> None:
        """Sets the climate properties of the biome.

        Parameters:
            temperature (float, optional): Temperature affects a variety of visual and behavioral things, including snow and ice placement, sponge drying, and sky color. Defaults to None.
            downfall (float, optional): Amount that precipitation affects colors and block changes. Setting to 0 will stop rain from falling in the biome. Defaults to None.
            snow_accumulation (list[float], optional): Minimum and maximum snow level, each multiple of 0.125 is another snow layer Value must have at least 2 items. Value must have at most 2 items. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_climate
        """
        super().__init__("climate")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if temperature is not None:
            if not (-50.0 <= temperature <= 50.0):
                raise ValueError("Temperature must be between -50.0 and 50.0")
            self._add_field("temperature", temperature)

        if downfall is not None:
            if not (0.0 <= downfall <= 1.0):
                raise ValueError("Downfall must be between 0.0 and 1.0")
            self._add_field("downfall", downfall)

        if snow_accumulation is not None:
            if len(snow_accumulation) != 2:
                raise ValueError("Snow accumulation must be a list of two values.")
            for val in snow_accumulation:
                if not (0.0 <= val <= 1.0):
                    raise ValueError(
                        "Snow accumulation values must be between 0.0 and 1.0"
                    )
            self._add_field("snow_accumulation", snow_accumulation)


class BiomeCreatureSpawnProbability(Component):
    _identifier = "minecraft:creature_spawn_probability"

    def __init__(self, probability: float = None) -> None:
        """Sets the probability that creatures will spawn within the biome when a chunk is generated.

        Parameters:
            probability (float, optional): Probability between 0.0 and 0.75 of creatures spawning within the biome on chunk generation. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_creature_spawn_probability
        """
        super().__init__("creature_spawn_probability")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if probability is not None:
            if not (0.0 <= probability <= 0.75):
                raise ValueError("Probability must be between 0.0 and 0.75")
            self._add_field("probability", probability)


class BiomeHumidity(Component):
    _identifier = "minecraft:humidity"

    def __init__(self, is_humid: bool = None) -> None:
        """Forces a biome to either always be humid or never humid. Humidity affects the spread chance and spread rate of fire in the biome.

        Parameters:
            is_humid (bool, optional): Whether the biome is humid or not. Affects fire spread mechanics. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_humidity
        """
        super().__init__("humidity")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if is_humid is not None:
            if not isinstance(is_humid, bool):
                raise ValueError("is_humid must be a boolean value")
            self._add_field("is_humid", is_humid)


class BiomeMapTints(Component):
    _identifier = "minecraft:map_tints"

    def __init__(self, foliage: Color = None, grass: dict = None) -> None:
        """Sets the color grass and foliage will be tinted by in this biome on the map.

        Parameters:
            foliage (Color, optional): Sets the color foliage will be tinted by in this biome on the map. Can be a string or array of numbers. Defaults to None.
            grass (dict, optional): Controls whether the grass will use a custom tint color or a noise based tint color. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_map_tints
        """
        super().__init__("map_tints")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if foliage is not None:
            self._add_field("foliage", AnvilFormatter.convert_color(foliage, HexRGB))

        if grass is not None:
            if not isinstance(grass, dict):
                raise ValueError("Grass must be a dictionary")
            self._add_field("grass", grass)


class BiomeMountainParameters(Component):
    _identifier = "minecraft:mountain_parameters"

    def __init__(
        self,
    ) -> None:
        """Noise parameters used to drive mountain terrain generation in Overworld.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_mountain_parameters
        """
        super().__init__("mountain_parameters")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

    def steep_material_adjustment(
        self,
        block: MinecraftBlockDescriptor,
        north_slopes: bool = None,
        south_slopes: bool = None,
        east_slopes: bool = None,
        west_slopes: bool = None,
    ) -> None:
        """Defines surface material for steep slopes.

        Parameters:
            block (MinecraftBlockDescriptor): The block material definition.
            north_slopes (bool, optional): Enable for north-facing slopes. Defaults to None.
            south_slopes (bool, optional): Enable for south-facing slopes. Defaults to None.
            east_slopes (bool, optional): Enable for east-facing slopes. Defaults to None.
            west_slopes (bool, optional): Enable for west-facing slopes. Defaults to None.
        """
        steep = {"steep_material_adjustment": {}}

        if north_slopes is not None:
            if not isinstance(north_slopes, bool):
                raise ValueError("North slopes setting must be a boolean")
            steep["steep_material_adjustment"]["north_slopes"] = north_slopes

        if south_slopes is not None:
            if not isinstance(south_slopes, bool):
                raise ValueError("South slopes setting must be a boolean")
            steep["steep_material_adjustment"]["south_slopes"] = south_slopes

        if east_slopes is not None:
            if not isinstance(east_slopes, bool):
                raise ValueError("East slopes setting must be a boolean")
            steep["steep_material_adjustment"]["east_slopes"] = east_slopes

        if west_slopes is not None:
            if not isinstance(west_slopes, bool):
                raise ValueError("West slopes setting must be a boolean")
            steep["steep_material_adjustment"]["west_slopes"] = west_slopes

        if not isinstance(block, MinecraftBlockDescriptor):
            raise ValueError(
                "Material name must be a MinecraftBlockDescriptor instance"
            )

        self._component.update(steep)

        return self

    def set_top_slide(self, enabled: bool):
        """Enable or disable top slide generation."""
        if not isinstance(enabled, bool):
            raise ValueError("Enabled must be a boolean value")
        self._add_field("top_slide", {"enabled": enabled})
        return self


@deprecated("This is a pre-Caves and Cliffs component and is unused for custom biomes.")
class BiomeMultiNoiseGenerationRules(Component):
    _identifier = "minecraft:multinoise_generation_rules"

    def __init__(self) -> None:
        """Controls how this biome is instantiated (and then potentially modified) during world generation of the nether.

        Parameters:
            target_altitude (float, optional): Altitude with which this biome should be generated, relative to other biomes. Defaults to None.
            target_humidity (float, optional): Humidity with which this biome should be generated, relative to other biomes. Defaults to None.
            target_temperature (float, optional): Temperature with which this biome should be generated, relative to other biomes. Defaults to None.
            target_weirdness (float, optional): Weirdness with which this biome should be generated, relative to other biomes. Defaults to None.
            weight (float, optional): Weight with which this biome should be generated, relative to other biomes. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_multinoise_generation_rules
        """
        super().__init__("multinoise_generation_rules")


@deprecated("This is a pre-Caves and Cliffs component and is unused for custom biomes.")
class BiomeOverworldGenerationRules(Component):
    _identifier = "minecraft:overworld_generation_rules"

    def __init__(self) -> None:
        """Controls how this biome is instantiated (and then potentially modified) during world generation of the overworld.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_generation_rules
        """
        super().__init__("overworld_generation_rules")


@deprecated(
    "This is a pre-Caves and Cliffs component. It does not change overworld height, and currently only affects map item rendering."
)
class BiomeOverworldHeight(Component):
    _identifier = "minecraft:overworld_height"

    @overload
    def __init__(
        self,
        noise_params: tuple[float, float],
    ) -> None:
        """Noise parameters used to drive terrain height in the Overworld.

        Parameters:
            noise_params (tuple[float, float]): First value is depth - more negative means deeper underwater, while more positive means higher. Second value is scale, which affects how much noise changes as it moves from the surface. Value must have at least 2 items. Value must have at most 2 items.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_height
        """
        ...

    @overload
    def __init__(self, noise_type: BiomeNoiseType) -> None:
        """Noise parameters used to drive terrain height in the Overworld.

        Parameters:
            noise_type (BiomeNoiseType): Specifies a preset based on a built-in setting rather than manually using noise_params.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_height
        """
        ...

    def __init__(
        self,
        arg: tuple[float, float] | BiomeNoiseType | None = None,
    ) -> None:
        super().__init__("overworld_height")
        if arg is not None:
            if isinstance(arg, tuple):
                if len(arg) != 2:
                    raise ValueError("Noise params must have exactly 2 values")
                for param in arg:
                    if not isinstance(param, (int, float)):
                        raise ValueError("All noise params must be numbers")
                self._add_field("noise_params", list(arg))
            elif isinstance(arg, str):
                if arg not in BiomeNoiseType.__args__:
                    raise ValueError(
                        f"Noise type must be one of: {BiomeNoiseType}. Got {arg}"
                    )
                self._add_field("noise_type", arg)


class BiomeReplaceBiomes(Component):
    _identifier = "minecraft:replace_biomes"

    def __init__(self) -> None:
        """Replaces a specified portion of one or more Minecraft biomes.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_replace_biomes
        """
        super().__init__("replace_biomes")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")
        self._replacements = []

    def add_replacement(
        self,
        targets: list[MinecraftBiomeTypes | str],
        amount: float,
        noise_frequency_scale: float,
        dimension: Dimension = Dimension.Overworld,
    ):
        """Add a biome replacement configuration.

        Parameters:
            targets (list[MinecraftBiomeTypes | str]): Biomes that are going to be replaced by the overriding biome. Target biomes must not contain namespaces.
            amount (float): Noise value used to determine whether or not the replacement is attempted, similar to a percentage. Must be in the range (0.0, 1.0].
            noise_frequency_scale (float): Scaling value used to alter the frequency of replacement attempts. A lower frequency will mean a bigger contiguous biome area that occurs less often. A higher frequency will mean smaller contiguous biome areas that occur more often. Must be in the range (0.0, 100.0].
            dimension (Dimension, optional): Dimension in which this replacement can happen. Must be 'minecraft:overworld'. Defaults to "minecraft:overworld".

        Returns:
            BiomeReplaceBiomes: Self for method chaining.
        """
        # Validate targets
        if not isinstance(targets, list):
            raise ValueError("Targets must be a list of MinecraftBiomeTypes or strings")
        if len(targets) < 1:
            raise ValueError("Targets must have at least 1 item")

        for target in targets:
            if not isinstance(target, (MinecraftBiomeTypes, str)):
                raise ValueError("All targets must be MinecraftBiomeTypes or strings")

        # Validate amount
        if not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")
        if not (0.0 < amount <= 1.0):
            raise ValueError("Amount must be in the range [0.0, 1.0)")

        # Validate noise_frequency_scale
        if not isinstance(noise_frequency_scale, (int, float)):
            raise ValueError("Noise frequency scale must be a number")
        if not (0.0 < noise_frequency_scale <= 100.0):
            raise ValueError("Noise frequency scale must be in the range [0.0, 100.0]")

        # Validate dimension
        if not isinstance(dimension, Dimension):
            raise ValueError("Dimension must be a Dimension")
        if dimension != Dimension.Overworld:
            raise ValueError("Dimension must be 'minecraft:overworld'")

        replacement = {
            "targets": targets,
            "amount": amount,
            "noise_frequency_scale": noise_frequency_scale,
            "dimension": dimension,
        }

        self._replacements.append(replacement)
        self._add_field("replacements", self._replacements)

        return self


class BiomeSurfaceMaterialAdjustments(Component):
    _identifier = "minecraft:surface_material_adjustments"

    def __init__(self):
        """Specify fine-detail changes to blocks used in terrain generation (based on a noise function).

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_material_adjustments
        """
        super().__init__("minecraft:surface_material_adjustments")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        self._adjustments = []

    def add_adjustment(
        self,
        height_range: tuple[int, int] = None,
        noise_frequency_scale: float = None,
        noise_range: tuple[float, float] = None,
        foundation_material: MinecraftBlockDescriptor = None,
        mid_material: MinecraftBlockDescriptor = None,
        sea_floor_material: MinecraftBlockDescriptor = None,
        sea_material: MinecraftBlockDescriptor = None,
        top_material: MinecraftBlockDescriptor = None,
    ):
        """An adjustment to generated terrain, replacing blocks based on the specified settings.
        Parameters:
            height_range (tuple[int, int]): Defines a range of noise values [min, max] for which this adjustment should be applied. Value must have at least 2 items. Value must have at most 2 items.
            noise_frequency_scale (float): The scale to multiply by the position when accessing the noise value for the material adjustments.
            noise_range (tuple[float, float]): Defines a range of noise values [min, max] for which this adjustment should be applied. Value must have at least 2 items. Value must have at most 2 items.
            foundation_material (MinecraftBlockDescriptor): Controls the block type used deep underground in this biome when this adjustment is active.
            mid_material (MinecraftBlockDescriptor): Controls the block type used in a layer below the surface of this biome when this adjustment is active.
            sea_floor_material (MinecraftBlockDescriptor): Controls the block type used as a floor for bodies of water in this biome when this adjustment is active.
            sea_material (MinecraftBlockDescriptor): Controls the block type used in the bodies of water in this biome when this adjustment is active.
            top_material (MinecraftBlockDescriptor): Controls the block type used for the surface of this biome when this adjustment is active.
        """

        if height_range is not None and (
            not isinstance(height_range, (list, tuple))
            or len(height_range) != 2
            or any(not isinstance(val, int) for val in height_range)
        ):
            raise ValueError("Height range must be a list or tuple of two integers")

        if noise_frequency_scale is not None and not isinstance(
            noise_frequency_scale, (int, float)
        ):
            raise ValueError("Noise frequency scale must be a number")

        if noise_range is not None and (
            not isinstance(noise_range, (list, tuple))
            or len(noise_range) != 2
            or any(not isinstance(val, (int, float)) for val in noise_range)
        ):
            raise ValueError("Noise range must be a list or tuple of two floats")

        for material in [
            foundation_material,
            mid_material,
            sea_floor_material,
            sea_material,
            top_material,
        ]:
            if material is not None and not isinstance(
                material, MinecraftBlockDescriptor
            ):
                raise ValueError(
                    "All materials must be MinecraftBlockDescriptor instances"
                )

        adjustment = {
            "height_range": height_range,
            "noise_frequency_scale": noise_frequency_scale,
            "noise_range": noise_range,
            "materials": {
                "foundation_material": foundation_material,
                "mid_material": mid_material,
                "sea_floor_material": sea_floor_material,
                "sea_material": sea_material,
                "top_material": top_material,
            },
        }

        self._adjustments.append(adjustment)
        self._add_field("adjustments", self._adjustments)

        return self


class BiomeSurfaceBuilder(_BaseBiomeSurfaceBuilder):
    _identifier = "minecraft:surface_builder"

    def __init__(self):
        """Controls the materials used for terrain generation.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_builder
        """
        super().__init__("surface_builder")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")


class BiomeSubSurfaceBuilder(_BaseBiomeSurfaceBuilder):
    _identifier = "minecraft:subsurface_builder"

    def __init__(self):
        """Allow specifying a minecraft:surface_builder to be applied to biomes located underneath regular terrain surface.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_subsurface_builder
        """
        super().__init__("subsurface_builder")
        self._enforce_version(BIOME_SERVER_VERSION, "1.26.20")


class BiomeNoiseGradient(Component):
    _identifier = "minecraft:noise_gradient"

    def __init__(self):
        """Places continuous bands of blocks according to a noise distribution.
        This surface builder's processing has been implemented with sub-terrain height ranges in mind.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_noise_gradient
        """
        super().__init__("noise_gradient")
        self._enforce_version(BIOME_SERVER_VERSION, "1.26.20")
        self._noise_block_specifiers = []

    def noise_type(self, builder_type: BiomeNoiseGradientBuilderType):
        """Sets the builder type for this noise gradient component.

        Parameters:
            builder_type (BiomeNoiseGradientBuilderType): The type of builder to use.
        """
        valid_types = [
            "minecraft:capped",
            "minecraft:frozen_ocean",
            "minecraft:mesa",
            "minecraft:noise_gradient",
            "minecraft:overworld",
            "minecraft:swamp",
            "minecraft:the_end",
        ]
        if builder_type not in valid_types:
            raise ValueError(f"Builder type must be one of: {valid_types}")
        self._add_field("type", builder_type)
        return self

    def noise_block_specifier(
        self,
        noise_range: tuple[float, float],
        block: MinecraftBlockDescriptor,
    ):
        """Add a noise block specifier associating a noise range with a block.
        The ranges provided are valid on the interval [0, 1] and may overlap at their endpoints.
        At least 1 specifier is required.

        Parameters:
            noise_range (tuple[float, float]): The [min, max] noise range valid on [0.0, 1.0].
            block (MinecraftBlockDescriptor): The block to place within this noise range.
        """
        if (
            not isinstance(noise_range, (list, tuple))
            or len(noise_range) != 2
            or any(not isinstance(v, (int, float)) for v in noise_range)
        ):
            raise ValueError("noise_range must be a list or tuple of two numbers")
        for val in noise_range:
            if not (0.0 <= val <= 1.0):
                raise ValueError("noise_range values must be in [0.0, 1.0]")
        if not isinstance(block, MinecraftBlockDescriptor):
            raise ValueError("block must be a MinecraftBlockDescriptor instance")

        self._noise_block_specifiers.append(
            {"noise_range": list(noise_range), "block": block}
        )
        self._add_field("noise_block_specifiers", self._noise_block_specifiers)
        return self

    def noise_descriptor(self, noise_descriptor: dict):
        """Set the noise descriptor specification for the surface builder.

        Parameters:
            noise_descriptor (dict): The specification for the noise used by the surface builder.
        """
        if not isinstance(noise_descriptor, dict):
            raise ValueError("noise_descriptor must be a dictionary")
        self._add_field("noise_descriptor", noise_descriptor)
        return self

    def non_replaceable_block(self, blocks: list[MinecraftBlockDescriptor]):
        """Add a block to the list of blocks that the surface builder is not allowed to replace.
        Leaving this list empty allows replacement of any non-air block.

        Parameters:
            blocks (list[MinecraftBlockDescriptor]): The blocks to prevent replacement of.
        """
        if not isinstance(blocks, list):
            raise ValueError(
                "blocks must be a list of MinecraftBlockDescriptor instances"
            )
        if not all(isinstance(block, MinecraftBlockDescriptor) for block in blocks):
            raise ValueError(
                "All elements in blocks must be MinecraftBlockDescriptor instances"
            )

        self._add_field("non_replaceable_blocks", blocks)
        return self


class BiomeTags(Component):
    _identifier = "minecraft:tags"

    def __init__(self, tags: list[str | MinecraftBiomeTags] = None) -> None:
        """Attach arbitrary string tags to this biome. Most biome tags are referenced by JSON settings, but some meanings of tags are directly implemented in the game's code.

        Parameters:
            tags (list[str | MinecraftBiomeTags], optional): Array of string tags used by other systems such as entity spawning. Common tags include: birch, cold, deep, desert, extreme_hills, flower_forest, forest, forest_generation, frozen, ice, ice_plains, jungle, hills, meadow, mesa, mountain, mutated, no_legacy_worldgen, ocean, pale_garden, plains, rare, swamp, taiga. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_tags
        """
        super().__init__("tags")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list of strings")

            for tag in tags:
                if not isinstance(tag, (str, MinecraftBiomeTags)):
                    raise ValueError(
                        "All tags must be strings or MinecraftBiomeTags enum values"
                    )

            self._add_field("tags", tags)


class BiomeVillageType(Component):
    _identifier = "minecraft:village_type"

    def __init__(
        self, village_type: Literal["default", "desert", "ice", "savanna", "taiga"]
    ) -> None:
        """SDetermines the type of village for the Biome.

        Parameters:
            village_type (Literal["default", "desert", "ice", "savanna", "taiga"]): The village type for this biome. Must be one of: "default", "desert", "ice", "savanna", "taiga".

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_village_type
        """
        super().__init__("village_type")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if not isinstance(village_type, str):
            raise ValueError("Village type must be a string")

        if village_type not in ["default", "desert", "ice", "savanna", "taiga"]:
            raise ValueError(
                "Village type must be one of: 'default', 'desert', 'ice', 'savanna', 'taiga'"
            )

        self._add_field("village_type", village_type)
