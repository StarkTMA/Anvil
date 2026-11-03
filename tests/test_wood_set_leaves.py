from types import SimpleNamespace

import pytest

from anvil.api.blocks import components as block_components
from anvil.kit.blocks.wood_set.blocks import leaves
from anvil.kit.blocks.wood_set.components import BlockWoodSetLeaves, BlockWoodSetSapling
from anvil.lib.lib import AnvilIO


@pytest.fixture
def make_leaves(monkeypatch):
    monkeypatch.setattr(
        block_components.BlockMaterialInstance, "add_instance", lambda self, spec: self
    )
    return leaves.create


def _component_ids(exported: dict) -> list[str]:
    return list(exported["components"])


def test_natural_state_is_off_for_placed_leaves(make_leaves):
    block = make_leaves("rotten", {"log"})
    states = block.server.description._description["description"]["states"]
    ((name, values),) = states.items()
    assert name.endswith(":natural")
    # The first value is the default, so placed leaves are not natural
    assert tuple(values) == (False, True)


def test_leaves_decay_on_random_ticks_not_a_scheduled_tick(make_leaves):
    # The script's onRandomTick does the decay (like vanilla), so no tick is scheduled
    block = make_leaves("rotten", {"log"})
    base = block.server.components.__json__()["components"]
    assert "minecraft:tick" not in base
    assert not block.server._permutations


def test_trunks_are_the_selected_ones_only(make_leaves):
    block = make_leaves("rotten", {"log", "wood", "sapling"})
    components = block.server.components.__json__()["components"]
    (params,) = [v for k, v in components.items() if k.endswith(":wood_set_leaves")]
    assert [trunk.split(":")[1] for trunk in params["trunks"]] == [
        "rotten_log",
        "rotten_wood",
    ]
    assert params["sapling"].endswith(":rotten_sapling")


def test_no_sapling_when_not_selected(make_leaves):
    block = make_leaves("rotten", {"log"})
    components = block.server.components.__json__()["components"]
    (params,) = [v for k, v in components.items() if k.endswith(":wood_set_leaves")]
    assert "sapling" not in params


@pytest.mark.parametrize(
    "kwargs", [{"distance": 0}, {"sapling_chance": 1.5}, {"stick_chance": -0.1}]
)
def test_invalid_params(kwargs):
    with pytest.raises(ValueError):
        BlockWoodSetLeaves(trunks=["a:log"], **kwargs).__json__()


def test_leaves_loot_table_conditions(make_leaves):
    block = make_leaves("rotten", {"log", "sapling"})
    components = block.server.components.__json__()["components"]
    assert "minecraft:loot" in components

    # Find the queued loot table for rotten_leaves
    from anvil.api.core.core import ANVIL

    queued_tables = [
        obj
        for obj in ANVIL._objects_list
        if getattr(obj, "_object_type", None) == "Loot Table"
    ]
    table = [t for t in queued_tables if t.name == "rotten_leaves"][-1]
    exported = AnvilIO._normalize_json_like(table._content)["pools"]

    # Pool 0: Shears
    assert exported[0]["conditions"] == [
        {"condition": "match_tool", "item": "minecraft:shears"}
    ]
    assert exported[0]["entries"][0]["name"].endswith(":rotten_leaves")

    # Pool 1: Silk Touch
    assert exported[1]["conditions"] == [
        {
            "condition": "match_tool",
            "enchantments": [{"enchantment": "silk_touch", "levels": {"range_min": 1}}],
        }
    ]
    assert exported[1]["entries"][0]["name"].endswith(":rotten_leaves")

    # Pool 2: Sapling
    assert exported[2]["conditions"] == [{"condition": "random_chance", "chance": 0.05}]
    assert exported[2]["entries"][0]["name"].endswith(":rotten_sapling")

    # Pool 3: Sticks
    assert exported[3]["conditions"] == [{"condition": "random_chance", "chance": 0.02}]
    assert exported[3]["entries"][0]["name"] == "minecraft:stick"
    assert exported[3]["entries"][0]["functions"] == [
        {"function": "set_count", "count": {"min": 1, "max": 2}}
    ]


def test_leaves_loot_table_without_sapling(make_leaves):
    from anvil.api.core.core import ANVIL

    ANVIL._objects_list.clear()

    block = make_leaves("rotten", {"log"})
    queued_tables = [
        obj
        for obj in ANVIL._objects_list
        if getattr(obj, "_object_type", None) == "Loot Table"
    ]
    (table,) = [t for t in queued_tables if t.name == "rotten_leaves"]
    exported = AnvilIO._normalize_json_like(table._content)["pools"]
    assert len(exported) == 3  # shears, silk touch, sticks (no sapling)
