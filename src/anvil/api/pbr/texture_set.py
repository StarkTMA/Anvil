from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import TEXTURE_SET_VERSION
from anvil.lib.jsonmodel import json_field, JsonFile, JsonObject, KeyFrame
from anvil.lib.lib import AnvilFormatter, AnvilValidator, Directory

__all__ = ["KeyFrame", "TextureComponents", "TextureSet"]


@dataclass(frozen=True)
class TextureComponents:
    """PBR texture components for blocks, items, and entities.

    Attributes:
        color: Base color texture filename or color value
        normal: Normal map texture filename or color value (mutually exclusive with heightmap)
        heightmap: Height/displacement map texture filename or color value (mutually exclusive with normal)
        mer: MER texture filename or color value (mutually exclusive with mers)
        mers: MERS texture filename or color value (mutually exclusive with mer)
    """

    color: str
    normal: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    height: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    mer: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None
    mers: str | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None

    def has_aux(self) -> bool:
        """Checks if the texture components have any auxiliary texture maps (normal, height, mer, or mers).

        Returns:
            bool: True if at least one auxiliary texture component is configured, False otherwise.
        """
        return bool(self.normal or self.height or self.mer or self.mers)


class _TextureSet(JsonObject):
    """The `minecraft:texture_set` object: the texture name or color of each layer."""

    color: str | None = None
    normal: str | None = None
    heightmap: str | None = None
    metalness_emissive_roughness: str | None = None
    metalness_emissive_roughness_subsurface: str | None = None

    def set_color(self, color: str) -> None:
        """Sets the color layer.

        Args:
            color (str): A texture name or a `#rrggbb` color.
        """
        self.color = color

    def set_normal(self, normal: str) -> None:
        """Sets the normal map layer.

        Args:
            normal (str): A texture name or a `#rrggbb` color.
        """
        self.normal = normal

    def set_heightmap(self, heightmap: str) -> None:
        """Sets the height map layer.

        Args:
            heightmap (str): A texture name or a `#rrggbb` color.
        """
        self.heightmap = heightmap

    def set_metalness_emissive_roughness(
        self, metalness_emissive_roughness: str
    ) -> None:
        """Sets the MER layer.

        Args:
            metalness_emissive_roughness (str): A texture name or a `#rrggbb` color.
        """
        self.metalness_emissive_roughness = metalness_emissive_roughness

    def set_metalness_emissive_roughness_subsurface(
        self, metalness_emissive_roughness_subsurface: str
    ) -> None:
        """Sets the MERS layer.

        Args:
            metalness_emissive_roughness_subsurface (str): A texture name or a `#rrggbbaa` color.
        """
        self.metalness_emissive_roughness_subsurface = (
            metalness_emissive_roughness_subsurface
        )

    def set_layers(self, layers: dict[str, str]) -> None:
        """Sets several layers at once.

        Args:
            layers (dict[str, str]): Each layer's key and its texture name or color.
        """
        for layer, value in layers.items():
            getattr(self, f"set_{layer}")(value)

    @property
    def layer_count(self) -> int:
        """The number of layers set."""
        return sum(
            value is not None
            for value in (
                self.color,
                self.normal,
                self.heightmap,
                self.metalness_emissive_roughness,
                self.metalness_emissive_roughness_subsurface,
            )
        )


class _TextureSetFile(JsonObject):
    """The content of a `.texture_set.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:texture_set",
    )

    format_version: str = json_field(default=TEXTURE_SET_VERSION, init=False)
    texture_set: _TextureSet = json_field(
        key="minecraft:texture_set", default_factory=_TextureSet
    )


class TextureSet(JsonFile):
    """Represents a PBR Texture Set configuration for Minecraft Bedrock Edition.

    Allows linking base color textures with physical property maps (normal, height, MER, MERS)
    and handles copying the files to the resource pack layout.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/visualreference/texture_set.v1.21.30)
    """

    _document = _TextureSetFile
    _object_type = "Texture Set"
    _extension = ".texture_set.json"
    _pack = Pack.RP

    def __init__(
        self,
        texture_name: str,
        target: Literal["blocks", "items", "entities", "particle", "actors"],
        overriding_vanilla: bool = False,
    ) -> None:
        """Initializes a new TextureSet instance.

        Args:
            texture_name (str): The name of the texture.
            target (Literal["blocks", "items"]): The target directory layout/namespace.

        Raises:
            RuntimeError: If PBR is not enabled in the configuration and auxiliary maps are specified.
        """
        super().__init__(texture_name)
        self._target = target
        self._overriding_vanilla = overriding_vanilla
        if self._overriding_vanilla:
            self._folder = Path("textures", target)
        else:
            self._folder = Path("textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME)

    def __validate(
        self,
        components: TextureComponents,
    ):
        """Validates PBR texture components for mutual exclusivity and format correctness.

        Args:
            components (TextureComponents): The texture components to validate.

        Returns:
            dict[str, str]: A dictionary of PBR maps and their validated/converted hex values.

        Raises:
            ValueError: If mutually exclusive components are provided.
            RuntimeError: If auxiliary maps are used when PBR is disabled in configuration.
        """
        if not CONFIG.PBR and components.has_aux():
            raise RuntimeError(
                "PBR maps (normal, height, MER, MERS) require PBR to be enabled in the config."
            )

        color_map: dict[str, str] = {}
        if components.normal is not None and components.height is not None:
            raise ValueError("Normal and heightmap textures are mutually exclusive.")
        if components.mer is not None and components.mers is not None:
            raise ValueError(
                "Metalness, emissive, roughness and subsurface textures are mutually exclusive."
            )

        if AnvilValidator.is_color_value(components.color):
            color_map["color"] = AnvilFormatter.convert_color(components.color, HexRGB)
        if AnvilValidator.is_color_value(components.normal):
            color_map["normal"] = AnvilFormatter.convert_color(
                components.normal, HexRGB
            )
        if AnvilValidator.is_color_value(components.height):
            color_map["heightmap"] = AnvilFormatter.convert_color(
                components.height, HexRGB
            )
        if AnvilValidator.is_color_value(components.mer):
            color_map["metalness_emissive_roughness"] = AnvilFormatter.convert_color(
                components.mer, HexRGB
            )
        if AnvilValidator.is_color_value(components.mers):
            color_map["metalness_emissive_roughness_subsurface"] = (
                AnvilFormatter.convert_color(components.mers, HexRGBA)
            )

        return color_map

    def __set_individual_textures(
        self,
        source: str,
        components: TextureComponents,
    ):
        """Queues individual texture files to be copied and populates the texture set definition content.

        Args:
            source (str): The source folder under 'assets/' (e.g., 'textures/items').
            components (TextureComponents): The PBR texture components.

        Raises:
            FileNotFoundError: If configured texture image files do not exist in 'assets/'.
        """
        color_map = self.__validate(components)

        color_map["color"] = components.color
        self._queued_textures: dict[str, dict[str, list[str]]] = {
            source: {components.color: [components.color]}
        }
        if not (Path("assets", source) / f"{components.color}.png").exists():
            raise FileNotFoundError(
                f"Color texture file '{components.color}.png' does not exist in 'assets/{source}'. {self._object_type}[{self.identifier.name}]"
            )

        if isinstance(components.normal, str) and not components.normal.startswith("#"):
            if not (Path("assets", source) / f"{components.normal}.png").exists():
                raise FileNotFoundError(
                    f"Normal texture file '{components.normal}.png' does not exist in 'assets/{source}'. {self._object_type}[{self.identifier.name}]"
                )
            color_map["normal"] = components.normal
            self._queued_textures.get(source).get(components.color).append(
                components.normal
            )

        if isinstance(components.height, str) and not components.height.startswith("#"):
            if not (Path("assets", source) / f"{components.height}.png").exists():
                raise FileNotFoundError(
                    f"Height texture file '{components.height}.png' does not exist in 'assets/{source}'. {self._object_type}[{self.identifier.name}]"
                )
            color_map["heightmap"] = components.height
            self._queued_textures.get(source).get(components.color).append(
                components.height
            )

        if isinstance(components.mer, str) and not components.mer.startswith("#"):
            if not (Path("assets", source) / f"{components.mer}.png").exists():
                raise FileNotFoundError(
                    f"MER texture file '{components.mer}.png' does not exist in 'assets/{source}'. {self._object_type}[{self.identifier.name}]"
                )
            color_map["metalness_emissive_roughness"] = components.mer
            self._queued_textures.get(source).get(components.color).append(
                components.mer
            )

        if isinstance(components.mers, str) and not components.mers.startswith("#"):
            if not (Path("assets", source) / f"{components.mers}.png").exists():
                raise FileNotFoundError(
                    f"MERS texture file '{components.mers}.png' does not exist in 'assets/{source}'. {self._object_type}[{self.identifier.name}]"
                )
            color_map["metalness_emissive_roughness_subsurface"] = components.mers
            self._queued_textures.get(source).get(components.color).append(
                components.mers
            )

        self._content.texture_set.set_layers(color_map)
        self._folder = self._folder / self._target

    def set_particle_textures(
        self,
        components: TextureComponents,
    ) -> "TextureSet":
        """Sets the texture components specifically for a particle texture set.

        Args:
            components (TextureComponents): The PBR texture components for the particle.
        """
        self.__set_individual_textures(
            "particles",
            components,
        )
        return self

    def set_item_textures(
        self,
        components: TextureComponents,
    ) -> "TextureSet":
        """Sets the texture components specifically for an item texture set.

        Args:
            components (TextureComponents): The PBR texture components for the item.
        """
        self.__set_individual_textures("textures/items", components)
        return self

    def set_blockbench_textures(
        self,
        blockbench: str,
        components: TextureComponents,
    ) -> "TextureSet":
        """Sets texture components using standard Blockbench exporter conventions.

        Args:
            blockbench (str): The name of the blockbench model asset directory.
            components (TextureComponents): The PBR texture components.
        """
        color_map = self.__validate(components)

        self._blockbench = _Blockbench(blockbench, self._target)
        self._blockbench.textures.queue_texture(components.color)
        color_map["color"] = components.color
        if isinstance(components.normal, str) and not components.normal.startswith("#"):
            self._blockbench.textures.queue_texture(components.normal)
            color_map["normal"] = components.normal
        if isinstance(components.height, str) and not components.height.startswith("#"):
            self._blockbench.textures.queue_texture(components.height)
            color_map["heightmap"] = components.height
        if isinstance(components.mer, str) and not components.mer.startswith("#"):
            self._blockbench.textures.queue_texture(components.mer)
            color_map["metalness_emissive_roughness"] = components.mer
        if isinstance(components.mers, str) and not components.mers.startswith("#"):
            self._blockbench.textures.queue_texture(components.mers)
            color_map["metalness_emissive_roughness_subsurface"] = components.mers

        self._folder = self._folder / self._target / blockbench
        self._content.texture_set.set_layers(color_map)
        return self

    def set_vanilla_texture(
        self,
        blockbench: str,
        components: TextureComponents,
        subfolder: str = "",
    ) -> "TextureSet":
        """Sets texture components for overriding a vanilla texture.

        Args:
            blockbench (str): The name of the blockbench model asset directory.
            components (TextureComponents): The PBR texture components.
            subfolder (str, optional): Subfolder under RP_PATH/textures/blocks. Defaults to "".
        """
        color_map = self.__validate(components)

        dest_dir = CONFIG.RP_PATH / "textures" / self._target / subfolder

        self._blockbench = _Blockbench(blockbench, self._target)
        self._blockbench.textures.queue_texture(components.color, dest_dir=dest_dir)
        color_map["color"] = components.color
        if isinstance(components.normal, str) and not components.normal.startswith("#"):
            self._blockbench.textures.queue_texture(
                components.normal, dest_dir=dest_dir
            )
            color_map["normal"] = components.normal
        if isinstance(components.height, str) and not components.height.startswith("#"):
            self._blockbench.textures.queue_texture(
                components.height, dest_dir=dest_dir
            )
            color_map["heightmap"] = components.height
        if isinstance(components.mer, str) and not components.mer.startswith("#"):
            self._blockbench.textures.queue_texture(components.mer, dest_dir=dest_dir)
            color_map["metalness_emissive_roughness"] = components.mer
        if isinstance(components.mers, str) and not components.mers.startswith("#"):
            self._blockbench.textures.queue_texture(components.mers, dest_dir=dest_dir)
            color_map["metalness_emissive_roughness_subsurface"] = components.mers

        self._content.texture_set.set_layers(color_map)
        return self

    def __export__(self) -> None:
        """Copies queued texture image assets to the destination resource pack and compiles the texture set definition JSON."""
        if hasattr(self, "_queued_textures"):
            for source, textures in self._queued_textures.items():
                for color, texture_list in textures.items():
                    for texture in texture_list:
                        Directory.copy_files(
                            Path("assets", source),
                            self._path,
                            f"{texture}.png",
                        )

        if CONFIG.PBR and (
            self._content.texture_set.layer_count > 1
            or self._target == "particle"
            or self._overriding_vanilla
        ):
            super().__export__()
