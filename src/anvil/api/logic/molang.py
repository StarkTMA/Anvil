from enum import StrEnum
from typing import Literal, Optional, overload
from warnings import deprecated

import orjson

from anvil.api.core.enums import InputModes, Slots
from anvil.lib.config import CONFIG
from anvil.lib.format_versions import MANIFEST_VERSION
from anvil.lib.schemas import MinecraftBiomeDescriptor

__all__ = [
    "Molang",
    "Query",
    "Context",
    "Variable",
    "TempVar",
    "Math",
    "molang_conditions",
    "arrow_operator",
]


def _checked(name: str, value, low: int, high: int):
    """`value`, after checking that a number is from `low` to `high`. Molang passes as is."""
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and not low <= value <= high
    ):
        raise ValueError(f"'{name}' must be from {low} to {high}, got {value}.")
    return value


def _list_of(query: str, what: str, values: list[str]) -> list[str]:
    """`values`, after checking it is a list rather than a single string."""
    if isinstance(values, str):
        raise TypeError(
            f"{query} takes a list of {what}, got the string {str(values)!r}. "
            f"Use {query}([{str(values)!r}])."
        )
    return list(values)


class _VarMeta(type):
    def __getattr__(cls, name):
        if name.startswith("_"):
            raise AttributeError(name)
        val = cls.__query__(cls, cls.handle, name)
        setattr(cls, name, val)
        return val


class MolangProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func()


class Molang(str):
    prefixes = (
        "q.",
        "v.",
        "c.",
        "t.",
        "query.",
        "variable.",
        "context.",
        "temp.",
        "math.",
    )

    @staticmethod
    def arrow(left: "Molang", right: "Molang") -> "Molang":
        """Returns a Molang object representing the arrow operator for Molang."""
        return Molang(f"({left}) -> ({right})")

    @staticmethod
    def condition(
        condition: "Molang",
        expression: "Molang",
        expression2: Optional["Molang"] = None,
    ) -> "Molang":
        """Returns a Molang object representing a conditional expression for Molang."""
        if expression2 is not None:
            return Molang(f"({condition} ? {expression} : {expression2})")
        else:
            return Molang(f"({condition} ? {expression})")

    @staticmethod
    def molang_return(molang: "Molang") -> "Molang":
        return Molang(f"return {molang}")

    @staticmethod
    def molang_block(statements: list["Molang"]) -> "Molang":
        body = "; ".join(str(s) for s in statements)
        return Molang(f"{{ {body}; }}")

    @staticmethod
    def molang_loop(n: int, statements: list["Molang"]) -> "Molang":
        return Molang(f"loop({n}, {Molang.molang_block(statements)})")

    @staticmethod
    def molang_for_each(
        variable: "Molang", array: "Molang", statements: list["Molang"]
    ) -> "Molang":
        return Molang(
            f"for_each({variable}, {array}, {Molang.molang_block(statements)})"
        )

    @MolangProperty
    def this() -> "Molang":
        return Molang("this")

    @MolangProperty
    def break_() -> "Molang":
        return Molang("break")

    @MolangProperty
    def continue_() -> "Molang":
        return Molang("continue")

    __hash__ = str.__hash__

    def __getitem__(self, molang: "Molang") -> "Molang":
        return Molang(f"{self}[{molang}]")

    def __parse_other__(self, other):
        if isinstance(other, (str, StrEnum)) and not isinstance(other, Molang):
            o = f"'{other}'"
        elif isinstance(other, bool):
            o = orjson.dumps(other).decode("utf-8")
        else:
            o = f"{other}"
        return o

    def __invert__(self) -> "Molang":
        return Molang(f"!({self})")

    def __eq__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} == {o})")

    def __ne__(self, other) -> "Molang":
        o = self.__parse_other__(other)

        return Molang(f"({self} != {o})")

    def __lt__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} < {o})")

    def __gt__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} > {o})")

    def __le__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} <= {o})")

    def __ge__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} >= {o})")

    def __and__(self, other) -> "Molang":
        return Molang(f"({self} && {other})")

    def __or__(self, other) -> "Molang":
        return Molang(f"({self} || {other})")

    def __add__(self, other) -> "Molang":
        return Molang(f"({self} + {other})")

    def __sub__(self, other) -> "Molang":
        return Molang(f"({self} - {other})")

    def __mul__(self, other) -> "Molang":
        return Molang(f"({self} * {other})")

    def __neg__(self) -> "Molang":
        return Molang(f"-{self}")

    def __truediv__(self, other) -> "Molang":
        return Molang(f"({self} / {other})")

    def __floordiv__(self, other) -> "Molang":
        return Math.floor(self / other)

    def __mod__(self, other) -> "Molang":
        return Math.mod(self, other)

    def __pow__(self, other) -> "Molang":
        return Math.pow(self, other)

    def __radd__(self, other) -> "Molang":
        return Molang(f"({other} + {self})")

    def __rsub__(self, other) -> "Molang":
        return Molang(f"({other} - {self})")

    def __rmul__(self, other) -> "Molang":
        return Molang(f"({other} * {self})")

    def __rtruediv__(self, other) -> "Molang":
        return Molang(f"({other} / {self})")

    def __rfloordiv__(self, other) -> "Molang":
        return Math.floor(other / self)

    def __rmod__(self, other) -> "Molang":
        return Math.mod(other, self)

    def __rpow__(self, other) -> "Molang":
        return Math.pow(other, self)

    def __abs__(self) -> "Molang":
        return Math.abs(self)

    def __round__(self) -> "Molang":
        return Math.round(self)

    def __xor__(self, other) -> "Molang":
        return Molang(f"({self} ?? {other})")

    def __pos__(self) -> "Molang":
        return self

    def __rand__(self, other) -> "Molang":
        return Molang(f"({other} && {self})")

    def __ror__(self, other) -> "Molang":
        return Molang(f"({other} || {self})")

    def __rxor__(self, other) -> "Molang":
        return Molang(f"({other} ?? {self})")

    @staticmethod
    def __power_of_two__(shift):
        return 2 ** shift if isinstance(shift, int) else Math.pow(2, shift)

    def __lshift__(self, other) -> "Molang":
        return self * Molang.__power_of_two__(other)

    def __rshift__(self, other) -> "Molang":
        return self // Molang.__power_of_two__(other)

    def __rlshift__(self, other) -> "Molang":
        return other * Molang.__power_of_two__(self)

    def __rrshift__(self, other) -> "Molang":
        return Math.floor(other / Molang.__power_of_two__(self))

    def __struct__(self, *Parameters) -> "Molang":
        return Molang(f"{self}.{'.'.join(Parameters)}")

    def __query__(self, qtype, query, *arguments) -> "Molang":
        a = f"{qtype}.{query}"
        if len(arguments):
            Parameters = ", ".join(
                (
                    f"'{arg}'"
                    if isinstance(arg, (str, StrEnum))
                    and not isinstance(arg, Molang)
                    and not any(arg.startswith(v) for v in Molang.prefixes)
                    else f"{arg}"
                )
                for arg in arguments
                if arg is not None
            )
            a += f"({Parameters})"
        return Molang(a)


class _Vec3Struct(Molang):
    """Molang struct with x, y, z component access."""

    def __new__(cls, molang: "Molang | str") -> "_Vec3Struct":
        return super().__new__(cls, str(molang))

    @property
    def x(self) -> "Molang":
        return Molang(self.__struct__("x"))

    @property
    def y(self) -> "Molang":
        return Molang(self.__struct__("y"))

    @property
    def z(self) -> "Molang":
        return Molang(self.__struct__("z"))


class _AabbStruct(Molang):
    """Molang struct for axis-aligned bounding boxes, with .min and .max each returning a Vec3Struct."""

    def __new__(cls, molang: "Molang | str") -> "_AabbStruct":
        return super().__new__(cls, str(molang))

    @property
    def min(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("min"))

    @property
    def max(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("max"))


class _ColorStruct(Molang):
    """Molang struct with r, g, b, a color component access, each 0.0 to 1.0."""

    def __new__(cls, molang: "Molang | str") -> "_ColorStruct":
        return super().__new__(cls, str(molang))

    @property
    def r(self) -> "Molang":
        return Molang(self.__struct__("r"))

    @property
    def g(self) -> "Molang":
        return Molang(self.__struct__("g"))

    @property
    def b(self) -> "Molang":
        return Molang(self.__struct__("b"))

    @property
    def a(self) -> "Molang":
        return Molang(self.__struct__("a"))


class _UVStruct(Molang):
    """Molang struct with u, v texture coordinate/size component access."""

    def __new__(cls, molang: "Molang | str") -> "_UVStruct":
        return super().__new__(cls, str(molang))

    @property
    def u(self) -> "Molang":
        return Molang(self.__struct__("u"))

    @property
    def v(self) -> "Molang":
        return Molang(self.__struct__("v"))


class _TRSStruct(Molang):
    """Molang struct with translation, rotation, and scale component access, each returning a Vec3Struct."""

    def __new__(cls, molang: "Molang | str") -> "_TRSStruct":
        return super().__new__(cls, str(molang))

    @property
    def translation(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("t"))

    @property
    def rotation(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("r"))

    @property
    def scale(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("s"))


class Query(Molang):
    handle = "q"

    @classmethod
    def AboveTopSolid(cls, x: int, z: int) -> Molang:
        """Returns the height of the block immediately above the highest solid block at the input (x,z) position.

        Args:
            x (int): X position.
            z (int): Y position.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "above_top_solid", x, z)

    @classmethod
    def ActorCount(cls) -> Molang:
        """Returns the number of actors rendered in the last frame.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "actor_count")

    @classmethod
    def All(cls, query: Molang, queries: list[Molang]) -> Molang:
        """Requires at least 3 arguments. Evaluates the first argument, then returns 1.0 if all of the following arguments evaluate to the same value as the first. Otherwise it returns 0.0.

        Args:
            query (Molang): Query to evaluate.
            queries (list[Molang]): arguments to test against.

        Returns:
            Molang(Molang): A Molang Instance
        """
        if len(queries) < 2:
            raise ValueError("Query.All requires at least 3 arguments.")

        return cls.__query__(cls, cls.handle, "all", query, *queries)

    @classmethod
    def AllAnimationsFinished(cls) -> Molang:
        """Only valid in an animation controller. Returns 1.0 if all animations in the current animation controller state have played through at least once, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "all_animations_finished")

    @classmethod
    def AllTags(cls, tags: list[str]) -> Molang:
        """Returns 1.0 if the item or block has all of the tags specified, else it return 0.0.

        Args:
            tags (list[str]): entity tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "all_tags", *_list_of("Query.AllTags", "tags", tags)
        )

    @classmethod
    def AngerLevel(cls) -> Molang:
        """If available, returns the anger level of the actor as an integer value from 0 to 1 less than the 'max_anger' defined on the actor, otherwise returns 0. Only returns a non-zero value in behavior packs.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "anger_level")

    @classmethod
    def AnimTime(cls) -> Molang:
        """Returns the time in seconds since the current animation started, else 0.0 if not called within an animation.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "anim_time")

    @classmethod
    def Any(cls, query: Molang, queries: list[Molang]) -> Molang:
        """Requires at least 3 arguments. Evaluates the first argument, then returns 1.0 if any of the following arguments evaluate to the same value as the first. Otherwise it returns 0.0.

        Args:
            query (Molang): Query to evaluate.
            queries (list[Molang]): arguments to test against.

        Returns:
            Molang(Molang): A Molang Instance
        """
        if len(queries) < 2:
            raise ValueError("Query.Any requires at least 3 arguments.")

        return cls.__query__(cls, cls.handle, "any", query, *queries)

    @classmethod
    def AnyAnimationFinished(cls) -> Molang:
        """Only valid in an animation controller. Returns 1.0 if any animation in the current animation controller state has played through at least once, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "any_animation_finished")

    @classmethod
    def AnyTag(cls, tags: list[str]) -> Molang:
        """Returns 1.0 if the item or block has any of the tags specified, else it returns 0.0.

        Args:
            tags (list[str]): entity tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "any_tag", *_list_of("Query.AnyTag", "tags", tags)
        )

    @classmethod
    def ApproxEq(cls, *Parameters) -> Molang:
        """Returns 1.0 if all of the arguments are within 0.000000 of each other, else it returns 0.0.

        Args:
            Parameters (Any): Arguments to test for approximate equality.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "approx_eq", *Parameters)

    @classmethod
    def ArmorColorSlot(cls, index: int, colorChannel: int) -> Molang:
        """Takes the armor slot index as a parameter and returns the color of the armor in the requested slot.

        Args:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "armor_color_slot",
            _checked("index", index, 0, 3),
            _checked("colorChannel", colorChannel, 0, 3),
        )

    @classmethod
    def ArmorMaterialSlot(cls, index: int) -> Molang:
        """Takes the armor slot index as a parameter and returns the armor material type in the requested armor slot.

        Args:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "armor_material_slot", index)

    @classmethod
    def ArmorTextureSlot(cls, index: int) -> Molang:
        """Takes the armor slot index as a parameter and returns the texture type of the requested slot.

        Args:
            index (int): Armour slot index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "armor_texture_slot", index)

    @classmethod
    def AverageFrameTime(cls, frame: int = 0) -> Molang:
        """Returns the time in *seconds* of the average frame time over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Args:
            frame (int, optional): Frame number.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "average_frame_time", _checked("frame", frame, 0, 30)
        )

    @classmethod
    def BaseSwingDuration(cls) -> Molang:
        """Returns the base swing duration of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "base_swing_duration")

    @classmethod
    def BlockFace(cls) -> Molang:
        """Returns the block face for this (only valid for certain triggers such as placing blocks, or interacting with block) (Down=0.0, Up=1.0, North=2.0, South=3.0, West=4.0, East=5.0, Undefined=6.0).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "block_face")

    @classmethod
    def BlockState(cls, state: str) -> Molang:
        """Returns the value of the associated block's Block State.

        Args:
            state (str): The block state to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        state = (
            f"{state}" if isinstance(state, StrEnum) else f"{CONFIG.NAMESPACE}:{state}"
        )
        return cls.__query__(cls, cls.handle, "block_state", state)

    @classmethod
    def Property(cls, property: str) -> Molang:
        """Returns the value of the associated property.

        Args:
            property (str): The property to query, no namespace.


        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "property", f"{CONFIG.NAMESPACE}:{property}"
        )

    @classmethod
    def HasProperty(cls, property: str) -> Molang:
        """Returns true if the entity has the property.

        Args:
            property (str): The block property to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "has_property", f"{CONFIG.NAMESPACE}:{property}"
        )

    @classmethod
    def Blocking(cls) -> Molang:
        """Returns 1.0 if the entity is blocking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "blocking")

    @classmethod
    def BodyXRotation(cls) -> Molang:
        """Returns the body pitch rotation if called on an actor, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "body_x_rotation")

    @classmethod
    def BodyYRotation(cls) -> Molang:
        """Returns the body yaw rotation if called on an actor, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "body_y_rotation")

    # More info needed
    @classmethod
    def BoneAabb(cls) -> "_AabbStruct":
        """Returns the axis aligned bounding box of a bone as a struct with members '.min', '.max', along with '.x', '.y', and '.z' values for each.

        Returns:
            _AabbStruct: A struct with .min and .max, each a _Vec3Struct
        """
        return _AabbStruct(cls.__query__(cls, cls.handle, "bone_aabb"))

    # More info needed
    @classmethod
    def BoneOrigin(cls) -> "_Vec3Struct":
        """Returns the initial (from the .geo) pivot of a bone as a struct with members '.x', '.y', and '.z'.

        Returns:
            _Vec3Struct: A struct with .x, .y, .z components
        """
        return _Vec3Struct(cls.__query__(cls, cls.handle, "bone_origin"))

    # More info needed
    @classmethod
    def BoneRotation(cls, bone_name: str) -> _Vec3Struct:
        """Returns the initial (from the .geo) rotation of a bone as a struct with members '.x', '.y', and '.z' in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _Vec3Struct(cls.__query__(cls, cls.handle, "bone_rotation", bone_name))

    @classmethod
    def CameraDistanceRangeLerp(cls, d1: int, d2: int) -> Molang:
        """Takes two distances (any order) and return a number from 0 to 1 based on the camera distance between the two ranges clamped to that range.

        For example, 'query.camera_distance_range_lerp(10, 20)' will return 0 for any distance less than or equal to 10, 0.2 for a distance of 12, 0.5 for 15, and 1 for 20 or greater.
        If you pass in (20, 10), a distance of 20 will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "camera_distance_range_lerp", d1, d2)

    @classmethod
    def CameraRotation(cls, axis: int) -> Molang:
        """Returns the rotation of the camera. Requires one argument representing the rotation axis you would like.

        Args:
            axis (int): 0 for x, 1 for y

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "camera_rotation", _checked("axis", axis, 0, 1)
        )

    @classmethod
    def CanClimb(cls) -> Molang:
        """Returns 1.0 if the entity can climb, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_climb")

    @classmethod
    def CanDamageNearbyMobs(cls) -> Molang:
        """Returns 1.0 if the entity can damage nearby mobs, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_damage_nearby_mobs")

    @classmethod
    def CanFly(cls) -> Molang:
        """Returns 1.0 if the entity can fly, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_fly")

    @classmethod
    def CanPowerJump(cls) -> Molang:
        """Returns 1.0 if the entity can power jump, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_power_jump")

    @classmethod
    def CanSwim(cls) -> Molang:
        """Returns 1.0 if the entity can swim, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_swim")

    @classmethod
    def CanWalk(cls) -> Molang:
        """Returns 1.0 if the entity can walk, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_walk")

    @classmethod
    def CapeFlapAmount(cls) -> Molang:
        """Returns value between 0.0 and 1.0 with 0.0 meaning "cape is fully down" and 1.0 means "cape is fully up."

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cape_flap_amount")

    @classmethod
    @deprecated(
        "Query.CardinalBlockFacePlacedOn is deprecated by Minecraft. Use Query.BlockFace instead."
    )
    def CardinalBlockFacePlacedOn(cls) -> Molang:
        """DEPRECATED (please use query.block_face instead) Returns the block face for this (only valid for on_placed_by_player trigger) (Down=0.0, Up=1.0, North=2.0, South=3.0, West=4.0, East=5.0, Undefined=6.0).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cardinal_block_face_placed_on")

    @classmethod
    def CardinalFacing(cls) -> Molang:
        """Returns the current facing of the player

        - Down=0.0
        - Up=1.0
        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cardinal_facing")

    @classmethod
    def CardinalFacing2D(cls) -> Molang:
        """Returns the current facing of the player ignoring up/down part of the direction

        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cardinal_facing_2d")

    @classmethod
    def CardinalPlayerFacing(cls) -> Molang:
        """Returns the current facing of the player

        - Down=0.0
        - Up=1.0
        - North=2.0
        - South=3.0
        - West=4.0
        - East=5.0
        - Undefined=6.0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cardinal_player_facing")

    # More info needed
    @classmethod
    def CombineEntities(cls) -> Molang:
        """Combines any valid entity references from all arguments into a single array.  Note that order is not preserved, and duplicates and invalid values are removed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "combine_entities")

    @classmethod
    def Count(cls, *element) -> Molang:
        """Counts the number of things passed to it (arrays are counted as the number of elements they contain; non-arrays count as 1).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "count", *element)

    @classmethod
    def CurrentSquishValue(cls) -> Molang:
        """Returns the squish value for the current entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "current_squish_value")

    @classmethod
    def Day(cls) -> Molang:
        """Returns the day of the current level.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "day")

    @classmethod
    def DeathTicks(cls) -> Molang:
        """Returns the elapsed ticks since the mob started dying.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "death_ticks")

    @classmethod
    def DebugOutput(cls) -> Molang:
        """### Server Client

        Debug log a value to the output debug window for builds that have one.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "debug_output")

    @classmethod
    def DeltaTime(cls) -> Molang:
        """Returns the time in seconds since the previous frame.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "delta_time")

    @classmethod
    def DistanceFromCamera(cls) -> Molang:
        """Returns the distance of the root of this actor or particle emitter from the camera.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "distance_from_camera")

    @classmethod
    def EffectEmitterCount(cls) -> Molang:
        """Returns the total number of active emitters of the callee's particle effect type.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "effect_emitter_count")

    @classmethod
    def EffectParticleCount(cls) -> Molang:
        """Returns the total number of active particles of the callee's particle effect type.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "effect_particle_count")

    @classmethod
    def EquipmentCount(cls) -> Molang:
        """Returns the number of equipped armor pieces for an actor from 0 to 4, not counting items held in hands. (To query for hand slots, use query.is_item_equipped or query.is_item_name_any).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "equipment_count")

    @classmethod
    def EquippedItemAllTags(cls, slot: Slots, tags: list[str]) -> Molang:
        """Takes a slot name followed by any tag you want to check for in the form of 'tag_name' and returns 1 if all of the tags are on that equipped item, 0 otherwise.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "equipped_item_all_tags",
            slot,
            *_list_of("Query.EquippedItemAllTags", "tags", tags),
        )

    @classmethod
    def EquippedItemAnyTag(cls, slot: Slots, tags: list[str]) -> Molang:
        """Takes a slot name followed by any tag you want to check for in the form of 'tag_name' and returns 0 if none of the tags are on that equipped item or 1 if at least 1 tag exists.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "equipped_item_any_tag",
            slot,
            *_list_of("Query.EquippedItemAnyTag", "tags", tags),
        )

    @classmethod
    def EquippedItemIsAttachable(cls, hand: int = 0) -> Molang:
        """Takes the desired hand slot as a parameter and returns whether the item is an attachable or not.

        Args:
            hand (int, optional): 0 for main hand, 1 for off hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "equipped_item_is_attachable",
            _checked("hand", hand, 0, 1),
        )

    @classmethod
    def EyeTargetXRotation(cls) -> Molang:
        """Returns the X eye rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "eye_target_x_rotation")

    @classmethod
    def EyeTargetYRotation(cls) -> Molang:
        """Returns the Y eye rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "eye_target_y_rotation")

    @classmethod
    def FacingTargetToRangeAttack(cls) -> Molang:
        """Returns 1.0 if the entity is attacking from range (minecraft:behavior.ranged_attack), else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "facing_target_to_range_attack")

    @classmethod
    def FrameAlpha(cls) -> Molang:
        """Returns the ratio (from 0 to 1) of how much between AI ticks this frame is being rendered.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "frame_alpha")

    @classmethod
    def FuseTime(cls) -> Molang:
        """Returns the remaining fuse time of an entity, or -1 if the entity doesn't have a "minecraft:explode" component.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "fuse_time")

    @classmethod
    def GetActorInfoId(cls) -> Molang:
        """Returns the integer ID of an actor by its string name.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_actor_info_id")

    @classmethod
    def GetAnimationFrame(cls) -> Molang:
        """Returns the current texture of the item.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_animation_frame")

    # More info needed
    @classmethod
    def GetDefaultBonePivot(cls) -> Molang:
        """Gets the specified axis of the specified bone orientation pivot.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_default_bone_pivot")

    @classmethod
    @deprecated(
        "Query.GetEquippedItemName is deprecated by Minecraft. Use Query.IsItemNameAny instead."
    )
    def GetEquippedItemName(cls, hand_slot: int, index=0) -> Molang:
        """DEPRECATED (Use query.is_item_name_any instead if possible so names can be changed later without breaking content.) Takes one optional hand slot as a parameter (0 or 'main_hand' for main hand, 1 or 'off_hand' for off hand), and a second parameter (0=default) if you would like the equipped item or any non-zero number for the currently rendered item, and returns the name of the item in the requested slot (defaulting to the main hand if no parameter is supplied) if there is one, otherwise returns ''.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "get_equipped_item_name",
            _checked("hand_slot", hand_slot, 0, 1),
            index,
        )

    # More info needed
    @classmethod
    def GetLocatorOffset(cls) -> Molang:
        """Gets specified axis of the specified locator offset.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_locator_offset")

    @classmethod
    @deprecated(
        "Query.GetName is deprecated by Minecraft. Use Query.IsNameAny instead."
    )
    def GetName(cls) -> Molang:
        """DEPRECATED (Use query.is_name_any instead if possible so names can be changed later without breaking content.) Get the name of the mob if there is one, otherwise return ''.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_name")

    # More info needed
    @classmethod
    def GetRootLocatorOffset(cls) -> Molang:
        """Gets specified axis of the specified locator offset of the root model.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_root_locator_offset")

    @classmethod
    def GroundSpeed(cls) -> Molang:
        """Returns the ground speed of the entity in meters/second.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ground_speed")

    @classmethod
    def HadComponentGroup(cls, component_group: str) -> Molang:
        """### Server Only.

        Usable only in behavior packs when determining the default value for an entity's Property. Requires one string argument. If the entity is being loaded from data that was last saved with a component_group with the specified name, returns 1.0, otherwise returns 0.0. The purpose of this query is to allow entity definitions to change and still be able to load the correct state of entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "had_component_group", component_group)

    @classmethod
    def HasAnyFamily(cls, *family: str) -> Molang:
        """Returns 1 if the entity has any of the specified families, else 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_any_family", *family)

    @classmethod
    def HasArmorSlot(cls, slot: Slots) -> Molang:
        """Takes the armor slot index as a parameter and returns 1.0 if the entity has armor in the requested slot, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_armor_slot", slot)

    @classmethod
    def HasBiomeTag(cls, tag: str) -> Molang:
        """Returns whether or not a Block Placement Target has a specific biome tag.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_biome_tag", tag)

    @classmethod
    def HasBlockState(cls, state: str) -> Molang:
        """Returns 1.0 if the associated block has the given block state or 0.0 if not.

        Args:
            state (str): The block state to query, no namespace.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "has_block_state", f"{CONFIG.NAMESPACE}:{state}"
        )

    @classmethod
    def HasCape(cls) -> Molang:
        """Returns 1.0 if the player has a cape, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_cape")

    @classmethod
    def HasCollision(cls) -> Molang:
        """Returns 1.0 if the entity has collisions enabled, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_collision")

    @classmethod
    def HasGravity(cls) -> Molang:
        """Returns 1.0 if the entity is affected by gravity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_gravity")

    @classmethod
    def HasOwner(cls) -> Molang:
        """Returns true if the entity has an owner ID, else it returns false.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_owner")

    @classmethod
    def HasRider(cls) -> Molang:
        """Returns 1.0 if the entity has a rider, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_rider")

    @classmethod
    def HasTarget(cls) -> Molang:
        """Returns 1.0 if the entity has a target, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_target")

    @classmethod
    def HeadRollAngle(cls) -> Molang:
        """Returns the roll angle of the head of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "head_roll_angle")

    @classmethod
    def HeadXRotation(cls, head_number: int = 0) -> Molang:
        """Takes one argument as a parameter. Returns the nth head x rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "head_x_rotation", head_number)

    @classmethod
    def HeadYRotation(cls, head_number: int = 0) -> Molang:
        """Takes one argument as a parameter. Returns the nth head y rotation of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "head_y_rotation", head_number)

    @classmethod
    def Health(cls) -> Molang:
        """Returns the health of the entity, or 0.0 if it doesn't make sense to call on this entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "health")

    @classmethod
    def HeartbeatInterval(cls) -> Molang:
        """Returns the heartbeat interval of the actor in seconds. Returns 0 when the actor has no heartbeat.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "heartbeat_interval")

    @classmethod
    def HeartbeatPhase(cls) -> Molang:
        """### Client Only

        Returns the heartbeat phase of the actor. 0.0 if at start of current heartbeat, 1.0 if at the end. Returns 0 on errors or when the actor has no heartbeat.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "heartbeat_phase")

    @classmethod
    def Heightmap(cls, x: int, z: int) -> Molang:
        """Takes two arguments: X and Z world values. Returns the world height (Y value) of the terrain at the specified position.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "heightmap", x, z)

    @classmethod
    def HurtDirection(cls) -> Molang:
        """Returns the hurt direction for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "hurt_direction")

    @classmethod
    def HurtTime(cls) -> Molang:
        """Returns the hurt time for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "hurt_time")

    @classmethod
    def InRange(cls, value: float, min: float, max: float) -> Molang:
        """Requires 3 numerical arguments: some value, a minimum, and a maximum. If the first argument is between the minimum and maximum (inclusive), returns 1.0. Otherwise it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "in_range", value, min, max)

    @classmethod
    def InvulnerableTicks(cls) -> Molang:
        """Returns the number of ticks of invulnerability the entity has left if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "invulnerable_ticks")

    @classmethod
    def IsAdmiring(cls) -> Molang:
        """Returns 1.0 if the entity is admiring, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_admiring")

    @classmethod
    def IsAlive(cls) -> Molang:
        """Returns 1.0 if the entity is alive, and 0.0 if it's dead.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_alive")

    @classmethod
    def IsAngry(cls) -> Molang:
        """Returns 1.0 if the entity is angry, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_angry")

    @classmethod
    def IsAttachedToEntity(cls) -> Molang:
        """Returns 1.0 if the actor is attached to an entity, else it will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_attached_to_entity")

    @classmethod
    def IsAvoidingBlock(cls) -> Molang:
        """Returns 1.0 if the entity is fleeing from a block, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_avoiding_block")

    @classmethod
    def IsAvoidingMobs(cls) -> Molang:
        """Returns 1.0 if the entity is fleeing from mobs, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_avoiding_mobs")

    @classmethod
    def IsBaby(cls) -> Molang:
        """Returns 1.0 if the entity is a baby, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_baby")

    @classmethod
    def IsBreathing(cls) -> Molang:
        """Returns 1.0 if the entity is breathing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_breathing")

    @classmethod
    def IsBribed(cls) -> Molang:
        """Returns 1.0 if the entity has been bribed, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_bribed")

    @classmethod
    def IsCarryingBlock(cls) -> Molang:
        """Returns 1.0 if the entity is carrying a block, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_carrying_block")

    @classmethod
    def IsCasting(cls) -> Molang:
        """Returns 1.0 if the entity is casting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_casting")

    @classmethod
    def IsCelebrating(cls) -> Molang:
        """Returns 1.0 if the entity is celebrating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_celebrating")

    @classmethod
    def IsCelebratingSpecial(cls) -> Molang:
        """Returns 1.0 if the entity is doing a special celebration, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_celebrating_special")

    @classmethod
    def IsCharged(cls) -> Molang:
        """Returns 1.0 if the entity is charged, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_charged")

    @classmethod
    def IsCharging(cls) -> Molang:
        """Returns 1.0 if the entity is charging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_charging")

    @classmethod
    def IsChested(cls) -> Molang:
        """Returns 1.0 if the entity has chests attached to it, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_chested")

    @classmethod
    def IsCritical(cls) -> Molang:
        """Returns 1.0 if the entity is critical, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_critical")

    @classmethod
    def IsCroaking(cls) -> Molang:
        """Returns 1.0 if the entity is croaking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_croaking")

    @classmethod
    def IsDancing(cls) -> Molang:
        """Returns 1.0 if the entity is dancing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_dancing")

    @classmethod
    def IsDelayedAttacking(cls) -> Molang:
        """Returns 1.0 if the entity is attacking using the delayed attack, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_delayed_attacking")

    @classmethod
    def IsDigging(cls) -> Molang:
        """Returns 1.0 if the entity is digging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_digging")

    @classmethod
    def IsEating(cls) -> Molang:
        """Returns 1.0 if the entity is eating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_eating")

    @classmethod
    def IsEatingMob(cls) -> Molang:
        """Returns 1.0 if the entity is eating a mob, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_eating_mob")

    @classmethod
    def IsElder(cls) -> Molang:
        """Returns 1.0 if the entity is an elder version of it, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_elder")

    @classmethod
    def IsEmerging(cls) -> Molang:
        """Returns 1.0 if the entity is emerging, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_emerging")

    @classmethod
    def IsEmoting(cls) -> Molang:
        """Returns 1.0 if the entity is emoting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_emoting")

    @classmethod
    def IsEnchanted(cls) -> Molang:
        """Returns 1.0 if the entity is enchanted, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_enchanted")

    @classmethod
    def IsFireImmune(cls) -> Molang:
        """Returns 1.0 if the entity is immune to fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_fire_immune")

    @classmethod
    def IsFirstPerson(cls) -> Molang:
        """Returns 1.0 if the entity is being rendered in first person mode, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_first_person")

    @classmethod
    def IsGhost(cls) -> Molang:
        """Returns 1.0 if an entity is a ghost, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_ghost")

    @classmethod
    def IsGliding(cls) -> Molang:
        """Returns 1.0 if the entity is gliding, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_gliding")

    @classmethod
    def IsGrazing(cls) -> Molang:
        """Returns 1.0 if the entity is grazing, or 0.0 if not.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_grazing")

    @classmethod
    def IsIdling(cls) -> Molang:
        """Returns 1.0 if the entity is idling, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_idling")

    @classmethod
    def IsIgnited(cls) -> Molang:
        """Returns 1.0 if the entity is ignited, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_ignited")

    @classmethod
    def IsIllagerCaptain(cls) -> Molang:
        """Returns 1.0 if the entity is an illager captain, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_illager_captain")

    @classmethod
    def IsInContactWithWater(cls) -> Molang:
        """Returns 1.0 if the entity is in contact with any water (water, rain, splash water bottle), else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_contact_with_water")

    @classmethod
    def IsInLove(cls) -> Molang:
        """Returns 1.0 if the entity is in love, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_love")

    @classmethod
    def IsInUI(cls) -> Molang:
        """Returns 1.0 if the entity is rendered as part of the UI, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_ui")

    @classmethod
    def IsInWater(cls) -> Molang:
        """Returns 1.0 if the entity is in water, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_water")

    @classmethod
    def IsInWaterOrRain(cls) -> Molang:
        """Returns 1.0 if the entity is in water or rain, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_water_or_rain")

    @classmethod
    def IsInterested(cls) -> Molang:
        """Returns 1.0 if the entity is interested, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_interested")

    @classmethod
    def IsInvisible(cls) -> Molang:
        """Returns 1.0 if the entity is invisible, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_invisible")

    @classmethod
    def IsItemEquipped(cls, hand: int = 0) -> Molang:
        """Takes one optional hand slot as a parameter and returns 1.0 if there is an item in the requested slot, otherwise returns 0.0.

        - 0 = main_hand
        - 1 = off_hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "is_item_equipped", _checked("hand", hand, 0, 1)
        )

    @classmethod
    def IsItemNameAny(
        cls, slot: Slots, index: int, item_identifiers: list[str]
    ) -> Molang:
        """Takes an equipment slot name (see the replaceitem command) and an optional slot index value. After that, takes one or more full name (with 'namespace:') strings to check for. Returns 1.0 if an item in the specified slot has any of the specified names, otherwise returns 0.0. An empty string '' can be specified to check for an empty slot. Note that querying slot.enderchest, slot.saddle, slot.armor, or slot.chest will only work in behavior packs. A preferred query to query.get_equipped_item_name, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "is_item_name_any",
            slot,
            index,
            *(str(item_identifier) for item_identifier in item_identifiers),
        )

    @classmethod
    def IsJumping(cls) -> Molang:
        """Returns 1.0 if the entity is jumping, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_jumping")

    @classmethod
    def IsLayingDown(cls) -> Molang:
        """Returns 1.0 if the entity is laying down, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_laying_down")

    @classmethod
    def IsLayingEgg(cls) -> Molang:
        """Returns 1.0 if the entity is laying an egg, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_laying_egg")

    @classmethod
    def IsLeashed(cls) -> Molang:
        """Returns 1.0 if the entity is leashed to something, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_leashed")

    @classmethod
    def IsLevitating(cls) -> Molang:
        """Returns 1.0 if the entity is levitating, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_levitating")

    @classmethod
    def IsLingering(cls) -> Molang:
        """Returns 1.0 if the entity is lingering, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_lingering")

    @classmethod
    def IsLocalPlayer(cls) -> Molang:
        """### Client Only
        Takes no arguments. Returns 1.0 if the entity is the local player for the current game window, else it returns 0.0. In splitscreen returns 0.0 for the other local players for other views. Always returns 0.0 if used in a behavior pack.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_local_player")

    @classmethod
    def IsMoving(cls) -> Molang:
        """Returns 1.0 if the entity is moving, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_moving")

    @classmethod
    def IsNameAny(cls, *names: str) -> Molang:
        """Takes one or more arguments. If the entity's name is any of the specified string values, returns 1.0. Otherwise returns 0.0.

        A preferred query to query.get_name, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_name_any", *names)

    @classmethod
    def IsOnFire(cls) -> Molang:
        """Returns 1.0 if the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_on_fire")

    @classmethod
    def IsOnGround(cls) -> Molang:
        """Returns 1.0 if the entity is on the ground, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_on_ground")

    @classmethod
    def IsOnScreen(cls) -> Molang:
        """Returns 1.0 if this is called on an entity at a time when it is known if it is on screen, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_on_screen")

    @classmethod
    def IsOnfire(cls) -> Molang:
        """Returns 1.0 if the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_onfire")

    @classmethod
    def IsOrphaned(cls) -> Molang:
        """Returns 1.0 if the entity is orphaned, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_orphaned")

    @classmethod
    def IsOwnerIdentifierAny(cls, *identifiers: str) -> Molang:
        """Takes one or more arguments. Returns whether the root actor identifier is any of the specified strings. A preferred query to query.owner_identifier, as it can be adjusted by Mojang to avoid breaking content if names are changed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_owner_identifier_any", *identifiers)

    @classmethod
    def IsPersonaOrPremiumSkin(cls) -> Molang:
        """Returns 1.0 if the player has a persona or premium skin, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_persona_or_premium_skin")

    @classmethod
    def IsPlayingDead(cls) -> Molang:
        """Returns 1.0 if the entity is playing dead, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_playing_dead")

    @classmethod
    def IsPowered(cls) -> Molang:
        """Returns 1.0 if the entity is powered, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_powered")

    @classmethod
    def IsPregnant(cls) -> Molang:
        """Returns 1.0 if the entity is pregnant, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_pregnant")

    @classmethod
    def IsRamAttacking(cls) -> Molang:
        """Returns 1.0 if the entity is using a ram attack, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_ram_attacking")

    @classmethod
    def IsResting(cls) -> Molang:
        """Returns 1.0 if the entity is resting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_resting")

    @classmethod
    def IsRiding(cls) -> Molang:
        """Returns 1.0 if the entity is riding, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_riding")

    @classmethod
    def IsRoaring(cls) -> Molang:
        """Returns 1.0 if the entity is currently roaring, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_roaring")

    @classmethod
    def IsRolling(cls) -> Molang:
        """Returns 1.0 if the entity is rolling, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_rolling")

    @classmethod
    def IsSaddled(cls) -> Molang:
        """Returns 1.0 if the entity has a saddle, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_saddled")

    @classmethod
    def IsScared(cls) -> Molang:
        """Returns 1.0 if the entity is scared, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_scared")

    @classmethod
    def IsSelectedItem(cls) -> Molang:
        """Returns true if the player has selected an item in the inventory, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_selected_item")

    @classmethod
    def IsShaking(cls) -> Molang:
        """Returns 1.0 if the entity is casting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_shaking")

    @classmethod
    def IsShakingWetness(cls) -> Molang:
        """Returns 1.0 if the entity is shaking water off, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_shaking_wetness")

    @classmethod
    def IsSheared(cls) -> Molang:
        """Returns 1.0 if the entity is able to be sheared and is

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sheared")

    @classmethod
    def IsShieldPowered(cls) -> Molang:
        """Returns 1.0f if the entity has an active powered shield if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_shield_powered")

    @classmethod
    def IsSilent(cls) -> Molang:
        """Returns 1.0 if the entity is silent, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_silent")

    @classmethod
    def IsSitting(cls) -> Molang:
        """Returns 1.0 if the entity is sitting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sitting")

    @classmethod
    def IsSleeping(cls) -> Molang:
        """Returns 1.0 if the entity is sleeping, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sleeping")

    @classmethod
    def IsSneaking(cls) -> Molang:
        """Returns 1.0 if the entity is sneaking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sneaking")

    @classmethod
    def IsSneezing(cls) -> Molang:
        """Returns 1.0 if the entity is sneezing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sneezing")

    @classmethod
    def IsSniffing(cls) -> Molang:
        """Returns 1.0 if the entity is sniffing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sniffing")

    @classmethod
    def IsSonicBoom(cls) -> Molang:
        """Returns 1.0 if the entity is using sonic boom, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sonic_boom")

    @classmethod
    def IsSprinting(cls) -> Molang:
        """Returns 1.0 if the entity is sprinting, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_sprinting")

    @classmethod
    def IsStackable(cls) -> Molang:
        """Returns 1.0 if the entity is stackable, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_stackable")

    @classmethod
    def IsStalking(cls) -> Molang:
        """Returns 1.0 if the entity is stalking, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_stalking")

    @classmethod
    def IsStanding(cls) -> Molang:
        """Returns 1.0 if the entity is standing, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_standing")

    @classmethod
    def IsStunned(cls) -> Molang:
        """Returns 1.0 if the entity is currently stunned, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_stunned")

    @classmethod
    def IsSwimming(cls) -> Molang:
        """Returns 1.0 if the entity is swimming, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_swimming")

    @classmethod
    def IsTamed(cls) -> Molang:
        """Returns 1.0 if the entity is tamed, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_tamed")

    @classmethod
    def IsTransforming(cls) -> Molang:
        """Returns 1.0 if the entity is transforming, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_transforming")

    @classmethod
    def IsUsingItem(cls) -> Molang:
        """Returns 1.0 if the entity is using an item, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_using_item")

    @classmethod
    def IsWallClimbing(cls) -> Molang:
        """Returns 1.0 if the entity is climbing a wall, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_wall_climbing")

    @classmethod
    def ItemInUseDuration(cls) -> Molang:
        """Returns the amount of time an item has been in use in seconds up to the maximum duration, else 0.0 if it doesn't make sense.

        **Note**: The value exported by this query is calculated by dividing the internal tick count by 200 to convert it to seconds from whatever internal unit is used.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "item_in_use_duration") / 200

    @classmethod
    def ItemIsCharged(cls, hand: int = 0) -> Molang:
        """Takes one optional hand slot as a parameter and returns 1.0 if the item is charged in the requested slot (defaulting to the main hand if no parameter is supplied), otherwise returns 0.0.

        - 0 = main_hand
        - 1 = off_hand

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "item_is_charged", _checked("hand", hand, 0, 1)
        )

    @classmethod
    def ItemMaxUseDuration(cls) -> Molang:
        """Returns the maximum amount of time the item can be used, else 0.0 if it doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "item_max_use_duration")

    @classmethod
    def ItemRemainingUseDuration(cls, hand: int = 0) -> Molang:
        """Returns the amount of time an item has left to use, else 0.0 if it doesn't make sense. Time remaining is normalized using the normalization value, only if one is given, else it is returned in seconds.

        - main_hand = 0
        - off_hand = 1

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "item_remaining_use_duration",
            _checked("hand", hand, 0, 1),
        )

    @classmethod
    def ItemSlotToBoneName(cls, slot: Slots) -> Molang:
        """Requires one parameter: the name of the equipment slot. This function returns the name of the bone this entity has mapped to that slot.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "item_slot_to_bone_name", slot)

    @classmethod
    def KeyFrameLerpTime(cls) -> Molang:
        """Returns the ratio between the previous and next key frames

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "key_frame_lerp_time")

    @classmethod
    def LastFrameTime(cls, frame: int = 0) -> Molang:
        """Returns the time in *seconds* of the last frame.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.


        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "last_frame_time", _checked("frame", frame, 0, 30)
        )

    @classmethod
    def LastHitByPlayer(cls) -> Molang:
        """### Server Only

        Returns 1.0 if the entity was last hit by the player, else it returns 0.0. If called by the client always returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "last_hit_by_player")

    @classmethod
    def LieAmount(cls) -> Molang:
        """Returns the lie down amount for the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "lie_amount")

    @classmethod
    def LifeSpan(cls) -> Molang:
        """Returns the limited life span of an entity, or 0.0 if it lives forever

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "life_span")

    @classmethod
    def LifeTime(cls) -> Molang:
        """Returns the time in seconds since the current animation started, else 0.0 if not called within an animation.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "life_time")

    @classmethod
    def LodIndex(cls, d1: int, d2: int, d3: int) -> Molang:
        """Takes an array of distances and returns the zero - based index of which range the actor is in based on distance from the camera.

        For example, 'query.lod_index(10, 20, 30)' will return 0, 1, or 2 based on whether the mob is less than 10, 20, or 30 units away from the camera, or it will return 3 if it is greater than 30.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "lod_index", d1, d2, d3)

    @classmethod
    def Log(cls, query) -> Molang:
        """Debug log a value to the content log.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "log", query)

    @classmethod
    def MainHandItemMaxDuration(cls) -> Molang:
        """Returns the use time maximum duration for the main hand item if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "main_hand_item_max_duration")

    @classmethod
    def MainHandItemUseDuration(cls) -> Molang:
        """Returns the use time for the main hand item.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "main_hand_item_use_duration")

    @classmethod
    def MarkVariant(cls) -> Molang:
        """Returns the entity's mark variant.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "mark_variant")

    @classmethod
    def MaxDurability(cls) -> Molang:
        """Returns the max durability an item can take.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "max_durability")

    @classmethod
    def MaxHealth(cls) -> Molang:
        """Returns the maximum health of the entity, or 0.0 if it doesn't make sense to call on this entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "max_health")

    @classmethod
    def MaxTradeTier(cls) -> Molang:
        """Returns the maximum trade tier of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "max_trade_tier")

    @classmethod
    def MaximumFrameTime(cls, frame: int = 0) -> Molang:
        """Returns the time in *seconds* of the most expensive frame over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "maximum_frame_time", _checked("frame", frame, 0, 30)
        )

    @classmethod
    def MinimumFrameTime(cls, frame: int = 0) -> Molang:
        """Returns the time in *seconds* of the least expensive frame over the last 'n' frames.
        If an argument is passed, it is assumed to be the number of frames in the past that you wish to query.

        frame = 0 will return the frame time of the frame before the current one.
        frame = 1 will return the average frame time of the previous two frames.

        Currently we store the history of the last 30 frames, although note that this may change in the future.
        Asking for more frames will result in only sampling the number of frames stored.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "minimum_frame_time", _checked("frame", frame, 0, 30)
        )

    @classmethod
    def ModelScale(cls) -> Molang:
        """Returns the scale of the current entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "model_scale")

    @classmethod
    def ModifiedDistanceMoved(cls) -> Molang:
        """Returns the total distance the entity has moved horizontally in meters (since the entity was last loaded, not necessarily since it was originally created) modified along the way by status flags such as is_baby or on_fire.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "modified_distance_moved")

    @classmethod
    def ModifiedMoveSpeed(cls) -> Molang:
        """Returns the current walk speed of the entity modified by status flags such as is_baby or on_fire.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "modified_move_speed")

    @classmethod
    def ModifiedSwingDuration(cls) -> Molang:
        """Returns the duration of the entity's swing modifier.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "modified_swing_duration")

    @classmethod
    def MoonBrightness(cls) -> Molang:
        """Returns the brightness of the moon

        - FULL_MOON = 1.0
        - WANING_GIBBOUS = 0.75
        - FIRST_QUARTER = 0.5
        - WANING_CRESCENT = 0.25
        - NEW_MOON = 0.0
        - WAXING_CRESCENT = 0.25
        - LAST_QUARTER = 0.5
        - WAXING_GIBBOUS = 0.75

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "moon_brightness")

    @classmethod
    def MoonPhase(cls) -> Molang:
        """Returns the phase of the moon

        - FULL_MOON = 0
        - WANING_GIBBOUS = 1
        - FIRST_QUARTER = 2
        - WANING_CRESCENT = 3
        - NEW_MOON = 4
        - WAXING_CRESCENT = 5
        - LAST_QUARTER = 6
        - WAXING_GIBBOUS = 7

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "moon_phase")

    @classmethod
    def MovementDirection(cls, axis: int) -> Molang:
        """Returns the specified axis of the normalized position delta of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "movement_direction", axis)

    @classmethod
    def Noise(cls) -> Molang:
        """Queries Perlin Noise Map.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "noise")

    @classmethod
    def OnFireTime(cls) -> Molang:
        """Returns the time that the entity is on fire, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "on_fire_time")

    @classmethod
    def OutOfControl(cls) -> Molang:
        """Returns 1.0 if the entity is out of control, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "out_of_control")

    @classmethod
    @deprecated("Query.OverlayAlpha is deprecated by Minecraft and will be removed.")
    def OverlayAlpha(cls) -> Molang:
        """DEPRECATED (Do not use - this function is deprecated and will be removed).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "overlay_alpha")

    @classmethod
    @deprecated(
        "Query.OwnerIdentifier is deprecated by Minecraft. Use Query.IsOwnerIdentifierAny instead."
    )
    def OwnerIdentifier(cls) -> Molang:
        """DEPRECATED (Use query.is_owner_identifier_any instead if possible so names can be changed later without breaking content.) Returns the root actor identifier.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "owner_identifier")

    @classmethod
    def PlayerLevel(cls) -> Molang:
        """Returns the players level if the actor is a player, otherwise returns 0

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "player_level")

    @classmethod
    def Position(cls, axis: int) -> Molang:
        """Returns the absolute position of an actor.  Takes one argument that represents the desired axis (0 == x-axis, 1 == y-axis, 2 == z-axis).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "position", _checked("axis", axis, 0, 2))

    @classmethod
    def PositionDelta(cls, axis: int) -> Molang:
        """Returns the position delta for an actor.  Takes one argument that represents the desired axis (0 == x-axis, 1 == y-axis, 2 == z-axis).

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "position_delta", _checked("axis", axis, 0, 2)
        )

    @classmethod
    def PreviousSquishValue(cls) -> Molang:
        """Returns the previous squish value for the current entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "previous_squish_value")

    @classmethod
    def RemainingDurability(cls) -> Molang:
        """Returns the how much durability an item has remaining. Behaviour pack exclusive, raises an error if used in a resource pack.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "remaining_durability")

    @classmethod
    def RollCounter(cls) -> Molang:
        """Returns the roll counter of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "roll_counter")

    @classmethod
    def RotationToCamera(cls, axis: int) -> Molang:
        """Returns the rotation required to aim at the camera.  Requires one argument representing the rotation axis you would like (0 for x, 1 for y)

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "rotation_to_camera", _checked("axis", axis, 0, 1)
        )

    @classmethod
    def ShakeAngle(cls) -> Molang:
        """Returns the shaking angle of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "shake_angle")

    @classmethod
    def ShakeTime(cls) -> Molang:
        """Returns the shake time of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "shake_time")

    @classmethod
    def ShieldBlockingBob(cls) -> Molang:
        """Returns the how much the offhand shield should translate down when blocking and being hit.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "shield_blocking_bob")

    @classmethod
    def ShowBottom(cls) -> Molang:
        """Returns 1.0 if we render the entity's bottom, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "show_bottom")

    @classmethod
    def SitAmount(cls) -> Molang:
        """Returns the current sit amount of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "sit_amount")

    @classmethod
    def SkinId(cls) -> Molang:
        """Returns the entity's skin ID

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "skin_id")

    @classmethod
    def SleepRotation(cls) -> Molang:
        """Returns the rotation of the bed the player is sleeping on.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "sleep_rotation")

    @classmethod
    def SneezeCounter(cls) -> Molang:
        """Returns the sneeze counter of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "sneeze_counter")

    @classmethod
    def Spellcolor(cls) -> _ColorStruct:
        """Returns a struct representing the entity spell color for the specified entity. The struct contains '.r' '.g' '.b' and '.a' members, each 0.0 to 1.0. If no actor is specified, each member value will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _ColorStruct(cls.__query__(cls, cls.handle, "spellcolor"))

    @classmethod
    def StandingScale(cls) -> Molang:
        """Returns the scale of how standing up the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "standing_scale")

    @classmethod
    def StructuralIntegrity(cls) -> Molang:
        """Returns the structural integrity for the actor, otherwise returns 0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "structural_integrity")

    @classmethod
    def SurfaceParticleColor(cls) -> _ColorStruct:
        """### Client Only

        Returns the particle color for the block located in the surface below the actor (scanned up to 10 blocks down). The struct contains '.r' '.g' '.b' and '.a' members, each 0.0 to 1.0. If no actor is specified or if no surface is found, each member value is set to 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _ColorStruct(cls.__query__(cls, cls.handle, "surface_particle_color"))

    @classmethod
    def SurfaceParticleTextureCoordinate(cls) -> _UVStruct:
        """### Client Only

        Returns the texture coordinate for generating particles for the block located in the surface below the actor (scanned up to 10 blocks down) in a struct with 'u' and 'v' keys. If no actor is specified or if no surface is found, u and v will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _UVStruct(
            cls.__query__(cls, cls.handle, "surface_particle_texture_coordinate")
        )

    @classmethod
    def SurfaceParticleTextureSize(cls) -> _UVStruct:
        """### Client Only

        Returns the texture size for generating particles for the block located in the surface below the actor (scanned up to 10 blocks down). If no actor is specified or if no surface is found, each member value will be 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _UVStruct(
            cls.__query__(cls, cls.handle, "surface_particle_texture_size")
        )

    @classmethod
    def SwellAmount(cls) -> Molang:
        """Returns how swollen the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "swell_amount")

    @classmethod
    def SwellingDir(cls) -> Molang:
        """Returns the swelling direction of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "swelling_dir")

    @classmethod
    def SwimAmount(cls) -> Molang:
        """Returns the amount the current entity is swimming.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "swim_amount")

    @classmethod
    def TailAngle(cls) -> Molang:
        """Returns the angle of the tail of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "tail_angle")

    @classmethod
    def TargetXRotation(cls) -> Molang:
        """Returns the x rotation required to aim at the entity's current target if it has one, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "target_x_rotation")

    @classmethod
    def TargetYRotation(cls) -> Molang:
        """Returns the y rotation required to aim at the entity's current target if it has one, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "target_y_rotation")

    @classmethod
    def TextureFrameIndex(cls) -> Molang:
        """Returns the icon index of the experience orb

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "texture_frame_index")

    @classmethod
    def TimeOfDay(cls) -> Molang:
        """Returns the time of day (midnight=0.0, sunrise=0.25, noon=0.5, sunset=0.75) of the dimension the entity is in.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "time_of_day")

    @classmethod
    def TimeSinceLastVibrationDetection(cls) -> Molang:
        """### Client Only

        Returns the time in seconds since the last vibration detected by the actor. On errors or if no vibration has been detected yet, returns -1.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "time_since_last_vibration_detection")

    @classmethod
    def TimeStamp(cls) -> Molang:
        """Returns the current time stamp of the level.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "time_stamp")

    @classmethod
    def TotalEmitterCount(cls) -> Molang:
        """Returns the total number of active emitters in the world.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "total_emitter_count")

    @classmethod
    def TotalParticleCount(cls) -> Molang:
        """Returns the total number of active particles in the world.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "total_particle_count")

    @classmethod
    def TradeTier(cls) -> Molang:
        """Returns the trade tier of the entity if it makes sense, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "trade_tier")

    @classmethod
    def UnhappyCounter(cls) -> Molang:
        """Returns how unhappy the entity is.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "unhappy_counter")

    @classmethod
    def Variant(cls) -> Molang:
        """Returns the entity's variant index.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "variant")

    @classmethod
    def VerticalSpeed(cls) -> Molang:
        """Returns the speed of the entity up or down in meters/second, where positive is up.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "vertical_speed")

    @classmethod
    def WalkDistance(cls) -> Molang:
        """Returns the walk distance of the entity.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "walk_distance")

    @classmethod
    def WingFlapPosition(cls) -> Molang:
        """Returns the wing flap position of the entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "wing_flap_position")

    @classmethod
    def WingFlapSpeed(cls) -> Molang:
        """Returns the wing flap speed of the entity, or 0.0 if this doesn't make sense.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "wing_flap_speed")

    @classmethod
    def YawSpeed(cls) -> Molang:
        """Returns the entity's yaw speed.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "yaw_speed")

    @classmethod
    def TimerFlag1(cls) -> Molang:
        """Returns the value of timer_flag_1 set by behavior.timer_flag_1

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "timer_flag_1")

    @classmethod
    def TimerFlag2(cls) -> Molang:
        """Returns the value of timer_flag_2 set by behavior.timer_flag_2

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "timer_flag_2")

    @classmethod
    def TimerFlag3(cls) -> Molang:
        """Returns the value of timer_flag_3 set by behavior.timer_flag_3

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "timer_flag_3")

    @classmethod
    def IsSpectator(cls) -> Molang:
        """Returns 1.0 if the entity is a spectator, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_spectator")

    @classmethod
    def IsCooldownCategory(
        cls, cooldown_name: str, slot: Slots, slot_id: int = 0
    ) -> Molang:
        """Returns 1.0 if the specified held or worn item has the specified cooldown category name, otherwise returns 0.0. First argument is the cooldown name to check for, second argument is the equipment slot name, and if required third argument is the numerical slot id. For second and third arguments, uses the same name and id that the replaceitem command takes when querying entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "is_cooldown_category", cooldown_name, slot, slot_id
        )

    @classmethod
    def CooldownTime(cls, slot: Slots, slot_id: int = 0) -> Molang:
        """Returns the total cooldown time in seconds for the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cooldown_time", slot, slot_id)

    @overload
    @classmethod
    def CooldownTimeRemaining(cls, slot: Slots, slot_id: int = 0) -> Molang:
        """Returns the cooldown time remaining in seconds for the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        ...

    @overload
    @classmethod
    def CooldownTimeRemaining(cls, cooldown_name: str) -> Molang:
        """Returns the cooldown time remaining in seconds for specified cooldown type, otherwise returns 0. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        ...

    @classmethod
    def CooldownTimeRemaining(
        cls, arg1: Slots | str = None, arg2: int = None
    ) -> Molang:
        """Returns the cooldown time remaining in seconds for specified cooldown type or the item held or worn by the specified equipment slot name (and if required second numerical slot id), otherwise returns 0. Uses the same name and id that the replaceitem command takes when querying entities. Returns highest cooldown if no parameters are supplied.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "cooldown_time_remaining", arg1, arg2)

    @classmethod
    def RelativeBlockHasAnyTag(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes an entity-relative position and one or more tag names, and returns either 0 or 1 based on if that block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "relative_block_has_any_tag",
            x,
            y,
            z,
            *_list_of("Query.RelativeBlockHasAnyTag", "tags", tags),
        )

    @classmethod
    def RelativeBlockHasAllTags(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes an entity-relative position and one or more tag names, and returns either 0 or 1 based on if that block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "relative_block_has_all_tags",
            x,
            y,
            z,
            *_list_of("Query.RelativeBlockHasAllTags", "tags", tags),
        )

    @classmethod
    def BlockNeighborHasAnyTag(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes a block-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "block_neighbor_has_any_tag",
            x,
            y,
            z,
            *_list_of("Query.BlockNeighborHasAnyTag", "tags", tags),
        )

    @classmethod
    def BlockNeighborHasAllTags(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes a block-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "block_neighbor_has_all_tags",
            x,
            y,
            z,
            *_list_of("Query.BlockNeighborHasAllTags", "tags", tags),
        )

    @classmethod
    def BlockHasAllTags(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes a world-origin-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "block_has_all_tags",
            x,
            y,
            z,
            *_list_of("Query.BlockHasAllTags", "tags", tags),
        )

    @classmethod
    def BlockHasAnyTag(cls, x: int, y: int, z: int, tags: list[str]) -> Molang:
        """Takes a world-origin-relative position and one or more tag names, and returns either 0 or 1 based on if the block at that position has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "block_has_any_tag",
            x,
            y,
            z,
            *_list_of("Query.BlockHasAnyTag", "tags", tags),
        )

    @classmethod
    def BoneOrientationTrs(cls, bone_name: str) -> _TRSStruct:
        """TRS stands for 'Translate/Rotate/Scale.' Takes the name of the bone as an argument. Returns the bone orientation matrix decomposed into the component translation/rotation/scale parts of the desired bone provided it exists in the queryable geometry of the entity, else this returns the identity matrix and throws a content error. The returned value is returned as a variable of type struct with members .t, .r, and .s, each with members .x, .y, and .z, and can be accessed as per this example: v.my_variable = q.bone_orientation_trs('rightarm'); return v.my_variable.r.x;

        Returns:
            Molang(Molang): A Molang Instance
        """
        return _TRSStruct(
            cls.__query__(cls, cls.handle, "bone_orientation_trs", bone_name)
        )

    @classmethod
    def BoneOrientationMatrix(cls, bone_name: str) -> Molang:
        """Takes the name of the bone as an argument. Returns the bone orientation (as a matrix) of the desired bone provided it exists in the queryable geometry of the entity, else this returns the identity matrix and throws a content error.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "bone_orientation_matrix", bone_name)

    @classmethod
    def IsAttached(cls) -> Molang:
        """### Client Only

        Returns 1.0 if the entity is attached to another entity (such as being held or worn), else it will return 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_attached")

    @classmethod
    def HasPlayerRider(cls) -> Molang:
        """Returns 1.0 if the entity has a player rider, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_player_rider")

    @classmethod
    def Scoreboard(cls, score) -> Molang:
        """### Server Only
        Returns the specified scoreboard value for this entity.

        Args:
            score (str): The name of the scoreboard to query.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "scoreboard", score)

    @classmethod
    def RideBodyXRotation(cls) -> Molang:
        """Returns the body pitch world-rotation of the ride an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ride_body_x_rotation")

    @classmethod
    def RideBodyYRotation(cls) -> Molang:
        """Returns the body pitch world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ride_body_y_rotation")

    @classmethod
    def RideHeadXRotation(cls) -> Molang:
        """Returns the head x world-rotation of the ride of an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ride_head_x_rotation")

    @classmethod
    def RideHeadYRotation(cls, clamp: int = 0) -> Molang:
        """Takes one optional argument as a parameter. Returns the head y world-rotation of the ride of an entity, else it returns 0.0. First parameter only for horses, zombie horses, skeleton horses, donkeys and mules that clamps rotation in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ride_head_y_rotation", clamp)

    @classmethod
    def RiderBodyXRotation(cls, rider: int = 0) -> Molang:
        """Returns the body pitch world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "rider_body_x_rotation", rider)

    @classmethod
    def RiderBodyYRotation(cls, rider: int = 0) -> Molang:
        """Returns the body yaw world-rotation of a valid rider at the provided index if called on an entity, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "rider_body_y_rotation", rider)

    @classmethod
    def RiderHeadXRotation(cls, head: int = 0) -> Molang:
        """Takes one argument as a parameter. Returns the head x world-rotation of the rider entity at the provided index, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "rider_head_x_rotation", head)

    @classmethod
    def RiderHeadYRotation(cls, head: int = 0, clamp: int = 0) -> Molang:
        """Takes one or two arguments as parameters. Returns the head y world-rotation of the rider entity at the provided index, else it returns 0.0. Horses, zombie horses, skeleton horses, donkeys and mules require a second parameter that clamps rotation in degrees.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "rider_head_y_rotation", head, clamp)

    @classmethod
    def ArmorDamageSlot(cls, index: int) -> Molang:
        """Returns the damage value of the item in an armor slot.

        Args:
            index (int): The armor slot: 0 head, 1 chest, 2 legs, 3 feet, 4 body.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "armor_damage_slot", _checked("index", index, 0, 4)
        )

    @classmethod
    def ClientMemoryTier(cls) -> Molang:
        """Returns a number representing the client RAM memory tier, 0 = 'Undetermined', 1 = 'SuperLow', 2 = 'Low', 3 = 'Mid', 4 = 'High', or 5 = 'SuperHigh'. Available on the Client (Resource Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "client_memory_tier")

    @classmethod
    def ServerMemoryTier(cls) -> Molang:
        """Returns a number representing the server RAM memory tier, 0 = 'SuperLow', 1 = 'Low', 2 = 'Mid', 3 = 'High', or 4 = 'SuperHigh'. Available on the server side (behavior Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "server_memory_tier")

    @classmethod
    def ClientMaxRenderDistance(cls) -> Molang:
        """Returns the max render distance in chunks of the current client. Available on the Client (Resource Packs) only.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "client_max_render_distance")

    @classmethod
    def LastInputModeIsAny(cls, input: InputModes) -> Molang:
        """Returns 1.0 if the last input mode is any of the specified input modes, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "last_input_mode_is_any", input)

    @classmethod
    def TouchOnlyAffectsHotbar(cls) -> Molang:
        """Returns 1.0 if the touch only affects hotbar, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "touch_only_affects_hotbar")

    @classmethod
    def GetPackSetting(cls, id: str) -> Molang:
        """### Client Only

        Returns value of Pack Setting slider, parameter is name of slider. Available on the Client (Resource Packs) only.

        Args:
            id (str): The name of the pack setting slider to query.
        Returns:
            Molang(Molang): A Molang Instance representing a numerical value of the slider.
        """
        if MANIFEST_VERSION < 3:
            raise ValueError(
                "Pack Settings are not supported in Manifest Version below 3."
            )

        from anvil.api.core.core import ManifestRP

        if f"{CONFIG.NAMESPACE}:{id}" not in ManifestRP()._setting_names("slider"):
            raise ValueError(
                f"Pack Setting '{id}' does not exist in sliders, make sure to register it using `ManifestRP()`."
            )

        return cls.__query__(
            cls, cls.handle, "get_pack_setting", f"{CONFIG.NAMESPACE}:{id}"
        )

    @classmethod
    def IsPackSettingEnabled(cls, id: str) -> Molang:
        """### Client Only

        Returns 1.0 if Pack Setting toggle is enabled, else it returns 0.0. Parameter is name of toggle. Available on the Client (Resource Packs) only.

        Args:
            id (str): The name of the pack setting toggle to query.

        Returns:
            Molang(Molang): A Molang Instance representing a boolean value of the toggle.
        """
        if MANIFEST_VERSION < 3:
            raise ValueError(
                "Pack Settings are not supported in Manifest Version below 3."
            )

        from anvil.api.core.core import ManifestRP

        if f"{CONFIG.NAMESPACE}:{id}" not in ManifestRP()._setting_names("toggle"):
            raise ValueError(
                f"Pack Setting '{id}' does not exist in toggles, make sure to register it using `ManifestRP()`."
            )

        return cls.__query__(
            cls, cls.handle, "is_pack_setting_enabled", f"{CONFIG.NAMESPACE}:{id}"
        )

    @classmethod
    def IsPackSettingSelected(cls, id: str, option: str) -> Molang:
        """### Client Only

        Returns 1.0 if Pack Setting dropdown selection matches the specified option, else it returns 0.0.

        Args:
            id (str): The name of the pack setting selection to query.
            option (str): The option to check for.

        Returns:
            Molang(Molang): A Molang Instance representing a boolean value of the selection.
        """

        if MANIFEST_VERSION < 3:
            raise ValueError(
                "Pack Settings are not supported in Manifest Version below 3."
            )

        from anvil.api.core.core import ManifestRP

        options = ManifestRP()._dropdown_options(f"{CONFIG.NAMESPACE}:{id}")

        if options is None:
            raise ValueError(
                f"Pack Setting '{id}' does not exist in dropdowns, make sure to register it using `ManifestRP()`."
            )

        if option not in options:
            raise ValueError(
                f"Option '{option}' does not exist in dropdown '{id}', available options are: {', '.join(options)}."
            )

        return cls.__query__(
            cls,
            cls.handle,
            "is_pack_setting_selected",
            f"{CONFIG.NAMESPACE}:{id}",
            option,
        )

    @classmethod
    def EntityBiomeHasAllTags(cls, tags: list[str]) -> Molang:
        """Takes one or more tag names, and returns either 0 or 1 based on if the biome the entity is currently in has all of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "entity_biome_has_all_tags",
            *_list_of("Query.EntityBiomeHasAllTags", "tags", tags),
        )

    @classmethod
    def EntityBiomeHasAnyTags(cls, tags: list[str]) -> Molang:
        """Takes one or more tag names, and returns either 0 or 1 based on if the biome the entity is currently in has any of the tags provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "entity_biome_has_any_tags",
            *_list_of("Query.EntityBiomeHasAnyTags", "tags", tags),
        )

    @classmethod
    def EntityBiomeHasAnyIdentifier(
        cls, identifiers: tuple[MinecraftBiomeDescriptor | str]
    ) -> Molang:
        """Takes one or more biome identifiers or MinecraftBiomeDescriptor instances, and returns either 0 or 1 based on if the biome the entity is currently in matches any of the identifiers provided.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls, cls.handle, "entity_biome_has_any_identifier", *identifiers
        )

    @classmethod
    def KineticWeaponDelay(cls) -> Molang:
        """Returns the "delay" value from the main-hand item's "minecraft:kinetic_weapon" component, or 0 if the component is not present.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "kinetic_weapon_delay")

    @classmethod
    def KineticWeaponDamageDuration(cls) -> Molang:
        """Returns the 'max_duration' value of 'damage_conditions' from the main-hand item's 'minecraft:kinetic_weapon' component, or 0 if the component is not present.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "kinetic_weapon_damage_duration")

    @classmethod
    def KineticWeaponKnockbackDuration(cls) -> Molang:
        """Returns the 'max_duration' value of 'knockback_conditions' from the main-hand item's 'minecraft:kinetic_weapon' component, or 0 if the component is not present.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "kinetic_weapon_knockback_duration")

    @classmethod
    def KineticWeaponDismountDuration(cls) -> Molang:
        """Returns the 'max_duration' value of 'dismount_conditions' from the main-hand item's 'minecraft:kinetic_weapon' component, or 0 if the component is not present.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "kinetic_weapon_dismount_duration")

    @classmethod
    def TicksSinceLastKineticWeaponHit(cls) -> Molang:
        """Returns the number of ticks elapsed since the user last hit something while using a kinetic weapon.
        Returns -1.0 if no kinetic weapon is being used or if nothing has been hit yet. Hits that occur while the user is unloaded are not counted.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "ticks_since_last_kinetic_weapon_hit")

    @classmethod
    def StateTime(cls) -> Molang:
        """Returns the time in seconds since the entity entered its current state.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "state_time")

    @classmethod
    def GetLevelSeedBasedFraction(cls) -> Molang:
        """Returns the level seed based fraction, a value between 0.0 and 1.0 that is determined by the world seed but changes every tick.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "get_level_seed_based_fraction")

    @classmethod
    def CanDash(cls) -> Molang:
        """Returns 1.0 if the entity can dash, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "can_dash")

    @classmethod
    def GraphicsModeIsAny(
        cls, modes: list[Literal["simple", "fancy", "deferred", "raytraced"]]
    ) -> Molang:
        """### Client Only

        Returns 1.0 if the client's graphics mode is any of the given modes, else it returns 0.0.

        Args:
            modes (list[Literal["simple", "fancy", "deferred", "raytraced"]]): The graphics modes to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "graphics_mode_is_any",
            *_list_of("Query.GraphicsModeIsAny", "graphics modes", modes),
        )

    @classmethod
    def HasDashCooldown(cls) -> Molang:
        """Returns 1.0 if the entity's dash is on cooldown, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_dash_cooldown")

    @classmethod
    def HasHeadGear(cls) -> Molang:
        """Returns 1.0 if the entity has an item in its head armor slot, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "has_head_gear")

    @classmethod
    def HeadIsInWater(cls) -> Molang:
        """Returns 1.0 if the entity's head is in water, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "head_is_in_water")

    @classmethod
    def IsCrawling(cls) -> Molang:
        """Returns 1.0 if the entity is crawling, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_crawling")

    @classmethod
    def IsInLava(cls) -> Molang:
        """Returns 1.0 if the entity is in lava, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_in_lava")

    @classmethod
    def IsRidingAnyEntityOfType(cls, types: list[str]) -> Molang:
        """Returns 1.0 if the entity is riding an entity of any of the given types, else it returns 0.0.

        Args:
            types (list[str]): The entity identifiers to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "is_riding_any_entity_of_type",
            *_list_of("Query.IsRidingAnyEntityOfType", "entity types", types),
        )

    @classmethod
    def IsSearching(cls) -> Molang:
        """Returns 1.0 if the entity is searching, else it returns 0.0.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "is_searching")

    @classmethod
    def LeashedEntityCount(cls) -> Molang:
        """Returns the number of entities this entity is the leash holder of.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(cls, cls.handle, "leashed_entity_count")

    @classmethod
    def HasAnyLeashedEntityOfType(cls, types: list[str]) -> Molang:
        """Returns 1.0 if the entity is leashing an entity of any of the given types, else it returns 0.0.

        Args:
            types (list[str]): The entity identifiers to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "has_any_leashed_entity_of_type",
            *_list_of("Query.HasAnyLeashedEntityOfType", "entity types", types),
        )

    @classmethod
    def HasAllBiomeTags(cls, tags: list[str]) -> Molang:
        """Returns 1.0 if the biome at the placement position has all of the given tags, else it returns 0.0.

        Args:
            tags (list[str]): The biome tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "has_all_biome_tags",
            *_list_of("Query.HasAllBiomeTags", "tags", tags),
        )

    @classmethod
    def HasAnyBiomeTags(cls, tags: list[str]) -> Molang:
        """Returns 1.0 if the biome at the placement position has any of the given tags, else it returns 0.0.

        Args:
            tags (list[str]): The biome tags to test for.

        Returns:
            Molang(Molang): A Molang Instance
        """
        return cls.__query__(
            cls,
            cls.handle,
            "has_any_biome_tags",
            *_list_of("Query.HasAnyBiomeTags", "tags", tags),
        )


class Context(Query):
    handle = "context"

    @classmethod
    def _set_var(cls, name) -> None:
        setattr(cls, name, cls.__query__(cls, cls.handle, name))

    @classmethod
    def OwningEntity(cls, molang: Optional[Molang] = None) -> Molang:
        if molang:
            return Molang.arrow(cls.__query__(cls, cls.handle, "owning_entity"), molang)
        return Molang.__query__(cls, cls.handle, "owning_entity")

    @classmethod
    def Other(cls, molang: Optional[Molang] = None) -> Molang:
        if molang:
            return Molang.arrow(cls.__query__(cls, cls.handle, "other"), molang)
        return Molang.__query__(cls, cls.handle, "other")

    @classmethod
    def ItemSlot(cls) -> Molang:
        return cls.__query__(cls, cls.handle, "item_slot")


class Variable(Molang):
    handle = "v"

    @classmethod
    def _set_var(cls, name) -> None:
        setattr(cls, name, cls.__query__(cls, "v", name))
        Context._set_var(name)

    @classmethod
    def IsFirstPerson(cls) -> Molang:
        return cls.__query__(cls, "v", "is_first_person")

    @classmethod
    def IsPaperdoll(cls) -> Molang:
        return cls.__query__(cls, "v", "is_paperdoll")

    @classmethod
    def AttackTime(cls) -> Molang:
        return cls.__query__(cls, "v", "attack_time")


class TempVar(Molang, metaclass=_VarMeta):
    handle = "t"


class Math(Molang):
    handle = "math"

    @classmethod
    def abs(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "abs", value)

    @classmethod
    def acos(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "acos", value)

    @classmethod
    def asin(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "asin", value)

    @classmethod
    def atan(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "atan", value)

    @classmethod
    def atan2(cls, y: str, x) -> Molang:
        return cls.__query__(cls, cls.handle, "atan2", y, x)

    @classmethod
    def ceil(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "ceil", value)

    @classmethod
    def clamp(cls, value, min, max) -> Molang:
        return cls.__query__(cls, cls.handle, "clamp", value, min, max)

    @classmethod
    def copy_sign(cls, value, sign) -> Molang:
        return cls.__query__(cls, cls.handle, "copy_sign", value, sign)

    @classmethod
    def cos(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "cos", value)

    @classmethod
    def die_roll(cls, num, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "die_roll", num, low, high)

    @classmethod
    def die_roll_integer(cls, num, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "die_roll_integer", num, low, high)

    @classmethod
    def exp(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "exp", value)

    @classmethod
    def floor(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "floor", value)

    @classmethod
    def hermite_blend(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "hermite_blend", value)

    @classmethod
    def lerp(cls, start, end, factor) -> Molang:
        return cls.__query__(
            cls,
            cls.handle,
            "lerp",
            start,
            end,
            _checked("factor", factor, 0, 1),
        )

    @classmethod
    def lerprotate(cls, start, end, factor) -> Molang:
        return cls.__query__(
            cls,
            cls.handle,
            "lerprotate",
            start,
            end,
            _checked("factor", factor, 0, 1),
        )

    @classmethod
    def ln(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "ln", value)

    @classmethod
    def max(cls, A, B) -> Molang:
        return cls.__query__(cls, cls.handle, "max", A, B)

    @classmethod
    def min(cls, A, B) -> Molang:
        return cls.__query__(cls, cls.handle, "min", A, B)

    @classmethod
    def min_angle(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "min_angle", value)

    @classmethod
    def mod(cls, value, denominator) -> Molang:
        return cls.__query__(cls, cls.handle, "mod", value, denominator)

    @classmethod
    def pi(cls) -> Molang:
        return cls.__query__(cls, cls.handle, "pi")

    @classmethod
    def pow(cls, base, exponent) -> Molang:
        return cls.__query__(cls, cls.handle, "pow", base, exponent)

    @classmethod
    def random(cls, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "random", low, high)

    @classmethod
    def random_integer(cls, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "random_integer", low, high)

    @classmethod
    def round(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "round", value)

    @classmethod
    def sign(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sign", value)

    @classmethod
    def sin(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sin", value)

    @classmethod
    def sqrt(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sqrt", value)

    @classmethod
    def trunc(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "trunc", value)

    @classmethod
    def inverse_lerp(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "inverse_lerp", start, end, factor)

    @classmethod
    def ease_in_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quad", start, end, factor)

    @classmethod
    def ease_out_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quad", start, end, factor)

    @classmethod
    def ease_in_out_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quad", start, end, factor)

    @classmethod
    def ease_in_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_cubic", start, end, factor)

    @classmethod
    def ease_out_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_cubic", start, end, factor)

    @classmethod
    def ease_in_out_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_cubic", start, end, factor)

    @classmethod
    def ease_in_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quart", start, end, factor)

    @classmethod
    def ease_out_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quart", start, end, factor)

    @classmethod
    def ease_in_out_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quart", start, end, factor)

    @classmethod
    def ease_in_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quint", start, end, factor)

    @classmethod
    def ease_out_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quint", start, end, factor)

    @classmethod
    def ease_in_out_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quint", start, end, factor)

    @classmethod
    def ease_in_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_sine", start, end, factor)

    @classmethod
    def ease_out_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_sine", start, end, factor)

    @classmethod
    def ease_in_out_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_sine", start, end, factor)

    @classmethod
    def ease_in_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_expo", start, end, factor)

    @classmethod
    def ease_out_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_expo", start, end, factor)

    @classmethod
    def ease_in_out_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_expo", start, end, factor)

    @classmethod
    def ease_in_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_circ", start, end, factor)

    @classmethod
    def ease_out_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_circ", start, end, factor)

    @classmethod
    def ease_in_out_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_circ", start, end, factor)

    @classmethod
    def ease_in_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_bounce", start, end, factor)

    @classmethod
    def ease_out_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_bounce", start, end, factor)

    @classmethod
    def ease_in_out_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_bounce", start, end, factor)

    @classmethod
    def ease_in_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_back", start, end, factor)

    @classmethod
    def ease_out_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_back", start, end, factor)

    @classmethod
    def ease_in_out_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_back", start, end, factor)

    @classmethod
    def ease_in_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_elastic", start, end, factor)

    @classmethod
    def ease_out_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_elastic", start, end, factor)

    @classmethod
    def ease_in_out_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_elastic", start, end, factor)


@deprecated(
    "arrow_operator is deprecated and will be removed in a future version. Use `Molang.arrow()` instead for better readability and maintainability."
)
def arrow_operator(left: Molang, right: Molang) -> Molang:
    """Returns a Molang object representing the arrow operator for Molang."""
    return Molang(f"({left}) -> ({right})")


@deprecated(
    "molang_conditions is deprecated and will be removed in a future version. Use `Molang.condition()` instead for better readability and maintainability."
)
def molang_conditions(
    condition: Molang, expression: Molang, expression2: Optional[Molang] = None
) -> Molang:
    return Molang.condition(condition, expression, expression2)
