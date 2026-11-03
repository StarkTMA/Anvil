import pytest

from anvil.lib import config
from anvil.lib.config import ConfigPackageTarget


@pytest.fixture(autouse=True)
def world_project():
    with config.override(_TARGET=ConfigPackageTarget.WORLD):
        yield


def test_vanilla_entity_files_keep_the_vanilla_identifier():
    from anvil.api.actors.entity import Entity

    entity = Entity("minecraft:zombie", is_vanilla=True)
    server = entity.server
    for file in (
        server,
        server._animation_controllers,
        server._animations,
        server._spawn_rule,
        entity.client,
    ):
        assert file.identifier == "minecraft:zombie"
        assert file.identifier.is_vanilla


@pytest.mark.parametrize(
    "module, cls",
    [
        ("anvil.api.items.items", "Item"),
        ("anvil.api.blocks.blocks", "Block"),
        ("anvil.api.biomes.biomes", "Biome"),
    ],
)
def test_vanilla_objects_keep_the_vanilla_identifier(module, cls):
    import importlib

    kind = getattr(importlib.import_module(module), cls)
    obj = kind(f"minecraft:{cls.lower()}_x", is_vanilla=True)
    assert obj.server.identifier == f"minecraft:{cls.lower()}_x"
    assert obj.server.identifier.is_vanilla
