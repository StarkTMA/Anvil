import pytest
from anvil.api.world.loot_tables import LootConditions, LootTable
from anvil.lib import config as anvil_config


@pytest.fixture(autouse=True)
def project_config(monkeypatch):
    values = {
        "NAMESPACE": "test",
        "BP_PATH": "BP",
        "RP_PATH": "RP",
        "PROJECT_NAME": "test",
    }
    monkeypatch.setattr(
        anvil_config._AnvilConfig._Proxy,
        "__getattr__",
        lambda self, name: values[name],
        raising=False,
    )


def test_pool_conditions_match_tool():
    table = LootTable("test_table")
    pool = table.pool()
    pool.conditions.match_tool(item="minecraft:shears")
    pool.entry("test:item")

    exported = pool.__export__()
    assert "conditions" in exported
    assert exported["conditions"] == [
        {"condition": "match_tool", "item": "minecraft:shears"}
    ]


def test_pool_conditions_silk_touch():
    table = LootTable("test_table")
    pool = table.pool()
    pool.conditions.match_tool(enchantments="silk_touch")
    pool.entry("test:item")

    exported = pool.__export__()
    assert exported["conditions"] == [
        {
            "condition": "match_tool",
            "enchantments": [{"enchantment": "silk_touch", "levels": {"range_min": 1}}],
        }
    ]


def test_pool_conditions_match_tool_filters():
    table = LootTable("test_table")
    pool = table.pool()
    pool.conditions.match_tool(
        filter_any=["minecraft:iron_tier"],
        filter_all=["minecraft:is_tool"],
        filter_none=["minecraft:is_shovel"],
    )
    exported = pool.__export__()
    assert exported["conditions"][0] == {
        "condition": "match_tool",
        "minecraft:match_tool_filter_any": ["minecraft:iron_tier"],
        "minecraft:match_tool_filter_all": ["minecraft:is_tool"],
        "minecraft:match_tool_filter_none": ["minecraft:is_shovel"],
    }


def test_entry_conditions_random_chance():
    table = LootTable("test_table")
    pool = table.pool()
    entry = pool.entry("test:item")
    entry.conditions.random_chance(0.05)

    exported = pool.__export__()
    assert "conditions" not in exported  # pool has no conditions
    assert exported["entries"][0]["conditions"] == [
        {"condition": "random_chance", "chance": 0.05}
    ]


def test_all_condition_types():
    conds = LootConditions()
    conds.random_chance(0.25)
    conds.random_chance_with_looting(0.1, 0.02)
    conds.random_difficulty_chance(0.5, peaceful=0.0, hard=0.7)
    conds.random_regional_difficulty_chance(0.15)
    conds.killed_by_player()
    conds.killed_by_player_or_pets()
    conds.killed_by_entity("minecraft:skeleton")
    conds.entity_killed("minecraft:magma_cube")
    conds.has_variant(2)
    conds.has_mark_variant(7)
    conds.entity_properties("this", {"on_fire": True})
    conds.add({"condition": "custom_cond", "custom_key": "val"})

    exported = conds.__export__()
    assert len(exported) == 12
    assert exported[0] == {"condition": "random_chance", "chance": 0.25}
    assert exported[1] == {
        "condition": "random_chance_with_looting",
        "chance": 0.1,
        "looting_multiplier": 0.02,
    }
    assert exported[2] == {
        "condition": "random_difficulty_chance",
        "default_chance": 0.5,
        "peaceful": 0.0,
        "hard": 0.7,
    }
    assert exported[3] == {
        "condition": "random_regional_difficulty_chance",
        "max_chance": 0.15,
    }
    assert exported[4] == {"condition": "killed_by_player"}
    assert exported[5] == {"condition": "killed_by_player_or_pets"}
    assert exported[6] == {
        "condition": "killed_by_entity",
        "entity_type": "minecraft:skeleton",
    }
    assert exported[7] == {
        "condition": "entity_killed",
        "entity_type": "minecraft:magma_cube",
    }
    assert exported[8] == {"condition": "has_variant", "value": 2}
    assert exported[9] == {"condition": "has_mark_variant", "value": 7}
    assert exported[10] == {
        "condition": "entity_properties",
        "entity": "this",
        "properties": {"on_fire": True},
    }
    assert exported[11] == {"condition": "custom_cond", "custom_key": "val"}


def test_pascal_case_aliases():
    conds = LootConditions()
    conds.MatchTool(item="minecraft:shears")
    conds.RandomChance(0.5)
    exported = conds.__export__()
    assert len(exported) == 2
    assert exported[0] == {"condition": "match_tool", "item": "minecraft:shears"}
    assert exported[1] == {"condition": "random_chance", "chance": 0.5}
