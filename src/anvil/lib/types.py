from dataclasses import dataclass, field
from typing import Literal, Mapping, TypedDict

type Vector2D = tuple[float, float]
type Vector3D = tuple[float, float, float]
type Vector4D = tuple[float, float, float, float]

type RGB = Vector3D
type RGBA = Vector4D
type ColorHex = str
type Color = RGB | RGBA | ColorHex
type Coordinate = Vector3D
type Coordinates = tuple[Vector3D, Vector3D, Vector3D]
type RelativePosition = tuple[int | Literal["^", "~"], int | Literal["^", "~"], int | Literal["^", "~"]]
type RelativeRotation = tuple[int | Literal["~"], int | Literal["~"]]

type Component = str
type Event = str
type Identifier = str
type Level = tuple[float, float]
type Range = tuple[float, float]
type Rotation = tuple[Coordinate, Coordinate]
type Seconds = int
type Tick = int
type Target = Literal["@p", "@r", "@a", "@e", "@s", "@c", "@v", "@initiator"]
type StructureProcessors = Literal["minecraft:block_ignore", "minecraft:protected_blocks", "minecraft:capped", "minecraft:rule"]
type Block = str


class ConstantIntProvider(TypedDict):
    value: int


class UniformIntProvider(TypedDict):
    min: int
    max: int

