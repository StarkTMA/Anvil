from types import SimpleNamespace

import pytest

from anvil.api.core.components import ComponentGroup, Permutation
from anvil.lib.jsonmodel import (
    ComponentPlacement,
    JsonComponent,
    JsonContainer,
    json_field,
    validate_components,
)

OWNER = SimpleNamespace(identifier="test:owner")


class _Health(JsonComponent):
    identifier = "minecraft:health"

    value: int = json_field()


class _Movement(JsonComponent):
    identifier = "minecraft:movement"

    value: float = json_field()


class _RootOnly(JsonComponent):
    identifier = "minecraft:root_only"
    _placement = ComponentPlacement.ROOT


class _NeedsHealth(JsonComponent):
    identifier = "minecraft:needs_health"
    _requires = (_Health,)


class _ClashesWithHealth(JsonComponent):
    identifier = "minecraft:clashes_with_health"
    _clashes = (_Health,)


def test_add_replaces_a_component_in_its_place():
    components = JsonContainer(name="components").add(
        _Health(value=6), _Movement(value=0.2), _Health(value=20)
    )
    assert components.__json__() == {
        "components": {
            "minecraft:health": {"value": 20},
            "minecraft:movement": {"value": 0.2},
        }
    }


def test_remove_and_has_take_classes_or_components():
    components = JsonContainer(name="components").add(
        _Health(value=6), _Movement(value=0.2)
    )
    assert components.has(_Health) and components.has(_Health(value=1))
    components.remove(_Health)
    assert not components.has(_Health)
    components.remove(_Movement(value=1))
    assert components.__json__() == {"components": {}}


def test_duplicate_identifiers_are_refused_on_export():
    components = JsonContainer(name="components")
    components._components.extend([_Health(value=6), _Health(value=2)])
    with pytest.raises(ValueError):
        components.__json__()


def test_component_group_and_permutation_json():
    group = JsonContainer(name="adult").add(_Health(value=2))
    assert group.name == "adult"
    assert group.__json__() == {"adult": {"minecraft:health": {"value": 2}}}

    permutation = Permutation(condition="q.block_state('x') == 1").add(_Health(value=1))
    assert permutation.__json__() == {
        "components": {"minecraft:health": {"value": 1}},
        "condition": "q.block_state('x') == 1",
    }


def test_permutation_has_no_name_argument():
    with pytest.raises(TypeError):
        Permutation(name="x", condition="1")


def test_component_group_is_a_json_container():
    assert issubclass(ComponentGroup, JsonContainer)
    assert ComponentGroup(name="adult").add(_Health(value=2)).__json__() == {
        "adult": {"minecraft:health": {"value": 2}}
    }


def test_containers_are_read_only():
    group = JsonContainer(name="adult")
    with pytest.raises(AttributeError):
        group.name = "baby"


def test_validate_placement():
    validate_components(OWNER, JsonContainer(name="components").add(_RootOnly()), [])
    with pytest.raises(ValueError, match="not allowed in component groups"):
        validate_components(
            OWNER,
            JsonContainer(name="components"),
            [JsonContainer(name="g").add(_RootOnly())],
        )
    with pytest.raises(ValueError, match="not allowed in permutations"):
        validate_components(
            OWNER,
            JsonContainer(name="components"),
            [Permutation(condition="1").add(_RootOnly())],
            is_block=True,
        )


def test_validate_requires_and_clashes():
    validate_components(
        OWNER,
        JsonContainer(name="components").add(_Health(value=1)),
        [JsonContainer(name="g").add(_NeedsHealth())],
    )
    with pytest.raises(ValueError, match="requires 'minecraft:health'"):
        validate_components(
            OWNER, JsonContainer(name="components").add(_NeedsHealth()), []
        )
    with pytest.raises(ValueError, match="clashes with 'minecraft:health'"):
        validate_components(
            OWNER,
            JsonContainer(name="components").add(
                _ClashesWithHealth(), _Health(value=1)
            ),
            [],
        )
