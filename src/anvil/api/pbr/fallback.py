from typing import Annotated, ClassVar

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import PBR_FALLBACK_SETTINGS_VERSION
from anvil.lib.jsonmodel import (
    JsonFile,
    JsonObject,
    RGB255Color,
    RGBA255Color,
    json_field,
)
from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA

__all__ = ["PBRFallback"]


class _PBRFallback(JsonObject):
    """The fallback MERS (Metalness, Emissive, Roughness, Subsurface) values of one kind of
    object that has no texture set. Unset keys are left out.
    """

    global_metalness_emissive_roughness: (
        Annotated[HexRGB | RGB | RGB255, RGB255Color] | None
    ) = None
    global_metalness_emissive_roughness_subsurface: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, RGBA255Color] | None
    ) = None

    def set_global_metalness_emissive_roughness(
        self, MER: HexRGB | RGB | RGB255
    ) -> None:
        """Sets the fallback metalness, emissive and roughness values.

        Args:
            MER (HexRGB | RGB | RGB255): The color holding the values, without an alpha channel.
        """
        self.global_metalness_emissive_roughness = MER

    def set_global_metalness_emissive_roughness_subsurface(
        self, MERS: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> None:
        """Sets the fallback metalness, emissive, roughness and subsurface values.

        Args:
            MERS (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The color holding the values, in any color format.
        """
        self.global_metalness_emissive_roughness_subsurface = MERS


class _PBRFallbackSettings(JsonObject):
    """The `minecraft:pbr_fallback_settings` object, one fallback per kind of object."""

    actors: _PBRFallback = json_field(default_factory=_PBRFallback)
    blocks: _PBRFallback = json_field(default_factory=_PBRFallback)
    items: _PBRFallback = json_field(default_factory=_PBRFallback)
    particles: _PBRFallback = json_field(default_factory=_PBRFallback)


class _PBRFallbackFile(JsonObject):
    """The content of `pbr/global.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:pbr_fallback_settings",
    )

    format_version: str = json_field(default=PBR_FALLBACK_SETTINGS_VERSION, init=False)
    settings: _PBRFallbackSettings = json_field(
        key="minecraft:pbr_fallback_settings", default_factory=_PBRFallbackSettings
    )


class PBRFallback(JsonFile):
    """PBR fallback settings acting as default values when texture sets are not provided.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/deferredrendering/pbrfallbackconfig_pbrfallbackconfigsettings)
    """

    _document = _PBRFallbackFile
    _file_name = "global"
    _extension = ".json"
    _pack = Pack.RP
    _folder = "pbr"
    _object_type = "PBR Fallback Settings"

    def __init__(self) -> None:
        """Initializes a PBRFallback instance.

        Raises:
            ValueError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError("PBR fallback requires PBR to be enabled in the config.")
        super().__init__(self._file_name)

    def block_fallback(
        self, MERS: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> "PBRFallback":
        """Sets the fallback MERS (Metalness, Emissive, Roughness, Subsurface) values for blocks that do not have PBR textures.

        Args:
            MERS (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The MERS values as a color in any format, written as four whole numbers from 0 to 255.
        """
        self._content.settings.blocks.set_global_metalness_emissive_roughness_subsurface(
            MERS
        )
        return self

    def actors_fallback(
        self, MERS: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> "PBRFallback":
        """Sets the fallback MERS (Metalness, Emissive, Roughness, Subsurface) values for actors that do not have PBR textures.

        Args:
            MERS (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The MERS values as a color in any format, written as four whole numbers from 0 to 255.
        """
        self._content.settings.actors.set_global_metalness_emissive_roughness_subsurface(
            MERS
        )
        return self

    def particles_fallback(
        self, MERS: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> "PBRFallback":
        """Sets the fallback MERS (Metalness, Emissive, Roughness, Subsurface) values for particles that do not have PBR textures.

        Args:
            MERS (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The MERS values as a color in any format, written as four whole numbers from 0 to 255.
        """
        self._content.settings.particles.set_global_metalness_emissive_roughness_subsurface(
            MERS
        )
        return self

    def items_fallback(
        self, MERS: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> "PBRFallback":
        """Sets the fallback MERS (Metalness, Emissive, Roughness, Subsurface) values for items that do not have PBR textures.

        Args:
            MERS (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The MERS values as a color in any format, written as four whole numbers from 0 to 255.
        """
        self._content.settings.items.set_global_metalness_emissive_roughness_subsurface(
            MERS
        )
        return self
