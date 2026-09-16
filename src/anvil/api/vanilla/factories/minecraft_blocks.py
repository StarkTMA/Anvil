import re
from typing import Any, Mapping

from anvil.lib.schemas import MinecraftBlockDescriptor

_PARAM_KEY_MAP: dict[str, str] = {
    "minecraft_vertical_half": "minecraft:vertical_half",
    "minecraft_cardinal_direction": "minecraft:cardinal_direction",
    "cardinal_direction": "minecraft:cardinal_direction",
    "minecraft_block_face": "minecraft:block_face",
    "minecraft_connection_down": "minecraft:connection_down",
    "minecraft_connection_east": "minecraft:connection_east",
    "minecraft_connection_north": "minecraft:connection_north",
    "minecraft_connection_south": "minecraft:connection_south",
    "minecraft_connection_up": "minecraft:connection_up",
    "minecraft_connection_west": "minecraft:connection_west",
    "minecraft_corner": "minecraft:corner",
    "corner": "minecraft:corner",
    "minecraft_multi_block_part": "minecraft:multi_block_part",
    "minecraft_sixteen_way_rotation": "minecraft:sixteen_way_rotation",
    "sixteen_way_rotation": "minecraft:sixteen_way_rotation",
}


def _create_block(
    identifier: str, states: Mapping[str, Any] | None = None
) -> MinecraftBlockDescriptor:
    if not states:
        return MinecraftBlockDescriptor(identifier, True)

    clean_states = {}
    for k, v in states.items():
        if v is not None:
            if identifier == "minecraft:observer" and k == "facing_direction":
                clean_states["minecraft:facing_direction"] = v
            else:
                clean_states[_PARAM_KEY_MAP.get(k, k)] = v

    return MinecraftBlockDescriptor(
        identifier, True, clean_states if clean_states else None
    )


def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", s)
    return s.lower()


def _make_block_factory(name: str, identifier: str):
    def factory(**states: Any) -> MinecraftBlockDescriptor:
        return _create_block(identifier, states)

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {name}"
    return factory


def __getattr__(name: str):
    if name.startswith("_"):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    if name.endswith("States"):
        return Any
    func = _make_block_factory(name, f"minecraft:{_to_snake(name)}")
    globals()[name] = func
    return func
