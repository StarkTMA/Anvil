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
from anvil.api.items.components import ItemDurability
from anvil.api.pbr.fallback import PBRFallback
from anvil.api.pbr.shadow import ShadowSettings
from anvil.api.world.particles import Particle
from anvil.lib import config
from anvil.lib.jsonmodel.enums import BlockFaceValues
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


def test_shadow_settings_file_schema():
    with config.override(PBR=True):
        settings = ShadowSettings().shadow_style("blocky_shadows", 16)
    schema = _check(settings._content, ShadowSettings.__schema__())
    assert schema["title"] == "Shadow Settings"
    assert schema["x-anvil-file"] == {
        "pack": "resource_pack",
        "folder": "shadows",
        "name": "global",
        "extension": ".json",
    }
    assert schema["required"] == ["format_version", "minecraft:shadow_settings"]
    body = schema["$defs"]["_ShadowSettings"]
    assert body["properties"]["shadow_style"]["enum"] == [
        "blocky_shadows",
        "soft_shadows",
    ]


def test_pbr_fallback_file_schema():
    with config.override(PBR=True):
        fallback = PBRFallback().block_fallback("#0000cc00")
    schema = _check(fallback._content, PBRFallback.__schema__())
    assert schema["title"] == "PBR Fallback Settings"
    assert schema["x-anvil-file"]["folder"] == "pbr"
    body = schema["$defs"]["_PBRFallback"]["properties"]
    assert body["global_metalness_emissive_roughness_subsurface"]["maxItems"] == 4


def _filled_pbr_files():
    from anvil.api.pbr.atmosphere import AtmosphericSettings
    from anvil.api.pbr.color_grading import ColorGradingSettings
    from anvil.api.pbr.cubemap import CubeMapSettings
    from anvil.api.pbr.fog import FogSettings
    from anvil.api.pbr.lighting import LightingSettings
    from anvil.api.pbr.texture_set import TextureSet
    from anvil.api.pbr.water import WaterSettings
    from anvil.lib.jsonmodel.enums import FogCameraLocation, RenderDistanceType

    frames = [(0.0, 1.0), (1.0, 2.0)]
    colors = [(0.0, "#ff8800"), (0.5, (0.2, 0.4, 0.6))]
    lighting = LightingSettings()
    lighting.orbital_lights(frames, "#ffffff", 0.4, colors, 10)
    lighting.flash_light(3, (255, 0, 0))
    lighting.emissive(0.5)
    lighting.ambient(frames, "#123")
    lighting.sky(0.5)
    fog = FogSettings("thick")
    fog.add_distance_location("#abd2ff", 0, 10)
    fog.add_distance_location(
        "#000000", 1, 5, RenderDistanceType.Fixed, FogCameraLocation.Water
    ).set_transition_fog("#111111", 0, 0.01, RenderDistanceType.Fixed, 0.25, 5, 0.6, 30)
    fog.water_density(0.8, False, 10, 5)
    fog.media_coefficients(water_scattering="#ff0000")
    fog.henyey_greenstein_g(0.75, 0.6)
    return [
        AtmosphericSettings()
        .horizon_blend_stops(0.1, frames, 0.3, 0.9)
        .rayleigh_strength(frames)
        .sky_zenith_color("#00f")
        .sky_horizon_color(colors),
        ColorGradingSettings()
        .midtones(contrast=(1, 1, 1), offset=(0, 0, 0))
        .highlights(highlightsMin=2, gain=[2, 2, 2])
        .shadows(shadowsMax=0.5)
        .temperature_grade(6500, "white_balance")
        .tone_mapping("aces"),
        WaterSettings()
        .particle_concentrations(1, 2, 3)
        .waves(True, octaves=4)
        .caustics(True, power=2, texture="textures/c"),
        lighting,
        fog,
        CubeMapSettings("test:sky").set_lighting(frames, 0.5, 0.0, True, False),
        TextureSet("sword", "items"),
    ]


def test_pbr_file_schemas():
    with config.override(PBR=True):
        files = _filled_pbr_files()
    for file in files:
        schema = _check(file._content, type(file).__schema__())
        assert schema["x-anvil-file"]["pack"] == "resource_pack"


def test_abstract_file_base_has_no_schema():
    from anvil.lib.jsonmodel import JsonFile

    class _Base(JsonFile):
        pass

    with pytest.raises(TypeError, match="abstract file base"):
        _Base.__schema__()
    with pytest.raises(TypeError, match="abstract file base"):
        _Base("x")


def test_particle_schema():
    schema = Particle.__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    assert schema["x-anvil-file"]["extension"] == ".particle.json"
    components = schema["$defs"]["_ParticleComponents"]["properties"]
    assert "minecraft:emitter_rate_steady" in components
