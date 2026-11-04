from typing import Annotated, ClassVar, overload

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    KeyFramed,
    Wrapped,
    json_field,
)

__all__ = ["CubeMapSettings"]


class _CubeMapLighting(JsonObject):
    """The `lighting` object of a cubemap. Unset keys are left out."""

    ambient_light_illuminance: (
        Annotated[float | list[tuple[float, float]], KeyFramed(0.0, 100000.0)] | None
    ) = None
    sky_light_contribution: Annotated[float, InRange(0.0, 1.0)] | None = None
    directional_light_contribution: Annotated[float, InRange(0.0, 1.0)] | None = None
    affected_by_atmospheric_scattering: bool | None = None
    affected_by_volumetric_scattering: bool | None = None

    def set_ambient_light_illuminance(
        self, ambient_light_illuminance: float | list[tuple[float, float]]
    ) -> None:
        """Sets the ambient illuminance in lux, from 0.0 to 100000.0."""
        self.ambient_light_illuminance = ambient_light_illuminance

    def set_sky_light_contribution(self, sky_light_contribution: float) -> None:
        """Sets how much the sky light contributes, from 0.0 to 1.0."""
        self.sky_light_contribution = sky_light_contribution

    def set_directional_light_contribution(
        self, directional_light_contribution: float
    ) -> None:
        """Sets how much the sun and moon contribute, from 0.0 to 1.0."""
        self.directional_light_contribution = directional_light_contribution

    def set_affected_by_atmospheric_scattering(
        self, affected_by_atmospheric_scattering: bool
    ) -> None:
        """Sets whether atmospheric scattering affects the cubemap."""
        self.affected_by_atmospheric_scattering = affected_by_atmospheric_scattering

    def set_affected_by_volumetric_scattering(
        self, affected_by_volumetric_scattering: bool
    ) -> None:
        """Sets whether volumetric scattering affects the cubemap."""
        self.affected_by_volumetric_scattering = affected_by_volumetric_scattering


class _CubeMapSettings(JsonObject):
    """The `minecraft:cubemap_settings` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    lighting: _CubeMapLighting = json_field(default_factory=_CubeMapLighting)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _CubeMapSettingsFile(JsonObject):
    """The content of a `cubemaps/*.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:cubemap_settings",
    )

    format_version: str = json_field(default=MANIFEST_BUILD, init=False)
    settings: _CubeMapSettings = json_field(
        key="minecraft:cubemap_settings", default_factory=_CubeMapSettings
    )


class CubeMapSettings(JsonFile):
    """Cubemap settings for sky and indirect lighting in Vibrant Visuals (PBR) rendering.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/cubemapcustomization)
    """

    _document = _CubeMapSettingsFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "cubemaps"
    _object_type = "Cube Map Settings"

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, identifier: str) -> None: ...

    def __init__(self, identifier: str = "minecraft:default_cubemap") -> None:
        """Initializes a CubeMapSettings instance.

        Args:
            identifier (str, optional): Unique identifier for the cubemap. Defaults to "minecraft:default_cubemap".

        Raises:
            ValueError: If PBR requires PBR to be enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Cube map settings require PBR to be enabled in the config."
            )

        is_vanilla = identifier == "minecraft:default_cubemap"
        super().__init__(identifier, is_vanilla)
        self._content.settings.set_description(self.identifier)

    def set_lighting(
        self,
        ambient_light_illuminance: list[tuple[float, float]] = [
            (0.0, 5.625),
            (1.0, 5.625),
        ],
        sky_light_contribution: float = 1.0,
        directional_light_contribution: float = 1.0,
        affected_by_atmospheric_scattering: bool = False,
        affected_by_volumetric_scattering: bool = False,
    ) -> "CubeMapSettings":
        """Set lighting parameters for the cubemap.

        Args:
            ambient_light_illuminance (list[tuple[float, float]], optional): Keyframed ambient illuminance (lux) over the day cycle. Each keyframe's time must be from 0.0 to 1.0 and each value from 0.0 to 100000.0. Defaults to a constant 5.625 lux across the day.
            sky_light_contribution (float, optional): How much the sky light contributes to the cubemap, in [0.0, 1.0]. Default 1.0.
            directional_light_contribution (float, optional): How much directional light (sun/moon) contributes to the cubemap, in [0.0, 1.0]. Default 1.0.
            affected_by_atmospheric_scattering (bool, optional): Whether the cubemap is affected by atmospheric scattering (horizon/sky effects). Use True for near-surface sky content. Default False.
            affected_by_volumetric_scattering (bool, optional): Whether the cubemap is affected by volumetric scattering (fog/light shafts). Default False.
        """

        lighting = self._content.settings.lighting
        lighting.set_ambient_light_illuminance(ambient_light_illuminance)
        lighting.set_sky_light_contribution(sky_light_contribution)
        lighting.set_directional_light_contribution(directional_light_contribution)
        lighting.set_affected_by_atmospheric_scattering(
            affected_by_atmospheric_scattering
        )
        lighting.set_affected_by_volumetric_scattering(
            affected_by_volumetric_scattering
        )
        return self
