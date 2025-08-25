import os

from anvil import CONFIG
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Identifier


class UITexturesObject(AddonObject):
    """Handles UI textures for the addon."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "textures")
    _textures = {}

    def __init__(self) -> None:
        """Initializes a UITexturesObject instance."""
        super().__init__("ui_texture")

    def add_item(self, texture_name: str, directory: str, *textures: str):
        """Adds item textures to the content.

        Parameters:
            texture_name (str): The name of the texture.
            directory (str): The directory path for the textures.
            textures (str): The names of the textures.
        """
        for texture in textures:
            if not FileExists(os.path.join("assets", "textures", "ui", directory, f"{texture}.png")):
                raise FileNotFoundError(
                    f"UI texture '{texture}.png' does not exist in '{os.path.join("assets", "textures", "ui", directory)}'. {self._object_type}[{texture_name}]"
                )
            self._textures.setdefault(directory, []).append(texture)

    @property
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
        for directory, sprites in self._textures.items():
            for sprite in sprites:
                CopyFiles(
                    os.path.join("assets", "textures", "ui", directory),
                    os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "ui", directory),
                    sprite + ".png",
                )


class ItemTexturesObject(AddonObject):
    """Handles item textures for the addon."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "textures")

    def __init__(self) -> None:
        """Initializes a ItemTexturesObject instance."""
        super().__init__("item_texture")

        self.content(JsonSchemes.item_texture(CONFIG.PROJECT_NAME))

    def add_item(self, item_name: str, directory, *item_sprites: str):
        """Adds item textures to the content.

        Parameters:
            item_name (str): The name of the item.
            directory (str): The directory path for the textures.
            item_sprites (str): The names of the item sprites.
        """
        for item in item_sprites:
            if not FileExists(os.path.join("assets", "textures", "items", f"{item}.png")):
                raise FileNotFoundError(
                    f"Item texture '{item}.png' does not exist in '{os.path.join("assets", "textures", "items")}'. {self._object_type}[{item_name}]"
                )

        self._content["texture_data"][f"{CONFIG.NAMESPACE}:{item_name}"] = {
            "textures": [
                *[
                    os.path.join("textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "items", directory, sprite).replace("\\", "/")
                    for sprite in item_sprites
                ]
            ]
        }

    @property
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

    def __init__(self) -> None:
        """Initializes a TerrainTexturesObject instance."""
        super().__init__("terrain_texture")
        self.content(JsonSchemes.terrain_texture(CONFIG.PROJECT_NAME))

    def add_block(self, block_name: str, directory: str, *block_textures: str):
        """Adds block textures to the content.

        Parameters:
            block_name (str): The name of the block.
            directory (str): The directory path for the textures.
            block_textures (str): The names of the block textures.
        """
        self._content["texture_data"][f"{CONFIG.NAMESPACE}:{block_name}"] = {
            "textures": [
                *[
                    os.path.join("textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "blocks", directory, face).replace("\\", "/")
                    for face in block_textures
                ]
            ]
        }

    @property
    def queue(self):
        """Queues the block textures.

        Returns:
            object: The parent's queue method result.
        """
        return super().queue()

    def _export(self):
        """Exports the block textures if at least one block texture was added.

        Returns:
            object: The parent's export method result.
        """
        if len(self._content["texture_data"]) > 0:
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


class BlocksJSONObject(AddonObject):
    _extension = ".json"
    _path = CONFIG.RP_PATH

    def __init__(self) -> None:
        super().__init__("blocks")
        self.content(JsonSchemes.blocks_json())

    def add_block(self, block_identifier: Identifier, block_data: dict):
        self._content.update({block_identifier: block_data})

    @property
    def queue(self):
        return super().queue()
