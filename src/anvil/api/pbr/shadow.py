from typing import Annotated, ClassVar, Literal

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import SHADOW_SETTINGS_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, Positive, json_field

__all__ = ["ShadowSettings"]


class _ShadowSettings(JsonObject):
    """The `minecraft:shadow_settings` object. Unset keys are left out, so the game uses soft
    shadows and a texel size of 16.
    """

    shadow_style: Literal["blocky_shadows", "soft_shadows"] | None = None
    texel_size: Annotated[int, Positive] | None = None

    def set_shadow_style(
        self, style: Literal["blocky_shadows", "soft_shadows"], texel_size: int
    ) -> None:
        """Sets the shadow style and the resolution shadow texels snap to.

        Args:
            style (Literal["blocky_shadows", "soft_shadows"]): The style of shadows to render.
            texel_size (int): The resolution shadow texels snap to.
        """
        self.shadow_style = style
        self.texel_size = texel_size


class _ShadowSettingsFile(JsonObject):
    """The content of `shadows/global.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:shadow_settings",
    )

    format_version: str = json_field(default=SHADOW_SETTINGS_VERSION, init=False)
    settings: _ShadowSettings = json_field(
        key="minecraft:shadow_settings", default_factory=_ShadowSettings
    )


class ShadowSettings(JsonFile):
    """Global shadow settings for Vibrant Visuals (PBR) rendering.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/shadowscustomization)
    """

    _document: _ShadowSettingsFile = _ShadowSettingsFile
    _file_name = "global"
    _extension = ".json"
    _pack = Pack.RP
    _folder = "shadows"
    _object_type = "Shadow Settings"

    def __init__(self) -> None:
        """Initializes a ShadowSettings instance.

        Raises:
            ValueError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__(self._file_name)

    def shadow_style(
        self, style: Literal["blocky_shadows", "soft_shadows"], texel_size: int = 16
    ) -> "ShadowSettings":
        """Sets the shadow style and resolution.

        Args:
            style (Literal["blocky_shadows", "soft_shadows"]): The style of shadows to render.
            texel_size (int, optional): The resolution shadow texels snap to, usually the
                resolution of the pack's block textures. Defaults to 16.
        """
        self._content.settings.set_shadow_style(style, texel_size)
        return self
