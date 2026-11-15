from .factories import minecraft_entities as MinecraftEntityTypes

__all__ = ["MinecraftEntityTypes", "vanilla_entities_ids"]


def vanilla_entities_ids() -> list[str]:
    return [
        "minecraft:frostbite",
        "minecraft:ice_ball",
    ]
