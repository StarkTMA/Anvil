from PIL import Image

import anvil.api.core.core as core
from anvil.lib import config


def test_pack_art_compiles_world_icon(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    # Create marketing directory
    marketing_dir = tmp_path / "marketing"
    marketing_dir.mkdir()

    # Create keyart.png
    keyart_img = Image.new("RGB", (100, 100), color="red")
    keyart_img.save(marketing_dir / "keyart.png")

    # Call pack_art
    with config.override(_TARGET="world", _LOCAL_EXPORT=True):
        core.pack_art(apply_overlay=False)
        world_icon_path = config.CONFIG._WORLD_PATH / "world_icon.jpeg"

    # Check that world_icon.jpeg was created in the world path
    assert world_icon_path.exists()

    # Verify that the image can be opened and is resized
    with Image.open(world_icon_path) as img:
        assert img.size == (800, 450)


def test_pack_art_compiles_world_icon_with_overlay(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

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
    with config.override(_TARGET="world", _LOCAL_EXPORT=True):
        core.pack_art(apply_overlay=True)
        world_icon_path = config.CONFIG._WORLD_PATH / "world_icon.jpeg"

    # Check that world_icon.jpeg was created in the world path
    assert world_icon_path.exists()

    # Verify image properties
    with Image.open(world_icon_path) as img:
        assert img.size == (800, 450)
