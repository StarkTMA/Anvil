from .factories import minecraft_items as MinecraftItemTypes

__all__ = ["MinecraftItemTypes", "vanilla_items_ids"]


def vanilla_items_ids() -> list[str]:
    return [
        "minecraft:frostbite_spawn_egg",
        "minecraft:ice_ball",
        "minecraft:ice_crystal",
        "minecraft:icicle",
    ]
