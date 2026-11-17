from .factories import minecraft_blocks as MinecraftBlockTypes

__all__ = ["MinecraftBlockTypes", "vanilla_block_ids"]


def vanilla_block_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:calcite_double_slab",
        "minecraft:calcite_pillar",
        "minecraft:calcite_slab",
        "minecraft:calcite_stairs",
        "minecraft:calcite_wall",
        "minecraft:chiseled_packed_ice",
        "minecraft:chiseled_soulshale",
        "minecraft:ice_crystal",
        "minecraft:icicle",
        "minecraft:packed_ice_brick_double_slab",
        "minecraft:packed_ice_brick_slab",
        "minecraft:packed_ice_brick_stairs",
        "minecraft:packed_ice_brick_wall",
        "minecraft:packed_ice_bricks",
        "minecraft:polished_calcite",
        "minecraft:polished_calcite_brick_double_slab",
        "minecraft:polished_calcite_brick_slab",
        "minecraft:polished_calcite_brick_stairs",
        "minecraft:polished_calcite_brick_wall",
        "minecraft:polished_calcite_bricks",
        "minecraft:polished_calcite_double_slab",
        "minecraft:polished_calcite_slab",
        "minecraft:polished_calcite_stairs",
        "minecraft:polished_calcite_wall",
        "minecraft:snow_brick_double_slab",
        "minecraft:snow_brick_slab",
        "minecraft:snow_brick_stairs",
        "minecraft:snow_brick_wall",
        "minecraft:snow_bricks",
    ]
