import re

from anvil.lib.jsonmodel import Identifier

_NAMES: dict[str, str] = {
    "VillagerV2": "minecraft:villager_v2",
    "ZombieVillagerV2": "minecraft:zombie_villager_v2",
}


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
    from anvil.api.vanilla.entities import vanilla_entity_ids

    identifier = _NAMES.get(name, f"minecraft:{_to_snake(name)}")
    if name.startswith("_") or identifier not in vanilla_entity_ids():
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    func = _make_factory(name)
    globals()[name] = func
    return func
