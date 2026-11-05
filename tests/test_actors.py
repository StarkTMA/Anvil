import pytest

from anvil.api.vanilla.entities import vanilla_entities_ids
from anvil.api.vanilla.factories.minecraft_entities import SulfurCube
from anvil.lib.jsonmodel import JsonComponent
from anvil.lib.jsonmodel.enums import FilterSubject
from anvil.lib.lib import AnvilIO


def payload(obj):
    """The JSON under a component's identifier, or the JSON of a part."""
    exported = obj.__json__()
    return exported[obj.identifier] if isinstance(obj, JsonComponent) else exported


def test_sulfur_cube_entity():
    desc = SulfurCube()
    assert desc == "minecraft:sulfur_cube"
    assert desc.is_vanilla
    assert "minecraft:sulfur_cube" in vanilla_entities_ids()


def test_entity_hide_held_items():
    from anvil.api.actors.entity import Entity

    entity = Entity("custom_entity")
    scripts = entity.client.description.scripts
    entity.client.description.set_hide_held_items(True)
    assert scripts.hide_held_items == "1"

    entity.client.description.set_hide_held_items("q.is_sheared")
    assert scripts.hide_held_items == "q.is_sheared"


def test_entity_ai_pickup_items():
    from anvil.api.actors.components import EntityAIPickupItems

    assert payload(EntityAIPickupItems()) == {}
    assert payload(EntityAIPickupItems(stop_if_holding_item=True)) == {
        "stop_if_holding_item": True
    }


def test_ai_goal_priority_and_control_flags():
    from anvil.api.actors.components import EntityAIFloat
    from anvil.lib.jsonmodel.enums import ControlFlags

    goal = EntityAIFloat(priority=0, control_flags=[ControlFlags.Jump])
    assert payload(goal) == {"priority": 0, "control_flags": ["jump"]}
    with pytest.raises(ValueError):
        payload(EntityAIFloat(priority=-1))


def test_ai_goal_entity_types():
    from anvil.api.actors.components import EntityAINearestAttackableTarget
    from anvil.api.core.filters import Filter

    goal = EntityAINearestAttackableTarget(
        priority=2, attack_interval=(1, 3), must_see=True
    ).add_entity_type(filters=Filter.is_family("player"), max_dist=24)
    exported = payload(goal)
    assert exported["attack_interval"] == {"min": 1, "max": 3}
    assert exported["must_see"] is True
    assert set(exported["entity_types"][0]) == {"filters", "max_dist"}
    assert exported["entity_types"][0]["max_dist"] == 24
    assert payload(EntityAINearestAttackableTarget(attack_interval=5)) == {
        "attack_interval": 5
    }


def test_ai_goal_ranges_and_triggers():
    from anvil.api.actors.components import (
        EntityAIGoHome,
        EntityAIRandomLookAround,
        EntityAITimerFlag1,
    )
    from anvil.api.core.components import EventTrigger

    timer = EntityAITimerFlag1(cooldown_range=(5, 10), duration_range=2, on_end="ended")
    assert payload(timer) == {
        "cooldown_range": {"min": 5, "max": 10},
        "duration_range": 2,
        "on_end": {"event": "ended", "target": "self"},
    }
    assert payload(EntityAIRandomLookAround(look_time=(2, 4))) == {
        "look_time": {"min": 2, "max": 4}
    }
    with pytest.raises(TypeError):
        payload(EntityAIRandomLookAround(look_time=(2.5, 4)))
    home = EntityAIGoHome(
        on_home=[EventTrigger(event="home", target=FilterSubject.Self), "arrived"],
        on_failed="lost",
    )
    assert AnvilIO._normalize_json_like(payload(home)) == {
        "on_home": [
            {"event": "home", "target": "self"},
            {"event": "arrived", "target": "self"},
        ],
        "on_failed": {"event": "lost", "target": "self"},
    }


def test_ai_goal_summon_and_send_event():
    from anvil.api.actors.components import (
        EntityAISendEvent,
        EntityAISummonEntity,
        SummonStep,
    )

    summon = EntityAISummonEntity().add_summon_choice(
        cast_duration=2,
        weight=1,
        sequence=[SummonStep(entity_type="minecraft:vex", num_entities_spawned=3)],
    )
    assert payload(summon) == {
        "summon_choices": [
            {
                "cast_duration": 2,
                "sequence": [
                    {"entity_type": "minecraft:vex", "num_entities_spawned": 3}
                ],
                "weight": 1,
            }
        ]
    }
    send = EntityAISendEvent().add_event_choice(weight=1, particle_color="#FFB38033")
    send.event_choices[0].add_step(event="wololo", base_delay=1)
    assert payload(send)["event_choices"][0]["sequence"] == [
        {"event": "wololo", "base_delay": 1}
    ]


def test_ai_goal_block_lists():
    from anvil.api.actors.components import (
        EntityAIEatBlock,
        EntityAIPlaceBlock,
        EntityAITransportItems,
    )

    eat = EntityAIEatBlock(success_chance="q.is_baby ? 0.02 : 0.001").add_block_pair(
        eat_block="minecraft:grass_block", replace_block="minecraft:dirt"
    )
    assert payload(eat)["eat_and_replace_block_pairs"] == [
        {"eat_block": "minecraft:grass_block", "replace_block": "minecraft:dirt"}
    ]
    place = EntityAIPlaceBlock(
        placeable_carried_blocks=["minecraft:dirt"], xz_range=(-2, 2)
    ).add_randomly_placeable_block(block="minecraft:sand", weight=2)
    assert payload(place) == {
        "placeable_carried_blocks": [{"name": "minecraft:dirt"}],
        "randomly_placeable_blocks": [
            {"block": {"name": "minecraft:sand"}, "weight": 2}
        ],
        "xz_range": {"min": -2, "max": 2},
    }
    with pytest.raises(ValueError):
        payload(
            EntityAITransportItems(
                allowed_items=["minecraft:apple"], disallowed_items=["minecraft:stone"]
            )
        )


def exported_namespace(exported):
    return next(iter(exported["set_property"])).split(":")[0]


def test_entity_bounciness():
    from anvil.api.actors.components import EntityBounciness

    bounciness = EntityBounciness(strength=0.5)
    assert bounciness.__json__() == {"minecraft:bounciness": {"strength": 0.5}}


def test_entity_air_drag_modifier():
    from anvil.api.actors.components import EntityAirDragModifier

    air_drag = EntityAirDragModifier(strength=0.8)
    assert air_drag.__json__() == {"minecraft:air_drag_modifier": {"strength": 0.8}}


def test_entity_apply_knockback_rules():
    from anvil.api.actors.components import EntityApplyKnockbackRules

    rules = EntityApplyKnockbackRules()
    rules.add_preset(extra_knockback_approach="multiply")
    assert payload(rules) == {"presets": [{"extra_knockback_approach": "multiply"}]}


def test_entity_pushable_by_entity():
    from anvil.api.actors.components import EntityPushableByEntity
    from anvil.api.core.filters import Filter

    push = EntityPushableByEntity().add_preset(
        filters=Filter.is_family("player"),
        push_mode="none",
        strength_multiplier=1.5,
        play_sound=False,
    )
    preset = payload(push)["presets"][0]
    assert set(preset) == {"filters", "push_mode", "strength_multiplier", "play_sound"}
    assert preset["push_mode"] == "none"
    assert preset["play_sound"] is False
    assert payload(EntityPushableByEntity()) == {}


def test_entity_area_attack():
    from anvil.api.actors.components import EntityAreaAttack
    from anvil.lib.jsonmodel.enums import DamageCause

    aa = EntityAreaAttack(cause=DamageCause.Magic, use_self_as_damage_source=False)
    assert payload(aa) == {"cause": "magic", "use_self_as_damage_source": False}


def test_entity_leashable():
    from anvil.api.actors.components import EntityLeashable, EntityLeashableTo
    from anvil.lib.jsonmodel.enums import LeashSpringType

    leash = EntityLeashable(unleash_on_removal=True).add_preset(
        max_distance=12, spring_type=LeashSpringType.Bouncy
    )
    assert payload(leash) == {
        "presets": [{"max_distance": 12, "spring_type": "bouncy"}],
        "unleash_on_removal": True,
    }

    leash_to = EntityLeashableTo(unleash_on_removal=False)
    assert payload(leash_to) == {"unleash_on_removal": False}


def test_entity_unleash_event_response():
    from anvil.api.actors.entity import Entity

    ent = Entity("test_unleash")
    evt = ent.server.event("minecraft:entity_spawned")
    evt.set_unleash(unleash_self=True, unleash_others=True)
    assert evt.__json__()["unleash"] == {
        "unleash_self": True,
        "unleash_others": True,
    }


def test_entity_filter_redstone_strength():
    from anvil.api.core.filters import Filter

    filt = Filter.redstone_strength_at_position(15)
    assert filt.test == "redstone_strength_at_position"
    assert filt.value == 15


def test_entity_flag_components_export_empty_objects():
    from anvil.api.actors.components import EntityCanClimb, EntityIsBaby

    assert EntityCanClimb().__json__() == {"minecraft:can_climb": {}}
    assert EntityIsBaby().__json__() == {"minecraft:is_baby": {}}


def test_entity_unset_options_are_left_out():
    from anvil.api.actors.components import EntityPhysics

    assert payload(EntityPhysics()) == {}
    assert payload(EntityPhysics(has_gravity=False)) == {"has_gravity": False}


def test_entity_single_value_is_required():
    import pytest

    from anvil.api.actors.components import EntityScale

    with pytest.raises(TypeError):
        EntityScale()
    assert payload(EntityScale(value=0.5)) == {"value": 0.5}


def test_entity_ranges():
    from anvil.api.actors.components import (
        EntityAttack,
        EntityHealth,
        EntityHorseJumpStrength,
    )

    assert payload(EntityHealth(value=20, max=30)) == {"value": 20, "max": 30}
    assert payload(EntityHealth(value=(10, 20))) == {
        "value": {"range_min": 10, "range_max": 20}
    }
    assert payload(EntityHorseJumpStrength(value=(0.4, 1.0))) == {
        "value": {"range_min": 0.4, "range_max": 1.0}
    }
    assert payload(EntityAttack(damage=(4, 2))) == {"damage": {"min": 2, "max": 4}}
    assert payload(EntityAttack(damage=3)) == {"damage": 3}


def test_entity_speeds_in_meters():
    from anvil.api.actors.components import (
        EntityFlyingSpeedMeters,
        EntityMovementMeters,
    )

    assert EntityMovementMeters(value=4.0).__json__() == {
        "minecraft:movement": {"value": 0.304}
    }
    assert EntityFlyingSpeedMeters(value=4.0).__json__() == {
        "minecraft:flying_speed": {"value": 0.3}
    }


def test_entity_knockback_resistance_is_checked_not_clamped():
    import pytest

    from anvil.api.actors.components import EntityKnockbackResistance

    with pytest.raises(ValueError):
        payload(EntityKnockbackResistance(value=10000))
    assert payload(EntityKnockbackResistance(value=-2)) == {"value": -2}


def test_entity_trigger_components():
    from anvil.api.actors.components import EntityOnDeath, EntityOnTargetEscape
    from anvil.api.core.components import EventTrigger
    from anvil.lib.jsonmodel.enums import FilterSubject

    on_death = EntityOnDeath(event="die", target=FilterSubject.Holder)
    assert isinstance(on_death, EventTrigger)
    assert on_death.__json__() == {
        "minecraft:on_death": {"event": "die", "target": "holder"}
    }
    assert EntityOnTargetEscape.identifier == "minecraft:on_target_escape"


def test_entity_event_parts():
    from anvil.api.actors.components import EntityGiveable, EntitySittable
    from anvil.api.core.components import EventTrigger
    from anvil.lib.jsonmodel.enums import FilterSubject

    sittable = EntitySittable(sit_event="sit", stand_event=EventTrigger(event="stand"))
    assert payload(sittable) == {
        "sit_event": {"event": "sit", "target": "self"},
        "stand_event": {"event": "stand"},
    }

    giveable = EntityGiveable(
        on_give=EventTrigger(event="given", target=FilterSubject.Self)
    ).add_items("minecraft:apple", "minecraft:bread")
    assert payload(giveable) == {
        "items": ["minecraft:apple", "minecraft:bread"],
        "on_give": {"event": "given", "target": "self"},
    }


def test_entity_environment_sensor_triggers():
    from anvil.api.actors.components import EntityEnvironmentSensor
    from anvil.api.core.filters import Filter

    sensor = EntityEnvironmentSensor().add_trigger(
        event="wet", filters=Filter.in_water(True)
    )
    exported = payload(sensor)
    assert exported["triggers"][0]["event"] == "wet"
    assert isinstance(exported["triggers"][0]["filters"], Filter)


def test_entity_on_equipment_changed_slots():
    import pytest

    from anvil.api.actors.components import EntityOnEquipmentChanged
    from anvil.lib.jsonmodel.enums import Slots

    changed = EntityOnEquipmentChanged().add_slot(slot=Slots.Head, on_equip="hat_on")
    assert payload(changed) == {
        "slots": [{"slot": "slot.armor.head", "on_equip": "hat_on"}]
    }
    changed.add_slot(slot=Slots.Head, on_unequip="hat_off")
    with pytest.raises(ValueError):
        payload(changed)


def test_entity_loot_and_trade_table_paths():
    from anvil.api.actors.components import EntityLoot

    assert payload(EntityLoot(table="loot_tables/a.json")) == {
        "table": "loot_tables/a.json"
    }


def test_entity_burns_in_daylight_slot():
    import pytest

    from anvil.api.actors.components import EntityBurnsInDaylight
    from anvil.lib.jsonmodel.enums import Slots

    assert payload(EntityBurnsInDaylight(protection_slot=Slots.Head)) == {
        "protection_slot": "slot.armor.head"
    }
    with pytest.raises(ValueError):
        payload(EntityBurnsInDaylight(protection_slot=Slots.Inventory))


def test_entity_damage_sensor_triggers():
    from anvil.api.actors.components import EntityDamageSensor
    from anvil.api.core.components import EventTrigger
    from anvil.lib.jsonmodel.enums import DamageCause, DamageSensor

    sensor = (
        EntityDamageSensor()
        .add_trigger(deals_damage=DamageSensor.No)
        .add_trigger(
            cause=DamageCause.Fall,
            deals_damage=False,
            on_damage=EventTrigger(event="landed"),
        )
    )
    assert payload(sensor) == {
        "triggers": [
            {"deals_damage": "no"},
            {"cause": "fall", "deals_damage": "no", "on_damage": {"event": "landed"}},
        ]
    }


def test_entity_timer_time_or_choices():
    import pytest

    from anvil.api.actors.components import EntityTimer, TimeChoice

    timer = EntityTimer(time_down_event="ring", time=(1, 3), looping=False)
    assert payload(timer) == {
        "time_down_event": {"event": "ring", "target": "self"},
        "looping": False,
        "time": {"min": 1, "max": 3},
    }
    with pytest.raises(ValueError):
        payload(
            EntityTimer(
                time_down_event="ring",
                time=2,
                random_time_choices=[TimeChoice(value=1, weight=2)],
            )
        )


def test_entity_shooter_writes_def():
    from anvil.api.actors.components import EntityShooter

    shooter = EntityShooter(def_="minecraft:arrow", aux_val=26).add_projectile(
        def_="minecraft:splash_potion", lose_target=True
    )
    assert payload(shooter) == {
        "def": "minecraft:arrow",
        "aux_val": 26,
        "projectiles": [{"def": "minecraft:splash_potion", "lose_target": True}],
    }


def test_entity_npc_data():
    import pytest

    from anvil.api.actors.components import EntityNPC, NPCData, NPCOffsets

    offsets = NPCOffsets(translate=(0, 1, 0), scale=(1, 1, 1))
    expected = {
        "npc_data": {
            "skin_list": [{"variant": 0}, {"variant": 1}],
            "portrait_offsets": {"translate": [0, 1, 0], "scale": [1, 1, 1]},
        }
    }
    built = EntityNPC().set_npc_data(skin_list=[0, 1], portrait_offsets=offsets)
    assert payload(built) == expected
    constructed = EntityNPC(
        npc_data=NPCData(skin_list=[0, 1], portrait_offsets=offsets)
    )
    assert payload(constructed) == expected
    with pytest.raises(ValueError):
        payload(EntityNPC())


def test_entity_inside_block_notifier_block_object():
    from anvil.api.actors.components import EntityInsideBlockNotifier

    notifier = EntityInsideBlockNotifier().add_block(
        block="minecraft:bubble_column", entered_block_event="in"
    )
    assert payload(notifier) == {
        "block_list": [
            {
                "block": {"name": "minecraft:bubble_column"},
                "entered_block_event": {"event": "in", "target": "self"},
            }
        ]
    }


def test_entity_spell_effects_names():
    from anvil.api.actors.components import EntitySpellEffects
    from anvil.api.vanilla.effects import MinecraftEffects

    spell = EntitySpellEffects(remove_effects=[MinecraftEffects.Poison]).add_effect(
        effect=MinecraftEffects.Regeneration, duration=5
    )
    assert payload(spell) == {
        "add_effects": [{"effect": "regeneration", "duration": 5}],
        "remove_effects": ["poison"],
    }


def test_entity_tameable_items():
    from anvil.api.actors.components import EntityTameable, TameItem

    tameable = EntityTameable(probability=0.5).add_tame_items(
        "minecraft:bone", TameItem(item="minecraft:fish", result_item="minecraft:bowl")
    )
    assert payload(tameable) == {
        "tame_items": [
            "minecraft:bone",
            {"item": "minecraft:fish", "result_item": "minecraft:bowl"},
        ],
        "probability": 0.5,
    }


def test_entity_spawn_on_death_range():
    from anvil.api.actors.components import EntitySpawnOnDeath

    assert payload(EntitySpawnOnDeath(additional_spawn_range=(1, 2))) == {
        "additional_spawn_range": {"min": 1, "max": 2}
    }


def test_entity_rideable_seats():
    from anvil.api.actors.components import EntityRideable

    rideable = EntityRideable(family_types=["player"], seat_count=2).add_seat(
        position=(0, 1, 0), max_rider_count=2, lock_rider_rotation=90
    )
    assert payload(rideable) == {
        "family_types": ["player"],
        "seat_count": 2,
        "seats": [
            {"position": [0, 1, 0], "max_rider_count": 2, "lock_rider_rotation": 90}
        ],
        "rider_can_interact": False,
    }
    with pytest.raises(ValueError):
        payload(
            EntityRideable().add_seat(
                position=(0, 0, 0), max_rider_count=1, third_person_camera_radius=0.5
            )
        )


def test_entity_breedable_and_offspring():
    from anvil.api.actors.components import (
        EntityBreedable,
        EntityHealth,
        EntityOffspring,
    )
    from anvil.lib.config import CONFIG

    breedable = (
        EntityBreedable(breed_items=["minecraft:wheat"], require_tame=False)
        .add_breeds_with(mate_type="minecraft:cow")
        .add_environment_requirement(block_types=["minecraft:water"], count=1, radius=4)
    )
    assert payload(breedable) == {
        "breed_items": ["minecraft:wheat"],
        "breeds_with": {"minecraft:cow": {}},
        "environment_requirements": [
            {"block_types": ["minecraft:water"], "count": 1, "radius": 4}
        ],
        "require_tame": False,
    }
    offspring = EntityOffspring(
        offspring_pairs=[("minecraft:cow", "minecraft:cow")],
        parent_centric_attribute_blending=[EntityHealth],
        property_inheritance=["minecraft:has_nectar", "size"],
        random_variant_mutation_interval=(0, 3),
    ).add_mutation_factor(variant=0.2)
    exported = AnvilIO._normalize_json_like(offspring.__json__())
    assert exported["minecraft:offspring"] == {
        "mutation_factor": [{"variant": 0.2}],
        "offspring_pairs": {"minecraft:cow": "minecraft:cow"},
        "parent_centric_attribute_blending": ["minecraft:health"],
        "property_inheritance": ["minecraft:has_nectar", f"{CONFIG.NAMESPACE}:size"],
        "random_variant_mutation_interval": {"range_min": 0, "range_max": 3},
    }


def test_entity_transformation():
    from anvil.api.actors.components import EntityTransformation, TransformationDelay

    transformation = EntityTransformation(
        into="minecraft:zombie<minecraft:entity_spawned>",
        delay=TransformationDelay(value=10, block_types=["minecraft:iron_bars"]),
    ).add_component_groups("converted")
    assert payload(transformation) == {
        "into": "minecraft:zombie<minecraft:entity_spawned>",
        "add": {"component_groups": ["converted"]},
        "delay": {"value": 10, "block_types": ["minecraft:iron_bars"]},
    }
    assert payload(EntityTransformation(into="minecraft:zombie", delay=5)) == {
        "into": "minecraft:zombie",
        "delay": {"value": 5},
    }
    assert payload(
        EntityTransformation(
            into="minecraft:zombie",
            begin_transform_sound=["unfect"],
            transformation_sound=["remedy"],
        )
    ) == {
        "into": "minecraft:zombie",
        "begin_transform_sound": ["unfect"],
        "transformation_sound": ["remedy"],
    }
    with pytest.raises(ValueError):
        payload(
            EntityTransformation(into="minecraft:zombie").set_delay(block_radius=-1)
        )
    with pytest.raises(ValueError):
        payload(EntityTransformation(into="minecraft:zombie", delay=-1))


def test_entity_interact():
    from anvil.api.actors.components import EntityInteract, RepairEntityItem
    from anvil.api.core.components import EventTrigger
    from anvil.lib.jsonmodel.enums import Slots

    interact = EntityInteract().add_interaction(
        on_interact=EventTrigger(event="fed", target=FilterSubject.Self),
        add_items="loot_tables/a.json",
        repair_entity_item=RepairEntityItem(slot=Slots.Mainhand, amount=5),
        spawn_items="loot_tables/b.json",
        swing=False,
    )
    assert AnvilIO._normalize_json_like(payload(interact)) == {
        "interactions": [
            {
                "add_items": {"table": "loot_tables/a.json"},
                "on_interact": {"event": "fed", "target": "self"},
                "repair_entity_item": {"slot": "slot.weapon.mainhand", "amount": 5},
                "spawn_items": {"table": "loot_tables/b.json"},
                "swing": False,
            }
        ]
    }


def test_entity_genetics():
    from anvil.api.actors.components import EntityGenetics, Gene

    gene = Gene(name="variant", allele_range=(0, 3)).add_genetic_variant(
        main_allele=1, birth_event="set_variant_1"
    )
    genetics = EntityGenetics(genes=[gene], mutation_rate=0.1)
    assert payload(genetics) == {
        "genes": [
            {
                "name": "variant",
                "allele_range": {"range_min": 0, "range_max": 3},
                "genetic_variants": [
                    {
                        "birth_event": {"event": "set_variant_1", "target": "self"},
                        "main_allele": 1,
                    }
                ],
            }
        ],
        "mutation_rate": 0.1,
    }
    with pytest.raises(ValueError):
        payload(Gene(name="a", allele_range=1).add_genetic_variant(birth_event="e"))


def test_entity_despawn_distance():
    from anvil.api.actors.components import EntityDespawn

    assert payload(EntityDespawn(despawn_from_distance=(32, 128))) == {
        "despawn_from_distance": {"min_distance": 32, "max_distance": 128}
    }
    with pytest.raises(ValueError):
        payload(EntityDespawn(despawn_from_distance=(128, 32)))


def test_entity_movement_and_navigation():
    from anvil.api.actors.components import (
        EntityMovementDolphin,
        EntityMovementJump,
        EntityNavigationWalk,
    )

    assert payload(EntityMovementJump(jump_delay=(0.5, 1.5), max_turn=20)) == {
        "max_turn": 20,
        "jump_delay": {"min": 0.5, "max": 1.5},
    }
    assert EntityMovementDolphin().__json__() == {"minecraft:movement.dolphin": {}}
    assert payload(
        EntityNavigationWalk(can_open_doors=True, blocks_to_avoid=["minecraft:magma"])
    ) == {"blocks_to_avoid": ["minecraft:magma"], "can_open_doors": True}


def test_entity_ageable_feed_items():
    from anvil.api.actors.components import EntityAgeable

    ageable = (
        EntityAgeable(duration=1200, grow_up="grow_up")
        .add_feed_item(item="minecraft:wheat")
        .add_feed_item(item="minecraft:carrot", growth=0.1)
    )
    assert payload(ageable) == {
        "duration": 1200,
        "feed_items": ["minecraft:wheat", {"item": "minecraft:carrot", "growth": 0.1}],
        "grow_up": {"event": "grow_up", "target": "self"},
    }


def test_entity_spawn_entity():
    from anvil.api.actors.components import EntitySpawnEntity

    spawn = EntitySpawnEntity().add_entity(
        spawn_item="minecraft:egg", min_wait_time=300, max_wait_time=600
    )
    assert payload(spawn) == {
        "entities": [
            {"spawn_item": "minecraft:egg", "max_wait_time": 600, "min_wait_time": 300}
        ]
    }


def test_reflect_projectiles_needs_experimental(monkeypatch):
    from anvil.beta.actors.components import EntityReflectProjectiles
    from anvil.lib.config import CONFIG

    component = EntityReflectProjectiles(
        azimuth_angle="math.random(-10, 10)",
        reflected_projectiles=["minecraft:arrow"],
        reflection_sound="reflect",
    )
    monkeypatch.setattr(CONFIG, "_EXPERIMENTAL", False, raising=False)
    with pytest.raises(ValueError, match="experimental"):
        AnvilIO._normalize_json_like(component)
    monkeypatch.setattr(CONFIG, "_EXPERIMENTAL", True, raising=False)
    assert AnvilIO._normalize_json_like(component) == {
        "minecraft:reflect_projectiles": {
            "azimuth_angle": "math.random(-10, 10)",
            "reflected_projectiles": ["minecraft:arrow"],
            "reflection_sound": "reflect",
        }
    }


def test_filter_has_component_takes_component_classes():
    from anvil.api.actors.components import EntityHealth
    from anvil.api.core.filters import Filter

    for value in (EntityHealth, EntityHealth(value=10), "minecraft:health"):
        assert (
            Filter.has_component(value).__export_dict__()["value"] == "minecraft:health"
        )


def test_entity_sensor_subsensor_event_is_a_name():
    from anvil.api.actors.components import EntitySensor

    sensor = EntitySensor().add_subsensor(event="stark:seen", range=(2, 2))
    assert str(sensor.__json__()).count("'event': 'stark:seen'") == 1


def test_part_builders_match_constructor_parts():
    from anvil.api.actors.components import (
        BandwidthValues,
        DenyParentsVariant,
        EntityBreedable,
        EntityConditionalBandwidthOptimization,
        EntityJumpDynamic,
        EntityProjectile,
        EntityTimer,
        EntityTransformation,
        JumpData,
        MutationFactor,
        ProjectileImpactDamage,
        ProjectileOnHit,
        TimeChoice,
        TransformationDelay,
    )

    pairs = [
        (
            EntityConditionalBandwidthOptimization().set_default_values(
                max_dropped_ticks=4
            ),
            EntityConditionalBandwidthOptimization(
                default_values=BandwidthValues(max_dropped_ticks=4)
            ),
        ),
        (
            EntityBreedable()
            .set_deny_parents_variant(chance=0.5, min_variant=0, max_variant=2)
            .set_mutation_factor(variant=0.1),
            EntityBreedable(
                deny_parents_variant=DenyParentsVariant(
                    chance=0.5, min_variant=0, max_variant=2
                ),
                mutation_factor=MutationFactor(variant=0.1),
            ),
        ),
        (
            EntityJumpDynamic()
            .set_regular_skip_data(height=0.3)
            .set_fast_skip_data(jump_delay=10),
            EntityJumpDynamic(
                regular_skip_data=JumpData(height=0.3),
                fast_skip_data=JumpData(jump_delay=10),
            ),
        ),
        (
            EntityProjectile().set_on_hit(
                impact_damage=ProjectileImpactDamage(filter="minecraft:arrow"),
                remove_on_hit=True,
            ),
            EntityProjectile(
                on_hit=ProjectileOnHit(
                    impact_damage=ProjectileImpactDamage(filter="minecraft:arrow"),
                    remove_on_hit=True,
                )
            ),
        ),
        (
            EntityTransformation(into="minecraft:cow").set_delay(
                value=2, block_chance=0.5
            ),
            EntityTransformation(
                into="minecraft:cow",
                delay=TransformationDelay(value=2, block_chance=0.5),
            ),
        ),
        (
            EntityTimer(time_down_event="ring")
            .add_random_time_choice(value=1, weight=2)
            .add_random_time_choice(value=3),
            EntityTimer(
                time_down_event="ring",
                random_time_choices=[
                    TimeChoice(value=1, weight=2),
                    TimeChoice(value=3),
                ],
            ),
        ),
    ]
    for built, constructed in pairs:
        assert payload(built) == payload(constructed)


def test_strict_float_ranges_write_objects():
    from anvil.api.actors.components import EntityMovementJump, EntityTimer

    assert payload(EntityTimer(time_down_event="ring", time=3.5))["time"] == {
        "min": 3.5,
        "max": 3.5,
    }
    assert payload(EntityMovementJump(jump_delay=0.1))["jump_delay"] == {
        "min": 0.1,
        "max": 0.1,
    }


def test_economy_trade_table_cured_discounts_are_objects():
    from anvil.api.actors.components import EntityEconomyTradeTable

    table = EntityEconomyTradeTable(
        table="trading/test.json",
        cured_discount=(-20, -25),
        max_cured_discount=(-25, -20),
    )
    body = payload(table)
    assert body["cured_discount"] == {"min": -25, "max": -20}
    assert body["max_cured_discount"] == {"min": -25, "max": -20}


def test_entity_trail_radius_range():
    from anvil.api.actors.components import EntityTrail

    trail = EntityTrail(
        block_type="minecraft:snow_layer",
        radius=2,
        replaceable_blocks=["minecraft:air", "minecraft:short_grass"],
        force_replace_matched_blocks=True,
    )
    assert payload(trail) == {
        "block_type": "minecraft:snow_layer",
        "force_replace_matched_blocks": True,
        "radius": 2,
        "replaceable_blocks": ["minecraft:air", "minecraft:short_grass"],
    }
    with pytest.raises(ValueError):
        payload(EntityTrail(radius=17))
    with pytest.raises(ValueError):
        payload(EntityTrail(radius=-2))
