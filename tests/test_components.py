import sys

import pytest

from anvil.api.actors.components import (
    EntityProjectile,
    ProjectileArrowEffect,
    ProjectileCatchFire,
    ProjectileImpactDamage,
    ProjectileMobEffect,
    ProjectileOnHit,
    ProjectileSpawnChance,
    ProjectileStickInGround,
)
from anvil.api.core.components import EventTrigger
from anvil.lib.jsonmodel import JsonComponent
from anvil.lib.lib import AnvilIO


def payload(obj):
    """The JSON under a component's identifier, or the JSON of a part."""
    exported = obj.__json__()
    return exported[obj.identifier] if isinstance(obj, JsonComponent) else exported


def _exported(component):
    """The component as written to the pack, after empty values are dropped."""
    return AnvilIO._normalize_json_like(component.__json__())["minecraft:projectile"]


def test_entity_projectile_defaults():
    assert payload(EntityProjectile()) == {}
    assert _exported(EntityProjectile()) == {}


def test_entity_projectile_properties():
    proj = EntityProjectile(
        anchor="eye_height",
        angle_offset=15.0,
        hit_nearest_passenger=True,
        ignored_entities=["minecraft:player", "minecraft:cow"],
        isolated_physics=False,
        owner_launch_immunity_ticks=10,
        reflect_immunity=2.5,
    )
    assert payload(proj) == {
        "anchor": "eye_height",
        "angle_offset": 15.0,
        "hit_nearest_passenger": True,
        "ignored_entities": ["minecraft:player", "minecraft:cow"],
        "isolated_physics": False,
        "owner_launch_immunity_ticks": 10,
        "reflect_immunity": 2.5,
    }
    with pytest.raises(ValueError):
        payload(EntityProjectile(anchor="feet"))


def test_entity_projectile_on_hit_switches_are_kept_empty():
    proj = EntityProjectile(
        on_hit=ProjectileOnHit(
            douse_fire=True,
            ignite=True,
            remove_on_hit=True,
            teleport_owner=False,
            arrow_effect=ProjectileArrowEffect(),
            stick_in_ground=ProjectileStickInGround(),
        )
    )
    assert _exported(proj) == {
        "on_hit": {
            "arrow_effect": {},
            "douse_fire": {},
            "ignite": {},
            "remove_on_hit": {},
            "stick_in_ground": {},
        }
    }


def test_entity_projectile_on_hit_parts():
    proj = EntityProjectile(
        on_hit=ProjectileOnHit(
            arrow_effect=ProjectileArrowEffect(apply_effect_to_blocking_targets=False),
            catch_fire=ProjectileCatchFire(
                fire_affected_by_griefing=True, on_fire_time=4.0
            ),
            grant_xp=(3, 7),
            impact_damage=ProjectileImpactDamage(
                damage=(2.0, 5.0),
                knockback=True,
                filter="zombie",
                difficulty_randomization="additive",
            ),
            mob_effect=[
                ProjectileMobEffect(effect="minecraft:poison", durationeasy=100)
            ],
            spawn_chance=ProjectileSpawnChance(
                spawn_definition="minecraft:chicken",
                first_spawn_chance=0.5,
                first_spawn_count=1,
                on_spawn=[EventTrigger(event="minecraft:entity_born")],
            ),
        )
    )
    assert _exported(proj) == {
        "on_hit": {
            "arrow_effect": {"apply_effect_to_blocking_targets": False},
            "catch_fire": {"fire_affected_by_griefing": True, "on_fire_time": 4.0},
            "grant_xp": {"minXP": 3, "maxXP": 7},
            "impact_damage": {
                "damage": {"min": 2.0, "max": 5.0},
                "difficulty_randomization": "additive",
                "filter": "zombie",
                "knockback": True,
            },
            "mob_effect": {"effects": [{"effect": "poison", "durationeasy": 100}]},
            "spawn_chance": {
                "spawn_definition": "minecraft:chicken",
                "first_spawn_chance": 0.5,
                "first_spawn_count": 1,
                "on_spawn": [{"event": "minecraft:entity_born"}],
            },
        }
    }


def test_entity_projectile_on_hit_checks():
    with pytest.raises(ValueError):
        payload(ProjectileImpactDamage(difficulty_randomization="random"))
    with pytest.raises(TypeError):
        payload(ProjectileImpactDamage(damage={"minimum": 1}))
    with pytest.raises(ValueError):
        payload(
            ProjectileSpawnChance(
                spawn_definition="minecraft:chicken", first_spawn_chance=2
            )
        )
