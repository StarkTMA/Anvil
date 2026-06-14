import os

from anvil.api.core.types import (
    RGBA255,
)
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilFormatter
from anvil.lib.schemas import AddonObject, JsonSchemes


class PBRFallback(AddonObject):
    """PBR fallback settings acting as default values when texture sets are not provided."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "pbr")
    _object_type = "PBR Fallback Settings"

    def __init__(self) -> None:
        """Initializes a PBRFallback instance.

        Raises:
            RuntimeError: If PBR requires PBR to be enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError("PBR fallback requires PBR to be enabled in the config.")
        super().__init__("global")
        self.content(JsonSchemes.pbr_fallback_settings())

    def block_fallback(self, MERS: RGBA255) -> None:
        """Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for blocks that do not have PBR textures.

        Parameters:
            MERS (RGBA255): The RGBA values representing the fallback MERS in the 0-255 range.
        """
        self._content["minecraft:pbr_fallback_settings"]["blocks"] = {
            "global_metalness_emissive_roughness_subsurface": AnvilFormatter.convert_color(
                MERS, RGBA255
            )
        }

    def actors_fallback(self, MERS: RGBA255) -> None:
        """Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for actors that do not have PBR textures.

        Parameters:
            MERS (RGBA255): The RGBA values representing the fallback MERS in the 0-255 range.
        """
        self._content["minecraft:pbr_fallback_settings"]["actors"] = {
            "global_metalness_emissive_roughness_subsurface": AnvilFormatter.convert_color(
                MERS, RGBA255
            )
        }

    def particles_fallback(self, MERS: RGBA255) -> None:
        """Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for particles that do not have PBR textures.

        Parameters:
            MERS (RGBA255): The RGBA values representing the fallback MERS in the 0-255 range.
        """
        self._content["minecraft:pbr_fallback_settings"]["particles"] = {
            "global_metalness_emissive_roughness_subsurface": AnvilFormatter.convert_color(
                MERS, RGBA255
            )
        }

    def items_fallback(self, MERS: RGBA255) -> None:
        """Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for items that do not have PBR textures.

        Parameters:
            MERS (RGBA255): The RGBA values representing the fallback MERS in the 0-255 range.
        """
        self._content["minecraft:pbr_fallback_settings"]["items"] = {
            "global_metalness_emissive_roughness_subsurface": AnvilFormatter.convert_color(
                MERS, RGBA255
            )
        }

    def queue(self):
        return super().queue()
