"""Tests for anvil/lib/jsonmodel — the JsonObject and JsonComponent base classes."""

import dataclasses
from typing import ClassVar

import pytest

from anvil.lib.jsonmodel import (
    ComponentPlacement,
    Identifier,
    JsonComponent,
    JsonObject,
    JsonValue,
    JsonValueComponent,
    json_field,
)
from anvil.lib.jsonmodel.validators import each, in_range, instance_of, length, one_of


class _Point(JsonObject):
    x: int = json_field(default=0, validators=[instance_of(int)])
    y: int = json_field(default=0, validators=[instance_of(int)])


class _Climate(JsonComponent):
    identifier = "minecraft:climate"

    temperature: float | None = json_field(default=None, validators=[in_range(-50, 50)])
    snow_accumulation: list[float] | None = json_field(
        default=None, validators=[length(2, 2), each(in_range(0, 1))]
    )
    points: list[_Point] = json_field(default_factory=list)

    def set_temperature(self, *, temperature: float) -> "_Climate":
        self.temperature = temperature
        return self

    def add_point(self, *, x: int, y: int) -> "_Climate":
        self.points.append(_Point(x=x, y=y))
        return self


class _Bare(JsonValueComponent):
    identifier = "minecraft:bare"
    _placement = ComponentPlacement.ROOT

    value: int = json_field(default=1)


def test_subclass_is_slotted_keyword_only_dataclass():
    with pytest.raises(TypeError):
        _Point(1, 2)
    point = _Point(x=1, y=2)
    assert not hasattr(point, "__dict__")
    with pytest.raises(AttributeError):
        point.z = 3


def test_defining_init_is_refused():
    with pytest.raises(TypeError, match="must not define __init__"):

        class _Bad(JsonObject):
            def __init__(self):
                pass


def test_export_skips_none_and_uses_identifier():
    climate = _Climate(temperature=0.5)
    assert climate.__json__() == {
        "minecraft:climate": {"temperature": 0.5, "points": []}
    }


def test_nested_objects_and_builders():
    climate = _Climate().add_point(x=1, y=2).add_point(x=3, y=4)
    assert climate.__json__()["minecraft:climate"]["points"] == [
        {"x": 1, "y": 2},
        {"x": 3, "y": 4},
    ]


def test_validators_run_at_export_only():
    climate = _Climate(temperature=99)
    with pytest.raises(ValueError):
        climate.__json__()
    climate.set_temperature(temperature=20)
    assert climate.__json__()["minecraft:climate"]["temperature"] == 20
    with pytest.raises(ValueError):
        _Climate(snow_accumulation=[0.1]).__json__()
    with pytest.raises(ValueError):
        _Climate(snow_accumulation=[0.1, 2]).__json__()
    with pytest.raises(TypeError):
        _Climate(temperature=True).__json__()


def test_builder_items_are_validated():
    with pytest.raises(TypeError):
        _Climate().add_point(x="a", y=1).__json__()


def test_key_alias_omit_default_and_constant_fields():
    class _Builder(JsonObject):
        type: str = json_field(default="minecraft:overworld", init=False)
        depth: int = json_field(default=7, key="sea_floor_depth", omit_default=True)

    assert _Builder().__json__() == {"type": "minecraft:overworld"}
    assert _Builder(depth=3).__json__() == {
        "type": "minecraft:overworld",
        "sea_floor_depth": 3,
    }
    with pytest.raises(TypeError):
        _Builder(type="other").__json__()


def test_value_objects_and_placement():
    class _Visible(JsonValue):
        bone: str = json_field(exclude=True)
        visible: bool = json_field()

    assert _Visible(bone="head", visible=False).__json__() is False
    bare = _Bare(value=4)
    assert bare.__json__() == {"minecraft:bare": 4}
    assert _Bare._placement == ComponentPlacement.ROOT
    assert _Climate._placement == ComponentPlacement.ANY


def test_identifier_is_a_plain_class_attribute_and_there_is_no_format_version():
    assert _Climate.identifier == "minecraft:climate"
    assert _Climate().identifier == "minecraft:climate"
    assert not hasattr(_Climate, "format_version")
    assert "identifier" not in [f.name for f in dataclasses.fields(_Climate)]


def test_component_without_identifier_is_refused():
    with pytest.raises(TypeError, match="must set `identifier`"):

        class _Nameless(JsonComponent):
            value: int = json_field(default=1)


def test_vanilla_identifier_must_be_in_the_minecraft_namespace():
    with pytest.raises(ValueError, match="'minecraft:name'"):

        class _Foreign(JsonComponent):
            identifier = "other:climate"


def test_identifier_is_parsed_into_an_identifier():
    assert isinstance(_Climate.identifier, Identifier)
    assert (_Climate.identifier.namespace, _Climate.identifier.name) == (
        "minecraft",
        "climate",
    )
    assert _Climate.identifier.is_vanilla


@pytest.fixture
def project_namespace(monkeypatch):
    import types

    from anvil.lib import config

    monkeypatch.setattr(config, "CONFIG", types.SimpleNamespace(NAMESPACE="proj"))


class _Custom(JsonComponent, abstract=True):
    _custom = True


def test_custom_identifier_must_be_in_the_project_namespace(project_namespace):
    class _Mine(_Custom):
        identifier = "proj:explosive"

    class _Bare(_Custom):
        identifier = "explosive"

    assert _Mine().__json__() == {"proj:explosive": {}}
    assert _Bare.identifier == "proj:explosive"
    assert not _Bare.identifier.is_vanilla
    with pytest.raises(ValueError, match="'proj:name'"):

        class _Theirs(_Custom):
            identifier = "other:explosive"

    with pytest.raises(ValueError, match="'proj:name'"):

        class _Vanilla(_Custom):
            identifier = "minecraft:explosive"


def test_abstract_bases_skip_the_identifier_and_cannot_be_instantiated():
    class _Shared(JsonComponent, abstract=True):
        a: int = json_field(default=1)

    class _Concrete(_Shared):
        identifier = "minecraft:concrete"

    with pytest.raises(TypeError, match="abstract"):
        _Shared().__json__()
    assert _Concrete(a=2).__json__() == {"minecraft:concrete": {"a": 2}}


def test_validate_hook_runs_at_export_after_field_validators():
    calls = []

    def field_check(name, value):
        calls.append(name)

    class _Hooked(JsonComponent):
        identifier = "minecraft:hooked"
        low: int = json_field(default=0, validators=[field_check])
        high: int = json_field(default=1)

        def __validate__(self) -> None:
            calls.append("validate")
            if self.low > self.high:
                raise ValueError("low must not exceed high")

        def __post_init__(self) -> None:
            calls.append("post_init")

    hooked = _Hooked()
    assert calls == ["post_init"]
    hooked.__json__()
    assert calls == ["post_init", "_Hooked.low", "validate"]
    with pytest.raises(ValueError):
        _Hooked(low=5, high=1).__json__()


def test_nested_object_has_no_identifier():
    assert not hasattr(_Point(), "identifier")
    assert _Point(x=1).__json__() == {"x": 1, "y": 0}


def test_dependencies_and_clashes_are_class_level():
    class _Needs(JsonComponent):
        identifier = "minecraft:needs"
        _requires: ClassVar = (_Climate,)
        _clashes: ClassVar = (_Bare,)

    needs = _Needs()
    assert [c.identifier for c in type(needs)._requires] == ["minecraft:climate"]
    assert [c.identifier for c in type(needs)._clashes] == ["minecraft:bare"]


def test_one_of():
    class _Choice(JsonObject):
        kind: str = json_field(default="a", validators=[one_of("a", "b")])

    with pytest.raises(ValueError):
        _Choice(kind="c").__json__()


def test_identity_equality_kept_for_containers():
    assert _Point(x=1) != _Point(x=1)


def test_inheritance_chain_keeps_fields_and_slots():
    class _Base(JsonComponent, abstract=True):
        a: int = json_field(default=1)

        def set_a(self, *, value: int) -> "_Base":
            self.a = value
            return self

    class _Child(_Base):
        identifier = "minecraft:child"
        b: int = json_field(default=2)

    child = _Child(a=5, b=6).set_a(value=7)
    assert child.__json__() == {"minecraft:child": {"a": 7, "b": 6}}
    assert not hasattr(child, "__dict__")


def test_anvil_io_normalizes_json_components():
    from anvil.lib.lib import AnvilIO

    assert AnvilIO._normalize_json_like({"c": _Climate(temperature=1.0)}) == {
        "c": {"minecraft:climate": {"temperature": 1.0}}
    }
    assert AnvilIO._normalize_json_like([_Point(x=1)]) == [{"x": 1, "y": 0}]
    assert AnvilIO._normalize_json_like(_Climate) == "minecraft:climate"


@pytest.mark.parametrize(
    "identifier",
    [
        "minecraft:climate",
        "minecraft:custom.part-2",
        "minecraft:sub/path",
        "minecraft:_hidden",
    ],
)
def test_valid_identifiers(identifier):
    _Ok = type("_Ok", (JsonComponent,), {"identifier": identifier})
    assert _Ok.identifier == identifier


@pytest.mark.parametrize("identifier", ["proj:custom.part-2", "proj:sub/path"])
def test_valid_custom_identifiers(identifier, project_namespace):
    _Ok = type("_Ok", (_Custom,), {"identifier": identifier})
    assert _Ok.identifier == identifier


@pytest.mark.parametrize(
    "identifier",
    [
        "climate",
        "Minecraft:climate",
        "minecraft:Climate",
        "1ns:climate",
        "minecraft:1climate",
        "minecraft:can_stand_on_powder_snow ",
        "minecraft:",
        ":climate",
        "a:b:c",
        "my_ns:climate",
    ],
)
def test_invalid_identifiers_are_refused(identifier):
    with pytest.raises(ValueError, match="Invalid name|Invalid namespace"):
        type("_Bad", (JsonComponent,), {"identifier": identifier})


def test_component_types_resolve_for_type_checkers():
    from annotationlib import Format, call_evaluate_function

    from anvil.api.core import types

    def evaluate(alias):
        return call_evaluate_function(alias.evaluate_value, Format.STRING)

    assert evaluate(types.ComponentClass) == "type[JsonComponent]"
    assert evaluate(types.ComponentClasses) == "tuple[ComponentClass, ...]"
    assert types.Validator.__value__.__args__[0] is str


def test_encoder_converts_only_the_json_form():
    class _Tinted(JsonObject):
        color: str | None = json_field(default=None, encoder=str.upper)

    tinted = _Tinted(color="#abc")
    assert tinted.__json__() == {"color": "#ABC"}
    assert tinted.color == "#abc"


def test_fields_are_read_only_from_outside():
    climate = _Climate(temperature=10)
    with pytest.raises(AttributeError, match="read-only"):
        climate.temperature = 20
    with pytest.raises(AttributeError, match="read-only"):
        del climate.temperature
    with pytest.raises(AttributeError):
        climate.not_a_field = 1
    assert climate.temperature == 10


def test_builders_change_related_fields_in_any_order():
    class _Range(JsonObject):
        low: int = json_field(default=0, validators=[instance_of(int)])
        high: int = json_field(default=1)

        def __validate__(self) -> None:
            if self.low > self.high:
                raise ValueError("low must not exceed high")

        def set_range(self, *, low: int, high: int) -> "_Range":
            self.high = high
            self.low = low
            return self

    rng = _Range().set_range(low=5, high=10)
    assert rng.__json__() == {"low": 5, "high": 10}
    with pytest.raises(TypeError):
        _Range().set_range(low="1", high=3).__json__()
    with pytest.raises(ValueError):
        _Range().set_range(low=50, high=3).__json__()


def test_own_methods_and_post_init_assign_normally():
    class _Derived(JsonObject):
        size: int = json_field(default=2)
        area: int | None = json_field(default=None, init=False)

        def __post_init__(self) -> None:
            self.area = self.size * self.size

    derived = _Derived(size=3)
    assert derived.area == 9
    with pytest.raises(AttributeError, match="read-only"):
        derived.area = 1


def test_an_object_cannot_change_another_objects_fields():
    class _Holder(JsonObject):
        point: _Point = json_field(default_factory=_Point)

        def move(self) -> None:
            self.point.x = 5

    with pytest.raises(AttributeError, match="read-only"):
        _Holder().move().__json__()


def test_abstract_check_survives_post_init_chains():
    calls = []

    class _Parent(JsonObject, abstract=True):
        def __post_init__(self) -> None:
            calls.append("parent")

    class _Child(_Parent):
        def __post_init__(self) -> None:
            super().__post_init__()
            calls.append("child")

    with pytest.raises(TypeError, match="abstract"):
        _Parent()
    _Child()
    assert calls == ["parent", "child"]
