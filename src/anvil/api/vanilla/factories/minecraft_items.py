import re
from typing import Literal

from anvil.lib.jsonmodel import Identifier


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
) -> Identifier:
    if potion_addition is not None:
        return Identifier.parse(
            "minecraft:potion_type", vanilla=True, data=potion_addition
        )
    return Identifier.parse("minecraft:potion", vanilla=True)


_NAMES: dict[str, str] = {}


def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", s)
    return s.lower()


def _make_factory(name: str):
    identifier = _NAMES.get(name, f"minecraft:{_to_snake(name)}")

    def factory() -> Identifier:
        return Identifier.parse(identifier, vanilla=True)

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {identifier}"
    return factory


def __getattr__(name: str):
    from anvil.api.vanilla.items import vanilla_items_ids

    identifier = _NAMES.get(name, f"minecraft:{_to_snake(name)}")
    if name.startswith("_") or identifier not in vanilla_items_ids():
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    func = _make_factory(name)
    globals()[name] = func
    return func
