from .factories import minecraft_blocks as MinecraftBlockTypes

__all__ = ["MinecraftBlockTypes", "vanilla_block_ids"]


def vanilla_block_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:chiseled_packed_ice",
        "minecraft:ice_crystal",
        "minecraft:icicle",
        "minecraft:packed_ice_brick_double_slab",
        "minecraft:packed_ice_brick_slab",
        "minecraft:packed_ice_brick_stairs",
        "minecraft:packed_ice_brick_wall",
        "minecraft:packed_ice_bricks",
        "minecraft:snow_brick_double_slab",
        "minecraft:snow_brick_slab",
        "minecraft:snow_brick_stairs",
        "minecraft:snow_brick_wall",
        "minecraft:snow_bricks",
    ]
