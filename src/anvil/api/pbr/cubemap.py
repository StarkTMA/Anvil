import os
from typing import overload

from anvil.api.pbr.texture_set import KeyFrame
from anvil.lib.config import CONFIG
from anvil.lib.lib import clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


class CubeMapSettings(AddonObject):
    """Cubemap settings for sky and indirect lighting in Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "cubemaps")
    _object_type = "Cube Map Settings"

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, identifier: str) -> None: ...

    def __init__(self, identifier: str = "minecraft:default_cubemap") -> None:
        """Initializes a CubeMapSettings instance.

        Parameters:
            identifier (str, optional): Unique identifier for the cubemap. Defaults to "minecraft:default_cubemap".

        Raises:
            RuntimeError: If PBR requires PBR to be enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Cube map settings require PBR to be enabled in the config."
            )

        if identifier == "minecraft:default_cubemap":
            super().__init__(identifier, True)
        else:
            super().__init__(identifier)

        self.content(JsonSchemes.cubemap_settings(self.identifier))

    def set_lighting(
        self,
        ambient_light_illuminance: list[KeyFrame] = [
            KeyFrame(0.0, 5.625),
            KeyFrame(1.0, 5.625),
        ],
        sky_light_contribution: float = 1.0,
        directional_light_contribution: float = 1.0,
        affected_by_atmospheric_scattering: bool = False,
        affected_by_volumetric_scattering: bool = False,
    ):
        """Set lighting parameters for the cubemap.

        Parameters:
            ambient_light_illuminance (list[KeyFrame], optional): Keyframed ambient illuminance (lux) over the day cycle. Each keyframe's time is clamped to [0.0, 1.0] and values should be in [0.0, 100000.0]. Defaults to a constant 5.625 lux across the day.
            sky_light_contribution (float, optional): How much the sky light contributes to the cubemap, in [0.0, 1.0]. Default 1.0.
            directional_light_contribution (float, optional): How much directional light (sun/moon) contributes to the cubemap, in [0.0, 1.0]. Default 1.0.
            affected_by_atmospheric_scattering (bool, optional): Whether the cubemap is affected by atmospheric scattering (horizon/sky effects). Use True for near-surface sky content. Default False.
            affected_by_volumetric_scattering (bool, optional): Whether the cubemap is affected by volumetric scattering (fog/light shafts). Default False.
        """

        self._content["minecraft:cubemap_settings"]["lighting"] = {
            "ambient_light_illuminance": KeyFrame.keyframe_dict(
                ambient_light_illuminance
            ),
            "sky_light_contribution": clamp(sky_light_contribution, 0.0, 1.0),
            "directional_light_contribution": clamp(
                directional_light_contribution, 0.0, 1.0
            ),
            "affected_by_atmospheric_scattering": affected_by_atmospheric_scattering,
            "affected_by_volumetric_scattering": affected_by_volumetric_scattering,
        }
