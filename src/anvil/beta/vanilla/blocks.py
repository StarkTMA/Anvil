from .factories import minecraft_blocks as MinecraftBlockTypes

__all__ = ["MinecraftBlockTypes", "vanilla_block_ids"]


def vanilla_block_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:ice_crystal",
        "minecraft:icicle",
        "minecraft:packed_ice_bricks",
        "minecraft:packed_ice_bricks_chiseled",
        "minecraft:packed_ice_bricks_double_slab",
        "minecraft:packed_ice_bricks_slab",
        "minecraft:packed_ice_bricks_stairs",
        "minecraft:packed_ice_bricks_wall",
    ]
