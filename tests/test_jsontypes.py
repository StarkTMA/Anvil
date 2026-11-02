"""Tests for anvil/lib/jsonmodel/jsontypes.py and the annotation walker."""

from enum import StrEnum
from typing import Annotated, Literal

import pytest

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.jsonmodel import (
    AsObject,
    AsString,
    BlockObject,
    Bounds,
    Chance,
    EffectName,
    ExpandFaces,
    FitToFrame,
    Hex,
    IndexInto,
    InRange,
    ItemObject,
    JsonObject,
    JsonValue,
    Kept,
    KeptObject,
    Keyed,
    Length,
    MetersPerSecond,
    MinMax,
    NonNegative,
    Ordered,
    Positive,
    PropertyName,
    RangeMinMax,
    RGBAColor,
    ShortTag,
    Trigger,
    Unique,
    Wrapped,
    XpRange,
    YesNo,
    json_field,
)
from anvil.lib.schemas import MinecraftBlockDescriptor

from anvil.api.core.components import EventTrigger

type Color = HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255


class _Mode(StrEnum):
    Fast = "fast"
    Slow = "slow"


class _Part(JsonObject):
    name: str = json_field(exclude=True)
    size: int = json_field(default=1)


class _Flag(JsonValue):
    name: str = json_field(exclude=True)
    on: bool = json_field()


def _json(cls, **fields):
    return cls(**fields).__json__()


def _refused(error, cls, **fields):
    with pytest.raises(error):
        cls(**fields).__json__()


# region The walker


def test_plain_types_are_checked():
    class _Plain(JsonObject):
        flag: bool | None = json_field(default=None)
        count: int | None = json_field(default=None)
        speed: float | None = json_field(default=None)
        name: str | None = json_field(default=None)

    assert _json(_Plain, speed=2, count=3) == {"speed": 2, "count": 3}
    _refused(TypeError, _Plain, count=True)
    _refused(TypeError, _Plain, count=1.5)
    _refused(TypeError, _Plain, speed=False)
    _refused(TypeError, _Plain, flag=1)
    _refused(TypeError, _Plain, name=3)


def test_literals_enums_and_unions():
    class _Choice(JsonObject):
        mode: _Mode | None = json_field(default=None)
        side: Literal["left", "right"] | None = json_field(default=None)
        fast: Literal[_Mode.Fast] | None = json_field(default=None)
        either: int | Literal["infinite"] | None = json_field(default=None)

    assert _json(_Choice, mode="slow", side="left", fast="fast", either=3) == {
        "mode": "slow",
        "side": "left",
        "fast": "fast",
        "either": 3,
    }
    assert _json(_Choice, either="infinite") == {"either": "infinite"}
    _refused(ValueError, _Choice, mode="medium")
    _refused(TypeError, _Choice, mode=3)
    _refused(ValueError, _Choice, side="up")
    _refused(ValueError, _Choice, fast=_Mode.Slow)
    _refused(ValueError, _Choice, either="forever")
    _refused(TypeError, _Choice, either=1.5)


def test_lists_tuples_and_parts():
    class _Shapes(JsonObject):
        offset: tuple[float, float, float] | None = json_field(default=None)
        names: list[str] | None = json_field(default=None)
        parts: list[_Part] | None = json_field(default=None)

    assert _json(_Shapes, offset=(1, 2, 3), names=("a",), parts=[_Part(name="x")]) == {
        "offset": [1, 2, 3],
        "names": ["a"],
        "parts": [{"size": 1}],
    }
    _refused(ValueError, _Shapes, offset=(1, 2))
    _refused(TypeError, _Shapes, offset=(1, 2, "3"))
    _refused(TypeError, _Shapes, names=["a", 1])
    _refused(TypeError, _Shapes, parts=[_Flag(name="x", on=True)])


def test_aliases_and_string_annotations():
    class _Late(JsonObject):
        color: Color | None = json_field(default=None)
        on_hit: "EventTrigger | None" = json_field(default=None)

    assert _json(_Late, color="#fff", on_hit=EventTrigger(event="hit")) == {
        "color": "#fff",
        "on_hit": {"event": "hit"},
    }
    _refused(TypeError, _Late, color=3)
    _refused(TypeError, _Late, on_hit="hit")


def test_metadata_on_one_arm_of_a_union():
    class _Tint(JsonObject):
        color: (
            Annotated[Literal["birch", "evergreen"], Wrapped("color_map")]
            | Annotated[Color, Hex]
        ) = json_field()

    assert _json(_Tint, color="birch") == {"color": {"color_map": "birch"}}
    assert _json(_Tint, color=(1.0, 0.0, 0.0)) == {"color": "#ff0000"}


def test_internal_state_is_not_checked():
    class _Stateful(JsonObject):
        _cache: int | None = json_field(default=None, init=False, exclude=True)

        def warm(self) -> "_Stateful":
            self._cache = "not an int"
            return self

    assert _Stateful().warm().__json__() == {}


# endregion

# region Constraints


def test_in_range():
    class _Ranged(JsonObject):
        chance: Annotated[float, Chance] | None = json_field(default=None)
        count: Annotated[int, NonNegative] | None = json_field(default=None)
        speed: Annotated[float, Positive] | None = json_field(default=None)
        pair: Annotated[tuple[int, int], InRange(0, 10)] | None = json_field(
            default=None
        )

    assert _json(_Ranged, chance=1, count=0, speed=0.1, pair=(0, 10))
    _refused(ValueError, _Ranged, chance=1.5)
    _refused(ValueError, _Ranged, count=-1)
    _refused(ValueError, _Ranged, speed=0)
    with pytest.raises(ValueError, match=r"pair\[1\]"):
        _Ranged(pair=(0, 11)).__json__()


def test_length_unique_and_ordered():
    class _Sized(JsonObject):
        tags: Annotated[list[Annotated[str, ShortTag]], Length(maximum=2)] | None = (
            json_field(default=None)
        )
        parts: Annotated[list[_Part], Unique("name")] | None = json_field(default=None)
        span: Annotated[tuple[int, int], Ordered] | None = json_field(default=None)

    assert _json(
        _Sized, tags=["a"], parts=[_Part(name="a"), _Part(name="b")], span=(1, 1)
    )
    _refused(ValueError, _Sized, tags=["a", "b", "c"])
    with pytest.raises(ValueError, match="64 characters"):
        _Sized(tags=["a" * 65]).__json__()
    with pytest.raises(ValueError, match="more than one"):
        _Sized(parts=[_Part(name="a"), _Part(name="a")]).__json__()
    with pytest.raises(ValueError, match="greater than its maximum"):
        _Sized(span=(2, 1)).__json__()


# endregion

# region Shapes


def test_bounds():
    class _Ranges(JsonObject):
        damage: Annotated[float | tuple[float, float], MinMax] | None = json_field(
            default=None
        )
        value: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
            default=None
        )
        xp: Annotated[int | tuple[int, int], XpRange] | None = json_field(default=None)
        span: Annotated[tuple[int, int], Bounds("low", "high")] | None = json_field(
            default=None
        )

    assert _json(_Ranges, damage=(4, 2), value=3, xp=5, span=(1, 2)) == {
        "damage": {"min": 2, "max": 4},
        "value": 3,
        "xp": {"minXP": 5, "maxXP": 5},
        "span": {"low": 1, "high": 2},
    }


def test_triggers_and_kept_parts():
    class _Events(JsonObject):
        on_hit: Annotated[EventTrigger | str, Trigger] | None = json_field(
            default=None
        )
        part: Annotated[_Part, Kept] | None = json_field(default=None)
        switch: Annotated[bool, Kept] | None = json_field(default=None)

    exported = _json(_Events, on_hit="explode", part=_Part(name="x"), switch=True)
    assert exported["on_hit"] == {"event": "explode", "target": "self"}
    assert isinstance(exported["part"], KeptObject) and exported["part"] == {"size": 1}
    assert isinstance(exported["switch"], KeptObject) and exported["switch"] == {}
    assert _json(_Events, switch=False) == {"switch": None}


def test_keyed_wrapped_and_object_shapes():
    class _Shaped(JsonObject):
        flags: Annotated[list[_Flag], Keyed("name")] | None = json_field(default=None)
        skins: list[Annotated[int, Wrapped("variant")]] | None = json_field(
            default=None
        )
        items: list[Annotated[str, ItemObject]] | None = json_field(default=None)
        block: Annotated[str | MinecraftBlockDescriptor, BlockObject] | None = (
            json_field(default=None)
        )
        pairs: Annotated[list[tuple[str, str]], AsObject] | None = json_field(
            default=None
        )

    exported = _json(
        _Shaped,
        flags=[_Flag(name="head", on=False)],
        skins=[0, 1],
        items=["minecraft:apple"],
        block=MinecraftBlockDescriptor("minecraft:stone", True),
        pairs=[("minecraft:cow", "minecraft:mooshroom")],
    )
    assert exported == {
        "flags": {"head": False},
        "skins": [{"variant": 0}, {"variant": 1}],
        "items": [{"item": "minecraft:apple"}],
        "block": {"name": "minecraft:stone"},
        "pairs": {"minecraft:cow": "minecraft:mooshroom"},
    }
    with pytest.raises(ValueError, match="more than one"):
        _Shaped(flags=[_Flag(name="a", on=True), _Flag(name="a", on=False)]).__json__()


def test_value_formats():
    class _Formats(JsonObject):
        tint: Annotated[Color, Hex] | None = json_field(default=None)
        potion: Annotated[Color, RGBAColor] | None = json_field(default=None)
        effect: Annotated[str, EffectName] | None = json_field(default=None)
        speed: (
            Annotated[float | tuple[float, float], MetersPerSecond(2), RangeMinMax]
            | None
        ) = json_field(default=None)
        anchor: Annotated[Literal[0, 1], IndexInto(("origin", "eye"))] | None = (
            json_field(default=None)
        )
        hurts: Annotated[bool, YesNo] | Literal["no_but_side_effects_apply"] | None = (
            json_field(default=None)
        )
        frame: Annotated[bool, FitToFrame] | None = json_field(default=None)
        name: Annotated[int, AsString] | None = json_field(default=None)

    assert _json(
        _Formats,
        tint=(255, 0, 0),
        potion="#ff0000",
        effect="minecraft:speed",
        speed=(4, 16),
        anchor=1,
        hurts=False,
        frame=True,
        name=3,
    ) == {
        "tint": "#ff0000",
        "potion": [1.0, 0.0, 0.0, 1.0],
        "effect": "speed",
        "speed": {"range_min": 0.3, "range_max": 0.61},
        "anchor": "eye",
        "hurts": "no",
        "frame": {},
        "name": "3",
    }


def test_faces_and_project_names(monkeypatch):
    from anvil.api.core.enums import BlockFaceValues
    from anvil.lib import config

    class _Named(JsonObject):
        faces: Annotated[list[BlockFaceValues], ExpandFaces] | None = json_field(
            default=None
        )
        properties: list[Annotated[str, PropertyName]] | None = json_field(default=None)

    with config.override(NAMESPACE="proj"):
        exported = _json(
            _Named, faces=[BlockFaceValues.Side], properties=["size", "minecraft:x"]
        )
    assert exported == {
        "faces": ["north", "south", "east", "west"],
        "properties": ["proj:size", "minecraft:x"],
    }


# endregion
