import os

from anvil.lib.config import CONFIG
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes


class ItemTexturesObject(AddonObject):
    """Handles item textures for the addon (singleton)."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "textures")
    _instance = None

    def __new__(cls):
        """Ensures only one instance of ItemTexturesObject exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(ItemTexturesObject, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes a ItemTexturesObject instance."""
        if not hasattr(self, "_initialized"):
            super().__init__("item_texture")
            self.content(JsonSchemes.item_texture(CONFIG.PROJECT_NAME))
            self._initialized = True

    def add_item(self, item_name: str, directory, item_sprites: list[str]):
        """Adds item textures to the content.

        Parameters:
            item_name (str): The name of the item.
            directory (str): The directory path for the textures.
            item_sprites (str): The names of the item sprites.
        """
        for item in item_sprites:
            if not FileExists(
                os.path.join("assets", "textures", "items", f"{item}.png")
            ):
                raise FileNotFoundError(
                    f"Item texture '{item}.png' does not exist in '{os.path.join("assets", "textures", "items")}'. {self._object_type}[{item_name}]"
                )

        self._content["texture_data"][f"{CONFIG.NAMESPACE}:{item_name}"] = {
            "textures": [
                *[
                    os.path.join(
                        "textures",
                        CONFIG.NAMESPACE,
                        CONFIG.PROJECT_NAME,
                        "items",
                        directory,
                        sprite,
                    ).replace("\\", "/")
                    for sprite in item_sprites
                ]
            ]
        }

    def queue(self):
        """Queues the item textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue("")

    def _export(self):
        """Exports the item textures if at least one item was added.

        Returns:
            object: The parent's export method result.
        """
        if len(self._content["texture_data"]) > 0:
            for items in self._content["texture_data"].values():
                for sprite in items["textures"]:
                    CopyFiles(
                        os.path.join("assets", "textures", "items"),
                        os.path.join(
                            CONFIG.RP_PATH,
                            sprite.rstrip(sprite.split("/")[-1]),
                        ),
                        sprite.split("/")[-1] + ".png",
                    )
            return super()._export()


class TerrainTexturesObject(AddonObject):
    """Handles terrain textures for the addon."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "textures")
    _instance = None

    def __new__(cls):
        """Ensures only one instance of TerrainTexturesObject exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(TerrainTexturesObject, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes a TerrainTexturesObject instance."""
        if not hasattr(self, "_initialized"):
            super().__init__("terrain_texture")
            self.content(JsonSchemes.terrain_texture(CONFIG.PROJECT_NAME))
            self._initialized = True

    def add_block(self, block_name: str, directory: str, block_textures: list[str]):
        """Adds block textures to the content.

        Parameters:
            block_name (str): The name of the block.
            directory (str): The directory path for the textures.
            block_textures (str): The names of the block textures.
        """
        self._content["texture_data"][f"{CONFIG.NAMESPACE}:{block_name}"] = {
            "textures": [
                *[
                    os.path.join(
                        "textures",
                        CONFIG.NAMESPACE,
                        CONFIG.PROJECT_NAME,
                        "blocks",
                        directory,
                        face,
                    )
                    for face in block_textures
                ]
            ]
        }

    def add_block_variations(
        self, block_name: str, directory: str, block_variant: list[dict[str, str]]
    ):
        """Adds block textures with variations to the content.

        Parameters:
            shortname (str): The shortname defined in terrain_texture.json for this block.
            blockbench_name (str): The name of the blockbench model.
            variations (list[dict]): List of variations for the block textures.
        """

        self._content["texture_data"][f"{CONFIG.NAMESPACE}:{block_name}"] = {
            "textures": {
                "variations": [
                    *[
                        {
                            "weight": variant["weight"],
                            "path": os.path.join(
                                "textures",
                                CONFIG.NAMESPACE,
                                CONFIG.PROJECT_NAME,
                                "blocks",
                                directory,
                                variant["texture"],
                            ),
                        }
                        for variant in block_variant
                    ]
                ]
            }
        }

    def queue(self):
        """Queues the block textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue()

    def _export(self):
        """Exports the block textures if at least one block texture was added.

        Returns:
            object: The parent's export method result, or None if no textures to export.
        """
        if len(self._content.get("texture_data", {})) > 0:
            return super()._export()
        return None


class FlipBookTexturesObject(AddonObject):
    """Handles flip book textures for the addon."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "textures")
    _instance = None

    def __new__(cls):
        """Ensures only one instance of FlipBookTexturesObject exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(FlipBookTexturesObject, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initializes a FlipBookTexturesObject instance."""
        if not hasattr(self, "_initialized"):
            super().__init__("flipbook_textures")
            self.content(JsonSchemes.flipbook_textures())
            self._initialized = True

    def add_block(
        self,
        block_name: str,
        directory: str,
        block_texture: str,
        frames: list[int],
        ticks_per_frame: int = None,
        atlas_index: int = None,
        atlas_tile_variant: int = None,
        replicate: int = 1,
        blend_frames: bool = True,
    ):
        """Adds an animated flipbook texture for a block.

        Flipbook textures are animated textures used by blocks like fire, water, lava and magma.
        The animation parameters defined here will be applied to blocks using this texture shortname.

        Parameters:
            block_name (str): The shortname defined in terrain_texture.json for this block.
            directory (str): The directory path for the textures relative to the project blocks folder.
            block_texture (str): The name of the block texture file (without extension).
            frames (list[int]): List with frame index to use on each frame, or the total number of frames to be repeated one after another. Defaults to [1].
            ticks_per_frame (int, optional): How fast frames should be changed. 20 ticks = 1 second. Defaults to 20.
            atlas_index (int, optional): The index of the texture array inside the terrain_texture.json definition. Use this when the shortname has multiple textures in an array and you want to animate a specific index.
            atlas_tile_variant (int, optional): The variant of the block's texture array inside the shortname's block variation. Use this when you want to animate a specific variation path.
            replicate (int, optional): Sets the size of pixels. Changes size of the piece of used texture. Can only take values that are multiples of two. Default: 1.
            blend_frames (bool, optional): Defines whether frames transition should be smooth or not. Defaults to True.

        Note:
            - The texture file should be a vertical strip containing all animation frames
            - atlas_index is used when terrain_texture.json has: "textures": ["path1", "path2"]
            - atlas_tile_variant is used when terrain_texture.json has variations array
            - replicate value of 2 renders 1/4 pixels of frame, x renders 1/x² pixels

        ## Documentation reference:
            https://wiki.bedrock.dev/blocks/flipbook-textures.html
        """
        path = os.path.join(
            "textures",
            CONFIG.NAMESPACE,
            CONFIG.PROJECT_NAME,
            "blocks",
            directory,
            block_texture,
        )

        flipbook_entry = {
            "atlas_tile": f"{CONFIG.NAMESPACE}:{block_name}",
            "flipbook_texture": path,
            "frames": frames,
        }

        if ticks_per_frame is not None:
            flipbook_entry["ticks_per_frame"] = ticks_per_frame

        if atlas_index is not None:
            flipbook_entry["atlas_index"] = atlas_index

        if atlas_tile_variant is not None:
            flipbook_entry["atlas_tile_variant"] = atlas_tile_variant

        if replicate != 1:
            flipbook_entry["replicate"] = replicate

        if not blend_frames:
            flipbook_entry["blend_frames"] = blend_frames

        self._content.append(flipbook_entry)

    def queue(self):
        """Queues the block textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue()

    def _export(self):
        """Exports the block textures if at least one block texture was added.

        Returns:
            object: The parent's export method result, or None if no textures to export.
        """
        if len(self._content) > 0 and isinstance(self._content, list):
            # for items in self._content["texture_data"].values():
            #    for sprite in items["textures"]:
            #        CopyFiles(
            #            os.path.join("assets", "textures", "blocks"),
            #            os.path.join(
            #                CONFIG.RP_PATH,
            #                sprite.rstrip(sprite.split("/")[-1]),
            #            ),
            #            sprite.split("/")[-1] + ".png",
            #        )
            return super()._export()
        return None
