import os
from pathlib import Path

import orjson
import pytest

from anvil.lib import config

is_github_actions = os.environ.get("GITHUB_ACTIONS") == "true"

try:
    import amulet

    import anvil.kit.world.ldtk as ldtk
    from anvil.kit.world.ldtk import LDtk

    has_amulet = True
except ImportError:
    has_amulet = False

if is_github_actions:
    pytestmark = pytest.mark.skip(
        reason="ldtk test is disabled on GitHub Actions (local only)"
    )
elif not has_amulet:
    pytestmark = pytest.mark.skip(reason="amulet is not installed")


@pytest.fixture(autouse=True)
def project_namespace():
    with config.override(NAMESPACE="my_ns", PROJECT_NAME="test_project"):
        yield


def test_ldtk_export_entities_yx_plane(tmp_path, monkeypatch):
    # Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Prepare LDtk file directory structure
    Path("world", "ldtk").mkdir(parents=True, exist_ok=True)
    ldtk_file_path = Path("world", "ldtk", "test_map.ldtk")

    # Define minimal valid LDtk structure
    ldtk_data = {
        "defaultGridSize": 16,
        "defs": {"tilesets": []},
        "levels": [
            {
                "identifier": "Level_Empty",
                "worldX": 0,
                "worldY": 0,
                "pxWid": 160,
                "pxHei": 160,
                "worldDepth": 0,
                "layerInstances": [],
                "externalRelPath": None,
            },
            {
                "identifier": "Level_With_Entities",
                "worldX": 160,  # origin x: 10
                "worldY": -320,  # origin y: -20
                "pxWid": 320,  # size x: 20
                "pxHei": 480,  # size y: 30
                "worldDepth": 5,
                "externalRelPath": None,
                "layerInstances": [
                    {
                        "__tilesetDefUid": 1,
                        "autoLayerTiles": [],
                        "gridTiles": [],
                        "entityInstances": [
                            {
                                "__identifier": "Spawn",
                                "px": [32, 64],  # local x: 2, y: 4
                                "__tile": {"tilesetUid": 1},
                                "fieldInstances": [
                                    {"__identifier": "vanilla", "__value": True},
                                    {"__identifier": "do_not_spawn", "__value": True},
                                ],
                            },
                            {
                                "__identifier": "Zombie",
                                "px": [80, 160],  # local x: 5, y: 10
                                "__tile": {"tilesetUid": 1},
                                "fieldInstances": [
                                    {"__identifier": "vanilla", "__value": False},
                                    {
                                        "__identifier": "point",
                                        "__value": {"cx": 5, "cy": 10},
                                    },
                                ],
                            },
                            {
                                "__identifier": "Skeleton",
                                "px": [160, 320],  # local x: 10, y: 20
                                "__tile": None,
                                "fieldInstances": [],
                            },
                        ],
                    }
                ],
            },
        ],
    }

    ldtk_file_path.write_bytes(orjson.dumps(ldtk_data))

    # Initialize LDtk
    ldtk_instance = LDtk("test_map")

    # Run convert in YX plane with offset
    ldtk_instance.convert(
        plane="yx", offset=(100, 200, 300), export_entities=True, export_world=False
    )

    # Output path for entity JSON
    entities_dir = Path("scripts", "javascript", "content", "levels")
    empty_level_json = entities_dir / "Level_Empty.json"
    entities_level_json = entities_dir / "Level_With_Entities.json"

    # Verify that the empty level file is skipped
    assert not empty_level_json.exists()

    # Verify that the level with entities exists and is correctly populated
    assert entities_level_json.exists()

    data = orjson.loads(entities_level_json.read_bytes())

    # Check corners
    # level origin = [10, -20]
    # level size = [20, 30]
    # offset = (100, 200, 300)
    # plane = "yx":
    # corner_0 (local 0, 0):
    #   x = origin_x + 0 + offset_x = 10 + 0 + 100 = 110
    #   y = -64 - origin_y - 0 + offset_y = -64 - (-20) - 0 + 200 = 156
    #   z = offset_z - layer = 300 - 5 = 295
    assert data["corner_0"] == {"x": 110, "y": 156, "z": 295}

    # corner_1 (local 20, 30):
    #   x = origin_x + 20 + offset_x = 10 + 20 + 100 = 130
    #   y = -64 - origin_y - 30 + offset_y = -64 - (-20) - 30 + 200 = 126
    #   z = offset_z - layer = 300 - 5 = 295
    assert data["corner_1"] == {"x": 130, "y": 126, "z": 295}

    # Check spawn point (local spawn x: 2, y: 4)
    #   x = 10 + 2 + 100 = 112
    #   y = -64 - origin_y - 4 + 200 = 152
    #   z = 295
    assert data["spawn_point"] == {"x": 112, "y": 152, "z": 295}

    # Check entities list
    entities_list = data["entities"]
    assert len(entities_list) == 2

    # Verify Spawn entity (do_not_spawn = True) is excluded from entities list
    assert not any(e["id"] == "minecraft:spawn" for e in entities_list)

    # Zombie entity
    zombie_ent = next(e for e in entities_list if e["id"] == "my_ns:zombie")
    # local x: 5, y: 10
    #   x = 10 + 5 + 100 = 115
    #   y = -64 - origin_y - 10 + 200 = 146
    #   z = 295
    assert zombie_ent["location"] == {"x": 115, "y": 146, "z": 295}
    assert zombie_ent["data"]["vanilla"] is False
    # Check that custom point data was also mapped:
    #   cx = cx + origin_x + offset_x = 5 + 10 + 100 = 115
    #   cy = -64 - origin_y - cy + offset_y = -64 - (-20) - 10 + 200 = 146
    assert zombie_ent["data"]["point"] == {"cx": 115, "cy": 146}

    # Skeleton entity (without vanilla field)
    skeleton_ent = next(e for e in entities_list if e["id"] == "my_ns:skeleton")
    # local x: 10, y: 20
    #   x = 10 + 10 + 100 = 120
    #   y = -64 - origin_y - 20 + 200 = 136
    #   z = 295
    assert skeleton_ent["location"] == {"x": 120, "y": 136, "z": 295}
    assert skeleton_ent["data"] == {}


def test_ldtk_export_entities_xz_plane(tmp_path, monkeypatch):
    # Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Prepare LDtk file directory structure
    Path("world", "ldtk").mkdir(parents=True, exist_ok=True)
    ldtk_file_path = Path("world", "ldtk", "test_map.ldtk")

    # Define minimal valid LDtk structure
    ldtk_data = {
        "defaultGridSize": 16,
        "defs": {"tilesets": []},
        "levels": [
            {
                "identifier": "Level_With_Entities",
                "worldX": 160,  # origin x: 10
                "worldY": -320,  # origin y: -20
                "pxWid": 320,  # size x: 20
                "pxHei": 480,  # size y: 30
                "worldDepth": 5,
                "externalRelPath": None,
                "layerInstances": [
                    {
                        "__tilesetDefUid": 1,
                        "autoLayerTiles": [],
                        "gridTiles": [],
                        "entityInstances": [
                            {
                                "__identifier": "Spawn",
                                "px": [32, 64],  # local x: 2, y: 4
                                "__tile": {"tilesetUid": 1},
                                "fieldInstances": [
                                    {"__identifier": "vanilla", "__value": True}
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }

    ldtk_file_path.write_bytes(orjson.dumps(ldtk_data))

    # Initialize LDtk
    ldtk_instance = LDtk("test_map")

    # Run convert in XZ plane with offset
    ldtk_instance.convert(
        plane="xz", offset=(100, 200, 300), export_entities=True, export_world=False
    )

    # Output path for entity JSON
    entities_dir = Path("scripts", "javascript", "content", "levels")
    entities_level_json = entities_dir / "Level_With_Entities.json"

    assert entities_level_json.exists()

    data = orjson.loads(entities_level_json.read_bytes())

    # level origin = [10, -20]
    # level size = [20, 30]
    # offset = (100, 200, 300)
    # plane = "xz":
    # corner_0 (local 0, 0):
    #   x = origin_x + 0 + offset_x = 10 + 0 + 100 = 110
    #   y = offset_y - layer = 200 - 5 = 195
    #   z = origin_z + 0 + offset_z = -20 + 0 + 300 = 280
    assert data["corner_0"] == {"x": 110, "y": 195, "z": 280}

    # corner_1 (local 20, 30):
    #   x = origin_x + 20 + offset_x = 10 + 20 + 100 = 130
    #   y = offset_y - layer = 200 - 5 = 195
    #   z = origin_z + 30 + offset_z = -20 + 30 + 300 = 310
    assert data["corner_1"] == {"x": 130, "y": 195, "z": 310}

    # Check spawn point (local spawn x: 2, y: 4)
    #   x = 10 + 2 + 100 = 112
    #   y = 200 - 5 = 195
    #   z = -20 + 4 + 300 = 284
    assert data["spawn_point"] == {"x": 112, "y": 195, "z": 284}


def test_ldtk_export_entities_yz_plane(tmp_path, monkeypatch):
    # Change current working directory to tmp_path
    monkeypatch.chdir(tmp_path)

    # Prepare LDtk file directory structure
    Path("world", "ldtk").mkdir(parents=True, exist_ok=True)
    ldtk_file_path = Path("world", "ldtk", "test_map.ldtk")

    # Define minimal valid LDtk structure
    ldtk_data = {
        "defaultGridSize": 16,
        "defs": {"tilesets": []},
        "levels": [
            {
                "identifier": "Level_With_Entities",
                "worldX": 160,  # origin x: 10
                "worldY": -320,  # origin y: -20
                "pxWid": 320,  # size x: 20
                "pxHei": 480,  # size y: 30
                "worldDepth": 5,
                "externalRelPath": None,
                "layerInstances": [
                    {
                        "__tilesetDefUid": 1,
                        "autoLayerTiles": [],
                        "gridTiles": [],
                        "entityInstances": [
                            {
                                "__identifier": "Spawn",
                                "px": [32, 64],  # local x: 2, y: 4
                                "__tile": {"tilesetUid": 1},
                                "fieldInstances": [
                                    {"__identifier": "vanilla", "__value": True}
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }

    ldtk_file_path.write_bytes(orjson.dumps(ldtk_data))

    # Initialize LDtk
    ldtk_instance = LDtk("test_map")

    # Run convert in YZ plane with offset
    ldtk_instance.convert(
        plane="yz", offset=(100, 200, 300), export_entities=True, export_world=False
    )

    # Output path for entity JSON
    entities_dir = Path("scripts", "javascript", "content", "levels")
    entities_level_json = entities_dir / "Level_With_Entities.json"

    assert entities_level_json.exists()

    data = orjson.loads(entities_level_json.read_bytes())

    # Check corners in YZ plane
    # level origin = [10, -20]
    # level size = [20, 30]
    # offset = (100, 200, 300)
    # plane = "yz":
    # corner_0 (local 0, 0):
    #   x = offset_x - layer = 100 - 5 = 95
    #   y = -64 - origin_y - 0 + offset_y = -64 - (-20) - 0 + 200 = 156
    #   z = origin_x + 0 + offset_z = 10 + 0 + 300 = 310
    assert data["corner_0"] == {"x": 95, "y": 156, "z": 310}

    # corner_1 (local 20, 30):
    #   x = offset_x - layer = 100 - 5 = 95
    #   y = -64 - origin_y - 30 + offset_y = -64 - (-20) - 30 + 200 = 126
    #   z = origin_x + 20 + offset_z = 10 + 20 + 300 = 330
    assert data["corner_1"] == {"x": 95, "y": 126, "z": 330}

    # Check spawn point (local spawn x: 2, y: 4)
    #   x = 100 - 5 = 95
    #   y = -64 - (-20) - 4 + 200 = 152
    #   z = 10 + 2 + 300 = 312
    assert data["spawn_point"] == {"x": 95, "y": 152, "z": 312}
