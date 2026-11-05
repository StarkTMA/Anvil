import orjson
import pytest

from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockCraftingTable,
    BlockCustomComponent,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockEmbeddedVisual,
    BlockFlammable,
    BlockFriction,
    BlockGeometry,
    BlockInstrumentSound,
    BlockLightDampening,
    BlockLiquidDetection,
    BlockMaterialInstance,
    BlockMovable,
    BlockPlacementFilter,
    BlockPrecipitationInteractions,
    BlockRedstoneConsumer,
    BlockRedstoneProducer,
    BlockSelectionBox,
    BlockTagComponent,
    BlockTick,
    BlockTransformation,
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
    ItemTagFilter,
    MaterialInstance,
    MaterialParams,
    NWayVisualRotation,
)
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.factories.minecraft_blocks import (
    Cinnabar,
    CinnabarBrickSlab,
    CinnabarBrickStairs,
    CinnabarBrickWall,
    PotentSulfur,
    Sulfur,
)
from anvil.api.vanilla.factories.minecraft_blocks import SulfurSpike as SulfurSpikeBlock
from anvil.lib.jsonmodel import json_field
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    PlacementDirectionTrait,
)
from anvil.lib.lib import AnvilIO


def test_new_blocks():
    cinnabar = Cinnabar()
    assert cinnabar == "minecraft:cinnabar"

    slab = CinnabarBrickSlab(minecraft_vertical_half="top")
    assert slab.name == "minecraft:cinnabar_brick_slab"
    assert slab.states["minecraft:vertical_half"] == "top"

    stairs = CinnabarBrickStairs(upside_down_bit="1b", weirdo_direction="2")
    assert stairs.name == "minecraft:cinnabar_brick_stairs"
    assert stairs.states["upside_down_bit"] == "1b"
    assert stairs.states["weirdo_direction"] == "2"

    wall = CinnabarBrickWall(wall_post_bit="1b")
    assert wall.name == "minecraft:cinnabar_brick_wall"
    assert wall.states["wall_post_bit"] == "1b"

    sulfur = Sulfur()
    assert sulfur == "minecraft:sulfur"

    potent = PotentSulfur()
    assert potent == "minecraft:potent_sulfur"

    spike_block = SulfurSpikeBlock(dripstone_thickness="tip", hanging="1b")
    assert spike_block.name == "minecraft:sulfur_spike"
    assert spike_block.states["dripstone_thickness"] == "tip"
    assert spike_block.states["hanging"] == "1b"


def test_placement_direction_trait_values():
    assert PlacementDirectionTrait.CardinalDirection == "minecraft:cardinal_direction"
    assert PlacementDirectionTrait.FacingDirection == "minecraft:facing_direction"
    assert (
        PlacementDirectionTrait.CornerAndCardinalDirection
        == "minecraft:corner_and_cardinal_direction"
    )


@pytest.fixture(autouse=True)
def anvil_project(tmp_path, monkeypatch):
    """Descriptors and localization read the project config, so run each test in a minimal project."""
    (tmp_path / "anvilconfig.json").write_bytes(
        orjson.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    import anvil.lib.config as config

    config.use(None)


def _export(component):
    return AnvilIO._normalize_json_like(component)


def test_bare_value_components():
    assert _export(BlockFriction(value=0.2)) == {"minecraft:friction": 0.2}
    assert _export(BlockLightDampening(value=0)) == {"minecraft:light_dampening": 0}
    assert _export(BlockDisplayName(value="Oak Door")) == {
        "minecraft:display_name": "Oak Door"
    }
    from anvil.api.blocks import components

    custom = f"{components.CONFIG.NAMESPACE}:planks"
    assert _export(BlockTagComponent(value=[MinecraftBlockTags.Wood, custom])) == {
        "minecraft:tags": ["wood", custom]
    }


def test_unset_options_are_left_out():
    assert _export(BlockMovable()) == {"minecraft:movable": {}}
    assert _export(BlockRedstoneConsumer(min_power=0)) == {
        "minecraft:redstone_consumer": {"min_power": 0}
    }
    assert _export(BlockConnectionRule(accepts_connections_from="none")) == {
        "minecraft:connection_rule": {"accepts_connections_from": "none"}
    }


def test_redstone_producer():
    assert _export(
        BlockRedstoneProducer(
            power=15,
            connected_faces=["up", "north"],
            strongly_powered_face="down",
            transform_relative=True,
        )
    ) == {
        "minecraft:redstone_producer": {
            "power": 15,
            "connected_faces": ["up", "north"],
            "strongly_powered_face": "down",
            "transform_relative": True,
        }
    }
    with pytest.raises(ValueError, match="power"):
        _export(BlockRedstoneProducer(power=16))


def test_switchable_components():
    assert _export(BlockFlammable()) == {"minecraft:flammable": True}
    assert _export(BlockFlammable(enabled=False)) == {"minecraft:flammable": False}
    assert _export(BlockDestructibleByExplosion(explosion_resistance=15)) == {
        "minecraft:destructible_by_explosion": {"explosion_resistance": 15}
    }
    with pytest.raises(ValueError, match="enabled is False"):
        _export(BlockDestructibleByExplosion(explosion_resistance=1, enabled=False))


def test_boxes():
    assert _export(BlockSelectionBox()) == {"minecraft:selection_box": True}
    assert _export(BlockCollisionBox(enabled=False)) == {
        "minecraft:collision_box": False
    }
    assert _export(BlockCollisionBox(origin=(-8, 0, -8), size=(16, 8, 16))) == {
        "minecraft:collision_box": [{"origin": [-8, 0, -8], "size": [16, 8, 16]}]
    }
    box = BlockCollisionBox(origin=(-8, 0, -8), size=(16, 8, 16)).add_box(
        origin=(-8, 8, -8), size=(16, 16, 16)
    )
    assert _export(box) == {
        "minecraft:collision_box": [
            {"origin": [-8, 0, -8], "size": [16, 8, 16]},
            {"origin": [-8, 8, -8], "size": [16, 16, 16]},
        ]
    }
    with pytest.raises(ValueError, match="must stay within"):
        _export(BlockSelectionBox(origin=(-8, 0, -8), size=(16, 24, 16)))
    with pytest.raises(ValueError, match="both origin and size"):
        _export(BlockSelectionBox(origin=(-8, 0, -8)))


def test_destructible_by_mining_item_speeds():
    mining = BlockDestructibleByMining(seconds_to_destroy=4.5)
    mining.add_item_specific_speed(item="minecraft:iron_axe", destroy_speed=1)
    mining.add_item_specific_speed(
        item=ItemTagFilter(tags="q.any_tag('minecraft:is_axe')"), destroy_speed=2
    )
    assert _export(mining) == {
        "minecraft:destructible_by_mining": {
            "seconds_to_destroy": 4.5,
            "item_specific_speeds": [
                {"item": "minecraft:iron_axe", "destroy_speed": 1},
                {"item": {"tags": "q.any_tag('minecraft:is_axe')"}, "destroy_speed": 2},
            ],
        }
    }
    assert _export(BlockDestructibleByMining(enabled=False)) == {
        "minecraft:destructible_by_mining": False
    }


def test_faces_are_expanded():
    filter_ = BlockPlacementFilter().add_condition(allowed_faces=[BlockFaceValues.Side])
    assert _export(filter_)["minecraft:placement_filter"]["conditions"] == [
        {"allowed_faces": ["north", "south", "east", "west"]}
    ]
    with pytest.raises(ValueError):
        _export(BlockConnectionRule(enabled_directions=[BlockFaceValues.Up]))


def test_liquid_detection():
    detection = BlockLiquidDetection().add_detection_rule(
        on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
        can_contain_liquid=True,
    )
    assert _export(detection) == {
        "minecraft:liquid_detection": {
            "detection_rules": [
                {"on_liquid_touches": "no_reaction", "can_contain_liquid": True}
            ]
        }
    }
    with pytest.raises(ValueError):
        _export(BlockLiquidDetection())


def test_tick_and_transformation():
    assert _export(BlockTick(interval_range=(20, 60))) == {
        "minecraft:tick": {"interval_range": [20, 60]}
    }
    with pytest.raises(ValueError, match="greater than its maximum"):
        _export(BlockTick(interval_range=(60, 20)))
    assert _export(BlockTransformation(rotation=(0, 90, 0), translation=(0, 0, 1))) == {
        "minecraft:transformation": {"translation": [0, 0, 1], "rotation": [0, 90, 0]}
    }


def test_block_flammable():
    flammable = BlockFlammable(
        catch_chance_modifier=5, destroy_chance_modifier=20, lava_flammable="always"
    )
    assert _export(flammable) == {
        "minecraft:flammable": {
            "catch_chance_modifier": 5,
            "destroy_chance_modifier": 20,
            "lava_flammable": "always",
        }
    }
    with pytest.raises(ValueError):
        _export(BlockFlammable(lava_flammable="sometimes"))


def test_block_geometry_default():
    geometry = BlockGeometry()
    assert _export(geometry) == {
        "minecraft:geometry": {"identifier": "minecraft:geometry.full_block"}
    }
    with pytest.raises(ValueError, match="custom geometry"):
        _export(BlockGeometry().add_bone_visibility(door=True))
    with pytest.raises(ValueError, match="vanilla geometry"):
        geometry.block_culling()


def test_embedded_visual_default():
    visual = BlockEmbeddedVisual(
        n_way_visual_rotation=NWayVisualRotation(y="minecraft:sixteen_way_rotation")
    )
    assert _export(visual) == {
        "minecraft:embedded_visual": {
            "geometry": {
                "identifier": "minecraft:geometry.full_block",
                "n_way_visual_rotation": {"y": "minecraft:sixteen_way_rotation"},
            }
        }
    }


def test_material_params_checks():
    with pytest.raises(ValueError, match="needs a tint_method"):
        MaterialParams(alpha_masked_tint=True).__json__()
    with pytest.raises(ValueError, match="opaque"):
        MaterialParams(
            alpha_masked_tint=True,
            tint_method="grass",
            render_method=BlockMaterial.Blend,
        ).__json__()
    assert MaterialParams(ambient_occlusion=2.5).__json__() == {
        "ambient_occlusion": 2.5
    }


def test_crafting_table_tags():
    assert _export(BlockCraftingTable(crafting_tags=["crafting_table"])) == {
        "minecraft:crafting_table": {"crafting_tags": ["crafting_table"]}
    }
    with pytest.raises(ValueError, match="64 characters"):
        _export(BlockCraftingTable(crafting_tags=["x" * 65]))


def test_custom_component():
    class Explosive(BlockCustomComponent):
        identifier = "test:explosive"

        power: float = json_field()

    assert _export(Explosive(power=2.5)) == {"test:explosive": {"power": 2.5}}
    with pytest.raises(TypeError):
        BlockCustomComponent()


def test_custom_tags_need_the_namespace():
    with pytest.raises(ValueError, match="namespace"):
        _export(BlockTagComponent(value=["other:planks"]))


def test_block_instrument_sound():
    assert _export(BlockInstrumentSound(up="note.bassattack", down="note.bit")) == {
        "minecraft:instrument_sound": {"up": "note.bassattack", "down": "note.bit"}
    }
    assert _export(BlockInstrumentSound(down="note.banjo")) == {
        "minecraft:instrument_sound": {"down": "note.banjo"}
    }
    with pytest.raises(ValueError, match="At least one of 'up' or 'down'"):
        _export(BlockInstrumentSound())


def test_precipitation_interactions():
    assert _export(
        BlockPrecipitationInteractions(precipitation_behavior="snowlogging")
    ) == {
        "minecraft:precipitation_interactions": {
            "precipitation_behavior": "snowlogging"
        }
    }
    with pytest.raises(ValueError):
        _export(BlockPrecipitationInteractions(precipitation_behavior="invalid"))


def test_safe_key():
    from anvil.lib.translator import AnvilTranslator

    assert AnvilTranslator.safe_key("Read Book") == "read_book"
    assert AnvilTranslator.safe_key("Sails & Spoils") == "sails_spoils"
    assert AnvilTranslator.safe_key("Captain's Log\\nDay 1") == "captain_s_log_day_1"
    assert AnvilTranslator.safe_key("Café Crème") == "cafe_creme"
    assert AnvilTranslator.safe_key("1st Mate") == "_1st_mate"


def test_block_names_are_keyed_from_the_identifier():
    from anvil.api.blocks.components import BlockCraftingTable, BlockDisplayName
    from anvil.api.blocks.server import BlockServer
    from anvil.lib.translator import AnvilTranslator

    server = BlockServer(name="oak_table")
    server.components.add(
        BlockDisplayName(value="Oak Table"),
        BlockCraftingTable(crafting_tags=["x"], table_name="Oak Bench"),
    )
    server.permutation("1").add(BlockDisplayName(value="Wet Oak Table"))
    server._before_export()
    server._before_export()

    prefix = f"tile.{server.identifier}"
    root = server.components.__json__()["components"]
    assert root["minecraft:display_name"] == f"{prefix}.name"
    assert root["minecraft:crafting_table"]["table_name"] == f"{prefix}.table_name"
    permutation = server.permutations[0].__json__()["components"]
    assert permutation["minecraft:display_name"] == f"{prefix}.wet_oak_table.name"
    translator = AnvilTranslator()
    assert translator.get_localization_value(f"{prefix}.name") == "Oak Table"
    assert translator.get_localization_value(f"{prefix}.table_name") == "Oak Bench"


def test_add_bone_visibility_is_keyed_by_bone(monkeypatch):
    from anvil.api.blocks import components

    monkeypatch.setattr(
        components,
        "_geometry_source",
        lambda blockbench, collection: ("geometry.test.door", object(), "door"),
    )
    geometry = BlockGeometry(blockbench="door").add_bone_visibility(
        open="q.block_state('open')", closed=False
    )
    assert _export(geometry)["minecraft:geometry"]["bone_visibility"] == {
        "open": "q.block_state('open')",
        "closed": False,
    }
    with pytest.raises(ValueError, match="more than one"):
        _export(
            BlockGeometry(blockbench="door")
            .add_bone_visibility(open=True)
            .add_bone_visibility(open=False)
        )
    with pytest.raises(TypeError):
        _export(BlockGeometry(blockbench="door").add_bone_visibility(open=1))
    with pytest.raises(TypeError):
        BlockGeometry(bone_visibility=[])


def test_material_instances_are_keyed_by_face():
    instances = BlockMaterialInstance(
        instances=[
            MaterialInstance(texture="test:planks"),
            MaterialInstance(
                face=BlockFaceValues.Up,
                texture="test:top",
                render_method=BlockMaterial.AlphaTest,
            ),
        ]
    )
    assert _export(instances) == {
        "minecraft:material_instances": {
            "*": {"texture": "test:planks"},
            "up": {"texture": "test:top", "render_method": "alpha_test"},
        }
    }
    with pytest.raises(ValueError, match="more than one"):
        _export(
            BlockMaterialInstance(
                instances=[
                    MaterialInstance(texture="test:a"),
                    MaterialInstance(face=BlockFaceValues.All, texture="test:b"),
                ]
            )
        )


def test_item_display_transforms_are_parts():
    gui = ItemDisplayGuiTransform(rotation=(30, 225, 0), fit_to_frame=True)
    assert gui.__json__() == {"rotation": [30, 225, 0], "fit_to_frame": {}}
    assert ItemDisplayGuiTransform(fit_to_frame=False).__json__() == {
        "fit_to_frame": False
    }
    with pytest.raises(ValueError):
        ItemDisplayTransform(scale=(1, 1)).__json__()


def test_block_descriptor_states():
    from anvil.api.blocks.blocks import Block

    block = Block("leaves")
    block.server.description.add_state("natural", (False, True))
    block.server.description.traits.set_placement_direction(
        traits=[PlacementDirectionTrait.CardinalDirection]
    )

    assert block.descriptor() == "test:leaves"
    assert _export(block.descriptor(natural=True, cardinal_direction="north")) == {
        "name": "test:leaves",
        "states": {"test:natural": True, "minecraft:cardinal_direction": "north"},
    }
    assert _export(block.descriptor(tags="q.any_tag('x')")) == {
        "name": "test:leaves",
        "tags": "q.any_tag('x')",
    }
    with pytest.raises(ValueError, match="Unknown state"):
        block.descriptor(decaying=True)
    with pytest.raises(ValueError, match="Invalid value"):
        block.descriptor(natural=1)
    with pytest.raises(ValueError, match="Invalid value"):
        block.descriptor(cardinal_direction="up")
    with pytest.raises(ValueError, match="Invalid namespace"):
        block.descriptor(**{"other:natural": True})


def test_block_descriptor_trait_values_from_enums():
    from anvil.api.blocks.blocks import Block
    from anvil.lib.jsonmodel.enums import CardinalDirectionsValues, ConnectionTrait

    fence = Block("fence")
    fence.server.description.traits.set_connection(
        [ConnectionTrait.CardinalConnections]
    )
    fence.server.description.traits.set_placement_direction(
        traits=[PlacementDirectionTrait.CornerAndCardinalDirection]
    )

    assert fence.descriptor(
        connection_north=True,
        cardinal_direction=CardinalDirectionsValues.EAST,
        corner="inner_left",
    ).states == {
        "minecraft:connection_north": True,
        "minecraft:cardinal_direction": "east",
        "minecraft:corner": "inner_left",
    }
    with pytest.raises(ValueError, match="Invalid value"):
        fence.descriptor(connection_north="true")


def test_block_descriptor_multi_block_part():
    from anvil.api.blocks.blocks import Block

    door = Block("door")
    door.server.description.traits.set_multi_block("up", 3)

    assert door.descriptor(multi_block_part=2).states == {
        "minecraft:multi_block_part": 2
    }
    with pytest.raises(ValueError, match="Invalid value"):
        door.descriptor(multi_block_part=3)


def test_part_builders_for_blocks_and_biomes():
    from anvil.api.biomes.components import BiomeMapTints, GrassTint
    from anvil.api.blocks.components import (
        BlockEntity,
        BlockEntityContainer,
        BlockGeometry,
        BlockRandomOffset,
        NWayVisualRotation,
        OffsetRange,
    )

    pairs = [
        (
            BiomeMapTints().set_grass(tint="#00FF00"),
            BiomeMapTints(grass=GrassTint(tint="#00FF00")),
        ),
        (
            BlockEntity().set_container(slot_count=9),
            BlockEntity(container=BlockEntityContainer(slot_count=9)),
        ),
        (
            BlockGeometry().set_n_way_visual_rotation(y="minecraft:cardinal_direction"),
            BlockGeometry(
                n_way_visual_rotation=NWayVisualRotation(
                    y="minecraft:cardinal_direction"
                )
            ),
        ),
        (
            BlockRandomOffset()
            .set_x(range=(-1, 1), steps=4)
            .set_y(range=(0, 2))
            .set_z(steps=2),
            BlockRandomOffset(
                x=OffsetRange(range=(-1, 1), steps=4),
                y=OffsetRange(range=(0, 2)),
                z=OffsetRange(steps=2),
            ),
        ),
    ]
    for built, constructed in pairs:
        assert built.__json__() == constructed.__json__()


def _check_file(file):
    jsonschema = pytest.importorskip("jsonschema")
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._document)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


@pytest.fixture
def no_write(monkeypatch):
    """Exports files without writing them."""
    monkeypatch.setattr("anvil.lib.jsonmodel.file.AnvilIO.file", lambda *a, **k: None)


def test_block_server_file(no_write):
    from anvil.api.blocks.blocks import Block
    from anvil.api.blocks.server import BlockServer
    from anvil.lib.jsonmodel.enums import (
        ItemCategory,
        ItemGroups,
        PlacementPositionTrait,
    )

    block = Block("lantern")
    description = block.server.description
    description.add_state("lit", (False, True))
    description.set_menu_category(ItemCategory.Items, ItemGroups.Anvil, True)
    description.traits.set_placement_position([PlacementPositionTrait.BlockFace])
    block.server.components.add(
        BlockGeometry(),
        BlockMaterialInstance(instances=[MaterialInstance(texture="test:lantern")]),
    )
    block.server.permutation("q.block_state('test:lit')").add(
        BlockLightDampening(value=0)
    )
    block.server.__export__()

    exported = _check_file(block.server)
    body = exported["minecraft:block"]
    assert body["description"] == {
        "identifier": "test:lantern",
        "states": {"test:lit": [False, True]},
        "menu_category": {
            "category": "items",
            "group": "minecraft:itemGroup.name.anvil",
            "is_hidden_in_commands": True,
        },
        "traits": {
            "minecraft:placement_position": {"enabled_states": ["minecraft:block_face"]}
        },
    }
    assert body["components"]["minecraft:display_name"] == "tile.test:lantern.name"
    assert body["components"]["minecraft:geometry"] == {
        "identifier": "minecraft:geometry.full_block"
    }
    assert body["permutations"] == [
        {
            "condition": "q.block_state('test:lit')",
            "components": {"minecraft:light_dampening": 0},
        }
    ]
    assert BlockServer.__schema__()["x-anvil-file"] == {
        "pack": "behavior_pack",
        "folder": "blocks",
        "extension": ".block.json",
    }


def test_block_server_needs_geometry_and_material(no_write):
    from anvil.api.blocks.blocks import Block

    block = Block("bare")
    with pytest.raises(ValueError, match="geometry"):
        block.server.__export__()
    block.server.components.add(BlockGeometry())
    with pytest.raises(ValueError, match="material instance"):
        block.server.__export__()


def test_block_traits_are_checked():
    from anvil.api.blocks.server import _BlockTraits
    from anvil.lib.jsonmodel.enums import ConnectionTrait, PlacementPositionTrait

    traits = _BlockTraits()
    with pytest.raises(ValueError, match="multiple of 90"):
        traits.set_placement_direction(y_rotation_offset=45)
    with pytest.raises(ValueError, match="CornerAndCardinalDirection"):
        traits.set_placement_direction(
            blocks_to_corner_with=["minecraft:stone"],
            traits=[PlacementDirectionTrait.CardinalDirection],
        )
    traits.set_placement_direction(
        y_rotation_offset=90,
        blocks_to_corner_with=["minecraft:stone"],
        traits=[PlacementDirectionTrait.CornerAndCardinalDirection],
    )
    assert _export(traits) == {
        "minecraft:placement_direction": {
            "enabled_states": ["minecraft:corner_and_cardinal_direction"],
            "y_rotation_offset": 90,
            "blocks_to_corner_with": ["minecraft:stone"],
        }
    }
    with pytest.raises(ValueError, match="multi_block"):
        traits.set_multi_block("up")

    door = _BlockTraits().set_multi_block("down", 3)
    assert _export(door) == {
        "minecraft:multi_block": {
            "enabled_states": ["minecraft:multi_block_part"],
            "parts": 3,
            "direction": "down",
        }
    }
    with pytest.raises(ValueError):
        door.set_connection([ConnectionTrait.CardinalConnections])
    with pytest.raises(ValueError):
        door.set_placement_position([PlacementPositionTrait.VerticalHalf])
    with pytest.raises(ValueError, match="between 2 and 4"):
        _BlockTraits().set_multi_block("up", 5)
    with pytest.raises(ValueError, match="experimental"):
        _BlockTraits().set_multi_block("north")


def test_block_state_limit():
    from anvil.api.blocks.blocks import Block

    block = Block("counter")
    with pytest.raises(ValueError, match="16 values"):
        block.server.description.add_state("count", list(range(17)))
    block.server.description.add_state("count", range(16))
    assert block.server.description.states["test:count"] == list(range(16))


def test_block_client_is_not_a_file():
    from anvil.api.blocks.blocks import Block
    from anvil.lib.jsonmodel import JsonFile

    block = Block("drum")
    assert not isinstance(block.client, JsonFile)
    assert block.client.identifier == "test:drum"
    assert block.client.name == "drum"
    assert block.client.queue() is block.client


def test_vanilla_factories_reject_unknown_names():
    from anvil.api.vanilla.blocks import MinecraftBlockTypes
    from anvil.api.vanilla.entities import MinecraftEntityTypes
    from anvil.api.vanilla.items import MinecraftItemTypes

    assert MinecraftBlockTypes.Magma() == "minecraft:magma"
    assert MinecraftEntityTypes.VillagerV2() == "minecraft:villager_v2"
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.MagmaBlock
    with pytest.raises(AttributeError):
        MinecraftItemTypes.MagmaBlock
    with pytest.raises(AttributeError):
        MinecraftEntityTypes.MagmaBlock
    with pytest.raises(AttributeError):
        MinecraftBlockTypes.OakLogStates


def test_vanilla_block_factories_and_descriptors():
    from anvil.api.blocks.blocks import Block
    from anvil.api.blocks.descriptor import BlockDescriptor
    from anvil.api.vanilla.blocks import MinecraftBlockTypes
    from anvil.api.vanilla.items import MinecraftItemTypes
    from anvil.lib.jsonmodel import BlockId, Identifier

    stone = MinecraftBlockTypes.Stone()
    assert isinstance(stone, Identifier) and stone == "minecraft:stone"
    log = MinecraftBlockTypes.OakLog(pillar_axis="y")
    assert isinstance(log, BlockDescriptor)
    assert _export(log) == {"name": "minecraft:oak_log", "states": {"pillar_axis": "y"}}
    assert _export(BlockDescriptor(tags="q.any_tag('stone')")) == {
        "tags": "q.any_tag('stone')"
    }
    with pytest.raises(ValueError):
        _export(BlockDescriptor())
    with pytest.raises(ValueError):
        _export(BlockDescriptor(states={"a": 1}, tags="q.any_tag('stone')"))

    BlockId.validate("block", stone)
    BlockId.validate("block", log)
    BlockId.validate("block", Block("ruby_ore"))
    BlockId.validate("block", "anything:goes")
    with pytest.raises(ValueError):
        BlockId.validate("block", MinecraftItemTypes.Apple())
    with pytest.raises(ValueError):
        BlockId.validate(
            "block",
            BlockDescriptor(name=Identifier.parse("minecraft:apple", vanilla=True)),
        )
