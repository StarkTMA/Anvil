import base64
import io

import orjson
import pytest
from PIL import Image

from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.color_grading import ColorGradingSettings
from anvil.api.pbr.fallback import PBRFallback
from anvil.api.pbr.fog import Fog, FogSettings
from anvil.api.pbr.lighting import LightingSettings, LocalLighting
from anvil.api.pbr.shadow import ShadowSettings
from anvil.api.pbr.water import WaterSettings
from anvil.lib import config
from anvil.lib.format_versions import (
    PBR_FALLBACK_SETTINGS_VERSION,
    SHADOW_SETTINGS_VERSION,
)
from anvil.lib.jsonmodel import KeyFramed, KeyFramedColor
from anvil.lib.lib import AnvilIO


@pytest.fixture(autouse=True)
def pbr_project():
    with config.override(PBR=True, NAMESPACE="testns"):
        yield


def test_keyframe_serialization():
    kf_val = [(0.0, 1.5), (1.0, 2.5)]
    assert KeyFramed().encode(kf_val) == {"0.0": 1.5, "1.0": 2.5}
    assert KeyFramed().encode(1.5) == 1.5

    kf_color = [(0.0, (255, 0, 0)), (1.0, "#00FF00")]
    assert KeyFramedColor().encode(kf_color) == {
        "0.0": (255, 0, 0),
        "1.0": "#00ff00",
    }
    assert KeyFramedColor().encode((255, 0, 0)) == (255, 0, 0)


def _exported(file, key):
    return AnvilIO._normalize_json_like(file._document)[key]


def test_atmospheric_settings():
    settings = AtmosphericSettings()

    # Keyframed and simple values for blend stops
    settings.horizon_blend_stops(
        min=0.1,
        start=[(0.0, 0.2), (1.0, 0.3)],
        mie_start=0.4,
        max=[(0.0, 0.5), (1.0, 0.6)],
    )
    assert _exported(settings, "minecraft:atmosphere_settings")[
        "horizon_blend_stops"
    ] == {
        "min": 0.1,
        "start": {"0.0": 0.2, "1.0": 0.3},
        "mie_start": 0.4,
        "max": {"0.0": 0.5, "1.0": 0.6},
    }

    # Rayleigh and Mie strengths
    settings.rayleigh_strength(0.5)
    assert (
        _exported(settings, "minecraft:atmosphere_settings")["rayleigh_strength"] == 0.5
    )
    settings.rayleigh_strength([(0.0, 0.1)])
    assert _exported(settings, "minecraft:atmosphere_settings")[
        "rayleigh_strength"
    ] == {"0.0": 0.1}

    settings.sun_mie_strength(0.8)
    assert (
        _exported(settings, "minecraft:atmosphere_settings")["sun_mie_strength"] == 0.8
    )
    settings.sun_mie_strength([(0.0, 0.2)])
    assert _exported(settings, "minecraft:atmosphere_settings")["sun_mie_strength"] == {
        "0.0": 0.2
    }

    settings.moon_mie_strength(0.7)
    assert (
        _exported(settings, "minecraft:atmosphere_settings")["moon_mie_strength"] == 0.7
    )
    settings.moon_mie_strength([(0.0, 0.3)])
    assert _exported(settings, "minecraft:atmosphere_settings")[
        "moon_mie_strength"
    ] == {"0.0": 0.3}

    settings.sun_glare_shape(1.2)
    assert (
        _exported(settings, "minecraft:atmosphere_settings")["sun_glare_shape"] == 1.2
    )
    settings.sun_glare_shape([(0.0, 1.1)])
    assert _exported(settings, "minecraft:atmosphere_settings")["sun_glare_shape"] == {
        "0.0": 1.1
    }

    # Sky zenith and horizon colors
    settings.sky_zenith_color([255, 0, 0])
    assert _exported(settings, "minecraft:atmosphere_settings")["sky_zenith_color"] == [
        255,
        0,
        0,
    ]
    settings.sky_zenith_color([(0.0, [255, 255, 255])])
    assert _exported(settings, "minecraft:atmosphere_settings")["sky_zenith_color"] == {
        "0.0": [255, 255, 255]
    }

    settings.sky_horizon_color([0, 255, 0])
    assert _exported(settings, "minecraft:atmosphere_settings")[
        "sky_horizon_color"
    ] == [
        0,
        255,
        0,
    ]
    settings.sky_horizon_color([(0.0, [0, 0, 0])])
    assert _exported(settings, "minecraft:atmosphere_settings")[
        "sky_horizon_color"
    ] == {"0.0": [0, 0, 0]}


def test_fog_settings_path_and_serialization():
    settings = FogSettings()
    # Path should end with 'fogs' (not 'fog')
    assert settings._path == config.CONFIG.RP_PATH / "fogs"
    assert settings.identifier.name == "fog"

    settings.water_density(0.5, uniform=True)
    assert _exported(settings, "minecraft:fog_settings")["volumetric"]["density"][
        "water"
    ] == {
        "max_density": 0.5,
        "uniform": True,
    }

    settings.air_density(0.8, zero_density_height=50.0, max_density_height=10.0)
    assert _exported(settings, "minecraft:fog_settings")["volumetric"]["density"][
        "air"
    ] == {
        "max_density": 0.8,
        "uniform": False,
        "zero_density_height": 50.0,
        "max_density_height": 10.0,
    }


def test_shadow_settings():
    settings = ShadowSettings()
    # Path should end with 'shadows' and filename should be 'global' (resulting in shadows/global.json)
    assert settings._path == config.CONFIG.RP_PATH / "shadows"
    assert settings._file_name == "global"

    assert AnvilIO._normalize_json_like(settings._document) == {
        "format_version": SHADOW_SETTINGS_VERSION,
        "minecraft:shadow_settings": {},
    }

    settings.shadow_style("soft_shadows", 32)
    assert AnvilIO._normalize_json_like(settings._document) == {
        "format_version": SHADOW_SETTINGS_VERSION,
        "minecraft:shadow_settings": {"shadow_style": "soft_shadows", "texel_size": 32},
    }


def test_shadow_settings_checked_on_export():
    settings = ShadowSettings().shadow_style("blocky_shadows", 0)
    with pytest.raises(ValueError):
        AnvilIO._normalize_json_like(settings._document)

    settings = ShadowSettings().shadow_style("sharp_shadows")
    with pytest.raises(ValueError):
        AnvilIO._normalize_json_like(settings._document)


def test_color_grading_settings():
    settings = ColorGradingSettings()

    # Check temperature grade writes to 'temperature' key
    settings.temperature_grade(temp_value=5000.0, type="color_temperature")
    temp_node = _exported(settings, "minecraft:color_grading_settings")[
        "color_grading"
    ]["temperature"]
    assert temp_node["enabled"] is True
    assert temp_node["temperature"] == 5000.0
    assert temp_node["type"] == "color_temperature"

    # Ensure legacy 'temperature_grade' key is not present
    assert (
        "temperature_grade"
        not in _exported(settings, "minecraft:color_grading_settings")["color_grading"]
    )


def test_lighting_settings():
    settings = LightingSettings()

    # Test orbital_lights with mix of values and keyframes
    settings.orbital_lights(
        sun_illuminance=[(0.0, 1000.0)],
        sun_color=[255, 255, 255],
        moon_illuminance=200.0,
        moon_color=[(0.5, [0, 0, 255])],
        orbital_offset_degrees=45.0,
    )
    directional = _exported(settings, "minecraft:lighting_settings")[
        "directional_lights"
    ]["orbital"]
    assert directional["sun"]["illuminance"] == {"0.0": 1000.0}
    assert directional["sun"]["color"] == [255, 255, 255]
    assert directional["moon"]["illuminance"] == 200.0
    assert directional["moon"]["color"] == {"0.5": [0, 0, 255]}
    assert directional["orbital_offset_degrees"] == 45.0

    # Test ambient with keyframes
    settings.ambient(
        illuminance=[(0.0, 2.0), (1.0, 3.0)],
        color=[(0.0, [255, 0, 0])],
    )
    ambient_node = _exported(settings, "minecraft:lighting_settings")["ambient"]
    assert ambient_node["illuminance"] == {"0.0": 2.0, "1.0": 3.0}
    assert ambient_node["color"] == {"0.0": [255, 0, 0]}

    # Test sky with keyframes
    settings.sky(intensity=[(0.0, 0.5), (1.0, 0.8)])
    sky_node = _exported(settings, "minecraft:lighting_settings")["sky"]
    assert sky_node["intensity"] == {"0.0": 0.5, "1.0": 0.8}


def test_local_lighting():
    settings = LocalLighting()
    settings.add_local_light("minecraft:glowstone", [255, 200, 150], "point_light")
    settings.add_point_light("minecraft:torch", "#ffffff")
    assert _exported(settings, "minecraft:local_light_settings") == {
        "minecraft:glowstone": {
            "light_color": [255, 200, 150],
            "light_type": "point_light",
        },
        "minecraft:torch": {"light_color": "#ffffff", "light_type": "static_light"},
    }
    assert settings.lights["minecraft:torch"].light_type == "static_light"
    with pytest.raises(ValueError):
        settings.add_local_light("minecraft:lamp", "#fff", "spot_light")
        settings._document.__json__()
    with config.override(PBR=False):
        with pytest.raises(ValueError):
            LocalLighting()


def test_pbr_fallback():
    fallback = PBRFallback()
    assert fallback._path == config.CONFIG.RP_PATH / "pbr"
    assert AnvilIO._normalize_json_like(fallback._document) == {
        "format_version": PBR_FALLBACK_SETTINGS_VERSION,
        "minecraft:pbr_fallback_settings": {},
    }

    fallback.block_fallback((0.0, 0.0, 0.8, 0.0))
    fallback.actors_fallback("#0000cc00")
    fallback.particles_fallback((0, 0, 204, 0))
    mers = {"global_metalness_emissive_roughness_subsurface": [0, 0, 204, 0]}
    assert AnvilIO._normalize_json_like(fallback._document) == {
        "format_version": PBR_FALLBACK_SETTINGS_VERSION,
        "minecraft:pbr_fallback_settings": {
            "actors": mers,
            "blocks": mers,
            "particles": mers,
        },
    }


def test_pbr_fallback_checked_on_export():
    fallback = PBRFallback().items_fallback("not a color")
    with pytest.raises(ValueError):
        AnvilIO._normalize_json_like(fallback._document)


def test_pbr_fallback_mer_has_no_alpha():
    fallback = PBRFallback()
    blocks = fallback._document.settings.blocks
    blocks.set_global_metalness_emissive_roughness("#ff8000")
    exported = AnvilIO._normalize_json_like(fallback._document)
    assert exported["minecraft:pbr_fallback_settings"]["blocks"] == {
        "global_metalness_emissive_roughness": [255, 128, 0]
    }

    blocks.set_global_metalness_emissive_roughness("#ff8000ff")
    with pytest.raises(ValueError, match="alpha"):
        AnvilIO._normalize_json_like(fallback._document)

    blocks.set_global_metalness_emissive_roughness((255, 128, 0, 255))
    with pytest.raises((TypeError, ValueError)):
        AnvilIO._normalize_json_like(fallback._document)


def test_combined_fog():
    from anvil.lib.jsonmodel.enums import FogCameraLocation, RenderDistanceType

    fog = Fog("test_fog")
    # Set vanilla distance settings
    fog.add_distance_location(
        color="#08c2e5",
        fog_start=20,
        fog_end=120,
        render_distance_type=RenderDistanceType.Fixed,
        camera_location=FogCameraLocation.Air,
    )

    # Set volumetric settings
    fog.water_density(0.001, uniform=True)
    fog.air_density(0.083, zero_density_height=135.0, max_density_height=82.0)
    fog.media_coefficients(
        water_scattering=[0.01, 0.05, 0.07],
        water_absorption=[0.012, 0.008, 0.0],
        air_scattering=[0.0325, 0.0335, 0.0435],
        air_absorption=[0.017, 0.007, 0.0],
    )
    fog.henyey_greenstein_g(air_g=0.1, water_g=0.34)

    fog.queue()

    # Verify both distance and volumetric keys are populated
    fog_settings = _exported(fog, "minecraft:fog_settings")
    assert "distance" in fog_settings
    assert "volumetric" in fog_settings
    assert fog_settings["distance"]["air"]["fog_color"] == "#08c2e5"
    assert fog_settings["distance"]["air"]["fog_start"] == 20
    assert fog_settings["distance"]["air"]["fog_end"] == 120
    assert fog_settings["volumetric"]["density"]["water"]["max_density"] == 0.001
    assert fog_settings["volumetric"]["density"]["air"]["max_density"] == 0.083
    assert fog_settings["volumetric"]["media_coefficients"]["water"]["scattering"] == [
        0.01,
        0.05,
        0.07,
    ]
    assert (
        fog_settings["volumetric"]["henyey_greenstein_g"]["air"]["henyey_greenstein_g"]
        == 0.1
    )


def test_fog_transition():
    from anvil.lib.jsonmodel.enums import FogCameraLocation, RenderDistanceType

    fog = Fog("transition")
    fog.add_distance_location(
        "#44aff5", 0, 60, RenderDistanceType.Fixed, FogCameraLocation.Water
    ).set_transition_fog("#44aff5", 0.0, 0.01, RenderDistanceType.Fixed, max_seconds=30)
    assert _exported(fog, "minecraft:fog_settings")["distance"]["water"] == {
        "fog_start": 0,
        "fog_end": 60,
        "fog_color": "#44aff5",
        "render_distance_type": "fixed",
        "transition_fog": {
            "init_fog": {
                "fog_start": 0.0,
                "fog_end": 0.01,
                "fog_color": "#44aff5",
                "render_distance_type": "fixed",
            },
            "max_seconds": 30,
        },
    }

    with pytest.raises(ValueError):
        fog.add_distance_location("#ffffff", 0, 1).set_transition_fog("#ffffff", 0, 1)


def test_pbr_values_checked_on_export():
    with pytest.raises(ValueError):
        _exported(WaterSettings("w").waves(octaves=0), "minecraft:water_settings")
    with pytest.raises(ValueError):
        _exported(Fog("f").air_density(2.0), "minecraft:fog_settings")
    fog = Fog("ends")
    fog.add_distance_location("#ffffff", 10, 5)
    with pytest.raises(ValueError):
        _exported(fog, "minecraft:fog_settings")


def test_keyframed_ranges_checked_on_export():
    lighting = LightingSettings("ranges")
    lighting.ambient([(0.0, 1.0), (1.0, 6.0)], "#ffffff")
    with pytest.raises(ValueError, match="_Ambient.illuminance"):
        _exported(lighting, "minecraft:lighting_settings")

    lighting = LightingSettings("sky")
    lighting.sky(0.05)
    with pytest.raises(ValueError, match="_Sky.intensity"):
        _exported(lighting, "minecraft:lighting_settings")


def test_keyframe_time_checked_on_export():
    settings = AtmosphericSettings("late").rayleigh_strength([(1.2, 1.0)])
    with pytest.raises(ValueError, match=r"rayleigh_strength\[0\] time"):
        _exported(settings, "minecraft:atmosphere_settings")


def test_settings_identifiers_are_checked():
    from anvil.api.pbr.cubemap import CubeMapSettings
    from anvil.lib.jsonmodel import Identifier

    lighting = LightingSettings("sunset")
    identifier = lighting._document.settings.description
    assert isinstance(identifier, Identifier)
    assert identifier == "testns:sunset"
    assert identifier.namespace == "testns"
    assert lighting.identifier is identifier

    cubemap = CubeMapSettings()
    assert cubemap._document.settings.description.is_vanilla

    with pytest.raises(ValueError, match="custom identifier"):
        WaterSettings("minecraft:clear_water")
    with pytest.raises(ValueError, match="custom identifier"):
        CubeMapSettings("minecraft:sky")


def test_fog_disabled_pbr():
    with config.override(PBR=False):
        fog = Fog("test_fog_no_pbr")

        with pytest.raises(ValueError):
            fog.water_density(0.5)

        with pytest.raises(ValueError):
            fog.air_density(0.5)

        with pytest.raises(ValueError):
            fog.media_coefficients()

        with pytest.raises(ValueError):
            fog.henyey_greenstein_g()


def test_fog_density_height_validation():
    fog = Fog("test_fog_height_val")
    with pytest.raises(ValueError):
        fog.air_density(
            0.5, uniform=False, zero_density_height=10.0, max_density_height=50.0
        )
    with pytest.raises(ValueError):
        fog.water_density(
            0.5, uniform=False, zero_density_height=10.0, max_density_height=50.0
        )


@pytest.fixture
def test_model(tmp_path, monkeypatch):
    """A Blockbench model `test_model` with blank textures, in a project at tmp_path."""
    from anvil.lib.blockbench import _Blockbench

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(_Blockbench, "_loaded_blockbench_models", {})
    image = io.BytesIO()
    Image.new("RGBA", (16, 16)).save(image, format="PNG")
    source = "data:image/png;base64," + base64.b64encode(image.getvalue()).decode()
    names = ["test_color", "test_normal", "test_mer", "test_height", "test_mers"]
    model = {
        "meta": {"format_version": "5.0", "model_format": "bedrock"},
        "model_identifier": "test_model",
        "resolution": {"width": 16, "height": 16},
        "elements": [],
        "outliner": [],
        "textures": [{"name": f"{name}.png", "source": source} for name in names],
    }
    folder = tmp_path / "assets" / "bbmodels"
    folder.mkdir(parents=True)
    (folder / "test_model.bbmodel").write_bytes(orjson.dumps(model))
    with config.override(_LOCAL_EXPORT=True):
        yield "test_model"


def test_textureset_vanilla_override(test_model):
    from anvil.api.pbr.texture_set import TextureComponents, TextureSet

    tset = TextureSet("test_block", "blocks", overriding_vanilla=True)
    assert tset._overriding_vanilla is True
    assert tset._path == config.CONFIG.RP_PATH / "textures" / "blocks"

    components = TextureComponents(
        color="test_color", normal="test_normal", mer="test_mer"
    )
    tset.set_vanilla_texture(test_model, components, subfolder="deepslate")

    folder = config.CONFIG.RP_PATH / "textures" / "blocks" / "deepslate"
    assert tset._blockbench._source == "blocks"
    assert tset._blockbench.textures._queued_textures == {
        "test_color": folder,
        "test_normal": folder,
        "test_mer": folder,
    }

    texture_set = _exported(tset, "minecraft:texture_set")
    assert texture_set["color"] == "test_color"
    assert texture_set["normal"] == "test_normal"
    assert texture_set["metalness_emissive_roughness"] == "test_mer"


def _texture_set_files(tset):
    return list(tset._path.glob("*.texture_set.json"))


def test_textureset_pbr_disabled_color_only(test_model):
    from anvil.api.pbr.texture_set import TextureComponents, TextureSet

    with config.override(PBR=False):
        tset = TextureSet("test_block", "blocks")
        tset.set_blockbench_textures(test_model, TextureComponents(color="test_color"))
        tset.__export__()
        assert _texture_set_files(tset) == []


def test_textureset_pbr_disabled_aux_map_raises_error(test_model):
    from anvil.api.pbr.texture_set import TextureComponents, TextureSet

    with config.override(PBR=False):
        tset = TextureSet("test_block", "blocks")
        for maps in (
            {"normal": "test_normal"},
            {"height": "test_height"},
            {"mer": "test_mer"},
            {"mers": "test_mers"},
        ):
            with pytest.raises(ValueError, match="PBR maps"):
                tset.set_blockbench_textures(
                    test_model, TextureComponents(color="test_color", **maps)
                )


def test_textureset_pbr_enabled_export(test_model):
    from anvil.api.pbr.texture_set import TextureComponents, TextureSet

    tset = TextureSet("test_block", "blocks")
    components = TextureComponents(color="test_color", normal="test_normal")
    tset.set_blockbench_textures(test_model, components)
    tset.__export__()
    assert len(_texture_set_files(tset)) == 1
