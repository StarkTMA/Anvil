import sys
from unittest.mock import MagicMock

# Set up mock config to avoid exit(1) during class definition imports
mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"

import anvil.lib.config

anvil.lib.config.CONFIG = mock_config

import pytest
from anvil.api.actors.components import EntityProjectile


def test_entity_projectile_defaults():
    proj = EntityProjectile()
    # Check default structure. By default, fields equal to defaults aren't added to the serialized dict.
    assert proj._component == {"on_hit": {}}


def test_entity_projectile_new_properties():
    proj = EntityProjectile(
        anchor="eye_height",
        angle_offset=15.0,
        hit_nearest_passenger=True,
        ignored_entities=["minecraft:player", "minecraft:cow"],
        isolated_physics=False,
        owner_launch_immunity_ticks=10,
        reflect_immunity=2.5,
    )
    comp = proj._component
    assert comp["anchor"] == "eye_height"
    assert comp["angle_offset"] == 15.0
    assert comp["hit_nearest_passenger"] is True
    assert comp["ignored_entities"] == ["minecraft:player", "minecraft:cow"]
    assert comp["isolated_physics"] is False
    assert comp["owner_launch_immunity_ticks"] == 10
    assert comp["reflect_immunity"] == 2.5


def test_entity_projectile_on_hit_methods():
    proj = EntityProjectile()
    proj.arrow_effect(apply_effect_to_blocking_targets=False)
    assert proj._component["on_hit"]["arrow_effect"] == {
        "apply_effect_to_blocking_targets": False
    }

    proj = EntityProjectile()
    proj.wind_burst_on_hit
    assert proj._component["on_hit"]["wind_burst_on_hit"] == {}

    proj = EntityProjectile()
    proj.remove_on_hit
    assert proj._component["on_hit"]["remove_on_hit"] == {}

    proj = EntityProjectile()
    proj.catch_fire_on_hit(fire_affected_by_griefing=True, on_fire_time=4.0)
    assert proj._component["on_hit"]["catch_fire"] == {
        "fire_affected_by_griefing": True,
        "on_fire_time": 4.0,
    }

    proj = EntityProjectile()
    proj.stick_in_ground(shake_time=1.5)
    assert proj._component["on_hit"]["stick_in_ground"] == {"shake_time": 1.5}

    proj = EntityProjectile()
    proj.stick_in_ground()
    assert proj._component["on_hit"]["stick_in_ground"] == {}

    proj = EntityProjectile()
    proj.thrown_potion_effect(effect=5)
    assert proj._component["on_hit"]["thrown_potion_effect"] == {"effect": 5}

    proj = EntityProjectile()
    proj.thrown_potion_effect()
    assert proj._component["on_hit"]["thrown_potion_effect"] == {}

    proj = EntityProjectile()
    proj.impact_damage(
        damage=(2.0, 5.0),
        knockback=True,
        channeling=True,
        set_last_hurt_requires_damage=False,
    )
    assert proj._component["on_hit"]["impact_damage"] == {
        "damage": {"min": 2.0, "max": 5.0},
        "knockback": True,
        "channeling": True,
        "set_last_hurt_requires_damage": False,
    }

    proj = EntityProjectile()
    proj.spawn_chance(
        spawn_definition="minecraft:chicken",
        first_spawn_chance=0.5,
        first_spawn_count=1,
        second_spawn_chance=0.25,
        second_spawn_count=4,
    )
    assert proj._component["on_hit"]["spawn_chance"] == {
        "spawn_definition": "minecraft:chicken",
        "first_spawn_chance": 0.5,
        "first_spawn_count": 1,
        "second_spawn_chance": 0.25,
        "second_spawn_count": 4,
    }

    proj = EntityProjectile()
    proj.on_hit(catch_fire=True, douse_fire=True, ignite=True, teleport_owner=True)
    assert proj._component["on_hit"]["catch_fire"] == {}
    assert proj._component["on_hit"]["douse_fire"] == {}
    assert proj._component["on_hit"]["ignite"] == {}
    assert proj._component["on_hit"]["teleport_owner"] == {}
