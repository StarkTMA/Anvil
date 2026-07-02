from anvil.api.vanilla.factories.minecraft_entities import SulfurCube
from anvil.api.vanilla.entities import vanilla_entity_ids


def test_sulfur_cube_entity():
    # Verify entity descriptor
    desc = SulfurCube()
    assert desc.identifier == "minecraft:sulfur_cube"
    assert "minecraft:sulfur_cube" in vanilla_entity_ids()


def test_entity_hide_held_items():
    from anvil.api.actors.actors import Entity
    entity = Entity("custom_entity")
    entity.client.description.hide_held_items(True)
    assert entity.client.description._description["description"]["scripts"]["hide_held_items"] == "1"

    entity.client.description.hide_held_items("q.is_sheared")
    assert entity.client.description._description["description"]["scripts"]["hide_held_items"] == "q.is_sheared"


def test_entity_ai_pickup_items():
    from anvil.api.actors.components import EntityAIPickupItems

    # Test default
    goal = EntityAIPickupItems()
    assert "stop_if_holding_item" not in goal._component

    # Test stop_if_holding_item=True
    goal_true = EntityAIPickupItems(stop_if_holding_item=True)
    assert goal_true._component["stop_if_holding_item"] is True


def test_execute_event_on_home_block():
    from anvil.api.actors.actors import Entity

    # 1. Test Base Event
    entity = Entity("custom_entity")
    event = entity.server.event("minecraft:entity_spawned")
    event.execute_event_on_home_block("my_block_event")

    exported = event.__export__()
    assert exported["minecraft:entity_spawned"]["execute_event_on_home_block"] == {"event": "my_block_event"}

    # 2. Test Sequence Event
    entity2 = Entity("custom_entity2")
    event2 = entity2.server.event("minecraft:entity_born")
    seq = event2.sequence
    seq.execute_event_on_home_block("my_born_seq_event")

    # 3. Test fixed play_sound and emit_particle in Sequence
    seq.play_sound("ambient.weather.thunder")
    seq.emit_particle("minecraft:basic_flame_particle")

    exported2 = event2.__export__()
    assert exported2["minecraft:entity_born"]["sequence"][0]["execute_event_on_home_block"] == {"event": "my_born_seq_event"}
    assert exported2["minecraft:entity_born"]["sequence"][0]["play_sound"] == {"sound": "ambient.weather.thunder"}
    assert exported2["minecraft:entity_born"]["sequence"][0]["emit_particle"] == {"particle": "minecraft:basic_flame_particle"}

    # 4. Test Randomize Event
    entity3 = Entity("custom_entity3")
    event3 = entity3.server.event("minecraft:on_prime")
    rand = event3.randomize
    rand.execute_event_on_home_block("my_prime_rand_event")

    # 5. Test fixed play_sound and emit_particle in Randomize
    rand.play_sound("ambient.weather.thunder")
    rand.emit_particle("minecraft:basic_flame_particle")

    exported3 = event3.__export__()
    assert exported3["minecraft:on_prime"]["randomize"][0]["execute_event_on_home_block"] == {"event": "my_prime_rand_event"}
    assert exported3["minecraft:on_prime"]["randomize"][0]["play_sound"] == {"sound": "ambient.weather.thunder"}
    assert exported3["minecraft:on_prime"]["randomize"][0]["emit_particle"] == {"particle": "minecraft:basic_flame_particle"}


def test_entity_bounciness():
    from anvil.api.actors.components import EntityBounciness
    bounciness = EntityBounciness(0.5)
    assert bounciness._component["strength"] == 0.5


def test_entity_air_drag_modifier():
    from anvil.api.actors.components import EntityAirDragModifier
    air_drag = EntityAirDragModifier(0.8)
    assert air_drag._component["strength"] == 0.8


def test_entity_apply_knockback_rules():
    from anvil.api.actors.components import EntityApplyKnockbackRules
    rules = EntityApplyKnockbackRules()
    rules.add_preset(extra_knockback_approach="multiply")
    assert rules._component["presets"][0]["extra_knockback_approach"] == "multiply"


def test_entity_pushable_by_entity():
    from anvil.api.actors.components import EntityPushableByEntity
    push = EntityPushableByEntity()
    push.add_preset(
        push_mode="none",
        strength_multiplier=1.5,
        min_distance=2.0,
        max_distance=5.0,
        push_scale_self=0.5,
        push_scale_other=0.8,
        play_sound_cooldown_in_seconds=3.0,
        play_sound_impulse_threshold=0.1,
        play_sound=False,
    )
    assert push._component["presets"][0]["push_mode"] == "none"
    assert push._component["presets"][0]["strength_multiplier"] == 1.5
    assert push._component["presets"][0]["min_distance"] == 2.0
    assert push._component["presets"][0]["max_distance"] == 5.0
    assert push._component["presets"][0]["push_scale_self"] == 0.5
    assert push._component["presets"][0]["push_scale_other"] == 0.8
    assert push._component["presets"][0]["play_sound_cooldown_in_seconds"] == 3.0
    assert push._component["presets"][0]["play_sound_impulse_threshold"] == 0.1
    assert push._component["presets"][0]["play_sound"] is False


def test_entity_area_attack():
    from anvil.api.actors.components import EntityAreaAttack
    from anvil.api.core.enums import DamageCause
    aa = EntityAreaAttack(cause=DamageCause.Magic, use_self_as_damage_source=False)
    assert aa._component["use_self_as_damage_source"] is False


def test_entity_leashable():
    from anvil.api.actors.components import EntityLeashable, EntityLeashableTo
    leash = EntityLeashable(unleash_on_removal=True)
    assert leash._component["unleash_on_removal"] is True

    leash_to = EntityLeashableTo(unleash_on_removal=False)
    assert leash_to._component["unleash_on_removal"] is False


def test_entity_unleash_event_response():
    from anvil.api.actors.actors import Entity
    ent = Entity("test_unleash")
    evt = ent.server.event("minecraft:entity_spawned")
    evt.unleash(unleash_self=True, unleash_others=True)
    exported = evt.__export__()
    assert exported["minecraft:entity_spawned"]["unleash"] == {"unleash_self": True, "unleash_others": True}


def test_entity_filter_redstone_strength():
    from anvil.api.core.filters import Filter
    filt = Filter.redstone_strength_at_position(15)
    assert filt.test == "redstone_strength_at_position"
    assert filt.value == 15
