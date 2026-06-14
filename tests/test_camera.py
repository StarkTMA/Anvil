import os
import pytest
from unittest.mock import MagicMock

# Setup mock CONFIG
mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"
mock_config.NAMESPACE = "testns"
mock_config.PROJECT_NAME = "test_project"

import anvil.lib.config
anvil.lib.config.CONFIG = mock_config

import anvil.lib.schemas
anvil.lib.schemas.CONFIG = mock_config

from anvil.api.core.enums import CameraPresets, AimAssistTargetMode, ControlSchemes
from anvil.api.core.camera import (
    AimAssistPreset,
    AimAssistCategory,
    AimAssistCategories,
    CameraPreset,
)


def test_aim_assist_preset():
    preset = AimAssistPreset("test_preset")
    assert preset._path == os.path.join("dummy_bp_path", "cameras", "presets")
    assert preset.identifier == "testns:test_preset"

    preset.item_settings({"minecraft:stone_axe": "axe_category"})
    preset.default_item_settings("default_category")
    preset.hand_settings("hand_category")
    preset.exclusion_list({"blocks": ["minecraft:dirt"]})
    preset.liquid_targeting_list({"items": ["minecraft:bucket"]})

    content = preset.__export__()
    assert content["minecraft:aim_assist_preset"]["item_settings"] == {"minecraft:stone_axe": "axe_category"}
    assert content["minecraft:aim_assist_preset"]["default_item_settings"] == "default_category"
    assert content["minecraft:aim_assist_preset"]["hand_settings"] == "hand_category"
    assert content["minecraft:aim_assist_preset"]["exclusion_list"] == {"blocks": ["minecraft:dirt"]}
    assert content["minecraft:aim_assist_preset"]["liquid_targeting_list"] == {"items": ["minecraft:bucket"]}


def test_aim_assist_category_and_categories():
    categories = AimAssistCategories()
    assert categories._path == os.path.join("dummy_bp_path", "cameras", "presets")
    assert categories._name == "categories"

    cat = categories.add_category("test_cat")
    cat.entity_default(5).block_default(10)
    cat.block_priority("minecraft:stone", 15)
    cat.entity_priority("minecraft:zombie", 20)

    content = categories.__export__()
    assert "minecraft:aim_assist_categories" in content
    cats_list = content["minecraft:aim_assist_categories"]["categories"]
    assert len(cats_list) == 1
    assert cats_list[0]["name"] == "test_cat"
    assert cats_list[0]["entity_default"] == 5
    assert cats_list[0]["block_default"] == 10
    assert cats_list[0]["priorities"]["blocks"]["minecraft:stone"] == 15
    assert cats_list[0]["priorities"]["entities"]["minecraft:zombie"] == 20


def test_camera_preset_inheritance():
    # 1. Inherit from CameraPresets Enum
    preset_enum = CameraPreset("cam_enum", CameraPresets.Free)
    assert preset_enum._inherit == "minecraft:free"

    # 2. Inherit from another CameraPreset
    preset_inst = CameraPreset("cam_inst", preset_enum)
    assert preset_inst._inherit == "testns:cam_enum"

    # 3. Inherit from string identifier
    preset_str = CameraPreset("cam_str", "testns:other_camera")
    assert preset_str._inherit == "testns:other_camera"

    # 4. Invalid inheritance type
    with pytest.raises(ValueError):
        CameraPreset("cam_invalid", 123)


def test_camera_preset_position_and_rotation():
    preset = CameraPreset("cam_pos_rot", CameraPresets.Free)

    # Test override to 0.0 (previously not possible due to `x != 0` check)
    preset.position(x=0.0, y=10.0, z=0.0)
    assert preset._camera_preset["minecraft:camera_preset"]["pos_x"] == 0.0
    assert preset._camera_preset["minecraft:camera_preset"]["pos_y"] == 10.0
    assert preset._camera_preset["minecraft:camera_preset"]["pos_z"] == 0.0

    # Test rotation pitch clamping to [-90, 90]
    preset.rotation(x=-120.0, y=45.0)
    assert preset._camera_preset["minecraft:camera_preset"]["rot_x"] == -90.0
    assert preset._camera_preset["minecraft:camera_preset"]["rot_y"] == 45.0

    preset.rotation(x=95.0, y=90.0)
    assert preset._camera_preset["minecraft:camera_preset"]["rot_x"] == 90.0

    # Test starting rotation pitch clamping
    preset.starting_rotation(x=-100.0, y=10.0)
    assert preset._camera_preset["minecraft:camera_preset"]["starting_rot_x"] == -90.0
    assert preset._camera_preset["minecraft:camera_preset"]["starting_rot_y"] == 10.0


def test_camera_preset_settings():
    preset = CameraPreset("cam_settings", CameraPresets.Free)

    # Player effects
    preset.player_effects(True)
    assert preset._camera_preset["minecraft:camera_preset"]["player_effects"] is True

    # Listener
    preset.listener(True)
    assert preset._camera_preset["minecraft:camera_preset"]["listener"] == "player"
    preset.listener("camera")
    assert preset._camera_preset["minecraft:camera_preset"]["listener"] == "camera"
    preset.listener(False)
    assert "listener" not in preset._camera_preset["minecraft:camera_preset"]

    # Control scheme
    preset.control_scheme("camera_relative")
    assert preset._camera_preset["minecraft:camera_preset"]["control_scheme"] == "camera_relative"
    preset.control_scheme(ControlSchemes.PlayerRelativeStrafe)
    assert preset._camera_preset["minecraft:camera_preset"]["control_scheme"] == "player_relative_strafe"

    # Extend player rendering
    preset.extend_player_rendering(True)
    assert preset._camera_preset["minecraft:camera_preset"]["extend_player_rendering"] is True

    # View offset, entity offset, radius
    preset.view_offset(1.0, 2.0)
    assert preset._camera_preset["minecraft:camera_preset"]["view_offset"] == [1.0, 2.0]

    preset.entity_offset(0.0, 1.5, 0.0)
    assert preset._camera_preset["minecraft:camera_preset"]["entity_offset"] == [0.0, 1.5, 0.0]

    preset.radius(15.0)
    assert preset._camera_preset["minecraft:camera_preset"]["radius"] == 15.0


def test_camera_preset_aim_assist():
    preset = CameraPreset("cam_aa", CameraPresets.Free)
    aa_preset = AimAssistPreset("aa_preset")
    preset.aim_assist(aa_preset, target_mode=AimAssistTargetMode.Angle, angle=[25.0, 35.0], distance=12.0)

    aa_data = preset._camera_preset["minecraft:camera_preset"]["aim_assist"]
    assert aa_data["preset"] == "testns:aa_preset"
    assert aa_data["target_mode"] == "angle"
    assert aa_data["angle"] == [25.0, 35.0]
    assert aa_data["distance"] == 12.0


def test_camera_preset_focus_target():
    preset = CameraPreset("cam_focus", CameraPresets.Free)

    # Valid limits
    preset.focus_target(
        rotation_speed=15.0,
        snap_to_target=True,
        horizontal_rotation_limit=[45.0, 45.0],
        vertical_rotation_limit=[30.0, 60.0],
        continue_targeting=True,
        tracking_radius=40.0
    )
    cam_data = preset._camera_preset["minecraft:camera_preset"]
    assert cam_data["rotation_speed"] == 15.0
    assert cam_data["snap_to_target"] is True
    assert cam_data["horizontal_rotation_limit"] == [45.0, 45.0]
    assert cam_data["vertical_rotation_limit"] == [30.0, 60.0]
    assert cam_data["continue_targeting"] is True
    assert cam_data["tracking_radius"] == 40.0

    # Limits exceeding maximum sums (horizontal sum > 360, vertical sum > 180)
    preset.focus_target(
        horizontal_rotation_limit=[200.0, 200.0],
        vertical_rotation_limit=[100.0, 100.0]
    )
    assert sum(preset._camera_preset["minecraft:camera_preset"]["horizontal_rotation_limit"]) == 360.0
    assert sum(preset._camera_preset["minecraft:camera_preset"]["vertical_rotation_limit"]) == 180.0
