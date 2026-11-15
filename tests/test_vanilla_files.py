import pytest

from anvil.lib import config
from anvil.lib.config import ConfigPackageTarget


@pytest.fixture(autouse=True)
def world_project():
    with config.override(_TARGET=ConfigPackageTarget.WORLD):
        yield


def test_vanilla_entity_files_keep_the_vanilla_identifier():
    from anvil.api.actors.animation_controllers import BPAnimationControllers
    from anvil.api.actors.animations import BPAnimations
    from anvil.api.actors.entity import Entity

    entity = Entity("minecraft:zombie", is_vanilla=True)
    server = entity.server
    for file in (
        server,
        BPAnimationControllers(server.description),
        BPAnimations(server.description),
        server._spawn_rule,
        entity.client,
    ):
        assert file.identifier == "minecraft:zombie"
        assert file.identifier.is_vanilla


def test_vanilla_block_files_keep_the_vanilla_identifier():
    from anvil.api.blocks.blocks import Block

    block = Block("minecraft:stone", is_vanilla=True)
    for file in (block.server, block.client):
        assert file.identifier == "minecraft:stone"
        assert file.identifier.is_vanilla
    with pytest.raises(ValueError):
        Block("minecraft:not_a_block", is_vanilla=True)


def test_vanilla_item_files_keep_the_vanilla_identifier():
    from anvil.api.items.items import Item

    item = Item("minecraft:apple", is_vanilla=True)
    for file in (item.server, item.client):
        assert file.identifier == "minecraft:apple"
        assert file.identifier.is_vanilla


@pytest.mark.parametrize(
    "module, cls",
    [
        ("anvil.api.biomes.biomes", "Biome"),
    ],
)
def test_vanilla_objects_keep_the_vanilla_identifier(module, cls):
    import importlib

    kind = getattr(importlib.import_module(module), cls)
    obj = kind(f"minecraft:{cls.lower()}_x", is_vanilla=True)
    assert obj.server.identifier == f"minecraft:{cls.lower()}_x"
    assert obj.server.identifier.is_vanilla
