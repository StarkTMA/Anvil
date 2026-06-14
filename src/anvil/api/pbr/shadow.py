import os
from typing import Literal

from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


class ShadowSettings(AddonObject):
    """Global shadow settings for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "shadows")
    _object_type = "Shadow Settings"

    def __init__(self) -> None:
        """Initializes a ShadowSettings instance.

        Raises:
            RuntimeError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("global")
        self.content(JsonSchemes.shadow_settings())

    def shadow_style(
        self, style: Literal["blocky_shadows", "soft_shadows"], texel_size: float = 16
    ):
        """Sets the shadow style and resolution.

        Parameters:
            style (Literal["blocky_shadows", "soft_shadows"]): The style of shadows to render.
            texel_size (float, optional): Texel size for shadows. Defaults to 16.
        """
        self._content["minecraft:shadow_settings"]["shadow_style"] = style
        self._content["minecraft:shadow_settings"]["texel_size"] = texel_size
