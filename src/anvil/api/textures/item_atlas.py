"""The resource pack's `textures/item_texture.json`: the item atlas."""

from pathlib import Path, PurePosixPath
from typing import Annotated, ClassVar, Literal, overload

from anvil.lib.blockbench import _Blockbench, _BlockBenchSource
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, json_field
from anvil.lib.lib import Directory


class _ItemTexture(JsonObject):
    """One entry of an atlas's `texture_data`, written as `name: {"textures": [...]}`.

    Args:
        name (str): The texture's short name, used by the item's icon.
        textures (list[str]): The texture paths, without extension.
    """

    name: str = json_field(exclude=True)
    textures: list[str] = json_field()


class _ItemTextureFile(JsonObject):
    """The content of `textures/item_texture.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "resource_pack_name",
        "texture_name",
        "texture_data",
    )

    resource_pack_name: str | None = None
    texture_name: Literal["atlas.items"] = json_field(default="atlas.items", init=False)
    texture_data: Annotated[list[_ItemTexture], Keyed("name")] = json_field(
        default_factory=list
    )

    def set_resource_pack_name(self, name: str) -> None:
        """Sets the name of the pack the atlas belongs to."""
        self.resource_pack_name = name

    def add_texture(self, name: str, textures: list[str]) -> None:
        """Adds a texture, replacing an earlier one with the same name."""
        self.texture_data = [item for item in self.texture_data if item.name != name]
        self.texture_data.append(_ItemTexture(name=name, textures=textures))


class ItemTexturesObject(JsonFile[_ItemTextureFile]):
    """The item atlas, `textures/item_texture.json`, which names the textures item icons use.
    There is one per pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/addcustomitems)
    """

    _extension = ".json"
    _pack = Pack.RP
    _folder = "textures"
    _object_type = "Item Textures"
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
            self._document.set_resource_pack_name(CONFIG.PROJECT_NAME)
            self._sprites: dict[str, list[str]] = {}
            self._initialized = True

    @overload
    def add_item(self, item_name: str, sprites: list[str]) -> "ItemTexturesObject":
        """Adds item textures from `assets/textures/items`.

        Args:
            item_name (str): The name of the item.
            sprites (list[str]): The names of the item sprites.
        """
        ...

    @overload
    def add_item(
        self, item_name: str, blockbench: str, sprites: list[str]
    ) -> "ItemTexturesObject":
        """Adds item textures from a Blockbench model.

        Args:
            item_name (str): The name of the item.
            blockbench (str): The blockbench model name.
            sprites (list[str]): The names of the item sprites.
        """
        ...

    def add_item(
        self,
        item_name: str,
        blockbench: str | list[str] | None = None,
        sprites: list[str] | None = None,
    ) -> "ItemTexturesObject":
        """Adds item textures, from a Blockbench model or from `assets/textures/items`.

        Args:
            item_name (str): The name of the item.
            blockbench (str | list[str], optional): The Blockbench model name, or the sprites
                when there is no model.
            sprites (list[str], optional): The names of the item sprites.

        Raises:
            FileNotFoundError: When a sprite has no `.png` in `assets/textures/items`.
        """
        if isinstance(blockbench, list):
            sprites, blockbench = blockbench, None
        sprites = sprites or []

        if blockbench:
            model = _Blockbench(blockbench, _BlockBenchSource.ITEM)
            for sprite in sprites:
                model.textures.queue_texture(sprite)
            paths = [
                PurePosixPath(
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "actors",
                    blockbench,
                    sprite,
                ).as_posix()
                for sprite in sprites
            ]
        else:
            source = Path("assets", "textures", "items")
            for sprite in sprites:
                if not (source / f"{sprite}.png").exists():
                    raise FileNotFoundError(
                        f"Item texture '{sprite}.png' does not exist in '{source}'. "
                        f"{self._object_type}[{item_name}]"
                    )
            paths = [
                PurePosixPath(
                    "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "items", sprite
                ).as_posix()
                for sprite in sprites
            ]
            self._sprites[item_name] = paths

        self._document.add_texture(f"{CONFIG.NAMESPACE}:{item_name}", paths)
        return self

    def queue(self) -> "ItemTexturesObject":
        """Queues the item atlas for export."""
        return super().queue("")

    def __export__(self) -> None:
        """Copies the item sprites and writes the atlas, when it has any texture."""
        if not self._document.texture_data:
            return None
        source = Path("assets", "textures", "items")
        for paths in self._sprites.values():
            for path in paths:
                sprite = PurePosixPath(path)
                Directory.copy_files(
                    source, CONFIG.RP_PATH / sprite.parent, f"{sprite.name}.png"
                )
        return super().__export__()
