from anvil.api.vanilla.factories.minecraft_blocks import (
    Cinnabar,
    CinnabarBrickSlab,
    CinnabarBrickStairs,
    CinnabarBrickWall,
    Sulfur,
    SulfurSpike as SulfurSpikeBlock,
    PotentSulfur,
)
from anvil.api.blocks.components import (
    BlockPrecipitationInteractions,
    BlockGeometry,
    BlockFlammable,
    BlockItemVisual,
    BlockEmbeddedVisual,
)
from anvil.api.core.enums import PlacementDirectionTrait


def test_new_blocks():
    # Verify Cinnabar block factory
    cinnabar = Cinnabar()
    assert cinnabar.identifier == "minecraft:cinnabar"

    # Verify CinnabarBrickSlab block factory with states
    slab = CinnabarBrickSlab(minecraft_vertical_half="top")
    assert slab.identifier == "minecraft:cinnabar_brick_slab"
    assert slab.states["minecraft:vertical_half"] == "top"

    # Verify CinnabarBrickStairs block factory with states
    stairs = CinnabarBrickStairs(upside_down_bit="1b", weirdo_direction="2")
    assert stairs.identifier == "minecraft:cinnabar_brick_stairs"
    assert stairs.states["upside_down_bit"] == "1b"
    assert stairs.states["weirdo_direction"] == "2"

    # Verify CinnabarBrickWall block factory with states
    wall = CinnabarBrickWall(wall_post_bit="1b")
    assert wall.identifier == "minecraft:cinnabar_brick_wall"
    assert wall.states["wall_post_bit"] == "1b"

    # Verify Sulfur block factory
    sulfur = Sulfur()
    assert sulfur.identifier == "minecraft:sulfur"

    # Verify PotentSulfur block factory
    potent = PotentSulfur()
    assert potent.identifier == "minecraft:potent_sulfur"

    # Verify SulfurSpike block factory with states
    spike_block = SulfurSpikeBlock(dripstone_thickness="tip", hanging="1b")
    assert spike_block.identifier == "minecraft:sulfur_spike"
    assert spike_block.states["dripstone_thickness"] == "tip"
    assert spike_block.states["hanging"] == "1b"


def test_new_block_components():
    # 1. Test BlockPrecipitationInteractions
    precip = BlockPrecipitationInteractions("snowlogging")
    assert precip.identifier == "minecraft:precipitation_interactions"
    assert precip._component["precipitation_behavior"] == "snowlogging"

    # 2. Test n_way_visual_rotation on BlockGeometry
    geom = BlockGeometry()
    geom.n_way_visual_rotation(y="minecraft:sixteen_way_rotation")
    assert geom._component["n_way_visual_rotation"] == {"y": "minecraft:sixteen_way_rotation"}

    # 3. Test PlacementDirectionTrait.SixteenWayRotation enum value
    assert PlacementDirectionTrait.SixteenWayRotation == "minecraft:sixteen_way_rotation"

    # 4. Test lava_flammable parameter on BlockFlammable
    flam = BlockFlammable(catch_chance_modifier=5, destroy_chance_modifier=20, lava_flammable="always")
    assert flam._component["lava_flammable"] == "always"

    # 5. Test BlockItemVisual.n_way_visual_rotation
    iv = BlockItemVisual()
    assert iv.identifier == "minecraft:item_visual"
    iv.n_way_visual_rotation(y="minecraft:sixteen_way_rotation")
    assert iv._component["geometry"]["n_way_visual_rotation"] == {"y": "minecraft:sixteen_way_rotation"}

    # 6. Test BlockEmbeddedVisual.n_way_visual_rotation and identifier
    ev = BlockEmbeddedVisual()
    assert ev.identifier == "minecraft:embedded_visual"
    ev.n_way_visual_rotation(y="minecraft:sixteen_way_rotation")
    assert ev._component["geometry"]["n_way_visual_rotation"] == {"y": "minecraft:sixteen_way_rotation"}
