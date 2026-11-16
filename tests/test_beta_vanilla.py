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


def test_brittle_ice_lives_in_beta():
    assert BetaBlockTypes.BrittleIce(age=3).states == {"age": 3}
    assert BetaItemTypes.BrittleIce() == "minecraft:brittle_ice"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.BrittleIce


def test_packed_ice_bricks_live_in_beta():
    assert BetaBlockTypes.PackedIceBricks() == "minecraft:packed_ice_bricks"
    assert BetaBlockTypes.PackedIceBricksSlab(minecraft_vertical_half="top").states == {
        "minecraft:vertical_half": "top"
    }
    assert BetaBlockTypes.PackedIceBricksStairs(
        minecraft_corner="inner_left", weirdo_direction=2
    ).states == {"minecraft:corner": "inner_left", "weirdo_direction": 2}
    assert BetaBlockTypes.PackedIceBricksWall(wall_post_bit=True).states == {
        "wall_post_bit": True
    }
    assert BetaItemTypes.PackedIceBricksWall() == "minecraft:packed_ice_bricks_wall"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.PackedIceBricks
    with pytest.raises(AttributeError):
        BetaBlockTypes.DiscPress
