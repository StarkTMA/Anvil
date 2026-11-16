from .factories import minecraft_items as MinecraftItemTypes

__all__ = ["MinecraftItemTypes", "vanilla_items_ids"]


def vanilla_items_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:frostbite_spawn_egg",
        "minecraft:ice_ball",
        "minecraft:ice_crystal",
        "minecraft:icicle",
        "minecraft:packed_ice_bricks",
        "minecraft:packed_ice_bricks_chiseled",
        "minecraft:packed_ice_bricks_slab",
        "minecraft:packed_ice_bricks_stairs",
        "minecraft:packed_ice_bricks_wall",
    ]
