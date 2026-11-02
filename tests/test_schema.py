"""Tests for `JsonObject.__schema__()`: each schema accepts the JSON its component exports."""

import pytest

from anvil.api.actors.components import (
    EntityBreedable,
    EntityNPC,
    EntityTimer,
    NPCOffsets,
)
from anvil.api.biomes.components import BiomeClientFoliageAppearance, BiomeClimate
from anvil.api.blocks.components import BlockGeometry, BlockPlacementFilter
from anvil.api.core.enums import BlockFaceValues
from anvil.api.items.components import ItemDurability
from anvil.lib.lib import AnvilIO

jsonschema = pytest.importorskip("jsonschema")


def _check(component, schema=None):
    schema = schema or type(component).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(component)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return schema


def test_entity_npc_schema():
    schema = _check(
        EntityNPC().set_npc_data(
            skin_list=[0, 1],
            portrait_offsets=NPCOffsets(translate=(0, 1, 0), scale=(1, 1, 1)),
        )
    )
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["required"] == ["minecraft:npc"]
    payload = schema["properties"]["minecraft:npc"]
    assert payload["properties"]["npc_data"] == {"$ref": "#/$defs/NPCData"}
    assert payload["required"] == ["npc_data"]
    assert schema["$defs"]["NPCData"]["required"] == ["skin_list"]
    offsets = schema["$defs"]["NPCOffsets"]["properties"]["translate"]
    assert offsets["minItems"] == offsets["maxItems"] == 3


def test_entity_timer_schema():
    timer = EntityTimer(time_down_event="explode").add_random_time_choice(
        weight=1, value=2
    )
    schema = _check(timer)
    payload = schema["properties"]["minecraft:timer"]
    assert payload["properties"]["time_down_event"] == {"$ref": "#/$defs/EventTrigger"}
    assert payload["required"] == ["time_down_event"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(
            {"minecraft:timer": {"time_down_event": {"event": "a"}, "looping": "yes"}},
            schema,
        )


def test_breedable_schema_keys_partners_by_mate():
    breedable = EntityBreedable().add_breeds_with(
        mate_type="minecraft:cow", breed_event="become_baby"
    )
    _check(breedable)


def test_block_schemas():
    _check(BlockGeometry())
    _check(
        BlockPlacementFilter().add_condition(
            allowed_faces=[BlockFaceValues.Side], block_filter=["minecraft:dirt"]
        )
    )


def test_item_schema():
    schema = _check(ItemDurability(max_durability=100, damage_chance=(10, 50)))
    payload = schema["properties"]["minecraft:durability"]
    assert payload["properties"]["damage_chance"]["properties"]["min"]["maximum"] == 100


def test_biome_schemas():
    schema = _check(
        BiomeClimate(temperature=0.8, downfall=0.4, snow_accumulation=[0.0, 0.125])
    )
    payload = schema["properties"]["minecraft:climate"]
    assert payload["properties"]["temperature"] == {
        "type": "number",
        "minimum": -50.0,
        "maximum": 50.0,
    }
    _check(BiomeClientFoliageAppearance(color="birch"))
    _check(BiomeClientFoliageAppearance(color=(1.0, 0.5, 0.0)))


def test_schema_refuses_what_export_refuses():
    schema = BiomeClimate.__schema__()
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"minecraft:climate": {"downfall": 1.5}}, schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"minecraft:climate": {"rainfall": 1}}, schema)
