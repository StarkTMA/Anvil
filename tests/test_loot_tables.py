import pytest

from anvil.api.world.loot_tables import LootConditions, LootTable
from anvil.lib.lib import AnvilIO


def _json(part):
    return AnvilIO._normalize_json_like(part)


def test_pool_conditions_match_tool():
    table = LootTable("test_table")
    pool = table.pool()
    pool.conditions.match_tool(item="minecraft:shears")
    pool.entry("test:item")

    exported = _json(pool)
    assert "conditions" in exported
    assert exported["conditions"] == [
        {"condition": "match_tool", "item": "minecraft:shears"}
    ]


def test_pool_conditions_silk_touch():
    table = LootTable("test_table")
    pool = table.pool()
    pool.conditions.match_tool(enchantments="silk_touch")
    pool.entry("test:item")

    exported = _json(pool)
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
    exported = _json(pool)
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

    exported = _json(pool)
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
    conds.entity_properties("this", on_fire=True)

    exported = _json(conds)
    assert len(exported) == 11
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


def test_pascal_case_aliases():
    conds = LootConditions()
    conds.MatchTool(item="minecraft:shears")
    conds.RandomChance(0.5)
    exported = _json(conds)
    assert len(exported) == 2
    assert exported[0] == {"condition": "match_tool", "item": "minecraft:shears"}
    assert exported[1] == {"condition": "random_chance", "chance": 0.5}


def test_entries_reference_loot_tables_by_path():
    inner = LootTable("inner")
    table = LootTable("outer")
    entry = table.pool().entry(inner, weight=2).set_quality(-1)
    entry.functions.FillContainer(inner)
    assert _json(table._document)["pools"][0]["entries"][0] == {
        "type": "loot_table",
        "name": inner.table_path,
        "count": 1,
        "weight": 2,
        "quality": -1,
        "functions": [{"function": "fill_container", "loot_table": inner.table_path}],
    }
    assert inner.table_path.startswith("loot_tables/")


def test_functions_use_documented_keys():
    table = LootTable("functions")
    functions = table.pool((3, 1)).entry("minecraft:wool").functions
    functions.LootingEnchant((0, 1)).RandomAuxValue((0, 15))
    functions.RandomBlockState("color", (0, 15)).EnchantRandomGear(2.0)
    pool = _json(table._document)["pools"][0]
    assert pool["rolls"] == {"min": 1, "max": 3}
    assert pool["entries"][0]["functions"] == [
        {"function": "looting_enchant", "count": {"min": 0, "max": 1}},
        {"function": "random_aux_value", "values": {"min": 0, "max": 15}},
        {
            "function": "random_block_state",
            "block_state": "color",
            "values": {"min": 0, "max": 15},
        },
        {"function": "enchant_random_gear", "chance": 2.0},
    ]


def test_added_functions():
    table = LootTable("added")
    pool = table.pool()
    pool.entry("minecraft:banner").functions.SetBannerDetails(
        0, "silver", [("gradient", "black"), ("border", "red")]
    ).ExplosionDecay()
    pool.entry("minecraft:suspicious_stew").functions.SetStewEffect([0, 3])
    pool.entry("minecraft:ominous_bottle").functions.SetOminousBottleAmplifier((3, 0))
    pool.entry("minecraft:ominous_bottle").functions.SetOminousBottleAmplifier(2)
    pool.entry("minecraft:iron_chestplate").functions.SetArmorTrim(
        "netherite", "wayfinder"
    )
    entries = _json(table._document)["pools"][0]["entries"]
    assert entries[0]["functions"] == [
        {
            "function": "set_banner_details",
            "type": 0,
            "base_color": "silver",
            "patterns": [
                {"pattern": "gradient", "color": "black"},
                {"pattern": "border", "color": "red"},
            ],
        },
        {"function": "explosion_decay"},
    ]
    assert entries[1]["functions"] == [
        {"function": "minecraft:set_stew_effect", "effects": [{"id": 0}, {"id": 3}]}
    ]
    assert entries[2]["functions"] == [
        {"function": "set_ominous_bottle_amplifier", "amplifier": {"min": 0, "max": 3}}
    ]
    assert entries[3]["functions"] == [
        {"function": "set_ominous_bottle_amplifier", "amplifier": {"min": 2, "max": 2}}
    ]
    assert entries[4]["functions"] == [
        {"function": "set_armor_trim", "material": "netherite", "pattern": "wayfinder"}
    ]


@pytest.mark.parametrize(
    "build",
    [
        lambda pool: pool.conditions.random_chance(1.5),
        lambda pool: pool.entry("minecraft:dirt").functions.SetDamage(1.2),
        lambda pool: pool.entry("minecraft:dirt", weight=0),
        lambda pool: pool.entry("minecraft:banner").functions.SetBannerDetails(
            1, patterns=[("gradient", "black")]
        ),
        lambda pool: pool.entry("minecraft:banner").functions.SetBannerDetails(
            0, patterns=[("gradient", "black")] * 7
        ),
        lambda pool: pool.entry("minecraft:suspicious_stew").functions.SetStewEffect(
            []
        ),
        lambda pool: pool.entry(
            "minecraft:ominous_bottle"
        ).functions.SetOminousBottleAmplifier(-1),
    ],
)
def test_out_of_range_values_raise_on_export(build):
    table = LootTable("invalid")
    build(table.pool())
    with pytest.raises(ValueError):
        _json(table._document)


def test_schema_validates_export():
    import jsonschema

    table = LootTable("schema")
    pool = table.pool(2).set_tiers(0.5, 1, 2)
    pool.conditions.match_tool(
        "minecraft:shears", ["silk_touch", ("fortune", 2)], durability=5
    )
    pool.entry(None, weight=3)
    pool.entry("minecraft:map").functions.ExplorationMap("monument").SetName("Map")
    pool.entry("minecraft:banner").functions.SetBannerDetails(
        0, "white", [("creeper", "lime")]
    ).ExplosionDecay().SetOminousBottleAmplifier((0, 4)).SetStewEffect([1])
    jsonschema.validate(_json(table._document), LootTable.__schema__())


def test_loot_table_has_a_format_version():
    table = LootTable("format")
    table.pool().entry("minecraft:stick")
    assert _json(table._document)["format_version"] == "1.26.60"
    assert next(iter(_json(table._document))) == "format_version"


def test_biome_has_tag_condition():
    conds = (
        LootConditions()
        .biome_has_tag("sulfur_caves")
        .biome_has_tag("birch", operator="!=")
    )
    assert _json(conds) == [
        {"condition": "biome_has_tag", "tag": "sulfur_caves"},
        {"condition": "biome_has_tag", "tag": "birch", "operator": "!="},
    ]
    with pytest.raises(ValueError):
        _json(LootConditions().biome_has_tag("birch", operator="=="))
