import sys
import os
from unittest.mock import MagicMock

# Setup mock CONFIG in config module, schemas, and pbr module to prevent exits and ensure PBR is enabled
mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"
mock_config.PBR = True
mock_config.NAMESPACE = "testns"
mock_config.PROJECT_NAME = "test_project"

import anvil.lib.config
anvil.lib.config.CONFIG = mock_config

import anvil.lib.schemas
anvil.lib.schemas.CONFIG = mock_config

import anvil.api.pbr.texture_set
anvil.api.pbr.texture_set.CONFIG = mock_config

import anvil.api.pbr.fog
anvil.api.pbr.fog.CONFIG = mock_config

import pytest
from anvil.api.core.types import RGB
from anvil.api.pbr.texture_set import KeyFrame
from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.shadow import ShadowSettings
from anvil.api.pbr.color_grading import ColorGradingSettings
from anvil.api.pbr.lighting import LightingSettings, LocalLighting
from anvil.api.pbr.fallback import PBRFallback
from anvil.api.pbr.fog import Fog

def test_keyframe_serialization():
    # Value keyframes
    kf_val = [KeyFrame(0.0, 1.5), KeyFrame(1.0, 2.5)]
    assert KeyFrame.keyframe_dict(kf_val) == {"0.0": 1.5, "1.0": 2.5}
    
    # Color keyframes - defaults to input normalization (RGB255) when passed as tuples
    kf_color = [KeyFrame(0.0, (255, 0, 0)), KeyFrame(1.0, (0, 255, 0))]
    assert KeyFrame.keyframe_dict(kf_color) == {"0.0": (255, 0, 0), "1.0": (0, 255, 0)}

    # Color keyframes with target type RGB
    assert KeyFrame.keyframe_dict(kf_color, RGB) == {"0.0": (1.0, 0.0, 0.0), "1.0": (0.0, 1.0, 0.0)}

def test_atmospheric_settings():
    settings = AtmosphericSettings()
    
    # Keyframed and simple values for blend stops
    settings.horizon_blend_stops(
        min=0.1,
        start=[KeyFrame(0.0, 0.2), KeyFrame(1.0, 0.3)],
        mie_start=0.4,
        max=[KeyFrame(0.0, 0.5), KeyFrame(1.0, 0.6)]
    )
    assert settings._content["minecraft:atmosphere_settings"]["horizon_blend_stops"] == {
        "min": 0.1,
        "start": {"0.0": 0.2, "1.0": 0.3},
        "mie_start": 0.4,
        "max": {"0.0": 0.5, "1.0": 0.6}
    }
    
    # Rayleigh and Mie strengths
    settings.rayleigh_strength(0.5)
    assert settings._content["minecraft:atmosphere_settings"]["rayleigh_strength"] == 0.5
    settings.rayleigh_strength([KeyFrame(0.0, 0.1)])
    assert settings._content["minecraft:atmosphere_settings"]["rayleigh_strength"] == {"0.0": 0.1}
    
    settings.sun_mie_strength(0.8)
    assert settings._content["minecraft:atmosphere_settings"]["sun_mie_strength"] == 0.8
    settings.sun_mie_strength([KeyFrame(0.0, 0.2)])
    assert settings._content["minecraft:atmosphere_settings"]["sun_mie_strength"] == {"0.0": 0.2}

    settings.moon_mie_strength(0.7)
    assert settings._content["minecraft:atmosphere_settings"]["moon_mie_strength"] == 0.7
    settings.moon_mie_strength([KeyFrame(0.0, 0.3)])
    assert settings._content["minecraft:atmosphere_settings"]["moon_mie_strength"] == {"0.0": 0.3}

    settings.sun_glare_shape(1.2)
    assert settings._content["minecraft:atmosphere_settings"]["sun_glare_shape"] == 1.2
    settings.sun_glare_shape([KeyFrame(0.0, 1.1)])
    assert settings._content["minecraft:atmosphere_settings"]["sun_glare_shape"] == {"0.0": 1.1}
    
    # Sky zenith and horizon colors
    settings.sky_zenith_color([255, 0, 0])
    assert settings._content["minecraft:atmosphere_settings"]["sky_zenith_color"] == (255, 0, 0)
    settings.sky_zenith_color([KeyFrame(0.0, [255, 255, 255])])
    assert settings._content["minecraft:atmosphere_settings"]["sky_zenith_color"] == {"0.0": (255, 255, 255)}

    settings.sky_horizon_color([0, 255, 绿 := 0])
    assert settings._content["minecraft:atmosphere_settings"]["sky_horizon_color"] == (0, 255, 0)
    settings.sky_horizon_color([KeyFrame(0.0, [0, 0, 0])])
    assert settings._content["minecraft:atmosphere_settings"]["sky_horizon_color"] == {"0.0": (0, 0, 0)}

def test_fog_settings_path_and_serialization():
    settings = FogSettings()
    # Path should end with 'fogs' (not 'fog')
    assert settings._path == os.path.join("dummy_rp_path", "fogs")
    assert settings._name == "fog"
    
    settings.water_density(0.5, uniform=True)
    assert settings._content["minecraft:fog_settings"]["volumetric"]["density"]["water"] == {
        "max_density": 0.5,
        "uniform": True,
    }
    
    settings.air_density(0.8, zero_density_height=50.0, max_density_height=10.0)
    assert settings._content["minecraft:fog_settings"]["volumetric"]["density"]["air"] == {
        "max_density": 0.8,
        "uniform": False,
        "zero_density_height": 50.0,
        "max_density_height": 10.0,
    }

def test_shadow_settings():
    settings = ShadowSettings()
    # Path should end with 'shadows' and filename should be 'global' (resulting in shadows/global.json)
    assert settings._path == os.path.join("dummy_rp_path", "shadows")
    assert settings._name == "global"
    
    settings.shadow_style("soft_shadows", 32)
    assert settings._content["minecraft:shadow_settings"]["shadow_style"] == "soft_shadows"
    assert settings._content["minecraft:shadow_settings"]["texel_size"] == 32

def test_color_grading_settings():
    settings = ColorGradingSettings()
    
    # Check temperature grade writes to 'temperature' key
    settings.temperature_grade(temp_value=5000.0, type="color_temperature")
    temp_node = settings._content["minecraft:color_grading_settings"]["color_grading"]["temperature"]
    assert temp_node["enabled"] is True
    assert temp_node["temperature"] == 5000.0
    assert temp_node["type"] == "color_temperature"
    
    # Ensure legacy 'temperature_grade' key is not present
    assert "temperature_grade" not in settings._content["minecraft:color_grading_settings"]["color_grading"]

def test_lighting_settings():
    settings = LightingSettings()
    
    # Test orbital_lights with mix of values and keyframes
    settings.orbital_lights(
        sun_illuminance=[KeyFrame(0.0, 1000.0)],
        sun_color=[255, 255, 255],
        moon_illuminance=200.0,
        moon_color=[KeyFrame(0.5, [0, 0, 255])],
        orbital_offset_degrees=45.0
    )
    directional = settings._content["minecraft:lighting_settings"]["directional_lights"]["orbital"]
    assert directional["sun"]["illuminance"] == {"0.0": 1000.0}
    assert directional["sun"]["color"] == (255, 255, 255)
    assert directional["moon"]["illuminance"] == 200.0
    assert directional["moon"]["color"] == {"0.5": (0, 0, 255)}
    assert directional["orbital_offset_degrees"] == 45.0
    
    # Test ambient with keyframes
    settings.ambient(
        illuminance=[KeyFrame(0.0, 2.0), KeyFrame(1.0, 3.0)],
        color=[KeyFrame(0.0, [255, 0, 0])]
    )
    ambient_node = settings._content["minecraft:lighting_settings"]["ambient"]
    assert ambient_node["illuminance"] == {"0.0": 2.0, "1.0": 3.0}
    assert ambient_node["color"] == {"0.0": (255, 0, 0)}
    
    # Test sky with keyframes
    settings.sky(
        intensity=[KeyFrame(0.0, 0.5), KeyFrame(1.0, 0.8)]
    )
    sky_node = settings._content["minecraft:lighting_settings"]["sky"]
    assert sky_node["intensity"] == {"0.0": 0.5, "1.0": 0.8}

def test_local_lighting():
    settings = LocalLighting()
    
    # Test add_local_light (uses format version 1.21.120+ schema key 'minecraft:local_light_settings')
    settings.add_local_light("minecraft:glowstone", [255, 200, 150], "point_light")
    assert settings._content["minecraft:local_light_settings"]["minecraft:glowstone"] == {
        "light_color": (255, 200, 150),
        "light_type": "point_light",
    }
    
    # Test legacy add_point_light maps to static_light
    settings.add_point_light("minecraft:torch", [255, 255, 255])
    assert settings._content["minecraft:local_light_settings"]["minecraft:torch"] == {
        "light_color": (255, 255, 255),
        "light_type": "static_light",
    }

def test_pbr_fallback():
    fallback = PBRFallback()
    
    # Test float tuple input
    fallback.block_fallback((0.0, 0.0, 0.8, 0.0))
    assert fallback._content["minecraft:pbr_fallback_settings"]["blocks"] == {
        "global_metalness_emissive_roughness_subsurface": (0, 0, 204, 0)
    }
    
    # Test hex string input
    fallback.actors_fallback("#0000cc00")
    assert fallback._content["minecraft:pbr_fallback_settings"]["actors"] == {
        "global_metalness_emissive_roughness_subsurface": (0, 0, 204, 0)
    }
    
    # Test integer tuple input
    fallback.particles_fallback((0, 0, 204, 0))
    assert fallback._content["minecraft:pbr_fallback_settings"]["particles"] == {
        "global_metalness_emissive_roughness_subsurface": (0, 0, 204, 0)
    }

def test_combined_fog():
    from anvil.api.core.enums import FogCameraLocation, RenderDistanceType
    
    fog = Fog("test_fog")
    # Set vanilla distance settings
    fog.add_distance_location(
        color="#08c2e5",
        fog_start=20,
        fog_end=120,
        render_distance_type=RenderDistanceType.Fixed,
        camera_location=FogCameraLocation.Air
    )
    
    # Set volumetric settings
    fog.water_density(0.001, uniform=True)
    fog.air_density(0.083, zero_density_height=135.0, max_density_height=82.0)
    fog.media_coefficients(
        water_scattering=(0.01, 0.05, 0.07),
        water_absorption=(0.012, 0.008, 0.0),
        air_scattering=(0.0325, 0.0335, 0.0435),
        air_absorption=(0.017, 0.007, 0.0)
    )
    fog.henyey_greenstein_g(air_g=0.1, water_g=0.34)
    
    fog.queue()
    
    # Verify both distance and volumetric keys are populated
    fog_settings = fog._content["minecraft:fog_settings"]
    assert "distance" in fog_settings
    assert "volumetric" in fog_settings
    assert fog_settings["distance"]["air"]["fog_color"] == "#08c2e5"
    assert fog_settings["distance"]["air"]["fog_start"] == 20
    assert fog_settings["distance"]["air"]["fog_end"] == 120
    assert fog_settings["volumetric"]["density"]["water"]["max_density"] == 0.001
    assert fog_settings["volumetric"]["density"]["air"]["max_density"] == 0.083
    assert fog_settings["volumetric"]["media_coefficients"]["water"]["scattering"] == (0.01, 0.05, 0.07)
    assert fog_settings["volumetric"]["henyey_greenstein_g"]["air"]["henyey_greenstein_g"] == 0.1

def test_fog_disabled_pbr():
    mock_config.PBR = False
    try:
        fog = Fog("test_fog_no_pbr")
        
        with pytest.raises(RuntimeError):
            fog.water_density(0.5)
            
        with pytest.raises(RuntimeError):
            fog.air_density(0.5)
            
        with pytest.raises(RuntimeError):
            fog.media_coefficients()
            
        with pytest.raises(RuntimeError):
            fog.henyey_greenstein_g()
    finally:
        mock_config.PBR = True


def test_fog_density_height_validation():
    fog = Fog("test_fog_height_val")
    with pytest.raises(ValueError):
        fog.air_density(0.5, uniform=False, zero_density_height=10.0, max_density_height=50.0)
    with pytest.raises(ValueError):
        fog.water_density(0.5, uniform=False, zero_density_height=10.0, max_density_height=50.0)


def test_textureset_vanilla_override():
    from anvil.api.pbr.texture_set import TextureSet, TextureComponents
    from unittest.mock import patch

    # Mock _Blockbench
    with patch("anvil.api.pbr.texture_set._Blockbench") as MockBlockbench:
        mock_bb = MockBlockbench.return_value
        
        tset = TextureSet("test_block", "blocks", overriding_vanilla=True)
        assert tset._overriding_vanilla is True
        assert tset._path == os.path.join("dummy_rp_path", "textures", "blocks")

        components = TextureComponents(
            color="test_color",
            normal="test_normal",
            mer="test_mer"
        )
        
        tset.set_vanilla_texture("test_model", components, subfolder="deepslate")
        
        # Verify blockbench was instantiated with test_model and blocks target
        MockBlockbench.assert_called_once_with("test_model", "blocks")
        
        # Verify queue_texture was called for all textures with correct dest_dir
        expected_dest_dir = os.path.join("dummy_rp_path", "textures", "blocks", "deepslate")
        
        mock_bb.textures.queue_texture.assert_any_call("test_color", dest_dir=expected_dest_dir)
        mock_bb.textures.queue_texture.assert_any_call("test_normal", dest_dir=expected_dest_dir)
        mock_bb.textures.queue_texture.assert_any_call("test_mer", dest_dir=expected_dest_dir)
        
        # Verify content update
        assert tset._content["minecraft:texture_set"]["color"] == "test_color"
        assert tset._content["minecraft:texture_set"]["normal"] == "test_normal"
        assert tset._content["minecraft:texture_set"]["metalness_emissive_roughness"] == "test_mer"


