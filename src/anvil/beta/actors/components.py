
from anvil.api.core.components import (
    Component,
)
from anvil.api.core.types import *
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.schemas import (
    MinecraftEntityDescriptor,
)


class EntityReflectProjectiles(Component):
    _identifier = "minecraft:reflect_projectiles"

    def __init__(
        self,
        azimuth_angle: Molang | str = None,
        elevation_angle: Molang | str = None,
        reflected_projectiles: list[MinecraftEntityDescriptor | Identifier] = None,
        reflection_scale: Molang | str = None,
        reflection_sound: str = "reflect",
    ) -> None:
        """[EXPERIMENTAL] Allows an entity to reflect projectiles.

        Parameters:
            azimuth_angle (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the angle in degrees to add to the projectile's y axis rotation. Defaults to None.
            elevation_angle (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the angle in degrees to add to the projectile's x axis rotation. Defaults to None.
            reflected_projectiles (list[MinecraftEntityDescriptor | Identifier], optional): [EXPERIMENTAL] An array of strings defining the types of projectiles that are reflected when they hit the entity. Defaults to None.
            reflection_scale (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the velocity scaling of the reflected projectile. Values below 1 decrease the projectile's velocity, and values above 1 increase it. Defaults to None.
            reflection_sound (str, optional): [EXPERIMENTAL] A string defining the name of the sound event to be played when a projectile is reflected. "reflect" unless specified. Defaults to "reflect".

        ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles)
        """
        if not CONFIG._EXPERIMENTAL:
            raise NotImplementedError(
                "The 'EntityReflectProjectiles' component is experimental and requires the experimental flag to be enabled in anvilconfig.json."
            )

        super().__init__("reflect_projectiles")
        if azimuth_angle is not None:
            self._add_field("azimuth_angle", azimuth_angle)
        if elevation_angle is not None:
            self._add_field("elevation_angle", elevation_angle)
        if reflected_projectiles is not None:
            self._add_field("reflected_projectiles", reflected_projectiles)
        if reflection_scale is not None:
            self._add_field("reflection_scale", reflection_scale)
        if reflection_sound != "reflect":
            self._add_field("reflection_sound", reflection_sound)
