"""`BlockTexture`: the texture a block face shows.

```python
body = BlockTexture(blockbench="lamp", color="body", normal="body_n", mer="body_mer")

BlockMaterialInstance().face(BlockFaceValues.All, body)
```

A vanilla texture is given by its short name, `MinecraftTerrainTextures.Stone`, and is
only referenced: nothing is added to the atlases.
"""

from dataclasses import dataclass

from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.textures import MinecraftTerrainTextures
from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.lib import AnvilValidator

__all__ = [
    "AnimatedTexture",
    "BlockTexture",
    "WeightedTexture",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class BlockTexture:
    """A texture of a Blockbench model in `assets/bbmodels`, with its PBR maps. Each map
    is the name of a texture in the same model, or a color.

    ```python
    BlockTexture(blockbench="lamp", color="body", mer="body_mer")
    ```

    Args:
        blockbench (str): The model's name, without `.bbmodel`.
        color (str): The texture's name in the model.
        normal (optional): The normal map. Not with `height`.
        height (optional): The height map. Not with `normal`.
        mer (optional): The metalness, emissive and roughness map. Not with `mers`.
        mers (optional): The MER map with subsurface scattering. Not with `mer`.
    """

    blockbench: str
    color: str
    normal: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    height: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    mer: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    mers: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None

    def __post_init__(self) -> None:
        names = [("BlockTexture", self.color), ("Blockbench model", self.blockbench)]
        names += [
            ("PBR map", value)
            for value in (self.normal, self.height, self.mer, self.mers)
            if isinstance(value, str) and not AnvilValidator.is_color_value(value)
        ]
        for what, name in names:
            if not name or any(c in name for c in "/\\."):
                raise ValueError(
                    f"{what} '{name}' must be a name only, without a folder or an "
                    "extension."
                )
        if self.normal is not None and self.height is not None:
            raise ValueError("Normal and heightmap textures are mutually exclusive.")
        if self.mer is not None and self.mers is not None:
            raise ValueError(
                "Metalness, emissive, roughness and subsurface textures are mutually exclusive."
            )

    @staticmethod
    def weighted(
        *textures: "tuple[BlockTexture | AnimatedTexture, float]",
    ) -> "WeightedTexture":
        """A block face texture picked by weight from several, per block position.

        Args:
            *textures (tuple[BlockTexture | AnimatedTexture, float]): Up to 256 `(texture,
                weight)` pairs of Blockbench textures, each weight from 0.05 to 1000000.
                Every texture carries the same PBR maps.
        """
        return WeightedTexture(tuple(textures))

    def animated(
        self,
        frames: list[int] | int,
        *,
        ticks: int | None = None,
        replicate: int = 1,
        blend: bool = True,
    ) -> "AnimatedTexture":
        """The texture as a flipbook on a block face. The image is a vertical strip of
        frames.

        Args:
            frames (list[int] | int): The frame shown on each step, or how many frames play
                one after another.
            ticks (int, optional): The ticks each frame shows. Game default 1.
            replicate (int, optional): Shows `1 / replicate²` of each frame's pixels, a
                power of two. Defaults to 1.
            blend (bool, optional): Blends one frame into the next. Defaults to True.
        """
        return AnimatedTexture(self, frames, ticks, replicate, blend)

    @property
    def components(self) -> TextureComponents:
        """The texture and its maps, for its texture set."""
        return TextureComponents(
            self.color, self.normal, self.height, self.mer, self.mers
        )


@dataclass(frozen=True, slots=True)
class AnimatedTexture:
    """A texture animated on a block face, made by `BlockTexture.animated`."""

    texture: BlockTexture
    frames: list[int] | int
    ticks: int | None = None
    replicate: int = 1
    blend: bool = True

    def __post_init__(self) -> None:
        if self.replicate < 1 or self.replicate & (self.replicate - 1):
            raise ValueError(
                f"animated() replicate must be a power of two. "
                f"BlockTexture[{self.texture.color}]"
            )


@dataclass(frozen=True, slots=True)
class WeightedTexture:
    """A block face texture picked by weight from several, made by `BlockTexture.weighted`."""

    textures: tuple[tuple[BlockTexture | AnimatedTexture, float], ...]

    def __post_init__(self) -> None:
        if not 1 <= len(self.textures) <= 256:
            raise ValueError("BlockTexture.weighted takes from 1 to 256 textures.")
        maps = set()
        for member, weight in self.textures:
            if not isinstance(member, (BlockTexture, AnimatedTexture)):
                raise TypeError(
                    f"BlockTexture.weighted can't hold {type(member).__name__}."
                )
            texture = member.texture if isinstance(member, AnimatedTexture) else member
            if not 0.05 <= weight <= 1000000:
                raise ValueError("A weight goes from 0.05 to 1000000.")
            maps.add(
                tuple(
                    value is None
                    for value in (
                        texture.normal,
                        texture.height,
                        texture.mer,
                        texture.mers,
                    )
                )
            )
        if len(maps) > 1:
            raise ValueError(
                "Every texture of BlockTexture.weighted must carry the same PBR maps."
            )
