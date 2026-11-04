from pathlib import Path

import orjson

try:
    import amulet
    from amulet.api.block import Block as amuletBlock
    from amulet.api.block import StringTag
except ImportError as error:
    raise ImportError(
        "anvil.kit.world.ldtk needs Amulet to build the world. "
        "Install it with: pip install mcanvil[ldtk]"
    ) from error

from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.lib.config import CONFIG
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import Directory


class LDtk:
    def _load_data(self):
        self._data = orjson.loads(self._file.read_bytes())

        if self._data["defaultGridSize"] != 16:
            raise ValueError("Grid size incompatible, must be 16px.")

    def _collect_tile_data(self):
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
        for level in self._data["levels"]:
            origin = [level["worldX"] // 16, level["worldY"] // 16]
            size = [abs(level["pxWid"]) // 16, abs(level["pxHei"]) // 16]

            self.dictionary["levels"][level["identifier"]] = {
                "origin": origin,
                "size": size,
                "layer": level["worldDepth"],
                "entities": [],
                "tiles": [],
                "corner_0": [origin[0], origin[1] - 64],
                "corner_1": [origin[0] + size[0], origin[1] - 64 + size[1]],
            }
            level_data = {}
            if level.get("layerInstances") is not None:
                level_data = level["layerInstances"]

            else:
                level_data = orjson.loads(
                    Path("world", "ldtk", level["externalRelPath"]).read_bytes()
                )["layerInstances"]

            for layer_ix, layer in enumerate(reversed(level_data)):
                for block in layer["autoLayerTiles"]:
                    self.dictionary["levels"][level["identifier"]]["tiles"].append(
                        {
                            "x": block["px"][0] / 16,
                            "y": block["px"][1] / 16,
                            "id": block["t"],
                            "tileset_id": layer["__tilesetDefUid"],
                        }
                    )
                for block in layer["gridTiles"]:
                    self.dictionary["levels"][level["identifier"]]["tiles"].append(
                        {
                            "x": block["px"][0] / 16,
                            "y": block["px"][1] / 16,
                            "id": block["t"],
                            "tileset_id": layer["__tilesetDefUid"],
                        }
                    )
                for entity in layer["entityInstances"]:
                    dat = {}
                    for tile_custom_data in entity["fieldInstances"]:
                        dat[tile_custom_data["__identifier"]] = tile_custom_data[
                            "__value"
                        ]
                    id = f'{"minecraft" if dat.get("vanilla", False) else CONFIG.NAMESPACE}:{entity["__identifier"].lower()}'
                    self.dictionary["levels"][level["identifier"]]["entities"].append(
                        {
                            "x": entity["px"][0] / 16,
                            "y": entity["px"][1] / 16,
                            "tileset_id": (
                                entity["__tile"]["tilesetUid"]
                                if entity.get("__tile") is not None
                                else None
                            ),
                            "entity_id": id,
                            "data": dat,
                        }
                    )

    def _prepare_level(self):
        world = amulet.load_level(CONFIG._WORLD_PATH)

        if self._clear_chunks:
            for chunk in world.all_chunk_coords("minecraft:overworld"):
                world.delete_chunk(*chunk, "minecraft:overworld")

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

        Args:
            filename (str): filename of the map, no extension.
            clear_chunks (bool, optional): If chunks should be cleared before writing to the map. Defaults to False.
        """
        self._file = Path("world", "ldtk", f"{filename}.ldtk")
        self.dictionary = {"tilesets": {}, "levels": {}, "entities": {}, "enums": []}
        self._clear_chunks = clear_chunks
        self._default_origin_block = default_origin_block
        self._load_data()
        self._collect_tile_data()
        self._collect_level_data()

    def convert(
        self,
        plane: str = "yz",
        offset: tuple[float, float, float] = (0, 0, 0),
        export_entities: bool = True,
        export_world: bool = True,
    ):
        import click

        click.echo(click.style("\r[INFO]: Converting LDtk world...", fg="cyan"))

        def map_coordinates(level_origin, x, y, layer):
            if plane in ["yx", "xy"]:
                return (
                    int(level_origin[0] + x + offset[0]),
                    int(-64 - level_origin[1] - y + offset[1]),
                    int(offset[2] - layer),
                )
            elif plane in ["xz", "zx"]:
                return (
                    int(level_origin[0] + x + offset[0]),
                    int(offset[1] - layer),
                    int(level_origin[1] + y + offset[2]),
                )
            elif plane in ["yz", "zy"]:
                return (
                    int(offset[0] - layer),
                    int(-64 - level_origin[1] - y + offset[1]),
                    int(level_origin[0] + x + offset[2]),
                )
            else:
                raise ValueError(f"Unsupported plane: {plane}")

        game_version = ("bedrock", [int(i) for i in MANIFEST_BUILD.split(".")])

        if export_world:
            world = self._prepare_level()
            for level_name, level in self.dictionary["levels"].items():
                for tile in level["tiles"]:
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
                    except AttributeError as error:
                        raise KeyError(
                            f"Error retrieving custom data for tile id: [{tile['id']}]"
                        ) from error

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
                        *mapped_coords,
                        "minecraft:overworld",
                        game_version,
                        origin_block,
                    )
                    world.set_version_block(
                        *mapped_coords, "minecraft:overworld", game_version, block
                    )

            world.save()
            world.close()
        if export_entities:
            import copy

            entities = {}
            for level_name, level in self.dictionary["levels"].items():
                level_entities = []
                spawn_point = None

                corner_0_mc = map_coordinates(level["origin"], 0, 0, level["layer"])
                corner_1_mc = map_coordinates(
                    level["origin"], level["size"][0], level["size"][1], level["layer"]
                )

                for entity in level["entities"]:
                    mapped_coords = map_coordinates(
                        level["origin"], entity["x"], entity["y"], level["layer"]
                    )

                    entity_data = copy.deepcopy(entity["data"])
                    point = entity_data.get("point")
                    if point is not None:
                        cy = point.get("cy")
                        cx = point.get("cx")
                        if plane in ["yx", "xy", "yz", "zy"]:
                            cy = -64 - level["origin"][1] - cy + offset[1]
                        elif plane in ["xz", "zx"]:
                            cy = level["origin"][1] + cy + offset[2]

                        point["cy"] = cy
                        if plane in ["yz", "zy"]:
                            point["cx"] = cx + level["origin"][0] + offset[2]
                        else:
                            point["cx"] = cx + level["origin"][0] + offset[0]

                    if entity["entity_id"].split(":")[-1] == "spawn":
                        spawn_point = {
                            "x": mapped_coords[0],
                            "y": mapped_coords[1],
                            "z": mapped_coords[2],
                        }

                    if not entity_data.get("do_not_spawn"):
                        level_entities.append(
                            {
                                "id": entity["entity_id"],
                                "location": {
                                    "x": mapped_coords[0],
                                    "y": mapped_coords[1],
                                    "z": mapped_coords[2],
                                },
                                "data": entity_data,
                            }
                        )

                entities[level_name] = {
                    "corner_0": {
                        "x": corner_0_mc[0],
                        "y": corner_0_mc[1],
                        "z": corner_0_mc[2],
                    },
                    "corner_1": {
                        "x": corner_1_mc[0],
                        "y": corner_1_mc[1],
                        "z": corner_1_mc[2],
                    },
                    "spawn_point": spawn_point,
                    "entities": level_entities,
                }

            if entities.keys() == 0:
                return

            path = Path("scripts", "javascript", "content", "levels")
            Directory.create(path)
            for level_name, level_data in entities.items():
                if len(level_data["entities"]) == 0:
                    continue
                (path / f"{level_name}.json").write_bytes(
                    orjson.dumps(level_data, option=orjson.OPT_INDENT_2)
                )
