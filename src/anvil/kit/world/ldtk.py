import json
import os

import amulet
from amulet.api.block import Block as amuletBlock
from amulet.api.block import StringTag
from halo import Halo

from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.lib.config import CONFIG
from anvil.lib.format_versions import MANIFEST_BUILD


# Requires Amulet core to build the world
class LDtk:
    def _load_data(self):
        # Using the builtin json library becasue it's
        # much faster at loading json compared to commentjson
        # and ldtk is a very big json file

        with open(self._file, "r") as File:
            self._data = json.load(File)

        if self._data["defaultGridSize"] != 16:
            raise ValueError("Grid size incompatible, must be 16px.")

    def _collect_tile_data(self):
        # Collecting tile data
        for tileset in self._data["defs"]["tilesets"]:
            self.dictionary["tilesets"][tileset["uid"]] = {}

            for tile in tileset["customData"]:
                self.dictionary["tilesets"][tileset["uid"]][tile["tileId"]] = {
                    "origin": self._default_origin_block.identifier,
                    "properties": "",
                }
                for tile_custom_data in tile["data"].split("\n"):
                    if tile_custom_data.startswith("id="):
                        self.dictionary["tilesets"][tileset["uid"]][tile["tileId"]][
                            "id"
                        ] = tile_custom_data.removeprefix("id=").removesuffix("\n")
                    if tile_custom_data.startswith("origin="):
                        self.dictionary["tilesets"][tileset["uid"]][tile["tileId"]][
                            "origin"
                        ] = tile_custom_data.removeprefix("origin=").removesuffix("\n")
                    if tile_custom_data.startswith("properties="):
                        self.dictionary["tilesets"][tileset["uid"]][tile["tileId"]][
                            "properties"
                        ] = (
                            tile_custom_data.removeprefix("properties=")
                            .removesuffix("\n")
                            .removeprefix("[")
                            .removesuffix("]")
                            .split(",")
                        )

    def _collect_level_data(self):
        # Collecting level Data
        for level in self._data["levels"]:
            self.dictionary["levels"][level["identifier"]] = {
                "origin": [abs(level["worldX"]) // 16, abs(level["worldY"]) // 16],
                "size": [abs(level["pxWid"]) // 16, abs(level["pxHei"]) // 16],
                "layer": level["worldDepth"],
                "entities": [],
                "tiles": [],
            }
            level_data = {}
            # Levels saved in the same file
            if level["layerInstances"]:
                level_data = level["layerInstances"]

            else:
                with open(
                    os.path.join("world", "ldtk", level["externalRelPath"]), "r"
                ) as File:
                    level_data = json.load(File)["layerInstances"]

            # Level Layers
            for layer_ix, layer in enumerate(reversed(level_data)):
                # Divide by 16 to normalize block/entity coordinates to the 16x tile grid
                # Auto Tiles
                # 0: No flips
                # 1: X flip
                # 2: Y flip
                # 3: X and Y flip
                for block in layer["autoLayerTiles"]:
                    self.dictionary["levels"][level["identifier"]]["tiles"].append(
                        {
                            "x": block["px"][0] / 16,
                            "y": block["px"][1] / 16,
                            "id": block["t"],
                            # "rotation": 180 if block["f"] == 3 else 90 if block["f"] == 2 else 270 if block["f"] == 1 else 0,
                            "tileset_id": layer["__tilesetDefUid"],
                        }
                    )
                # Grid Tiles
                for block in layer["gridTiles"]:
                    self.dictionary["levels"][level["identifier"]]["tiles"].append(
                        {
                            "x": block["px"][0] / 16,
                            "y": block["px"][1] / 16,
                            "id": block["t"],
                            "tileset_id": layer["__tilesetDefUid"],
                        }
                    )
                # Entities
                for entity in layer["entityInstances"]:
                    dat = {}
                    # Collecting Entity data per level
                    for tile_custom_data in entity["fieldInstances"]:
                        dat[tile_custom_data["__identifier"]] = tile_custom_data[
                            "__value"
                        ]
                    id = f'{"minecraft" if dat["vanilla"] else CONFIG.NAMESPACE}:{entity["__identifier"].lower()}'
                    self.dictionary["levels"][level["identifier"]]["entities"].append(
                        {
                            "x": entity["px"][0] / 16,
                            "y": entity["px"][1] / 16,
                            "tileset_id": entity["__tile"]["tilesetUid"],
                            "entity_id": id,
                            "data": dat,
                        }
                    )

    def _dump_dictionary(self):
        with open(self._file.split(".")[0] + ".json", "w") as File:
            json.dump(self.dictionary, File)

    def _prepare_level(self):
        world = amulet.load_level(CONFIG._WORLD_PATH)

        # The following deletes EVERYTHING, DO NOT USE IF YOU HAVE HAND BUILT STRUCTURES
        if self._clear_chunks:
            for chunk in world.all_chunk_coords("minecraft:overworld"):
                world.delete_chunk(*chunk, "minecraft:overworld")

        # The following creates chunks that are present only in LDtk
        for level in self.dictionary["levels"].values():
            for x in range(level["origin"][0], level["size"][0], 16):
                for y in range(level["origin"][1], level["size"][1], 16):
                    world.create_chunk(x // 16, y // 16, "minecraft:overworld")

        return world

    def __init__(
        self,
        filename: str,
        *,
        clear_chunks: bool = False,
        default_origin_block=MinecraftBlockTypes.Air(),
    ) -> None:
        """Converts LDtk map to Minecraft worlds.

        Parameters:
            filename (str): filename of the map, no extension.
            clear_chunks (bool, optional): If chunks should be cleared before writing to the map. Defaults to False.
        """
        self._file = os.path.join("world", "ldtk", filename + ".ldtk")
        self.dictionary = {"tilesets": {}, "levels": {}, "entities": {}, "enums": []}
        self._clear_chunks = clear_chunks
        self._default_origin_block = default_origin_block
        self._load_data()
        self._collect_tile_data()
        self._collect_level_data()
        # self._dump_dictionary()

    @Halo(text="Converting LDtk world", spinner="dots")
    def convert(
        self,
        plane: str = "yz",
        offset: tuple[float, float, float] = (0, 0, 0),
        export_entities: bool = True,
    ):
        def map_coordinates(level_origin, x, y, layer):
            if plane in ["yx", "xy"]:
                return (
                    int(level_origin[0] + x + offset[0]),
                    int(-64 + level_origin[1] - y + offset[1]),
                    int(offset[2] - layer),
                )
            elif plane in ["xz", "zx"]:
                return (
                    int(level_origin[0] + x + offset[0]),
                    int(offset[1] - layer),
                    int(level_origin[1] + y + offset[2]),
                )
            else:
                raise ValueError(f"Unsupported plane: {plane}")

        game_version = ("bedrock", [int(i) for i in MANIFEST_BUILD.split(".")])
        world = self._prepare_level()

        for level_name, level in self.dictionary["levels"].items():
            for tile in level["tiles"]:
                functions = {k: [] for k in self.dictionary["enums"]}
                mapped_coords = map_coordinates(
                    level["origin"], tile["x"], tile["y"], level["layer"]
                )

                try:
                    prop_get = (
                        self.dictionary.get("tilesets")
                        .get(tile["tileset_id"])
                        .get(tile["id"])
                        .get("properties")
                    )
                except:
                    raise KeyError(
                        f"Error retrieving custom data for tile id: [{tile['id']}]"
                    )

                properties = {
                    str(k): StringTag(v)
                    for k, v in [p.split("=") for p in prop_get]
                    if type(prop_get) is list
                }

                origin_block = amuletBlock(
                    *self.dictionary["tilesets"][tile["tileset_id"]][tile["id"]][
                        "origin"
                    ].split(":"),
                    properties,
                )
                block = amuletBlock(
                    *self.dictionary["tilesets"][tile["tileset_id"]][tile["id"]][
                        "id"
                    ].split(":"),
                    properties,
                )

                world.set_version_block(
                    *mapped_coords, "minecraft:overworld", game_version, origin_block
                )
                world.set_version_block(
                    *mapped_coords, "minecraft:overworld", game_version, block
                )

        with open(os.path.join("scripts", "javascript", "entities.ts"), "w") as File:
            entities = {}
            if export_entities:
                for level_name, level in self.dictionary["levels"].items():
                    entities[level_name] = []
                    for entity in level["entities"]:
                        mapped_coords = map_coordinates(
                            level["origin"], entity["x"], entity["y"], level["layer"]
                        )

                        point = entity["data"].get("point")
                        if point != None:
                            cy = point.get("cy")
                            cx = point.get("cx")
                            if plane in ["yx", "xy"]:
                                cy = -64 + level["origin"][1] - cy + offset[1]
                            elif plane in ["xz", "zx"]:
                                cy = level["origin"][1] + cy + offset[2]

                            entity["data"]["point"]["cy"] = cy
                            entity["data"]["point"]["cx"] = (
                                cx + level["origin"][0] + offset[0]
                            )

                        entities[level_name].append(
                            {
                                "id": entity["entity_id"],
                                "location": {
                                    "x": mapped_coords[0],
                                    "y": mapped_coords[1],
                                    "z": mapped_coords[2],
                                },
                                "data": entity["data"],
                            }
                        )
            File.write(f"export const entities = {json.dumps(entities, indent=4)}")

        world.save()
        world.close()
