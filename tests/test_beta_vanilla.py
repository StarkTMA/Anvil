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
    with config.override(_TARGET="world", _PREVIEW=True, _EXPERIMENTAL=True):
        create()


def test_experimental_ids_in_fields_need_the_flag():
    with config.override(_EXPERIMENTAL=False):
        with pytest.raises(ValueError, match="not a vanilla item"):
            ItemId.validate("item", BetaItemTypes.IceBall())
    with config.override(_PREVIEW=True, _EXPERIMENTAL=True):
        ItemId.validate("item", BetaItemTypes.IceBall())
    assert BetaEntityTypes.Frostbite() == "minecraft:frostbite"


def test_brittle_ice_lives_in_beta():
    assert BetaBlockTypes.BrittleIce(age=3).states == {"age": 3}
    assert BetaItemTypes.BrittleIce() == "minecraft:brittle_ice"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.BrittleIce


def test_packed_ice_bricks_live_in_beta():
    assert BetaBlockTypes.PackedIceBricks() == "minecraft:packed_ice_bricks"
    assert BetaBlockTypes.ChiseledPackedIce() == "minecraft:chiseled_packed_ice"
    assert BetaBlockTypes.PackedIceBrickSlab(minecraft_vertical_half="top").states == {
        "minecraft:vertical_half": "top"
    }
    assert BetaBlockTypes.PackedIceBrickStairs(
        minecraft_corner="inner_left", weirdo_direction=2
    ).states == {"minecraft:corner": "inner_left", "weirdo_direction": 2}
    assert BetaBlockTypes.PackedIceBrickWall(wall_post_bit=True).states == {
        "wall_post_bit": True
    }
    assert BetaItemTypes.PackedIceBrickWall() == "minecraft:packed_ice_brick_wall"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.PackedIceBricks
    with pytest.raises(AttributeError):
        BetaBlockTypes.DiscPress


def test_snow_bricks_live_in_beta():
    assert BetaBlockTypes.SnowBricks() == "minecraft:snow_bricks"
    assert BetaBlockTypes.SnowBrickSlab(minecraft_vertical_half="bottom").states == {
        "minecraft:vertical_half": "bottom"
    }
    assert BetaBlockTypes.SnowBrickWall(wall_post_bit=False).states == {
        "wall_post_bit": False
    }
    assert BetaItemTypes.SnowBrickStairs() == "minecraft:snow_brick_stairs"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.SnowBricks


def test_beta_tag_enums_hold_only_the_new_tags():
    from enum import StrEnum

    from anvil.api.items.components import ItemTags
    from anvil.api.vanilla.biomes import MinecraftBiomeTags
    from anvil.api.vanilla.items import MinecraftItemTags
    from anvil.beta.vanilla.biomes import MinecraftBiomeTypes as BetaBiomeTypes
    from anvil.beta.vanilla.items import MinecraftItemTags as BetaItemTags

    for enum in (BetaItemTags, BetaBiomeTypes):
        assert issubclass(enum, StrEnum)
    assert {tag.name: tag.value for tag in BetaItemTags} == {
        "SulfurCubeArchetypeSlowBouncy": "minecraft:sulfur_cube_archetype_slow_bouncy",
        "SulfurCubeArchetypeHot": "minecraft:sulfur_cube_archetype_hot",
        "SulfurCubeArchetypeCold": "minecraft:sulfur_cube_archetype_cold",
    }
    assert not hasattr(MinecraftItemTags, "SulfurCubeArchetypeHot")
    tags = ItemTags(tags=[MinecraftItemTags.Arrow, BetaItemTags.SulfurCubeArchetypeHot])
    assert tags.__json__() == {
        "minecraft:tags": {
            "tags": ["minecraft:arrow", "minecraft:sulfur_cube_archetype_hot"]
        }
    }
