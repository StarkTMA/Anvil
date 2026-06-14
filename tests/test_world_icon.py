import os
import shutil
from unittest.mock import MagicMock
import pytest
from PIL import Image

# Import CONFIG and pack_art
import anvil.api.core.core as core
from anvil.lib.config import ConfigPackageTarget

def test_pack_art_compiles_world_icon(tmp_path, monkeypatch):
    # Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Mock CONFIG properties
    mock_config = MagicMock()
    mock_config._TARGET = ConfigPackageTarget.WORLD
    mock_config._WORLD_PATH = str(tmp_path / "world")
    mock_config.BP_PATH = str(tmp_path / "bp")
    mock_config.RP_PATH = str(tmp_path / "rp")
    
    # Patch core.CONFIG
    monkeypatch.setattr(core, "CONFIG", mock_config)

    # Create marketing directory
    marketing_dir = tmp_path / "marketing"
    marketing_dir.mkdir()

    # Create keyart.png
    keyart_img = Image.new("RGB", (100, 100), color="red")
    keyart_img.save(marketing_dir / "keyart.png")

    # Call pack_art
    core.pack_art(apply_overlay=False)

    # Check that world_icon.jpeg was created in the world path
    world_icon_path = tmp_path / "world" / "world_icon.jpeg"
    assert world_icon_path.exists()

    # Verify that the image can be opened and is resized
    with Image.open(world_icon_path) as img:
        assert img.size == (800, 450)


def test_pack_art_compiles_world_icon_with_overlay(tmp_path, monkeypatch):
    # Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Mock CONFIG properties
    mock_config = MagicMock()
    mock_config._TARGET = ConfigPackageTarget.WORLD
    mock_config._WORLD_PATH = str(tmp_path / "world")
    mock_config.BP_PATH = str(tmp_path / "bp")
    mock_config.RP_PATH = str(tmp_path / "rp")
    
    # Patch core.CONFIG
    monkeypatch.setattr(core, "CONFIG", mock_config)

    # Create marketing directory
    marketing_dir = tmp_path / "marketing"
    marketing_dir.mkdir()

    # Create keyart.png and keyart_overlay.png
    keyart_img = Image.new("RGB", (100, 100), color="blue")
    keyart_img.save(marketing_dir / "keyart.png")
    
    # Overlay needs alpha channel to be split in resize function (requires RGBA)
    overlay_img = Image.new("RGBA", (100, 100), color=(0, 255, 0, 128))
    overlay_img.save(marketing_dir / "keyart_overlay.png")

    # Call pack_art with apply_overlay=True
    core.pack_art(apply_overlay=True)

    # Check that world_icon.jpeg was created in the world path
    world_icon_path = tmp_path / "world" / "world_icon.jpeg"
    assert world_icon_path.exists()

    # Verify image properties
    with Image.open(world_icon_path) as img:
        assert img.size == (800, 450)
