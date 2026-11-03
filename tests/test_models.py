"""Tests for the typed geometry, animation and voxel shape files."""

import pytest

from anvil.api.models.animations import Animations
from anvil.api.models.geometry import (
    Geometry,
    ItemDisplayGuiTransform,
    ItemDisplayTransforms,
)
from anvil.api.models.voxel_shape import VoxelShape
from anvil.lib.lib import AnvilIO

jsonschema = pytest.importorskip("jsonschema")


def _json(value):
    return AnvilIO._normalize_json_like(value)


def _check(file):
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = _json(file._content)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def test_animations_file():
    animations = Animations("mob")
    walk = animations.animation("walk", loop=True)
    walk.bone("arm").add_rotation(0.5, [0, 30, 0]).add_rotation(
        0, [0, 0, 0], pre=[1, 1, 1]
    )
    walk.bone("leg", relative_to_rotation="entity").add_position(
        0.25, ["q.x", 0, 0], lerp_mode="catmullrom"
    )
    walk.particle(0.25, "dust", "foot").particle(0.25, "smoke", script="v.a = 1")
    walk.sound(0.1, "step").add_timeline(0.5, "v.x = 1").add_timeline(0.5, "v.y = 2;")
    animations.animation("idle", length=2.0)

    assert _check(animations) == {
        "format_version": "1.10.0",
        "animations": {
            "animation.test.mob.walk": {
                "loop": True,
                "bones": {
                    "arm": {
                        "rotation": {
                            "0.0": {"pre": [1, 1, 1], "post": [0, 0, 0]},
                            "0.5": [0, 30, 0],
                        }
                    },
                    "leg": {
                        "relative_to": {"rotation": "entity"},
                        "position": {
                            "0.25": {"post": ["q.x", 0, 0], "lerp_mode": "catmullrom"}
                        },
                    },
                },
                "particle_effects": {
                    "0.25": [
                        {"effect": "dust", "locator": "foot"},
                        {"effect": "smoke", "pre_effect_script": "v.a = 1;"},
                    ]
                },
                "sound_effects": {"0.1": [{"effect": "step"}]},
                "timeline": {"0.5": ["v.x = 1;", "v.y = 2;"]},
            },
            "animation.test.mob.idle": {"animation_length": 2.0},
        },
    }
    assert walk.identifier == "animation.test.mob.walk"
    assert animations.get("walk") is walk


def test_keyframe_at_the_same_time_is_replaced():
    animation = Animations("mob").animation("walk")
    animation.bone("arm").add_scale(1, [2, 2, 2]).add_scale(1.0, [3, 3, 3])
    assert _json(animation.bone("arm")) == {"scale": {"1.0": [3, 3, 3]}}


def test_animation_errors():
    animations = Animations("mob")
    animation = animations.animation("walk")
    with pytest.raises(ValueError):
        animations.animation("walk")
    with pytest.raises(ValueError):
        animation.bone("arm").add_position(
            0, [0, 0, 0], pre=[0, 0, 0], lerp_mode="linear"
        )
    animation.set_loop("forever")
    with pytest.raises(ValueError):
        _json(animation)


def test_voxel_shape_file():
    shape = VoxelShape("table")
    top = shape.group("top").box(min=(0, 12, 0), max=(16, 16, 16))
    shape.group("legs").box((0, 0, 0), (2, 12, 2))
    top.group("edge").box((0, 11, 0), (16, 12, 1))
    assert shape.shape_identifier == "test:table"
    assert _check(shape) == {
        "format_version": "1.21.110",
        "minecraft:voxel_shape": {
            "description": {"identifier": "test:table"},
            "shape": {
                "boxes": [
                    {"min": [0, 12, 0], "max": [16, 16, 16]},
                    {"min": [0, 11, 0], "max": [16, 12, 1]},
                    {"min": [0, 0, 0], "max": [2, 12, 2]},
                ]
            },
        },
    }
    top.remove()
    assert len(_json(shape._content)["minecraft:voxel_shape"]["shape"]["boxes"]) == 1


@pytest.mark.parametrize(
    "low, high",
    [((0, 0, 0), (0, 8, 16)), ((-31, 0, 0), (16, 8, 16)), ((16, 0, 0), (20, 8, 16))],
)
def test_voxel_box_limits(low, high):
    shape = VoxelShape("bad")
    shape.group("root").box(low, high)
    with pytest.raises(ValueError):
        _json(shape._content)


def test_voxel_shape_needs_a_box():
    with pytest.raises(ValueError):
        _json(VoxelShape("empty")._content)


def _mob():
    geometry = Geometry("mob", texture_size=(64, 32))
    body = geometry.bone("body", pivot=(0, 12, 0))
    body.cube(origin=(-4, 12, -2), size=(8, 12, 4), uv=(16, 16))
    arm = body.bone("arm", pivot=(5, 22, 0), rotation=(0, 0, 10))
    arm.cube(
        origin=(4, 12, -2),
        size=(4, 12, 4),
        north=((0, 0), (4, 12)),
        up=((4, 0), (4, 4), 90),
        inflate=0.5,
    )
    arm.locator("hand", (6, 12, 0)).locator("tip", (6, 10, 0), rotation=(0, 90, 0))
    geometry.bone("head", pivot=(0, 24, 0))
    return geometry


def test_geometry_file():
    assert _check(_mob()) == {
        "format_version": "1.26.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.test.mob",
                    "visible_bounds_width": 1,
                    "visible_bounds_height": 1,
                    "visible_bounds_offset": [0, 0, 0],
                    "texture_width": 64,
                    "texture_height": 32,
                },
                "bones": [
                    {
                        "name": "body",
                        "pivot": [0, 12, 0],
                        "cubes": [
                            {"origin": [-4, 12, -2], "size": [8, 12, 4], "uv": [16, 16]}
                        ],
                    },
                    {
                        "name": "arm",
                        "parent": "body",
                        "pivot": [5, 22, 0],
                        "rotation": [0, 0, 10],
                        "cubes": [
                            {
                                "origin": [4, 12, -2],
                                "size": [4, 12, 4],
                                "uv": {
                                    "north": {"uv": [0, 0], "uv_size": [4, 12]},
                                    "up": {
                                        "uv": [4, 0],
                                        "uv_size": [4, 4],
                                        "uv_rotation": 90,
                                    },
                                },
                                "inflate": 0.5,
                            }
                        ],
                        "locators": {
                            "hand": [6, 12, 0],
                            "tip": {"offset": [6, 10, 0], "rotation": [0, 90, 0]},
                        },
                    },
                    {"name": "head", "pivot": [0, 24, 0]},
                ],
            }
        ],
    }


def test_bones_stay_in_tree_order():
    geometry = _mob()
    geometry.find("body").bone("leg")
    names = [
        bone["name"]
        for bone in _json(geometry._content)["minecraft:geometry"][0]["bones"]
    ]
    assert names == ["body", "arm", "leg", "head"]
    geometry.find("body").remove()
    names = [
        bone["name"]
        for bone in _json(geometry._content)["minecraft:geometry"][0]["bones"]
    ]
    assert names == ["head"]
    assert geometry.find("arm") is None


def test_geometry_transforms_and_copies():
    geometry = _mob()
    clone = geometry.clone("copy")
    geometry.translate((1, 0, 0)).scale(2)
    arm = geometry.find("arm")
    assert arm.pivot == (12, 44, 0)
    assert arm.cubes[0].origin == (10, 24, -4)
    assert arm.cubes[0].size == (8, 24, 8)
    assert arm.cubes[0].inflate == 1.0
    assert arm.locators[0].offset == (14, 24, 0)
    assert clone.find("arm").pivot == (5, 22, 0)
    assert clone.find("arm").cubes[0].uv is not arm.cubes[0].uv
    assert clone.geometry_identifier == "geometry.test.copy"

    target = Geometry("target")
    target.merge(_mob(), prefix="m_")
    assert target.find("m_arm").parent == "m_body"


def test_geometry_errors():
    geometry = _mob()
    with pytest.raises(ValueError):
        geometry.bone("arm")
    with pytest.raises(ValueError):
        geometry.find("arm").locator("hand", (0, 0, 0))
    with pytest.raises(ValueError):
        geometry.find("body").cube((0, 0, 0), (1, 1, 1), (0, 0), north=((0, 0), (1, 1)))
    with pytest.raises(AttributeError):
        geometry.find("arm").pivot = (0, 0, 0)
    geometry.find("head").cube((0, 0, 0), (1, 1, 1), north=((0, 0), (1, 1), 45))
    with pytest.raises(ValueError):
        _json(geometry._content)


def test_geometry_item_display_transforms():
    geometry = Geometry("block")
    geometry.set_item_display_transforms(
        ItemDisplayTransforms(gui=ItemDisplayGuiTransform(rotation=(30, 45, 0)))
    )
    exported = _check(geometry)["minecraft:geometry"][0]
    assert exported["item_display_transforms"] == {"gui": {"rotation": [30, 45, 0]}}
    copy = geometry.clone("other").item_display_transforms
    assert copy.gui is not geometry.item_display_transforms.gui
