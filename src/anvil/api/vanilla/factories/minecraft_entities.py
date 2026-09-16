import re

from anvil.lib.schemas import MinecraftEntityDescriptor

_PARAM_KEY_MAP: dict[str, str] = {
    "VillagerV2": "minecraft:villager_v2",
    "ZombieVillagerV2": "minecraft:zombie_villager_v2",
}


def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", s)
    return s.lower()


def _make_entity_factory(name: str):
    ident = _PARAM_KEY_MAP.get(name, f"minecraft:{_to_snake(name)}")

    def factory() -> MinecraftEntityDescriptor:
        return MinecraftEntityDescriptor(ident, True)

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {name}"
    return factory


def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    func = _make_entity_factory(name)
    globals()[name] = func
    return func
