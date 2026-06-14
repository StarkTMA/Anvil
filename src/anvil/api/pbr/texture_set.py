import os
from dataclasses import dataclass
from typing import Literal

from anvil.api.core.types import (
    Color,
    HexRGB,
    HexRGBA,
)
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilFormatter, AnvilValidator, Directory, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


@dataclass
class KeyFrame:
    """Represents a single keyframe for animating properties over the daily cycle.

    Attributes:
        time (float): The time of day, between 0.0 and 1.0 (clamped).
        value (float | Color): The value at this keyframe (could be a float, RGB tuple, or Hex color).
    """

    time: float
    value: float | Color

    @classmethod
    def keyframe_dict(
        cls,
        keyframes: list["KeyFrame"],
        target_color_format=None,
    ) -> dict[str, float | Color]:
        """Converts a list of KeyFrames into a dictionary suitable for Minecraft JSON.

        Each keyframe's time will be clamped to [0.0, 1.0] and formatted as a string key.

        Args:
            keyframes (list[KeyFrame]): A list of keyframe instances to convert.
            target_color_format (optional): The target color type class (e.g. HexRGB, RGB) to convert color values to.

        Returns:
            dict[str, float | Color]: A dictionary mapping normalized time strings to their corresponding values.
        """
        result = {}
        for k in keyframes:
            time_str = str(clamp(k.time, 0.0, 1.0))
            if AnvilValidator.is_color_value(k.value):
                result[time_str] = AnvilFormatter.convert_color(
                    k.value, target_color_format
                )
            else:
                result[time_str] = k.value
        return result


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
    normal: str | Color | None = None
    height: str | Color | None = None
    mer: str | Color | None = None
    mers: str | Color | None = None

    def has_aux(self) -> bool:
        """Checks if the texture components have any auxiliary texture maps (normal, height, mer, or mers).

        Returns:
            bool: True if at least one auxiliary texture component is configured, False otherwise.
        """
        return bool(self.normal or self.height or self.mer or self.mers)


class TextureSet(AddonObject):
    """Represents a PBR Texture Set configuration for Minecraft Bedrock Edition.

    Allows linking base color textures with physical property maps (normal, height, MER, MERS)
    and handles copying the files to the resource pack layout.
    """

    _object_type = "Texture Set"
    _extension = ".texture_set.json"
    _path = os.path.join(
        CONFIG.RP_PATH,
        "textures",
        CONFIG.NAMESPACE,
        CONFIG.PROJECT_NAME,
    )

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
            RuntimeError: If PBR is not enabled in the configuration.
        """
        super().__init__(texture_name)
        if not CONFIG.PBR:
            raise RuntimeError("Texture sets require PBR to be enabled in the config.")

        self.content(JsonSchemes.texture_set())
        self._target = target
        self._overriding_vanilla = overriding_vanilla
        if self._overriding_vanilla:
            self._path = os.path.join(
                CONFIG.RP_PATH,
                "textures",
                target,
            )
        else:
            self._path = os.path.join(
                CONFIG.RP_PATH,
                "textures",
                CONFIG.NAMESPACE,
                CONFIG.PROJECT_NAME,
            )

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
        """
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
        if not os.path.exists(
            os.path.join("assets", source, f"{components.color}.png")
        ):
            raise FileNotFoundError(
                f"Color texture file '{components.color}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
            )

        if isinstance(components.normal, str) and not components.normal.startswith("#"):
            if not os.path.exists(
                os.path.join("assets", source, f"{components.normal}.png")
            ):
                raise FileNotFoundError(
                    f"Normal texture file '{components.normal}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["normal"] = components.normal
            self._queued_textures.get(source).get(components.color).append(
                components.normal
            )

        if isinstance(components.height, str) and not components.height.startswith("#"):
            if not os.path.exists(
                os.path.join("assets", source, f"{components.height}.png")
            ):
                raise FileNotFoundError(
                    f"Height texture file '{components.height}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["heightmap"] = components.height
            self._queued_textures.get(source).get(components.color).append(
                components.height
            )

        if isinstance(components.mer, str) and not components.mer.startswith("#"):
            if not os.path.exists(
                os.path.join("assets", source, f"{components.mer}.png")
            ):
                raise FileNotFoundError(
                    f"MER texture file '{components.mer}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["metalness_emissive_roughness"] = components.mer
            self._queued_textures.get(source).get(components.color).append(
                components.mer
            )

        if isinstance(components.mers, str) and not components.mers.startswith("#"):
            if not os.path.exists(
                os.path.join("assets", source, f"{components.mers}.png")
            ):
                raise FileNotFoundError(
                    f"MERS texture file '{components.mers}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["metalness_emissive_roughness_subsurface"] = components.mers
            self._queued_textures.get(source).get(components.color).append(
                components.mers
            )

        self._content["minecraft:texture_set"].update(color_map)
        self._path = os.path.join(self._path, self._target)

    def set_particle_textures(
        self,
        components: TextureComponents,
    ):
        """Sets the texture components specifically for a particle texture set.

        Args:
            components (TextureComponents): The PBR texture components for the particle.
        """
        self.__set_individual_textures(
            "particles",
            components,
        )

    def set_item_textures(
        self,
        components: TextureComponents,
    ):
        """Sets the texture components specifically for an item texture set.

        Args:
            components (TextureComponents): The PBR texture components for the item.
        """
        self.__set_individual_textures("textures/items", components)

    def set_blockbench_textures(
        self,
        blockbench_name: str,
        components: TextureComponents,
    ):
        """Sets texture components using standard Blockbench exporter conventions.

        Args:
            blockbench_name (str): The name of the blockbench model asset directory.
            components (TextureComponents): The PBR texture components.
        """
        color_map = self.__validate(components)

        self._blockbench = _Blockbench(blockbench_name, self._target)
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

        self._path = os.path.join(self._path, self._target, blockbench_name)
        self._content["minecraft:texture_set"].update(color_map)

    def set_vanilla_texture(
        self,
        blockbench_name: str,
        components: TextureComponents,
        subfolder: str = "",
    ):
        """Sets texture components for overriding a vanilla texture.

        Args:
            blockbench_name (str): The name of the blockbench model asset directory.
            components (TextureComponents): The PBR texture components.
            subfolder (str, optional): Subfolder under RP_PATH/textures/blocks. Defaults to "".
        """
        color_map = self.__validate(components)

        dest_dir = os.path.join(
            CONFIG.RP_PATH,
            "textures",
            self._target,
            subfolder,
        )

        self._blockbench = _Blockbench(blockbench_name, self._target)
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

        self._content["minecraft:texture_set"].update(color_map)

    def __export__(self):
        """Copies queued texture image assets to the destination resource pack and compiles the texture set definition JSON."""
        if hasattr(self, "_queued_textures"):
            for source, textures in self._queued_textures.items():
                for color, texture_list in textures.items():
                    for texture in texture_list:
                        Directory.copy_files(
                            os.path.join("assets", source),
                            self._path,
                            f"{texture}.png",
                        )

        if (
            len(self._content["minecraft:texture_set"].keys()) > 1
            or self._target == "particle"
            or self._overriding_vanilla
        ):
            super().__export__()
