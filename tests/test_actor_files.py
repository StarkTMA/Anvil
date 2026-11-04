"""Tests for the typed actor files: materials, spawn rules, render controllers, animations,
animation controllers, events and the entity and item client descriptions."""

import pytest
from anvil.api.actors.animation_controllers import BPAnimationControllers
from anvil.api.actors.animations import BPAnimations
from anvil.api.actors.entity import Entity
from anvil.api.actors.materials import Material, MaterialsObject
from anvil.api.actors.render_controller import RenderControllers
from anvil.api.actors.spawn_rules import SpawnRule
from anvil.api.core.filters import Filter
from anvil.api.items.client import ItemClient
from anvil.lib import config
from anvil.lib.jsonmodel.enums import (
    Difficulty,
    MaterialDefinitions,
    MaterialFunc,
    MaterialStates,
    Population,
    Vibrations,
)
from anvil.lib.lib import AnvilIO
from anvil.lib.translator import AnvilTranslator

jsonschema = pytest.importorskip("jsonschema")


@pytest.fixture(autouse=True)
def project(monkeypatch):
    monkeypatch.setattr(MaterialsObject, "_instance", None)
    monkeypatch.setattr(AnvilTranslator, "add_localization_entry", lambda *a: None)
    with config.override(NAMESPACE="testns", PROJECT_NAME="proj"):
        yield


def _check(file):
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._content)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def test_material_settings_and_variants():
    material = Material("glow", "entity_alphatest").add_states(MaterialStates.Blending)
    material.add_defines(MaterialDefinitions.USE_UV_ANIM)
    material.remove_states(MaterialStates.DisableCulling)
    material.set_frontFace(stencilFunc=MaterialFunc.Always).set_stencilRef(3)
    material.add_samplerState(0, textureFilter="Point")
    material.add_variant("skinning").add_defines(MaterialDefinitions.USE_OVERLAY)
    material.queue()
    assert material.identifier == "testns.glow"
    assert _check(MaterialsObject())["materials"] == {
        "version": "1.0.0",
        "testns.glow:entity_alphatest": {
            "+states": ["Blending"],
            "-states": ["DisableCulling"],
            "+defines": ["USE_UV_ANIM"],
            "frontFace": {"stencilFunc": "Always"},
            "stencilRef": 3,
            "+samplerStates": [{"samplerIndex": 0, "textureFilter": "Point"}],
            "variants": [{"skinning": {"+defines": ["USE_OVERLAY"]}}],
        },
    }


def test_material_with_the_same_key_replaces_the_first():
    Material("glow", "entity_alphatest").add_states(MaterialStates.Blending).queue()
    Material("glow", "entity_alphatest").set_depthFunc(MaterialFunc.Always).queue()
    materials = _check(MaterialsObject())["materials"]
    assert materials["testns.glow:entity_alphatest"] == {"depthFunc": "Always"}


def test_material_refuses_a_stencil_ref_out_of_range():
    Material("bad").set_stencilRef(300).queue()
    with pytest.raises(ValueError):
        MaterialsObject()._content.__json__()


def test_spawn_rule_conditions():
    rule = SpawnRule("testns:crab")
    rule.description.set_population_control(Population.Animal)
    condition = rule.add_condition
    condition.spawns_on_surface().weight(40).herd(2, 4).herd(1, 1, "grow", 1)
    condition.biome_filter([Filter.has_biome_tag("beach")])
    condition.density_limit(surface=5).difficulty_filter(max_difficulty=Difficulty.Hard)
    body = _check(rule)["minecraft:spawn_rules"]
    assert body["description"] == {
        "identifier": "testns:crab",
        "population_control": "animal",
    }
    assert body["conditions"] == [
        {
            "minecraft:spawns_on_surface": {},
            "minecraft:weight": {"default": 40},
            "minecraft:herd": [
                {"min_size": 2, "max_size": 4},
                {"min_size": 1, "max_size": 1, "event": "grow", "event_skip_count": 1},
            ],
            "minecraft:biome_filter": [{"test": "has_biome_tag", "value": "beach"}],
            "minecraft:density_limit": {"surface": 5},
            "minecraft:difficulty_filter": {"max": "hard"},
        }
    ]


def test_spawn_rule_refuses_values_out_of_range():
    rule = SpawnRule("testns:imp")
    rule.add_condition.brightness_filter(0, 20)
    with pytest.raises(ValueError):
        rule._content.__json__()
    rule = SpawnRule("testns:imp")
    rule.add_condition.delay_filter(1, 2, "testns:imp", 150)
    with pytest.raises(ValueError):
        rule._content.__json__()


def test_spawn_rule_without_conditions_is_not_queued():
    assert SpawnRule("testns:none").queue() is None


def test_render_controller_arrays_and_default_material():
    description = Entity("testns:ship").client.description
    rc = description.render_controller("root", "q.is_alive")
    rc.texture_array("skins", ["a", "b"], "q.variant").set_geometry("ship")
    rc.add_part_visibility("sail", False).set_overlay_color(1, 0, 0, 0)
    assert description.render_controller("root") is rc
    file = RenderControllers(description)
    file.queue()
    assert rc.reference == {"controller.render.testns.ship.root": "q.is_alive"}
    assert _check(file)["render_controllers"] == {
        "controller.render.testns.ship.root": {
            "arrays": {"textures": {"array.skins": ["Texture.a", "Texture.b"]}},
            "geometry": "Geometry.ship",
            "materials": [{"*": "material.default"}],
            "textures": ["array.skins[q.variant]"],
            "part_visibility": [{"sail": False}],
            "overlay_color": {"r": 0, "g": 0, "b": 0, "a": 1},
        }
    }


def test_render_controller_checks_its_references():
    rc = Entity("testns:ship").client.description.render_controller("root")
    rc.set_geometry("ship").add_texture("hull")
    rc._validate(["hull"], ["ship"], ["default"])
    with pytest.raises(ValueError):
        rc._validate(["sail"], ["ship"], ["default"])
    with pytest.raises(ValueError):
        rc.material("*", "glass")._validate(["hull"], ["ship"], ["default"])


def test_render_controller_uv_anim_is_for_entities():
    rc = ItemClient("testns:hat").description.render_controller("root")
    with pytest.raises(ValueError):
        rc.set_uv_anim((0, 0), (1, 1))


def test_bp_animation_timeline():
    server = Entity("testns:mob").server
    animation = server.description.animation("tick", loop=True, animate=True)
    animation.add_timeline(0.0, ["say hi", "@s grow", "v.x = 1"])
    animation.add_timeline(1.5, ["kill @s"])
    assert server.description.animation("tick") is animation
    server.description.__prepare_export__(server)
    description = server.description.__json__()
    assert description["animations"] == {"tick": "animation.testns.mob.tick"}
    assert description["scripts"] == {"animate": ["tick"]}
    file = BPAnimations(server.description)
    file.queue()
    assert _check(file)["animations"] == {
        "animation.testns.mob.tick": {
            "loop": True,
            "animation_length": 1.55,
            "timeline": {
                "0.0": ["/say hi", "@s grow", "v.x = 1;"],
                "1.5": ["/kill @s"],
            },
        }
    }


def test_animation_controllers_leave_empty_controllers_out():
    server = Entity("testns:mob").server
    server.description.animation_controller("empty", animate=True).add_state("default")
    controller = server.description.animation_controller("life", animate=True)
    controller.add_state("default").transition("dead", "q.health <= 0")
    controller.add_state("dead").add_on_entry("@s die")
    assert controller.add_state("dead") is controller.states[1]
    assert server.description.animation_controller("life") is controller
    server.description.__prepare_export__(server)
    file = BPAnimationControllers(server.description)
    file.queue()
    description = server.description.__json__()
    assert description["animations"] == {"life": "controller.animation.testns.mob.life"}
    assert [e.name for e in server.description.scripts.animate] == ["life"]
    assert _check(file)["animation_controllers"] == {
        "controller.animation.testns.mob.life": {
            "initial_state": "default",
            "states": {
                "default": {"transitions": [{"dead": "q.health <= 0"}]},
                "dead": {"on_entry": ["@s die"]},
            },
        }
    }


def test_animation_controller_needs_its_transition_targets():
    server = Entity("testns:mob").server
    server.description.animation_controller("life").add_state("default").transition(
        "gone", "1"
    )
    file = BPAnimationControllers(server.description)
    file.queue()
    with pytest.raises(ValueError):
        file._content.__json__()


def test_rp_controller_states():
    entity = Entity("testns:ghost")
    description = entity.client.description
    state = description.animation_controller("look").add_state("default")
    with pytest.raises(ValueError):
        state.add_on_entry("say hi")
    state.add_on_entry("v.x", 1).set_blend_transition(0.2)
    state.set_blend_via_shortest_path().sound_effect("boo")
    assert AnvilIO._normalize_json_like(state) == {
        "on_entry": ["v.x=1;"],
        "sound_effects": [{"effect": "boo", "locator": "root"}],
        "blend_transition": 0.2,
        "blend_via_shortest_path": True,
    }


def test_rp_controller_particles_must_be_defined():
    description = Entity("testns:ghost").client.description
    description.animation_controller("look").add_state("default").particle("smoke")
    with pytest.raises(ValueError):
        description.__json__()


def test_entity_events():
    entity = Entity("testns:mob")
    event = (
        entity.server.event("testns:spawned")
        .add_component_groups(["a"])
        .add_component_groups(["b"])
    )
    event.add_property("mode", 1).set_emit_vibration(Vibrations.EntityAct)
    entity.server.event("testns:roll").add_randomize().set_weight(
        3
    ).add_component_groups(["c"]).add_randomize().add_component_groups(
        ["d"]
    ).add_sequence().set_trigger(
        "testns:spawned"
    )
    assert entity.server.event("testns:spawned") is event
    with pytest.raises(ValueError):
        event.set_trigger("x").set_trigger("y")
    events = _check(entity.server)["minecraft:entity"]["events"]
    assert events["testns:spawned"] == {
        "add": {"component_groups": ["a", "b"]},
        "set_property": {"testns:mode": 1},
        "emit_vibration": {"vibration": "entity_act"},
        "trigger": "x",
    }
    assert events["testns:roll"] == {
        "randomize": [
            {"weight": 3, "add": {"component_groups": ["c"]}},
            {
                "weight": 1,
                "add": {"component_groups": ["d"]},
                "sequence": [{"trigger": "testns:spawned"}],
            },
        ]
    }


def test_entity_spawn_category():
    entity = Entity("testns:mob")
    entity.server.description.config(spawn_category="monster")
    entity.server.__export__()
    _check(entity.server)
    description = AnvilIO._normalize_json_like(entity.server._body.description)
    assert description["spawn_category"] == "monster"

    entity = Entity("testns:other")
    entity.server.description.config(spawn_category="monsters")
    with pytest.raises(ValueError):
        entity.server.__export__()
        _check(entity.server)


def test_entity_server_description():
    entity = Entity("testns:mob")
    server = entity.server
    server.description.config(is_spawnable=False)
    server.description.add_enum_property("mode", ("a", "b"), "a").add_int_property(
        "hp", (0, 5)
    )
    server.description.animation("tick", animate=True).add_timeline(0, ["say hi"])
    server.description.animation_controller("unused", animate=True).add_state("default")
    server.__export__()
    _check(server)
    description = AnvilIO._normalize_json_like(server._body.description)
    assert description == {
        "identifier": "testns:mob",
        "animations": {"tick": "animation.testns.mob.tick"},
        "scripts": {"animate": ["tick"]},
        "is_spawnable": False,
        "properties": {
            "testns:mode": {
                "type": "enum",
                "default": "a",
                "values": ["a", "b"],
                "client_sync": False,
            },
            "testns:hp": {
                "type": "int",
                "default": 0,
                "range": [0, 5],
                "client_sync": False,
            },
        },
    }
    assert [p.name for p in server.description.properties] == [
        "testns:mode",
        "testns:hp",
    ]


def test_entity_client_description_needs_a_render_controller():
    entity = Entity("testns:mob")
    with pytest.raises(ValueError):
        entity.client.description.__prepare_export__(entity.client)


def test_entity_client_description_lists_render_controllers():
    entity = Entity("testns:mob")
    description = entity.client.description
    description.set_dummy().add_material("glow", "testns.glow").init_vars(x=1)
    description.render_controller("root").set_geometry("mob")
    description.render_controller("faces", False)
    description.__prepare_export__(entity.client)
    _check(entity.client)
    assert AnvilIO._normalize_json_like(description) == {
        "identifier": "testns:mob",
        "materials": {"default": "entity_alphatest", "glow": "testns.glow"},
        "scripts": {"initialize": ["v.x=1;"]},
        "render_controllers": [
            "controller.render.testns.mob.root",
            {"controller.render.testns.mob.faces": False},
        ],
        "spawn_egg": {"base_color": "#ffffff", "overlay_color": "#000000"},
    }


def test_spawn_egg_colors_take_any_color():
    description = Entity("testns:mob").client.description
    description.set_spawn_egg_color((255, 0, 0), (0.0, 0.0, 1.0))
    assert description.spawn_egg.__json__() == {
        "base_color": "#ff0000",
        "overlay_color": "#0000ff",
    }


def test_description_maps_keep_the_last_entry():
    description = Entity("testns:mob").client.description
    description.add_material("default", "entity").add_material("glow", "glow")
    description.add_material("default", "entity_emissive")
    assert AnvilIO._normalize_json_like(description.__json__()["materials"]) == {
        "default": "entity_emissive",
        "glow": "glow",
    }


def test_item_client_has_no_entity_keys():
    attachable = ItemClient("testns:hat")
    attachable.description.set_dummy()
    attachable.description.__prepare_export__(attachable)
    assert _check(attachable)["minecraft:attachable"] == {
        "description": {
            "identifier": "testns:hat",
            "materials": {"default": "entity_alphatest"},
        }
    }


def test_kit_entity_outline_materials():
    from anvil.kit.actors.materials import add_entity_outline

    add_entity_outline(xray_mode=True).queue()
    materials = _check(MaterialsObject())["materials"]
    assert materials["testns.entity_outline_base:entity_alphatest"]["stencilRef"] == 3
    outline = materials["testns.entity_outline:entity_alphatest"]
    assert outline["depthFunc"] == "Always"
    assert outline["frontFace"] == {"stencilFunc": "NotEqual"}


def test_entity_references_accept_an_entity_or_a_vanilla_identifier():
    from anvil.api.actors.components.combat import EntityTransformation
    from anvil.api.vanilla.entities import MinecraftEntityTypes

    entity = Entity("crab")
    assert entity.identifier == "testns:crab"
    assert entity.server.identifier is entity.identifier
    exported = AnvilIO._normalize_json_like(EntityTransformation(into=entity))
    assert exported["minecraft:transformation"]["into"] == entity.identifier
    exported = AnvilIO._normalize_json_like(
        EntityTransformation(into=MinecraftEntityTypes.Zombie())
    )
    assert exported["minecraft:transformation"]["into"] == "minecraft:zombie"


def test_runtime_identifier_must_be_vanilla():
    from anvil.api.vanilla.entities import MinecraftEntityTypes

    entity = Entity("crab")
    entity.server.description.config(runtime_identifier=MinecraftEntityTypes.Arrow())
    assert entity.server.description.runtime_identifier == "minecraft:arrow"
    with pytest.raises(ValueError):
        entity.server.description.config(runtime_identifier=Entity("shark").identifier)
    with pytest.raises(TypeError):
        entity.server.description.config(runtime_identifier=Entity("shark"))


def test_actor_scripts_shared_add_animate():
    from anvil.api.actors.animation_controllers import _ActorScripts
    from anvil.api.actors.client import _ActorClientScripts

    server = _ActorScripts().add_animate("walk").add_animate("walk")
    client = _ActorClientScripts().add_animate("idle", "q.is_moving").set_scale(2)
    assert server.__json__() == {"animate": ["walk"]}
    payload = client.__json__()
    assert payload["animate"] == [{"idle": "q.is_moving"}]
    assert payload["scale"] == 2


def test_spawn_egg_texture_index_zero_is_written():
    from anvil.api.actors.client import _SpawnEgg

    assert _SpawnEgg(texture="tut:egg", texture_index=0).__json__() == {
        "texture": "tut:egg",
        "texture_index": 0,
    }
    assert _SpawnEgg(texture="tut:egg").__json__() == {"texture": "tut:egg"}


def test_event_builders_write_fields():
    from anvil.api.actors.events import _Event

    event = (
        _Event("testns:phase")
        .add_component_groups(["a"])
        .add_component_groups(["b"])
        .remove_component_groups(["c"])
        .add_queue_command(["say hi"])
        .set_emit_vibration(Vibrations.EntityAct)
        .set_play_sound("random.pop")
        .set_emit_particle("minecraft:basic_flame_particle")
        .set_execute_event_on_home_block("testns:ring")
        .set_unleash(unleash_self=True)
    )
    payload = event.__json__()
    assert payload["add"] == {"component_groups": ["a", "b"]}
    assert payload["remove"] == {"component_groups": ["c"]}
    assert payload["queue_command"] == {"command": ["say hi"]}
    assert payload["emit_vibration"] == {"vibration": "entity_act"}
    assert payload["play_sound"] == {"sound": "random.pop"}
    assert payload["emit_particle"] == {"particle": "minecraft:basic_flame_particle"}
    assert payload["execute_event_on_home_block"] == {"event": "testns:ring"}
    assert payload["unleash"] == {"unleash_self": True}
    assert "sequence" not in payload and "randomize" not in payload
    assert "set_property" not in payload


def test_event_trigger_once_and_sequence_randomize_exclusive():
    from anvil.api.actors.events import _Event

    event = _Event("testns:once").set_trigger("testns:a")
    with pytest.raises(ValueError):
        event.set_trigger("testns:b")
    both = _Event("testns:both")
    both.add_sequence()
    both.add_randomize()
    with pytest.raises(ValueError):
        both.__json__()


def test_event_nested_sequence_and_randomize():
    from anvil.api.actors.events import _Event

    event = _Event("testns:nested")
    first = event.add_sequence().add_component_groups(["x"])
    option = first.add_sequence().add_randomize().set_weight(3).set_trigger("testns:y")
    option.add_randomize().set_unleash(unleash_others=True)
    assert event.__json__()["sequence"] == [
        {"add": {"component_groups": ["x"]}},
        {
            "randomize": [
                {"trigger": "testns:y", "weight": 3},
                {"unleash": {"unleash_others": True}, "weight": 1},
            ]
        },
    ]
