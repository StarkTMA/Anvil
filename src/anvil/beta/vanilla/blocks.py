from .factories import minecraft_blocks as MinecraftBlockTypes

__all__ = ["MinecraftBlockTypes", "vanilla_block_ids"]


def vanilla_block_ids() -> list[str]:
    return [
        "minecraft:brittle_ice",
        "minecraft:disc_press",  # Needs a free addon?
        "minecraft:ice_crystal",
        "minecraft:icicle",
    ]
