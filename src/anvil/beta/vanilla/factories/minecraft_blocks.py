import re
from typing import Any

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.jsonmodel import Identifier

_STATE_KEYS: dict[str, str] = {
    "minecraft_cardinal_direction": "minecraft:cardinal_direction",
    "minecraft_block_face": "minecraft:block_face",
}


def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    s = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", s)
    return s.lower()


def _make_factory(name: str):
    identifier = f"minecraft:{_to_snake(name)}"

    def factory(**states: Any) -> Identifier | BlockDescriptor:
        states = {_STATE_KEYS.get(k, k): v for k, v in states.items() if v is not None}
        name = Identifier.parse(identifier, vanilla=True)
        if states:
            return BlockDescriptor(name=name, states=states)
        return name

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {identifier}"
    return factory


def __getattr__(name: str):
    from anvil.beta.vanilla.blocks import vanilla_block_ids

    if (
        name.startswith("_")
        or f"minecraft:{_to_snake(name)}" not in vanilla_block_ids()
    ):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    func = _make_factory(name)
    globals()[name] = func
    return func
