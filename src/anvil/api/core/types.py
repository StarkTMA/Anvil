from typing import TYPE_CHECKING, Any, Callable, Literal, TypeAlias

from anvil.api.core.enums import BlockFaceValues, Slots

if TYPE_CHECKING:
    from anvil.lib.jsonmodel import JsonComponent
    from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor

# Vectors
type Vector2D = tuple[float, float]
type Vector3D = tuple[float, float, float]
type Vector4D = tuple[float, float, float, float]

type Vector2DInt = tuple[int, int]
type Vector3DInt = tuple[int, int, int]
type Vector4DInt = tuple[int, int, int, int]

# Colors
type RGB = Vector3D
type RGBA = Vector4D
type RGB255 = Vector3DInt
type RGBA255 = Vector4DInt
type HexRGB = str
type HexRGBA = str
type Color = RGB | RGBA | RGB255 | RGBA255 | HexRGB | HexRGBA

# Coordinates and rotations
type Coordinate = Vector3D
type Coordinates = tuple[Vector3D, Vector3D, Vector3D]
type RelativePosition = tuple[
    int | Literal["^", "~"], int | Literal["^", "~"], int | Literal["^", "~"]
]
type RelativeRotation = tuple[int | Literal["~"], int | Literal["~"]]
type Rotation = tuple[Coordinate, Coordinate]

# Minecraft-specific types
type Identifier = str
type Seconds = int
type Tick = int
type StructureProcessors = Literal[
    "minecraft:block_ignore",
    "minecraft:protected_blocks",
    "minecraft:capped",
    "minecraft:rule",
]

# Command selectors
type Target = Literal["@p", "@r", "@a", "@e", "@s", "@c", "@v", "@initiator"]

InstrumentSound: TypeAlias = Literal[
    "note.harp",
    "note.bd",
    "note.snare",
    "note.hat",
    "note.bassattack",
    "note.flute",
    "note.bell",
    "note.guitar",
    "note.chime",
    "note.xylophone",
    "note.iron_xylophone",
    "note.cow_bell",
    "note.didgeridoo",
    "note.bit",
    "note.banjo",
    "note.pling",
    "note.trumpet",
    "note.trumpet_exposed",
    "note.trumpet_weathered",
    "note.trumpet_oxidized",
    "note.zombie",
    "note.skeleton",
    "note.creeper",
    "note.enderdragon",
    "note.witherskeleton",
    "note.piglin",
    "note.none",
]

# Components
type NumberRange = tuple[float, float]

type BlockReference = MinecraftBlockDescriptor | Identifier | str

type ItemReference = MinecraftItemDescriptor | Identifier | str

# JSON model
type JsonPayload = dict[str, Any]

type ComponentIdentifier = Identifier

type JsonExport = dict[ComponentIdentifier, Any]

type ComponentClass = type[JsonComponent]

type ComponentClasses = tuple[ComponentClass, ...]

type Validator = Callable[[str, Any], None]

type Validators = tuple[Validator, ...] | list[Validator]

type DefaultFactory = Callable[[], Any]

type Encoder = Callable[[Any], Any]

# Biomes
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

BiomeVillageTypes = Literal["default", "desert", "ice", "savanna", "taiga"]

BiomeClimateCategory = Literal["medium", "warm", "lukewarm", "cold", "frozen"]

FoliageColorMap = Literal[
    "birch",
    "dry_foliage",
    "evergreen",
    "foliage",
    "mangrove_swamp_foliage",
    "swamp_foliage",
]

GrassColorMap = Literal["grass", "swamp_grass"]

type BiomeTransformation = str | list[tuple[str, int]]

# Blocks
BlockDefaultGeometry = Literal[
    "minecraft:geometry.full_block",
    "minecraft:geometry.full_block_v1",
    "minecraft:geometry.cross",
]

BlockCullingLayer = Literal[
    "minecraft:culling_layer.undefined", "minecraft:culling_layer.leaves"
]

BlockConnectionSource = Literal["all", "only_fences", "none"]

BlockPrecipitationBehavior = Literal[
    "obstruct_rain", "obstruct_rain_accumulate_snow", "none", "snowlogging"
]

BlockChestObstructionRule = Literal["always", "never", "shape"]

BlockSupportShape = Literal["fence", "stair"]

BlockLavaFlammable = Literal["always", "never"]

BlockSticky = Literal["none", "same"]

type BlockFaces = list[BlockFaceValues]

# Items
ItemUseAnimations = Literal[
    "eat",
    "drink",
    "block",
    "bow",
    "splash",
    "linger",
    "camera",
    "crossbow",
    "none",
    "brush",
    "spear",
    "spyglass",
]

ItemCooldownType = Literal["attack", "use"]

ItemStartUsing = Literal["always", "if_first"]

ItemPlantAtFace = Literal["UP", "DOWN", "NORTH", "SOUTH", "EAST", "WEST"]

ItemWearableSlots = Literal[
    Slots.Body,
    Slots.Chest,
    Slots.Feet,
    Slots.Head,
    Slots.Legs,
    Slots.Mainhand,
    Slots.Offhand,
]

type Chance = float | FeatureChance

type Weighted[T] = tuple[T, float]
