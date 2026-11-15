from .factories import minecraft_blocks as MinecraftBlockTypes

__all__ = ["MinecraftBlockTypes", "vanilla_block_ids"]


def vanilla_block_ids() -> list[str]:
    return [
        "minecraft:disc_press",
        "minecraft:ice_crystal",
        "minecraft:icicle",
    ]
