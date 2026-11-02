from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import JsonComponent, json_field
from anvil.lib.schemas import MinecraftEntityDescriptor


class EntityReflectProjectiles(JsonComponent):
    """[EXPERIMENTAL] Allows an entity to reflect projectiles. Needs the experimental flag in anvilconfig.json.

    Args:
        azimuth_angle (Molang | str | float, optional): Angle in degrees added to the projectile's y axis rotation. Game default 0.
        elevation_angle (Molang | str | float, optional): Angle in degrees added to the projectile's x axis rotation. Game default 0.
        reflected_projectiles (list[MinecraftEntityDescriptor | str], optional): Projectiles that are reflected when they hit the entity.
        reflection_scale (Molang | str | float, optional): Velocity scale of the reflected projectile. Below 1 slows it, above 1 speeds it up. Game default 1.
        reflection_sound (str, optional): Sound event played when a projectile is reflected. Game default reflect.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles)
    """

    identifier = "minecraft:reflect_projectiles"

    azimuth_angle: Molang | str | float | None = json_field(default=None)
    elevation_angle: Molang | str | float | None = json_field(default=None)
    reflected_projectiles: list[MinecraftEntityDescriptor | str] | None = json_field(
        default=None
    )
    reflection_scale: Molang | str | float | None = json_field(default=None)
    reflection_sound: str | None = json_field(default=None)

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise NotImplementedError(
                "EntityReflectProjectiles is experimental and needs the experimental flag in anvilconfig.json."
            )
