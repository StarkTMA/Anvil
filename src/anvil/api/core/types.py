from typing import Literal, TypeAlias

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
