import pytest
from anvil.api.vanilla.factories.minecraft_items import SulfurSpike, MusicDiscBounce
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.api.items.components import ItemUseModifiers


def test_new_items():
    # Verify new item descriptors
    spike = SulfurSpike()
    assert spike.identifier == "minecraft:sulfur_spike"

    disc = MusicDiscBounce()
    assert disc.identifier == "minecraft:music_disc_bounce"


def test_promoted_tags():
    # Verify SulfurCubeArchetype tags are promoted and accessible
    assert MinecraftItemTags.SulfurCubeArchetypeBouncy == "minecraft:sulfur_cube_archetype_bouncy"
    assert MinecraftItemTags.SulfurCubeArchetypeRegular == "minecraft:sulfur_cube_archetype_regular"
    assert MinecraftItemTags.SulfurCubeArchetypeSticky == "minecraft:sulfur_cube_archetype_sticky"


def test_use_modifiers_start_using():
    # Verify start_using parameter in ItemUseModifiers
    mod = ItemUseModifiers(use_duration=2.0, start_using="always")
    assert mod._component["start_using"] == "always"
