import re
from typing import Literal

from anvil.lib.schemas import MinecraftItemDescriptor


def Potion(
    potion_addition: (
        Literal[
            "water",
            "awkward",
            "mundane",
            "thick",
            "healing",
            "regeneration",
            "swiftness",
            "strength",
            "harming",
            "poison",
            "slowness",
            "weakness",
            "water_breathing",
            "fire_resistance",
            "nightvision",
            "invisibility",
            "leaping",
            "slow_falling",
            "turtle_master",
            "wither",
            "strong_healing",
            "strong_harming",
            "long_leaping",
            "strong_leaping",
            "long_nightvision",
            "long_poison",
            "strong_poison",
            "long_regeneration",
            "strong_regeneration",
            "long_slowness",
            "strong_slowness",
            "long_strength",
            "strong_strength",
            "long_swiftness",
            "strong_swiftness",
            "long_turtle_master",
            "strong_turtle_master",
            "long_water_breathing",
            "long_fire_resistance",
            "long_invisibility",
            "long_slow_falling",
            "long_weakness",
            "strong_wither",
        ]
        | None
    ) = None,
) -> MinecraftItemDescriptor:
    if potion_addition is not None:
        return MinecraftItemDescriptor("minecraft:potion_type").set_identifier_data(
            potion_addition
        )
    return MinecraftItemDescriptor("minecraft:potion")


def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", s)
    return s.lower()


def _make_item_factory(name: str):
    ident = f"minecraft:{_to_snake(name)}"

    def factory() -> MinecraftItemDescriptor:
        return MinecraftItemDescriptor(ident)

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {name}"
    return factory


def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    func = _make_item_factory(name)
    globals()[name] = func
    return func
