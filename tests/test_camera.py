"""Tests for the typed camera preset and aim assist files."""

import pytest

from anvil.api.camera import (
    AimAssistCategories,
    AimAssistPreset,
    CameraPreset,
)
from anvil.lib import config
from anvil.lib.jsonmodel.enums import AimAssistTargetMode, CameraPresets, ControlSchemes
from anvil.lib.lib import AnvilIO

jsonschema = pytest.importorskip("jsonschema")


@pytest.fixture(autouse=True)
def project_namespace():
    with config.override(NAMESPACE="testns"):
        yield


def _check(file):
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._content)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def test_aim_assist_preset():
    preset = AimAssistPreset("test_preset")
    assert preset._path == config.CONFIG.BP_PATH / "cameras" / "presets"
    assert preset.identifier == "testns:test_preset"

    preset.item_setting("minecraft:stone_axe", "axe_category")
    preset.item_setting("minecraft:stone_axe", "other_category")
    preset.item_setting("minecraft:bow", "bow_category")
    preset.default_item_settings("default_category").hand_settings("hand_category")
    preset.exclusion_list(["minecraft:bedrock", "minecraft:arrow"])
    preset.liquid_targeting_list(["minecraft:bucket"])

    exported = _check(preset)
    assert exported["format_version"] == "1.21.70"
    assert exported["minecraft:aim_assist_preset"] == {
        "identifier": "testns:test_preset",
        "item_settings": {
            "minecraft:stone_axe": "other_category",
            "minecraft:bow": "bow_category",
        },
        "default_item_settings": "default_category",
        "hand_settings": "hand_category",
        "exclusion_list": ["minecraft:bedrock", "minecraft:arrow"],
        "liquid_targeting_list": ["minecraft:bucket"],
    }


def test_aim_assist_preset_leaves_unset_keys_out():
    exported = _check(AimAssistPreset("bare"))
    assert exported["minecraft:aim_assist_preset"] == {"identifier": "testns:bare"}


def test_aim_assist_categories():
    categories = AimAssistCategories()
    assert categories._path == config.CONFIG.BP_PATH / "cameras" / "presets"
    assert categories.name == "categories"

    category = categories.add_category("test_cat")
    category.entity_default(5).block_default(10)
    category.block_priority("minecraft:stone", 15)
    category.entity_priority("minecraft:zombie", 20)
    categories.add_category("empty")

    exported = _check(categories)
    assert exported["minecraft:aim_assist_categories"]["categories"] == [
        {
            "name": "test_cat",
            "priorities": {
                "entity_default": 5,
                "block_default": 10,
                "entities": {"minecraft:zombie": 20},
                "blocks": {"minecraft:stone": 15},
            },
        },
        {"name": "empty", "priorities": {}},
    ]


def test_aim_assist_categories_refuse_a_duplicate_name():
    categories = AimAssistCategories()
    categories.add_category("same")
    with pytest.raises(ValueError):
        categories.add_category("same")


def test_camera_preset_inheritance():
    from_enum = CameraPreset("cam_enum", CameraPresets.Free)
    from_preset = CameraPreset("cam_inst", from_enum)
    from_text = CameraPreset("cam_str", "testns:other_camera")

    assert from_enum._content.preset.inherit_from == "minecraft:free"
    assert from_preset._content.preset.inherit_from == "testns:cam_enum"
    assert from_text._content.preset.inherit_from == "testns:other_camera"
    with pytest.raises(TypeError):
        CameraPreset("cam_invalid", 123)


def test_camera_preset_settings():
    preset = CameraPreset("cam", CameraPresets.FollowOrbit)
    preset.position(x=0.0, y=10.0).position(z=-2)
    preset.rotation(x=-90, y=45).starting_rotation(x=10, y=20)
    preset.player_effects(True).listener(True)
    preset.control_scheme(ControlSchemes.PlayerRelativeStrafe)
    preset.extend_player_rendering()
    preset.view_offset(1.0, 2.0).entity_offset(0.0, 1.5, 0.0).radius(15)

    body = _check(preset)["minecraft:camera_preset"]
    assert body == {
        "identifier": "testns:cam",
        "inherit_from": "minecraft:follow_orbit",
        "pos_x": 0.0,
        "pos_y": 10.0,
        "pos_z": -2,
        "rot_x": -90,
        "rot_y": 45,
        "starting_rot_x": 10,
        "starting_rot_y": 20,
        "player_effects": True,
        "listener": "player",
        "control_scheme": "player_relative_strafe",
        "extend_player_rendering": True,
        "view_offset": [1.0, 2.0],
        "entity_offset": [0.0, 1.5, 0.0],
        "radius": 15,
    }

    preset.listener(False)
    assert "listener" not in _check(preset)["minecraft:camera_preset"]


@pytest.mark.parametrize(
    "build",
    [
        lambda preset: preset.rotation(x=-120),
        lambda preset: preset.starting_rotation(x=95),
        lambda preset: preset.radius(0),
        lambda preset: preset.focus_target(horizontal_rotation_limit=(200, 200)),
        lambda preset: preset.focus_target(vertical_rotation_limit=(100, 100)),
        lambda preset: preset.focus_target(rotation_speed=-1),
    ],
)
def test_camera_preset_refuses_out_of_range_values(build):
    preset = CameraPreset("cam_range", CameraPresets.Free)
    build(preset)
    with pytest.raises(ValueError):
        preset._content.__json__()


def test_camera_preset_aim_assist():
    preset = CameraPreset("cam_aa", CameraPresets.Free)
    preset.aim_assist(
        AimAssistPreset("aa_preset"),
        target_mode=AimAssistTargetMode.Angle,
        angle=(35.0, 25.0),
        distance=12.0,
    )
    assert _check(preset)["minecraft:camera_preset"]["aim_assist"] == {
        "preset": "testns:aa_preset",
        "target_mode": "angle",
        "angle": [35.0, 25.0],
        "distance": 12.0,
    }

    preset.aim_assist(AimAssistPreset("far"), distance=20)
    with pytest.raises(ValueError):
        preset._content.__json__()


def test_camera_preset_focus_target():
    preset = CameraPreset("cam_focus", CameraPresets.Free)
    preset.focus_target(
        rotation_speed=15.0,
        snap_to_target=True,
        horizontal_rotation_limit=(45.0, 45.0),
        vertical_rotation_limit=(30.0, 60.0),
        continue_targeting=True,
        tracking_radius=40.0,
    )
    body = _check(preset)["minecraft:camera_preset"]
    assert body["rotation_speed"] == 15.0
    assert body["snap_to_target"] is True
    assert body["horizontal_rotation_limit"] == [45.0, 45.0]
    assert body["vertical_rotation_limit"] == [30.0, 60.0]
    assert body["continue_targeting"] is True
    assert body["tracking_radius"] == 40.0
