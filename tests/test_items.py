import orjson

import pytest
from anvil.api.core.enums import DamageCause, Slots
from anvil.api.items.components import (
    ItemAllowOffHand,
    ItemBlockPlacer,
    ItemBundleInteraction,
    ItemCooldown,
    ItemCustomComponent,
    ItemDamage,
    ItemDamageAbsorption,
    ItemDigger,
    ItemDisplayName,
    ItemDurability,
    ItemDurabilitySensor,
    ItemDyeable,
    ItemFireResistant,
    ItemFood,
    ItemFuel,
    ItemGlint,
    ItemInteractButton,
    ItemKineticWeapon,
    ItemMaxStackSize,
    ItemPiercingWeapon,
    ItemRarity,
    ItemRepairable,
    ItemShooter,
    ItemStorageItem,
    ItemSwingDuration,
    ItemUseAnimation,
    ItemUseModifiers,
    ItemWearable,
)
from anvil.lib.jsonmodel import json_field
from anvil.lib.lib import AnvilIO
from anvil.lib.schemas import MinecraftBlockDescriptor
from anvil.api.vanilla.factories.minecraft_items import SulfurSpike, MusicDiscBounce
from anvil.api.vanilla.items import MinecraftItemTags


def test_new_items():
    spike = SulfurSpike()
    assert spike.identifier == "minecraft:sulfur_spike"

    disc = MusicDiscBounce()
    assert disc.identifier == "minecraft:music_disc_bounce"


def test_promoted_tags():
    assert (
        MinecraftItemTags.SulfurCubeArchetypeBouncy
        == "minecraft:sulfur_cube_archetype_bouncy"
    )
    assert (
        MinecraftItemTags.SulfurCubeArchetypeRegular
        == "minecraft:sulfur_cube_archetype_regular"
    )
    assert (
        MinecraftItemTags.SulfurCubeArchetypeSticky
        == "minecraft:sulfur_cube_archetype_sticky"
    )


@pytest.fixture(autouse=True)
def anvil_project(tmp_path, monkeypatch):
    """Descriptors and localization read the project config, so run each test in a minimal project."""
    (tmp_path / "anvilconfig.json").write_bytes(
        orjson.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    import anvil.lib.config as config

    config.use(None)


def _export(component):
    return AnvilIO._normalize_json_like(component)


def test_bare_value_components():
    assert _export(ItemMaxStackSize(value=16)) == {"minecraft:max_stack_size": 16}
    assert _export(ItemGlint()) == {"minecraft:glint": True}
    assert _export(ItemAllowOffHand(value=False)) == {"minecraft:allow_off_hand": False}
    assert _export(ItemDamage(value=5)) == {"minecraft:damage": 5}
    assert _export(ItemRarity(value="rare")) == {"minecraft:rarity": "rare"}
    assert _export(ItemUseAnimation(value="drink")) == {
        "minecraft:use_animation": "drink"
    }


def test_object_value_components():
    assert _export(ItemFireResistant()) == {"minecraft:fire_resistant": {"value": True}}
    assert _export(ItemSwingDuration(value=0.5)) == {
        "minecraft:swing_duration": {"value": 0.5}
    }
    assert _export(ItemSwingDuration()) == {"minecraft:swing_duration": {}}


def test_unset_options_are_left_out():
    assert _export(ItemFuel(duration=15)) == {"minecraft:fuel": {"duration": 15}}
    assert _export(ItemFood()) == {"minecraft:food": {}}
    assert _export(ItemBlockPlacer(block="test:block")) == {
        "minecraft:block_placer": {"block": "test:block"}
    }
    assert _export(ItemCooldown(category="attack", duration=0.2)) == {
        "minecraft:cooldown": {"category": "attack", "duration": 0.2}
    }


def test_use_modifiers_start_using():
    assert _export(ItemUseModifiers(use_duration=2.0, start_using="if_first")) == {
        "minecraft:use_modifiers": {"use_duration": 2.0, "start_using": "if_first"}
    }
    with pytest.raises(ValueError):
        _export(ItemUseModifiers(use_duration=2.0, start_using="sometimes"))
    with pytest.raises(ValueError):
        _export(ItemUseModifiers(use_duration=2.0, movement_modifier=1.5))


def test_ranges_are_written_as_min_max():
    assert _export(ItemDurability(max_durability=36, damage_chance=(10, 50))) == {
        "minecraft:durability": {
            "max_durability": 36,
            "damage_chance": {"min": 10, "max": 50},
        }
    }
    assert _export(ItemPiercingWeapon(reach=(0, 4.5))) == {
        "minecraft:piercing_weapon": {"reach": {"min": 0, "max": 4.5}}
    }
    with pytest.raises(ValueError):
        _export(ItemDurability(max_durability=36, damage_chance=(10, 150)))


def test_kinetic_weapon_conditions_are_written():
    weapon = (
        ItemKineticWeapon(delay=5)
        .set_damage_conditions(max_duration=20, min_speed=0.5)
        .set_knockback_conditions(min_relative_speed=1.0)
    )
    assert _export(weapon) == {
        "minecraft:kinetic_weapon": {
            "delay": 5,
            "damage_conditions": {"max_duration": 20, "min_speed": 0.5},
            "knockback_conditions": {"min_relative_speed": 1.0},
        }
    }
    assert ItemUseModifiers in type(weapon)._requires


def test_list_builders():
    digger = (
        ItemDigger(use_efficiency=True)
        .add_destroy_speed(
            block=MinecraftBlockDescriptor(tags="query.any_tag('wood')"), speed=6
        )
        .add_destroy_speed(block="minecraft:coal_ore", speed=2)
    )
    assert _export(digger) == {
        "minecraft:digger": {
            "destroy_speeds": [
                {"block": {"tags": "query.any_tag('wood')"}, "speed": 6},
                {"block": "minecraft:coal_ore", "speed": 2},
            ],
            "use_efficiency": True,
        }
    }

    shooter = ItemShooter(charge_on_draw=True).add_ammunition(
        item="minecraft:arrow", use_offhand=True
    )
    assert _export(shooter) == {
        "minecraft:shooter": {
            "ammunition": [{"item": "minecraft:arrow", "use_offhand": True}],
            "charge_on_draw": True,
        }
    }

    repairable = ItemRepairable(on_repaired="minecraft:celebrate").add_repair_item(
        items=["minecraft:diamond"], repair_amount=25
    )
    assert _export(repairable) == {
        "minecraft:repairable": {
            "repair_items": [{"items": ["minecraft:diamond"], "repair_amount": 25}],
            "on_repaired": "minecraft:celebrate",
        }
    }


def test_durability_sensor_needs_a_threshold():
    sensor = ItemDurabilitySensor()
    with pytest.raises(ValueError):
        _export(sensor)
    sensor.add_durability_threshold(durability=10, sound_event="random.break")
    assert _export(sensor) == {
        "minecraft:durability_sensor": {
            "durability_thresholds": [{"durability": 10, "sound_event": "random.break"}]
        }
    }
    assert ItemDurability in type(sensor)._requires


def test_component_checks_run_on_export():
    with pytest.raises(ValueError):
        _export(ItemMaxStackSize(value=65))
    with pytest.raises(ValueError):
        _export(ItemDamageAbsorption(absorbable_causes=[]))
    with pytest.raises(ValueError):
        _export(ItemWearable(slot=Slots.Hotbar))
    with pytest.raises(TypeError):
        _export(ItemGlint(value="yes"))
    assert _export(ItemDamageAbsorption(absorbable_causes=[DamageCause.Fall])) == {
        "minecraft:damage_absorption": {"absorbable_causes": ["fall"]}
    }


def test_dependencies():
    assert set(ItemBundleInteraction._requires) == {
        ItemStorageItem,
        ItemMaxStackSize,
    }
    assert ItemUseModifiers in ItemFood._requires


def test_fields_are_read_only():
    stack = ItemMaxStackSize(value=16)
    with pytest.raises(AttributeError):
        stack.value = 32
    with pytest.raises(TypeError):
        ItemMaxStackSize(16)


def test_dyeable_writes_hex():
    assert _export(ItemDyeable(default_color=(255, 0, 0))) == {
        "minecraft:dyeable": {"default_color": "#ff0000"}
    }


def test_display_name_keeps_the_text():
    assert _export(ItemDisplayName(value="Oak Boat")) == {
        "minecraft:display_name": {"value": "Oak Boat"}
    }


def test_interact_button_text_is_localized():
    assert _export(ItemInteractButton()) == {"minecraft:interact_button": True}
    key = _export(ItemInteractButton(value="Read Book"))["minecraft:interact_button"]
    assert key.startswith("key.") and key.endswith(".read_book")


def test_custom_component():
    class Explosive(ItemCustomComponent):
        identifier = "test:explosive"

        power: float = json_field()
        fuse: int = json_field(default=40, omit_default=True)

    assert _export(Explosive(power=2.5)) == {"test:explosive": {"power": 2.5}}
    with pytest.raises(TypeError):
        ItemCustomComponent()
