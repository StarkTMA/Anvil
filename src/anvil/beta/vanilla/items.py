from enum import StrEnum

from .factories import minecraft_items as MinecraftItemTypes

__all__ = ["MinecraftItemTypes", "MinecraftItemTags", "vanilla_items_ids"]


def vanilla_items_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:calcite_pillar",
        "minecraft:calcite_slab",
        "minecraft:calcite_stairs",
        "minecraft:calcite_wall",
        "minecraft:chiseled_packed_ice",
        "minecraft:frostbite_spawn_egg",
        "minecraft:ice_ball",
        "minecraft:ice_crystal",
        "minecraft:icicle",
        "minecraft:music_disc_flurry",
        "minecraft:packed_ice_brick_slab",
        "minecraft:packed_ice_brick_stairs",
        "minecraft:packed_ice_brick_wall",
        "minecraft:packed_ice_bricks",
        "minecraft:polished_calcite",
        "minecraft:polished_calcite_brick_slab",
        "minecraft:polished_calcite_brick_stairs",
        "minecraft:polished_calcite_brick_wall",
        "minecraft:polished_calcite_bricks",
        "minecraft:polished_calcite_slab",
        "minecraft:polished_calcite_stairs",
        "minecraft:polished_calcite_wall",
        "minecraft:snow_brick_slab",
        "minecraft:snow_brick_stairs",
        "minecraft:snow_brick_wall",
        "minecraft:snow_bricks",
    ]


class MinecraftItemTags(StrEnum):
    """Experimental vanilla item tags."""

    SulfurCubeArchetypeSlowBouncy = "minecraft:sulfur_cube_archetype_slow_bouncy"
    SulfurCubeArchetypeHot = "minecraft:sulfur_cube_archetype_hot"
    SulfurCubeArchetypeCold = "minecraft:sulfur_cube_archetype_cold"
