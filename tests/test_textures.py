"""Tests for `BlockTexture`, and the block faces, item icons and entity textures that take it."""

import base64
import io
from types import SimpleNamespace

import orjson
import pytest
from PIL import Image

from anvil.api.blocks.components import BlockMaterialInstance
from anvil.api.core.core import ANVIL
from anvil.api.items.components import ItemIcon
from anvil.api.pbr.texture_set import TextureSet
from anvil.api.textures import (
    FlipBookTexturesObject,
    ItemTexturesObject,
    TerrainTexturesObject,
    BlockTexture,
)
from anvil.api.vanilla import MinecraftItemTextures, MinecraftTerrainTextures
from anvil.lib import config
from anvil.lib.blockbench import _Blockbench
from anvil.lib.jsonmodel.enums import BlockFaceValues, BlockMaterial
from anvil.lib.lib import AnvilIO

MODEL = "crystal_lamp"
IMAGES = [
    "body",
    "body_n",
    "body_mer",
    "body_cracked",
    "cracked_n",
    "cracked_mer",
    "body_pulse",
    "pulse_n",
    "pulse_mer",
    "crystal",
    "crystal_mers",
]


@pytest.fixture(autouse=True)
def project(tmp_path, monkeypatch):
    """A project at tmp_path with a Blockbench model, item sprites and fresh atlases."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(_Blockbench, "_loaded_blockbench_models", {})
    monkeypatch.setattr(ANVIL, "_objects_list", [])
    for cls in (TerrainTexturesObject, ItemTexturesObject, FlipBookTexturesObject):
        monkeypatch.setattr(cls, "_instance", None)

    image = io.BytesIO()
    Image.new("RGBA", (16, 16)).save(image, format="PNG")
    source = "data:image/png;base64," + base64.b64encode(image.getvalue()).decode()
    model = {
        "meta": {"format_version": "5.0", "model_format": "bedrock"},
        "model_identifier": MODEL,
        "resolution": {"width": 16, "height": 16},
        "elements": [],
        "outliner": [],
        "textures": [{"name": f"{name}.png", "source": source} for name in IMAGES],
    }
    (tmp_path / "assets" / "bbmodels").mkdir(parents=True)
    (tmp_path / "assets" / "bbmodels" / f"{MODEL}.bbmodel").write_bytes(
        orjson.dumps(model)
    )
    for folder, name in [
        ("textures/items", "gem"),
        ("textures/items", "gem_mer"),
    ]:
        (tmp_path / "assets" / folder).mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (16, 16)).save(tmp_path / "assets" / folder / f"{name}.png")

    with config.override(PBR=True, NAMESPACE="testns", _LOCAL_EXPORT=True):
        yield


def _json(value):
    return AnvilIO._normalize_json_like(getattr(value, "_document", value))


def _block(name=MODEL):
    return SimpleNamespace(name=name)


# region Building textures


def test_textures_take_names_only():
    for bad in ["blocks/stone", "stone.png", "", "a\\b"]:
        with pytest.raises(ValueError, match="name only"):
            BlockTexture(blockbench=MODEL, color=bad)
    with pytest.raises(ValueError, match="name only"):
        BlockTexture(blockbench="models/lamp", color="body")


def test_pbr_animation_and_weighted_rules():
    body = BlockTexture(blockbench=MODEL, color="body")
    with pytest.raises(ValueError, match="mutually exclusive"):
        BlockTexture(blockbench=MODEL, color="body", normal="a", height="b")
    with pytest.raises(ValueError, match="power of two"):
        body.animated(4, replicate=3)
    with pytest.raises(TypeError, match="can't hold"):
        BlockTexture.weighted((BlockTexture.weighted((body, 1)), 1))
    with pytest.raises(ValueError, match="same PBR maps"):
        BlockTexture.weighted(
            (
                BlockTexture(blockbench=MODEL, color="body", normal="body_n"),
                1,
            ),
            (body, 1),
        )
    with pytest.raises(ValueError, match="0.05"):
        BlockTexture.weighted((body, 0))


def test_uses_refuse_textures_they_cannot_show():
    body = BlockTexture(blockbench=MODEL, color="body")
    with pytest.raises(ValueError, match="vanilla icon takes no model or maps"):
        ItemIcon(color=MinecraftItemTextures.Apple, mer="apple_mer")
    with pytest.raises(ValueError, match="BlockFaceValues.Side"):
        BlockMaterialInstance().face(BlockFaceValues.Side, body)


# endregion

# region Block faces


def test_block_faces_with_variations_pbr_animations_and_materials():
    model = MODEL
    body = BlockTexture(blockbench=model, color="body", normal="body_n", mer="body_mer")
    cracked = BlockTexture(
        blockbench=model, color="body_cracked", normal="cracked_n", mer="cracked_mer"
    )
    pulse = BlockTexture(
        blockbench=model, color="body_pulse", normal="pulse_n", mer="pulse_mer"
    ).animated(frames=[0, 1, 2, 3, 2, 1], ticks=3, blend=True)
    crystal = BlockTexture(
        blockbench=model, color="crystal", mers="crystal_mers"
    ).animated(frames=[0, 1, 2, 3], ticks=5)
    instances = (
        BlockMaterialInstance()
        .face(
            "*",
            BlockTexture.weighted((body, 6), (cracked, 3), (pulse, 1)),
            render_method=BlockMaterial.Opaque,
            isotropic=True,
        )
        .face(
            BlockFaceValues.Up,
            MinecraftTerrainTextures.Stone,
            face_dimming=False,
        )
        .face("crystal", crystal, render_method=BlockMaterial.Blend, emissive=True)
    )
    assert not TerrainTexturesObject()._document.texture_data

    instances.__prepare_export__(_block())
    assert _json(instances) == {
        "minecraft:material_instances": {
            "*": {
                "texture": "testns:crystal_lamp_all",
                "render_method": "opaque",
                "isotropic": True,
            },
            "up": {"texture": "stone", "face_dimming": False},
            "crystal": {
                "texture": "testns:crystal_lamp_crystal",
                "render_method": "blend",
                "emissive": True,
            },
        }
    }

    folder = "textures/testns/test/blocks/crystal_lamp"
    atlas = _json(TerrainTexturesObject())["texture_data"]
    assert atlas == {
        "testns:crystal_lamp_all": {
            "textures": {
                "variations": [
                    {"path": f"{folder}/body", "weight": 6},
                    {"path": f"{folder}/body_cracked", "weight": 3},
                    {"path": f"{folder}/body_pulse", "weight": 1},
                ]
            }
        },
        "testns:crystal_lamp_crystal": {"textures": [f"{folder}/crystal"]},
    }

    flipbooks = _json(FlipBookTexturesObject())
    assert flipbooks == [
        {
            "flipbook_texture": f"{folder}/body_pulse",
            "atlas_tile": "testns:crystal_lamp_all",
            "frames": [0, 1, 2, 3, 2, 1],
            "ticks_per_frame": 3,
            "atlas_tile_variant": 2,
        },
        {
            "flipbook_texture": f"{folder}/crystal",
            "atlas_tile": "testns:crystal_lamp_crystal",
            "frames": [0, 1, 2, 3],
            "ticks_per_frame": 5,
        },
    ]

    texture_sets = [o for o in ANVIL._objects_list if isinstance(o, TextureSet)]
    layers = {
        t.identifier.name: _json(t)["minecraft:texture_set"] for t in texture_sets
    }
    assert layers["body"] == {
        "color": "body",
        "normal": "body_n",
        "metalness_emissive_roughness": "body_mer",
    }
    assert layers["crystal"]["metalness_emissive_roughness_subsurface"] == (
        "crystal_mers"
    )
    queued = _Blockbench(MODEL, "blocks").textures._queued_textures
    assert set(queued) == set(IMAGES)


def test_block_face_names_come_from_the_block_and_face():
    body = BlockTexture(blockbench=MODEL, color="body")
    crystal = BlockTexture(blockbench=MODEL, color="crystal")
    root = BlockMaterialInstance().face("*", body)
    same = BlockMaterialInstance().face("*", body)
    other = BlockMaterialInstance().face("*", crystal)
    for instances in (root, same, other):
        instances.__prepare_export__(_block("lamp"), root=False)
    assert root.instances[0].texture == "testns:lamp_all"
    assert same.instances[0].texture == "testns:lamp_all"
    assert other.instances[0].texture == "testns:lamp_all_2"

    BlockMaterialInstance().face("*", body).__prepare_export__(_block("other_lamp"))
    assert set(_json(TerrainTexturesObject())["texture_data"]) == {
        "testns:lamp_all",
        "testns:lamp_all_2",
        "testns:other_lamp_all",
    }


def test_vanilla_block_faces_are_only_referenced():
    instances = BlockMaterialInstance().face("*", MinecraftTerrainTextures.Stone)
    instances.__prepare_export__(_block("granite_top"))
    assert _json(instances) == {
        "minecraft:material_instances": {"*": {"texture": "stone"}}
    }
    assert not TerrainTexturesObject()._document.texture_data


# endregion

# region Item icons


def test_item_icons():
    icon = ItemIcon(color="gem", mer="gem_mer")
    assert _json(icon) == {"minecraft:icon": {"textures": {"default": "testns:gem"}}}
    assert _json(ItemTexturesObject())["texture_data"] == {
        "testns:gem": {"textures": ["textures/testns/test/items/gem"]}
    }

    blade = ItemIcon(blockbench=MODEL, color="body")
    assert _json(blade) == {"minecraft:icon": {"textures": {"default": "testns:body"}}}


def test_vanilla_item_icons_are_only_referenced():
    apple = ItemIcon(color=MinecraftItemTextures.Apple)
    assert _json(apple) == {"minecraft:icon": {"textures": {"default": "apple"}}}
    assert not ItemTexturesObject()._document.texture_data


# endregion

# region Entities


def test_entity_textures():
    from anvil.api.actors.client import EntityClient

    description = EntityClient("lamp_bug").description
    description.add_texture(blockbench=MODEL, color="body", mer="body_mer")
    assert description.textures == {
        "body": "textures/testns/test/actors/crystal_lamp/body"
    }
    with pytest.raises(TypeError):
        description.add_texture(MODEL, "body")


# endregion
