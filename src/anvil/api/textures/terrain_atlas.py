"""The resource pack's `textures/terrain_texture.json`: the block atlas."""

from pathlib import PurePosixPath
from typing import Annotated, ClassVar, Literal

from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import (
    InRange,
    JsonFile,
    JsonObject,
    Keyed,
    Length,
    NonNegative,
    json_field,
)


class _TerrainVariation(JsonObject):
    """One texture of a variations texture.

    Args:
        path (str): The texture path, without extension.
        weight (float): How likely the texture is picked, from 0.05 to 1000000.
    """

    path: str = json_field()
    weight: Annotated[float, InRange(0.05, 1000000)] = json_field()


class _TerrainVariations(JsonObject):
    """A texture picked from weighted textures by the block's position."""

    variations: Annotated[list[_TerrainVariation], Length(1, 256)] = json_field()


class _TerrainTexture(JsonObject):
    """One entry of the terrain atlas's `texture_data`.

    Args:
        name (str): The texture's short name, used by material instances.
        textures (list[str] | _TerrainVariations): The texture paths, or weighted textures.
    """

    name: str = json_field(exclude=True)
    textures: list[str] | _TerrainVariations = json_field()


class _TerrainTextureFile(JsonObject):
    """The content of `textures/terrain_texture.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "resource_pack_name",
        "texture_name",
        "texture_data",
    )

    texture_name: Literal["atlas.terrain"] = json_field(
        default="atlas.terrain", init=False
    )
    num_mip_levels: Annotated[int, NonNegative] = json_field(default=1)
    padding: Annotated[int, NonNegative] = json_field(default=8)
    resource_pack_name: str | None = None
    texture_data: Annotated[list[_TerrainTexture], Keyed("name")] = json_field(
        default_factory=list
    )

    def set_resource_pack_name(self, name: str) -> None:
        """Sets the name of the pack the atlas belongs to."""
        self.resource_pack_name = name

    def add_texture(self, name: str, textures: list[str] | _TerrainVariations) -> None:
        """Adds a texture, replacing an earlier one with the same name."""
        self.texture_data = [item for item in self.texture_data if item.name != name]
        self.texture_data.append(_TerrainTexture(name=name, textures=textures))

    def add_variations(self, name: str, variations: list[tuple[str, float]]) -> None:
        """Adds a texture picked from `(path, weight)` textures by the block's position."""
        self.add_texture(
            name,
            _TerrainVariations(
                variations=[
                    _TerrainVariation(path=path, weight=weight)
                    for path, weight in variations
                ]
            ),
        )


class TerrainTexturesObject(JsonFile[_TerrainTextureFile]):
    """The terrain atlas, `textures/terrain_texture.json`, which names the textures block
    material instances use. There is one per pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/variationsblocktexture)
    """

    _extension = ".json"
    _pack = Pack.RP
    _folder = "textures"
    _object_type = "Terrain Textures"
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
            self._document.set_resource_pack_name(CONFIG.PROJECT_NAME)
            self._initialized = True

    @staticmethod
    def _name(block_name: str, force_vanilla: bool) -> str:
        return block_name if force_vanilla else f"{CONFIG.NAMESPACE}:{block_name}"

    def add_block(
        self,
        block_name: str,
        directory: str,
        block_textures: list[str],
        force_vanilla: bool = False,
    ) -> "TerrainTexturesObject":
        """Adds block textures.

        Args:
            block_name (str): The texture's short name, `<namespace>:<block_name>`.
            directory (str): The folder of the textures, inside the project's blocks folder.
            block_textures (list[str]): The texture names.
            force_vanilla (bool, optional): Uses `block_name` as it is, as vanilla textures
                do. Defaults to False.
        """
        self._document.add_texture(
            self._name(block_name, force_vanilla),
            [
                PurePosixPath(
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "blocks",
                    directory,
                    face,
                ).as_posix()
                for face in block_textures
            ],
        )
        return self

    def add_block_variations(
        self,
        block_name: str,
        directory: str,
        block_variant: list[tuple[str, float]],
        force_vanilla: bool = False,
    ) -> "TerrainTexturesObject":
        """Adds a block texture picked from weighted textures by the block's position.

        Args:
            block_name (str): The texture's short name, `<namespace>:<block_name>`.
            directory (str): The folder of the textures, inside the project's blocks folder.
            block_variant (list[tuple[str, float]]): Up to 256 `(texture, weight)` pairs,
                each weight from 0.05 to 1000000.
            force_vanilla (bool, optional): Uses `block_name` as it is, as vanilla textures
                do. Defaults to False.
        """
        self._document.add_variations(
            self._name(block_name, force_vanilla),
            [
                (
                    PurePosixPath(
                        "textures",
                        CONFIG.NAMESPACE,
                        CONFIG.PROJECT_NAME,
                        "blocks",
                        directory,
                        texture,
                    ).as_posix(),
                    weight,
                )
                for texture, weight in block_variant
            ],
        )
        return self

    def queue(self) -> "TerrainTexturesObject":
        """Queues the terrain atlas for export."""
        return super().queue()

    def __export__(self) -> None:
        """Writes the atlas, when it has any texture."""
        if not self._document.texture_data:
            return None
        return super().__export__()
