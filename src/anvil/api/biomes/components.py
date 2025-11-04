from warnings import deprecated

from anvil.api.vanilla.biomes import MinecraftBiomeTags, MinecraftBiomeTypes
from anvil.api.core.components import _BaseComponent
from anvil.lib.enums import Dimension
from anvil.lib.format_versions import BIOME_SERVER_VERSION
from anvil.lib.lib import convert_color
from anvil.lib.schemas import BlockDescriptor
from anvil.lib.types import Color, HexRGB


class BiomeClimate(_BaseComponent):
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


class BiomeCreatureSpawnProbability(_BaseComponent):
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


class BiomeHumidity(_BaseComponent):
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


class BiomeMapTints(_BaseComponent):
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
            self._add_field("foliage", convert_color(foliage, HexRGB))

        if grass is not None:
            if not isinstance(grass, dict):
                raise ValueError("Grass must be a dictionary")
            self._add_field("grass", grass)


class BiomeMountainParameters(_BaseComponent):
    _identifier = "minecraft:mountain_parameters"

    def __init__(
        self,
        block: BlockDescriptor,
        north_slopes: bool = None,
        south_slopes: bool = None,
        east_slopes: bool = None,
        west_slopes: bool = None,
    ) -> None:
        """Noise parameters used to drive mountain terrain generation in Overworld.

        Parameters:
            block (BlockDescriptor): The block material definition.
            north_slopes (bool, optional): Enable for north-facing slopes. Defaults to None.
            south_slopes (bool, optional): Enable for south-facing slopes. Defaults to None.
            east_slopes (bool, optional): Enable for east-facing slopes. Defaults to None.
            west_slopes (bool, optional): Enable for west-facing slopes. Defaults to None.
        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_mountain_parameters
        """
        super().__init__("mountain_parameters")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

        if north_slopes is not None:
            if not isinstance(north_slopes, bool):
                raise ValueError("North slopes setting must be a boolean")
            self._add_field("north_slopes", north_slopes)

        if south_slopes is not None:
            if not isinstance(south_slopes, bool):
                raise ValueError("South slopes setting must be a boolean")
            self._add_field("south_slopes", south_slopes)

        if east_slopes is not None:
            if not isinstance(east_slopes, bool):
                raise ValueError("East slopes setting must be a boolean")
            self._add_field("east_slopes", east_slopes)

        if west_slopes is not None:
            if not isinstance(west_slopes, bool):
                raise ValueError("West slopes setting must be a boolean")
            self._add_field("west_slopes", west_slopes)

        if not isinstance(block, BlockDescriptor):
            raise ValueError("Material name must be a BlockDescriptor instance")

        self._add_dict(
            {
                "material": {
                    "name": block.identifier,
                    "states": block.states if block.states != "" else {},
                }
            }
        )

    def steep_material_adjustment(
        self,
        block: BlockDescriptor,
        north_slopes: bool = None,
        south_slopes: bool = None,
        east_slopes: bool = None,
        west_slopes: bool = None,
    ) -> None:
        """Defines surface material for steep slopes.

        Parameters:
            block (BlockDescriptor): The block material definition.
            north_slopes (bool, optional): Enable for north-facing slopes. Defaults to None.
            south_slopes (bool, optional): Enable for south-facing slopes. Defaults to None.
            east_slopes (bool, optional): Enable for east-facing slopes. Defaults to None.
            west_slopes (bool, optional): Enable for west-facing slopes. Defaults to None.
        """
        self._add_field("steep_material_adjustment", {})

        if north_slopes is not None:
            if not isinstance(north_slopes, bool):
                raise ValueError("North slopes setting must be a boolean")
            self["steep_material_adjustment"]["north_slopes"] = north_slopes

        if south_slopes is not None:
            if not isinstance(south_slopes, bool):
                raise ValueError("South slopes setting must be a boolean")
            self["steep_material_adjustment"]["south_slopes"] = south_slopes

        if east_slopes is not None:
            if not isinstance(east_slopes, bool):
                raise ValueError("East slopes setting must be a boolean")
            self["steep_material_adjustment"]["east_slopes"] = east_slopes

        if west_slopes is not None:
            if not isinstance(west_slopes, bool):
                raise ValueError("West slopes setting must be a boolean")
            self["steep_material_adjustment"]["west_slopes"] = west_slopes

        if not isinstance(block, BlockDescriptor):
            raise ValueError("Material name must be a BlockDescriptor instance")

        self["steep_material_adjustment"]["material"] = {
            "name": block.identifier,
            "states": block.states if block.states != "" else {},
        }

    def set_top_slide(self, enabled: bool):
        """Enable or disable top slide generation."""
        if not isinstance(enabled, bool):
            raise ValueError("Enabled must be a boolean value")
        self._add_field("top_slide", {"enabled": enabled})
        return self


@deprecated("This is a pre-Caves and Cliffs component and is unused for custom biomes.")
class BiomeMultiNoiseGenerationRules(_BaseComponent):
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
class BiomeOverworldGenerationRules(_BaseComponent):
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
class BiomeOverworldHeight(_BaseComponent):
    _identifier = "minecraft:overworld_height"

    def __init__(
        self, noise_params: list[float] = None, noise_type: str = None
    ) -> None:
        """Noise parameters used to drive terrain height in the Overworld.

        Parameters:
            noise_params (list[float], optional): First value is depth - more negative means deeper underwater, while more positive means higher. Second value is scale, which affects how much noise changes as it moves from the surface. Value must have at least 2 items. Value must have at most 2 items. Defaults to None.
            noise_type (str, optional): Specifies a preset based on a built-in setting rather than manually using noise_params. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_overworld_height
        """
        super().__init__("overworld_height")

        if noise_params is not None:
            if not isinstance(noise_params, list):
                raise ValueError("Noise params must be a list")
            if len(noise_params) != 2:
                raise ValueError("Noise params must have exactly 2 values")
            for param in noise_params:
                if not isinstance(param, (int, float)):
                    raise ValueError("All noise params must be numbers")
            self._add_field("noise_params", noise_params)

        if noise_type is not None:
            if not isinstance(noise_type, str):
                raise ValueError("Noise type must be a string")
            self._add_field("noise_type", noise_type)


class BiomeReplaceBiomes(_BaseComponent):
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


class BiomeSurfaceMaterialAdjustments(_BaseComponent):
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
        height_range: tuple[int, int],
        noise_frequency_scale: float,
        noise_range: tuple[float, float],
        foundation_material: BlockDescriptor,
        mid_material: BlockDescriptor,
        sea_floor_material: BlockDescriptor,
        sea_material: BlockDescriptor,
        top_material: BlockDescriptor,
    ):
        """An adjustment to generated terrain, replacing blocks based on the specified settings.
        Parameters:
            height_range (tuple[int, int]): Defines a range of noise values [min, max] for which this adjustment should be applied. Value must have at least 2 items. Value must have at most 2 items.
            noise_frequency_scale (float): The scale to multiply by the position when accessing the noise value for the material adjustments.
            noise_range (tuple[float, float]): Defines a range of noise values [min, max] for which this adjustment should be applied. Value must have at least 2 items. Value must have at most 2 items.
            foundation_material (BlockDescriptor): Controls the block type used deep underground in this biome when this adjustment is active.
            mid_material (BlockDescriptor): Controls the block type used in a layer below the surface of this biome when this adjustment is active.
            sea_floor_material (BlockDescriptor): Controls the block type used as a floor for bodies of water in this biome when this adjustment is active.
            sea_material (BlockDescriptor): Controls the block type used in the bodies of water in this biome when this adjustment is active.
            top_material (BlockDescriptor): Controls the block type used for the surface of this biome when this adjustment is active.
        """

        if not isinstance(height_range, (list, tuple)) or len(height_range) != 2:
            raise ValueError("Height range must be a list or tuple of two integers")
        for val in height_range:
            if not isinstance(val, int):
                raise ValueError("All height range values must be integers")

        if not isinstance(noise_frequency_scale, (int, float)):
            raise ValueError("Noise frequency scale must be a number")

        if not isinstance(noise_range, (list, tuple)) or len(noise_range) != 2:
            raise ValueError("Noise range must be a list or tuple of two floats")
        for val in noise_range:
            if not isinstance(val, (int, float)):
                raise ValueError("All noise range values must be numbers")

        for material in [
            foundation_material,
            mid_material,
            sea_floor_material,
            sea_material,
            top_material,
        ]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        adjustment = {
            "height_range": height_range,
            "noise_frequency_scale": noise_frequency_scale,
            "noise_range": noise_range,
            "materials": {
                "foundation_material": {
                    "name": foundation_material.identifier,
                    "states": (
                        foundation_material.states
                        if foundation_material.states != ""
                        else {}
                    ),
                },
                "mid_material": {
                    "name": mid_material.identifier,
                    "states": mid_material.states if mid_material.states != "" else {},
                },
                "sea_floor_material": {
                    "name": sea_floor_material.identifier,
                    "states": (
                        sea_floor_material.states
                        if sea_floor_material.states != ""
                        else {}
                    ),
                },
                "sea_material": {
                    "name": sea_material.identifier,
                    "states": sea_material.states if sea_material.states != "" else {},
                },
                "top_material": {
                    "name": top_material.identifier,
                    "states": top_material.states if top_material.states != "" else {},
                },
            },
        }

        self._adjustments.append(adjustment)
        self._add_field("adjustments", self._adjustments)

        return self


class BiomeSurfaceBuilder(_BaseComponent):
    _identifier = "minecraft:surface_builder"

    def __init__(self):
        """Controls the materials used for terrain generation.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/examples/components/minecraftbiomes_surface_builder
        """
        super().__init__("surface_builder")
        self._enforce_version(BIOME_SERVER_VERSION, "1.21.100")

    def set_overworld_builder(
        self,
        surface_type: str,
        foundation_material: BlockDescriptor,
        mid_material: BlockDescriptor,
        sea_floor_material: BlockDescriptor,
        sea_material: BlockDescriptor,
        top_material: BlockDescriptor,
        sea_floor_depth: int = None,
    ):
        """Controls the blocks used for the default Minecraft Overworld terrain generation.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
            foundation_material (BlockDescriptor): Controls the block type used deep underground in this biome.
            mid_material (BlockDescriptor): Controls the block type used in a layer below the surface of this biome.
            top_material (BlockDescriptor): Controls the block type used for the surface of this biome.
            sea_floor_material (BlockDescriptor): Controls the block type used as a floor for bodies of water in this biome.
            sea_material (BlockDescriptor): Controls the block type used for the bodies of water in this biome.
            sea_floor_depth (int, optional): Controls how deep below the world water level the floor should occur. Value must be <= 127. Defaults to None.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        for material in [
            foundation_material,
            mid_material,
            top_material,
            sea_floor_material,
            sea_material,
        ]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        if sea_floor_depth is not None:
            if not isinstance(sea_floor_depth, int):
                raise ValueError("Sea floor depth must be an integer")
            if sea_floor_depth > 127:
                raise ValueError("Sea floor depth must be <= 127")

        builder = {
            "type": surface_type,
            "foundation_material": {
                "name": foundation_material.identifier,
                "states": (
                    foundation_material.states
                    if foundation_material.states != ""
                    else {}
                ),
            },
            "mid_material": {
                "name": mid_material.identifier,
                "states": mid_material.states if mid_material.states != "" else {},
            },
            "top_material": {
                "name": top_material.identifier,
                "states": top_material.states if top_material.states != "" else {},
            },
            "sea_floor_material": {
                "name": sea_floor_material.identifier,
                "states": (
                    sea_floor_material.states if sea_floor_material.states != "" else {}
                ),
            },
            "sea_material": {
                "name": sea_material.identifier,
                "states": sea_material.states if sea_material.states != "" else {},
            },
        }

        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth

        self._add_field("builder", builder)
        return self

    def set_frozen_ocean_builder(
        self,
        surface_type: str,
        foundation_material: BlockDescriptor,
        mid_material: BlockDescriptor,
        sea_floor_material: BlockDescriptor,
        sea_material: BlockDescriptor,
        top_material: BlockDescriptor,
        sea_floor_depth: int = None,
    ):
        """Similar to overworld_surface. Adds icebergs.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
            foundation_material (BlockDescriptor): Controls the block type used deep underground in this biome.
            mid_material (BlockDescriptor): Controls the block type used in a layer below the surface of this biome.
            top_material (BlockDescriptor): Controls the block type used for the surface of this biome.
            sea_floor_material (BlockDescriptor): Controls the block type used as a floor for bodies of water in this biome.
            sea_material (BlockDescriptor): Controls the block type used for the bodies of water in this biome.
            sea_floor_depth (int, optional): Controls how deep below the world water level the floor should occur. Value must be <= 127. Defaults to None.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        for material in [
            foundation_material,
            mid_material,
            top_material,
            sea_floor_material,
            sea_material,
        ]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        if sea_floor_depth is not None:
            if not isinstance(sea_floor_depth, int):
                raise ValueError("Sea floor depth must be an integer")
            if sea_floor_depth > 127:
                raise ValueError("Sea floor depth must be <= 127")

        builder = {
            "type": surface_type,
            "foundation_material": {
                "name": foundation_material.identifier,
                "states": (
                    foundation_material.states
                    if foundation_material.states != ""
                    else {}
                ),
            },
            "mid_material": {
                "name": mid_material.identifier,
                "states": mid_material.states if mid_material.states != "" else {},
            },
            "top_material": {
                "name": top_material.identifier,
                "states": top_material.states if top_material.states != "" else {},
            },
            "sea_floor_material": {
                "name": sea_floor_material.identifier,
                "states": (
                    sea_floor_material.states if sea_floor_material.states != "" else {}
                ),
            },
            "sea_material": {
                "name": sea_material.identifier,
                "states": sea_material.states if sea_material.states != "" else {},
            },
        }

        if sea_floor_depth is not None:
            builder["sea_floor_depth"] = sea_floor_depth

        self._add_field("builder", builder)
        return self

    def set_mesa_builder(
        self,
        surface_type: str,
        clay_material: BlockDescriptor,
        foundation_material: BlockDescriptor,
        hard_clay_material: BlockDescriptor,
        mid_material: BlockDescriptor,
        sea_floor_material: BlockDescriptor,
        sea_material: BlockDescriptor,
        top_material: BlockDescriptor,
        bryce_pillars: bool = None,
        has_forest: bool = None,
        sea_floor_depth: int = None,
    ):
        """Similar to overworld_surface. Adds colored strata and optional pillars.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
            foundation_material (BlockDescriptor): Controls the block type used deep underground in this biome.
            mid_material (BlockDescriptor): Controls the block type used in a layer below the surface of this biome.
            top_material (BlockDescriptor): Controls the block type used for the surface of this biome.
            sea_floor_material (BlockDescriptor): Controls the block type used as a floor for bodies of water in this biome.
            sea_material (BlockDescriptor): Controls the block type used for the bodies of water in this biome.
            clay_material (BlockDescriptor): Base clay block to use.
            hard_clay_material (BlockDescriptor): Hardened clay block to use.
            bryce_pillars (bool, optional): Whether the mesa generates with pillars. Defaults to None.
            has_forest (bool, optional): Places coarse dirt and grass at high altitudes. Defaults to None.
            sea_floor_depth (int, optional): Controls how deep below the world water level the floor should occur. Value must be <= 127. Defaults to None.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        for material in [
            foundation_material,
            mid_material,
            top_material,
            sea_floor_material,
            sea_material,
            clay_material,
            hard_clay_material,
        ]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        if bryce_pillars is not None and not isinstance(bryce_pillars, bool):
            raise ValueError("Bryce pillars must be a boolean")

        if has_forest is not None and not isinstance(has_forest, bool):
            raise ValueError("Has forest must be a boolean")

        if sea_floor_depth is not None:
            if not isinstance(sea_floor_depth, int):
                raise ValueError("Sea floor depth must be an integer")
            if sea_floor_depth > 127:
                raise ValueError("Sea floor depth must be <= 127")

        builder = {
            "type": surface_type,
            "foundation_material": {
                "name": foundation_material.identifier,
                "states": (
                    foundation_material.states
                    if foundation_material.states != ""
                    else {}
                ),
            },
            "mid_material": {
                "name": mid_material.identifier,
                "states": mid_material.states if mid_material.states != "" else {},
            },
            "top_material": {
                "name": top_material.identifier,
                "states": top_material.states if top_material.states != "" else {},
            },
            "sea_floor_material": {
                "name": sea_floor_material.identifier,
                "states": (
                    sea_floor_material.states if sea_floor_material.states != "" else {}
                ),
            },
            "sea_material": {
                "name": sea_material.identifier,
                "states": sea_material.states if sea_material.states != "" else {},
            },
            "clay_material": {
                "name": clay_material.identifier,
                "states": clay_material.states if clay_material.states != "" else {},
            },
            "hard_clay_material": {
                "name": hard_clay_material.identifier,
                "states": (
                    hard_clay_material.states if hard_clay_material.states != "" else {}
                ),
            },
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
        surface_type: str,
        foundation_material: BlockDescriptor,
        mid_material: BlockDescriptor,
        sea_floor_material: BlockDescriptor,
        sea_material: BlockDescriptor,
        top_material: BlockDescriptor,
        sea_floor_depth: int = None,
        max_puddle_depth_below_sea_level: int = None,
    ):
        """Used to add decoration to the surface of swamp biomes such as water lilies.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
            foundation_material (BlockDescriptor): Controls the block type used deep underground in this biome.
            mid_material (BlockDescriptor): Controls the block type used in a layer below the surface of this biome.
            top_material (BlockDescriptor): Controls the block type used for the surface of this biome.
            sea_floor_material (BlockDescriptor): Controls the block type used as a floor for bodies of water in this biome.
            sea_material (BlockDescriptor): Controls the block type used for the bodies of water in this biome.
            sea_floor_depth (int, optional): Controls how deep below the world water level the floor should occur. Value must be <= 127. Defaults to None.
            max_puddle_depth_below_sea_level (int, optional): Controls the depth at which surface level blocks can be replaced with water for puddles. The number represents the number of blocks (0, 127) below sea level that we will go down to look for a surface block. Value must be <= 127. Defaults to None.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        for material in [
            foundation_material,
            mid_material,
            top_material,
            sea_floor_material,
            sea_material,
        ]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        if sea_floor_depth is not None:
            if not isinstance(sea_floor_depth, int):
                raise ValueError("Sea floor depth must be an integer")
            if sea_floor_depth > 127:
                raise ValueError("Sea floor depth must be <= 127")

        if max_puddle_depth_below_sea_level is not None:
            if not isinstance(max_puddle_depth_below_sea_level, int):
                raise ValueError("Max puddle depth below sea level must be an integer")
            if max_puddle_depth_below_sea_level > 127:
                raise ValueError("Max puddle depth below sea level must be <= 127")

        builder = {
            "type": surface_type,
            "foundation_material": {
                "name": foundation_material.identifier,
                "states": (
                    foundation_material.states
                    if foundation_material.states != ""
                    else {}
                ),
            },
            "mid_material": {
                "name": mid_material.identifier,
                "states": mid_material.states if mid_material.states != "" else {},
            },
            "top_material": {
                "name": top_material.identifier,
                "states": top_material.states if top_material.states != "" else {},
            },
            "sea_floor_material": {
                "name": sea_floor_material.identifier,
                "states": (
                    sea_floor_material.states if sea_floor_material.states != "" else {}
                ),
            },
            "sea_material": {
                "name": sea_material.identifier,
                "states": sea_material.states if sea_material.states != "" else {},
            },
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
        surface_type: str,
        beach_material: BlockDescriptor,
        ceiling_materials: list[BlockDescriptor],
        floor_materials: list[BlockDescriptor],
        foundation_material: BlockDescriptor,
        sea_material: BlockDescriptor,
    ):
        """Generates surface on blocks with non-solid blocks above or below.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
            foundation_material (BlockDescriptor): Material used to replace solid blocks that are not surface blocks.
            sea_material (BlockDescriptor): Material used to replace air blocks below sea level.
            beach_material (BlockDescriptor): Material used to decorate surface near sea level.
            ceiling_materials (list[BlockDescriptor]): Materials used for the surface ceiling. Value must have at least 1 items.
            floor_materials (list[BlockDescriptor]): Materials used for the surface floor. Value must have at least 1 items.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        for material in [foundation_material, sea_material, beach_material]:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        if not isinstance(ceiling_materials, list) or len(ceiling_materials) < 1:
            raise ValueError("Ceiling materials must be a list with at least 1 item")

        if not isinstance(floor_materials, list) or len(floor_materials) < 1:
            raise ValueError("Floor materials must be a list with at least 1 item")

        for material in ceiling_materials + floor_materials:
            if not isinstance(material, BlockDescriptor):
                raise ValueError("All materials must be BlockDescriptor instances")

        builder = {
            "type": surface_type,
            "foundation_material": {
                "name": foundation_material.identifier,
                "states": (
                    foundation_material.states
                    if foundation_material.states != ""
                    else {}
                ),
            },
            "sea_material": {
                "name": sea_material.identifier,
                "states": sea_material.states if sea_material.states != "" else {},
            },
            "beach_material": {
                "name": beach_material.identifier,
                "states": beach_material.states if beach_material.states != "" else {},
            },
            "ceiling_materials": [
                {
                    "name": material.identifier,
                    "states": material.states if material.states != "" else {},
                }
                for material in ceiling_materials
            ],
            "floor_materials": [
                {
                    "name": material.identifier,
                    "states": material.states if material.states != "" else {},
                }
                for material in floor_materials
            ],
        }

        self._add_field("builder", builder)
        return self

    def set_end_builder(self, surface_type: str):
        """Use default Minecraft End terrain generation.

        Parameters:
            surface_type (str): Controls the type of surface builder to use.
        """
        if not isinstance(surface_type, str):
            raise ValueError("Surface type must be a string")

        builder = {"type": surface_type}

        self._add_field("builder", builder)
        return self


class BiomeTags(_BaseComponent):
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
