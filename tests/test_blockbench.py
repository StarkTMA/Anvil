import os
import tempfile
import base64
from unittest.mock import MagicMock
from PIL import Image
import io

# Setup mock CONFIG in config module, schemas, etc.
mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"
mock_config.NAMESPACE = "testns"
mock_config.PROJECT_NAME = "test_project"

import anvil.lib.config
anvil.lib.config.CONFIG = mock_config

from anvil.lib.blockbench import _TexturesManager

def test_texture_layer_blending():
    # Construct a bbmodel with texture having layers
    bbmodel = {
        "model_identifier": "test_model",
        "textures": [
            {
                "name": "grass_side.tga",
                "path": "",
                "folder": "",
                "namespace": "",
                "id": "151",
                "group": "",
                "scope": 0,
                "width": 8,
                "height": 8,
                "uv_width": 16,
                "uv_height": 16,
                "particle": False,
                "use_as_default": True,
                "layers_enabled": True,
                "sync_to_project": "",
                "file_format": "tga",
                "render_mode": "default",
                "render_sides": "auto",
                "wrap_mode": "limited",
                "pbr_channel": "color",
                "fps": 7,
                "frame_time": 1,
                "frame_order_type": "loop",
                "frame_order": "",
                "frame_interpolate": False,
                "visible": True,
                "internal": True,
                "saved": False,
                "uuid": "c3b51bd7-b150-9a50-2b50-03c000de3956",
                "layers": [
                    {
                        "name": "default",
                        "offset": [0, 0],
                        "scale": [1, 1],
                        "opacity": 100,
                        "visible": True,
                        "blend_mode": "default",
                        "width": 8,
                        "height": 8,
                        "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAASElEQVR4AbyOuw0AIQxDrSxyy5xuyugWSUUHFbBIiizArw6UWH6d9WQSkXaCMGJm8GBm0KsJT/H5VLEMQ7LtjcHPATVml3msAwAA//9SSo2eAAAABklEQVQDANgeS0FRbJOqAAAAAElFTkSuQmCC"
                    },
                    {
                        "name": "layer",
                        "offset": [0, 0],
                        "scale": [1, 1],
                        "opacity": 100,
                        "visible": True,
                        "blend_mode": "alpha_mask",
                        "width": 8,
                        "height": 8,
                        "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAJElEQVR4AbyNsQ0AAAiDmob/X9YPZJOEFTpCIxTIpRfkkIfCAgAA//8PLzsWAAAABklEQVQDACFxIFFyN+SSAAAAAElFTkSuQmCC"
                    }
                ],
                "source": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAQ0lEQVR4AbyNwQ0AIAgDCXE0N3A9BjBhBIYy4S+KvsGnTe/VpkURWS8QXKoKEUQEWMcos/eQZlbugo+k/lFg5vT/BBsAAP//4ct4wAAAAAZJREFUAwC25kDJMdXjKwAAAABJRU5ErkJggg=="
            }
        ]
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Instantiate _TexturesManager
        manager = _TexturesManager("test_model", "blocks", bbmodel)
        
        # Queue the texture
        manager.queue_texture("grass_side", dest_dir=tmpdir)
        
        # Export
        manager.__export__()
        
        # Verify that grass_side.tga was created in tmpdir
        tga_path = os.path.join(tmpdir, "grass_side.tga")
        assert os.path.exists(tga_path)
        
        # Load the TGA and verify pixels match expected
        img = Image.open(tga_path).convert("RGBA")
        
        # Load the source image (precompiled/expected result)
        expected_bytes = base64.b64decode(bbmodel["textures"][0]["source"].split("base64,")[-1])
        expected_img = Image.open(io.BytesIO(expected_bytes)).convert("RGBA")
        
        # Check size
        assert img.size == (8, 8)
        assert expected_img.size == (8, 8)
        
        # Check pixel values
        for y in range(8):
            for x in range(8):
                p_actual = img.getpixel((x, y))
                p_expected = expected_img.getpixel((x, y))
                
                # Check premultiplied match
                r_a, g_a, b_a, a_a = p_actual
                r_e, g_e, b_e, a_e = p_expected
                pm_a = (round(r_a * a_a / 255.0), round(g_a * a_a / 255.0), round(b_a * a_a / 255.0), a_a)
                pm_e = (round(r_e * a_e / 255.0), round(g_e * a_e / 255.0), round(b_e * a_e / 255.0), a_e)
                
                assert pm_a == pm_e, f"Mismatch at ({x}, {y}): {pm_a} != {pm_e}"
