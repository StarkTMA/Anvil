import pytest

from anvil.api.actors.entity import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.items.items import Item
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.beta.vanilla.blocks import MinecraftBlockTypes as BetaBlockTypes
from anvil.beta.vanilla.entities import MinecraftEntityTypes as BetaEntityTypes
from anvil.beta.vanilla.items import MinecraftItemTypes as BetaItemTypes
from anvil.lib import config
from anvil.lib.jsonmodel import ItemId


def test_experimental_blocks_live_in_beta():
    assert BetaBlockTypes.Icicle(hanging=True).states == {"hanging": True}
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.Icicle


@pytest.mark.parametrize(
    "create",
    [
        lambda: Entity("frostbite", is_vanilla=True),
        lambda: Block("icicle", is_vanilla=True),
        lambda: Item("ice_ball", is_vanilla=True),
    ],
)
def test_experimental_vanilla_objects_need_the_flag(create):
    with config.override(_TARGET="world", _EXPERIMENTAL=False):
        with pytest.raises(ValueError, match="experimental"):
            create()
    with config.override(_TARGET="world", _EXPERIMENTAL=True):
        create()


def test_experimental_ids_in_fields_need_the_flag():
    with config.override(_EXPERIMENTAL=False):
        with pytest.raises(ValueError, match="not a vanilla item"):
            ItemId.validate("item", BetaItemTypes.IceBall())
    with config.override(_EXPERIMENTAL=True):
        ItemId.validate("item", BetaItemTypes.IceBall())
    assert BetaEntityTypes.Frostbite() == "minecraft:frostbite"
