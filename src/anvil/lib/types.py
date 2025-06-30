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
type Molang = str
type Range = tuple[float, float]
type Rotation = tuple[Coordinate, Coordinate]
type Seconds = int
type Tick = int
type Target = Literal["@p", "@r", "@a", "@e", "@s", "@c", "@v", "@initiator"]
type StructureProcessors = Literal["minecraft:block_ignore", "minecraft:protected_blocks", "minecraft:capped", "minecraft:rule"]


class ConstantIntProvider(TypedDict):
    value: int


class UniformIntProvider(TypedDict):
    min: int
    max: int


@dataclass(slots=True)
class BlockDescriptor:
    _name: str
    _is_vanilla: bool = False
    _states: Mapping[str, str | int | float | bool] = field(default_factory=dict)
    _tags: set[str] = field(default_factory=set)
    _identifier: Identifier = field(init=False, repr=False)

    @property
    def tags(self) -> set[str]:
        """Returns the tags associated with the block."""
        return self._tags

    @property
    def identifier(self) -> Identifier:
        if self._is_vanilla or self._name.startswith("minecraft:"):
            self._is_vanilla = True
            self._identifier = f'minecraft:{self._name.split(":")[-1]}'
        else:
            from anvil import CONFIG

            self._identifier = f'{CONFIG.NAMESPACE}:{self._name.split(":")[-1]}'

        return self._identifier

    @property
    def name(self) -> str:
        """Returns the name of the block."""
        return self._name

    @property
    def states(self) -> str:
        """Returns a string representation of the block states."""
        if not self._states:
            return ""
        return "{" + ", ".join(f"{k}={v}" for k, v in self._states.items()) + "}"

    def __str__(self) -> str:
        if not self.states:
            return self.identifier
        return f"{self.identifier} [{self.states}]"


@dataclass(slots=True)
class EntityDescriptor:
    _name: str
    _is_vanilla: bool = False
    _allow_runtime: bool = True

    @property
    def identifier(self) -> Identifier:
        if self._is_vanilla or self._name.startswith("minecraft:"):
            self._is_vanilla = True
            self._identifier = f'minecraft:{self._name.split(":")[-1]}'
        else:
            from anvil import CONFIG

            self._identifier = f'{CONFIG.NAMESPACE}:{self._name.split(":")[-1]}'

        return self._identifier

    @property
    def allow_runtime(self) -> bool:
        """Returns whether the entity can be created at runtime."""
        return self._allow_runtime

    @property
    def name(self) -> str:
        """Returns the name of the block."""
        return self._name

    def __str__(self) -> str:
        return self.identifier
