"""Tests for the typed texture atlases, sound files and pack manifests."""

import pytest

from anvil.api.blocks.blocks_json import BlocksJSONObject
from anvil.api.core.manifest import ManifestBP, ManifestRP
from anvil.api.sounds import (
    MusicDefinition,
    MusicInfo,
    ServerSoundDefinition,
    SoundDefinition,
    SoundEvent,
)
from anvil.api.textures import (
    FlipBookTexturesObject,
    ItemTexturesObject,
    TerrainTexturesObject,
)
from anvil.lib import config
from anvil.lib.jsonmodel.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    BlockSoundGroup,
    DurationInfoMode,
    EntitySoundEvent,
    SoundCategory,
)
from anvil.lib.lib import AnvilIO

jsonschema = pytest.importorskip("jsonschema")

SINGLETONS = (
    ItemTexturesObject,
    TerrainTexturesObject,
    FlipBookTexturesObject,
    SoundDefinition,
    ServerSoundDefinition,
    MusicDefinition,
    SoundEvent,
    BlocksJSONObject,
    ManifestRP,
    ManifestBP,
)


@pytest.fixture(autouse=True)
def fresh_files(monkeypatch, tmp_path):
    """Each test gets new singletons, in a project folder with one sound and one sprite."""
    for cls in SINGLETONS:
        monkeypatch.setattr(cls, "_instance", None)
    (tmp_path / "assets" / "sounds" / "mob").mkdir(parents=True)
    (tmp_path / "assets" / "sounds" / "mob" / "roar.ogg").write_bytes(b"")
    (tmp_path / "assets" / "textures" / "items").mkdir(parents=True)
    (tmp_path / "assets" / "textures" / "items" / "gem.png").write_bytes(b"")
    monkeypatch.chdir(tmp_path)
    with config.override(NAMESPACE="testns", PROJECT_NAME="proj"):
        yield


def _check(file):
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._document)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


# region Textures


def test_item_textures():
    atlas = ItemTexturesObject().add_item("gem", ["gem"])
    assert ItemTexturesObject() is atlas
    assert _check(atlas) == {
        "resource_pack_name": "proj",
        "texture_name": "atlas.items",
        "texture_data": {
            "testns:gem": {"textures": ["textures/testns/proj/items/gem"]}
        },
    }


def test_item_textures_refuse_a_missing_sprite():
    with pytest.raises(FileNotFoundError):
        ItemTexturesObject().add_item("ruby", ["ruby"])


def test_terrain_textures():
    atlas = TerrainTexturesObject()
    atlas.add_block("ore", "ores", ["ore", "ore_side"])
    atlas.add_block("dirt", "soil", ["dirt"], force_vanilla=True)
    atlas.add_block_variations("stone", "rock", [("stone_0", 1), ("stone_1", 2.5)])

    assert _check(atlas)["texture_data"] == {
        "testns:ore": {
            "textures": [
                "textures/testns/proj/blocks/ores/ore",
                "textures/testns/proj/blocks/ores/ore_side",
            ]
        },
        "dirt": {"textures": ["textures/testns/proj/blocks/soil/dirt"]},
        "testns:stone": {
            "textures": {
                "variations": [
                    {"path": "textures/testns/proj/blocks/rock/stone_0", "weight": 1},
                    {"path": "textures/testns/proj/blocks/rock/stone_1", "weight": 2.5},
                ]
            }
        },
    }


def test_terrain_variation_weight_is_checked():
    atlas = TerrainTexturesObject()
    atlas.add_block_variations("stone", "rock", [("stone_0", 0.01)])
    with pytest.raises(ValueError):
        atlas._document.__json__()


def test_flipbook_textures():
    flipbook = FlipBookTexturesObject()
    flipbook.add_block("lava", "fluid", "lava", [0, 1], ticks_per_frame=20)
    flipbook.add_block("fire", "fire", "fire", 4, replicate=2, blend_frames=False)

    assert _check(flipbook) == [
        {
            "atlas_tile": "testns:lava",
            "flipbook_texture": "textures/testns/proj/blocks/fluid/lava",
            "frames": [0, 1],
            "ticks_per_frame": 20,
        },
        {
            "atlas_tile": "testns:fire",
            "flipbook_texture": "textures/testns/proj/blocks/fire/fire",
            "frames": 4,
            "replicate": 2,
            "blend_frames": False,
        },
    ]


def test_flipbook_replicate_must_be_a_power_of_two():
    flipbook = FlipBookTexturesObject()
    flipbook.add_block("lava", "fluid", "lava", [0], replicate=3)
    with pytest.raises(ValueError):
        flipbook._document.__json__()


# endregion
# region Sounds


def test_sound_definitions():
    definitions = SoundDefinition()
    roar = definitions.sound_reference(
        "roar", SoundCategory.Hostile, max_distance=16, subtitle="subtitle.roar"
    )
    roar.add_sound("mob/roar").add_sound("mob/roar", volume=0.5, is_3d=False)

    assert _check(definitions)["sound_definitions"] == {
        "testns:roar": {
            "category": "hostile",
            "max_distance": 16,
            "subtitle": "subtitle.roar",
            "sounds": [
                "sounds/testns/mob/roar",
                {"name": "sounds/testns/mob/roar", "volume": 0.5, "is3D": False},
            ],
        }
    }


def test_sound_defined_again_replaces_the_first():
    definitions = SoundDefinition()
    definitions.sound_reference("roar", SoundCategory.Hostile).add_sound("mob/roar")
    definitions.sound_reference("roar", SoundCategory.Neutral)
    assert _check(definitions)["sound_definitions"] == {
        "testns:roar": {"category": "neutral"}
    }


def test_sound_file_must_exist():
    with pytest.raises(FileNotFoundError):
        SoundDefinition().sound_reference("x", SoundCategory.Block).add_sound("nope")


def test_music_definitions():
    MusicDefinition().music_definition("game", min_delay=2, max_delay=4)
    assert _check(MusicDefinition()) == {
        "game": {"event_name": "testns:music.game", "max_delay": 4, "min_delay": 2}
    }
    assert "testns:music.game" in _check(SoundDefinition())["sound_definitions"]


def test_server_sound_definitions():
    SoundDefinition().sound_reference(
        "battle",
        SoundCategory.Music,
        server_sound=MusicInfo(tags=["combat"], duration=8.0, artist="me"),
    )
    assert _check(ServerSoundDefinition())["minecraft:server_sound_definitions"] == [
        {
            "testns:battle": {
                "music_info": {"artist": "me"},
                "duration_info": {"tracking": "game_time", "duration": 8.0},
                "tags": ["combat"],
            }
        }
    ]
    assert DurationInfoMode.GameTime == "game_time"


def test_sound_events():
    events = SoundEvent()
    events.add_entity_event(
        "testns:crab", "crab_hurt", EntitySoundEvent.Hurt, SoundCategory.Hostile
    )
    events.add_entity_event(
        "testns:crab",
        "crab_baby",
        EntitySoundEvent.Ambient,
        SoundCategory.Hostile,
        variant_query="q.is_baby ? 'baby' : 'adult'",
        variant_map="baby",
    )
    events.add_block_event(
        "testns:ore", "ore_break", BlockSoundEvent.Break, pitch=1.0, volume=0.5
    )
    events.add_block_interactive_event(
        "testns:ore", "ore_step", BlockInteractiveSoundEvent.Step
    )
    events.add_individual_event("ambient.cave", SoundCategory.Ambient)
    events.add_individual_named_sound("ambient.loop", pitch=(1, 1.1))

    assert _check(events) == {
        "block_sounds": {
            "testns:ore": {
                "events": {
                    "break": {"sound": "testns:ore_break", "pitch": 1.0, "volume": 0.5}
                }
            }
        },
        "entity_sounds": {
            "entities": {
                "testns:crab": {
                    "events": {
                        "hurt": {
                            "sound": "testns:crab_hurt",
                            "pitch": [0.8, 1.2],
                            "volume": 1.0,
                        }
                    },
                    "variants": {
                        "key": "q.is_baby ? 'baby' : 'adult'",
                        "map": {
                            "baby": {
                                "events": {
                                    "ambient": {
                                        "sound": "testns:crab_baby",
                                        "pitch": [0.8, 1.2],
                                        "volume": 1.0,
                                    }
                                }
                            }
                        },
                    },
                }
            }
        },
        "individual_event_sounds": {
            "events": {"ambient.cave": {"sound": "testns:ambient.cave", "volume": 1.0}}
        },
        "individual_named_sounds": {
            "sounds": {
                "ambient.loop": {
                    "sound": "testns:ambient.loop",
                    "pitch": [1, 1.1],
                    "volume": 1.0,
                }
            }
        },
        "interactive_sounds": {
            "block_sounds": {
                "testns:ore": {
                    "events": {
                        "step": {
                            "sound": "testns:ore_step",
                            "pitch": [0.8, 1.2],
                            "volume": 1.0,
                        }
                    }
                }
            }
        },
    }
    assert set(_check(SoundDefinition())["sound_definitions"]) == {
        "testns:crab_hurt",
        "testns:crab_baby",
        "testns:ore_break",
        "testns:ore_step",
        "testns:ambient.cave",
        "testns:ambient.loop",
    }


def test_sound_event_variant_needs_its_variant():
    with pytest.raises(ValueError):
        SoundEvent().add_entity_event(
            "testns:crab",
            "crab_baby",
            EntitySoundEvent.Ambient,
            SoundCategory.Hostile,
            variant_query="q.is_baby",
        )


def test_blocks_json():
    blocks = BlocksJSONObject()
    blocks.add_block("testns:ore")
    blocks.add_block("testns:plank", BlockSoundGroup.Wood)
    blocks.add_block("testns:ore", "stone")
    assert _check(blocks) == {
        "format_version": "1.21.40",
        "testns:ore": {"sound": "stone"},
        "testns:plank": {"sound": "wood"},
    }


# endregion
# region Manifests


def test_manifests():
    rp, bp = ManifestRP(), ManifestBP()
    assert ManifestRP() is rp and rp is not bp

    rp_json, bp_json = _check(rp), _check(bp)
    assert rp_json["format_version"] == 3
    assert rp_json["header"]["uuid"] == bp_json["dependencies"][0]["uuid"]
    assert bp_json["header"]["uuid"] == rp_json["dependencies"][0]["uuid"]
    assert rp_json["modules"][0]["type"] == "resources"
    assert bp_json["modules"][0]["type"] == "data"
    assert rp_json["header"]["name"] == "pack.name"
    assert "settings" not in rp_json


def test_manifest_settings():
    settings = ManifestRP().settings
    settings.label("Options").toggle("wind", "Wind", False)
    settings.slider("chance", "Chance", 0, 100, 5, 20)
    ManifestRP().settings.label("More").dropdown(
        "speed", "Speed", [("slow", "Slow"), ("fast", "Fast")], "fast"
    )

    assert _check(ManifestRP())["settings"] == [
        {"type": "label", "text": "pack.manifest.setting.label_0"},
        {
            "type": "toggle",
            "name": "testns:wind",
            "text": "pack.manifest.setting.toggle_0",
            "default": False,
        },
        {
            "type": "slider",
            "name": "testns:chance",
            "text": "pack.manifest.setting.slider_0",
            "min": 0,
            "max": 100,
            "step": 5,
            "default": 20,
        },
        {"type": "label", "text": "pack.manifest.setting.label_1"},
        {
            "type": "dropdown",
            "name": "testns:speed",
            "text": "pack.manifest.setting.dropdown_0",
            "options": [
                {"name": "slow", "text": "pack.manifest.setting.dropdown_0.option_0"},
                {"name": "fast", "text": "pack.manifest.setting.dropdown_0.option_1"},
            ],
            "default": "fast",
        },
    ]
    assert ManifestRP()._setting_names("toggle") == ["testns:wind"]
    assert ManifestRP()._dropdown_options("testns:speed") == ["slow", "fast"]
    assert ManifestRP()._dropdown_options("testns:wind") is None


@pytest.mark.parametrize(
    "build",
    [
        lambda settings: settings.slider("s", "S", 10, 0, 1, 5),
        lambda settings: settings.slider("s", "S", 0, 10, 0, 5),
        lambda settings: settings.slider("s", "S", 0, 10, 1, 50),
        lambda settings: settings.dropdown("d", "D", [("a", "A")], "b"),
        lambda settings: settings.dropdown("d", "D", [], "b"),
    ],
)
def test_manifest_settings_are_checked(build):
    build(ManifestBP().settings)
    with pytest.raises(ValueError):
        ManifestBP()._document.__json__()


def test_manifest_setting_names_are_unique():
    settings = ManifestBP().settings.toggle("same", "A")
    with pytest.raises(ValueError):
        settings.slider("same", "B", 0, 1, 1, 0)


# endregion
