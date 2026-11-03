"""The resource pack's `textures/flipbook_textures.json`: animated block textures."""

from pathlib import PurePosixPath
from typing import Annotated

from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import (
    AtLeastOne,
    JsonFile,
    JsonObject,
    JsonValue,
    NonNegative,
    json_field,
)


class _FlipbookTexture(JsonObject):
    """One animated texture of `flipbook_textures.json`. Unset keys are left out."""

    atlas_tile: str = json_field()
    flipbook_texture: str = json_field()
    frames: list[Annotated[int, NonNegative]] | Annotated[int, AtLeastOne] = (
        json_field()
    )
    ticks_per_frame: Annotated[int, AtLeastOne] | None = None
    atlas_index: Annotated[int, NonNegative] | None = None
    atlas_tile_variant: Annotated[int, NonNegative] | None = None
    replicate: Annotated[int, AtLeastOne] = json_field(default=1, omit_default=True)
    blend_frames: bool = json_field(default=True, omit_default=True)

    def __validate__(self) -> None:
        if self.replicate & (self.replicate - 1):
            raise ValueError("A flipbook's replicate must be a power of two.")


class _FlipbookTexturesFile(JsonValue):
    """The content of `textures/flipbook_textures.json`: a list of animated textures."""

    textures: list[_FlipbookTexture] = json_field(default_factory=list)

    def add_texture(self, texture: _FlipbookTexture) -> None:
        """Adds an animated texture."""
        self.textures.append(texture)


class FlipBookTexturesObject(JsonFile):
    """The animated block textures, `textures/flipbook_textures.json`. There is one per
    pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/createanimatedblocktexture)
    """

    _document = _FlipbookTexturesFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "textures"
    _object_type = "Flipbook Textures"
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
            self._initialized = True

    def add_block(
        self,
        block_name: str,
        directory: str,
        block_texture: str,
        frames: list[int] | int,
        ticks_per_frame: int | None = None,
        atlas_index: int | None = None,
        atlas_tile_variant: int | None = None,
        replicate: int = 1,
        blend_frames: bool = True,
    ) -> "FlipBookTexturesObject":
        """Animates a block texture. The texture file is a vertical strip of frames.

        Args:
            block_name (str): The short name of the texture in the terrain atlas,
                `<namespace>:<block_name>`.
            directory (str): The folder of the texture, inside the project's blocks folder.
            block_texture (str): The texture file name, without extension.
            frames (list[int] | int): The frame shown on each step, or how many frames play
                one after another.
            ticks_per_frame (int, optional): The ticks each frame shows, 20 ticks being one
                second. Game default 1.
            atlas_index (int, optional): The texture to animate when the short name has a
                list of textures.
            atlas_tile_variant (int, optional): The variation to animate when the short name
                has variations.
            replicate (int, optional): Shows `1 / replicate²` of each frame's pixels, a power
                of two. Defaults to 1.
            blend_frames (bool, optional): Blends one frame into the next. Defaults to True.

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/createanimatedblocktexture)
        """
        self._content.add_texture(
            _FlipbookTexture(
                atlas_tile=f"{CONFIG.NAMESPACE}:{block_name}",
                flipbook_texture=PurePosixPath(
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "blocks",
                    directory,
                    block_texture,
                ).as_posix(),
                frames=frames,
                ticks_per_frame=ticks_per_frame,
                atlas_index=atlas_index,
                atlas_tile_variant=atlas_tile_variant,
                replicate=replicate,
                blend_frames=blend_frames,
            )
        )
        return self

    def queue(self) -> "FlipBookTexturesObject":
        """Queues the flipbook textures for export."""
        return super().queue()

    def __export__(self) -> None:
        """Writes the flipbook textures, when there is any."""
        if not self._content.textures:
            return None
        return super().__export__()
