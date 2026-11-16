from typing import Annotated

from anvil.api.actors.entity import Entity
from anvil.api.core.components import EventTrigger
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import EntityId, JsonComponent, JsonObject, json_field
from anvil.lib.jsonmodel.enums import FilterSubject


class TimeMarkerSensorTrigger(JsonObject):
    """A world clock time marker `minecraft:time_marker_sensor` listens for, and the event it runs.

    Args:
        clock (str): The name of the world clock to listen to.
        time_marker (str): The name of the time marker on the clock to listen for.
        on_time_marker (EventTrigger): Event to run when the time marker fires, with its conditions and target.
    """

    clock: str = json_field()
    time_marker: str = json_field()
    on_time_marker: EventTrigger = json_field()


class EntityReflectProjectiles(JsonComponent):
    """[EXPERIMENTAL] Allows an entity to reflect projectiles. Needs the experimental flag in anvilconfig.json.

    Args:
        azimuth_angle (Molang | str | float, optional): Angle in degrees added to the projectile's y axis rotation. Game default 0.
        elevation_angle (Molang | str | float, optional): Angle in degrees added to the projectile's x axis rotation. Game default 0.
        reflected_projectiles (list[str | Entity], optional): Projectiles that are reflected when they hit the entity.
        reflection_scale (Molang | str | float, optional): Velocity scale of the reflected projectile. Below 1 slows it, above 1 speeds it up. Game default 1.
        reflection_sound (str, optional): Sound event played when a projectile is reflected. Game default reflect.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles)
    """

    identifier = "minecraft:reflect_projectiles"

    azimuth_angle: Molang | str | float | None = json_field(default=None)
    elevation_angle: Molang | str | float | None = json_field(default=None)
    reflected_projectiles: list[Annotated[str | Entity, EntityId]] | None = json_field(
        default=None
    )
    reflection_scale: Molang | str | float | None = json_field(default=None)
    reflection_sound: str | None = json_field(default=None)

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityReflectProjectiles is experimental: turn on features.experimental in anvilconfig.json."
            )


class EntityCanStandOnBrittleIce(JsonComponent):
    """[EXPERIMENTAL] Allows an entity to stand on brittle ice. Needs the experimental flag in anvilconfig.json.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_stand_on_brittle_ice)
    """

    identifier = "minecraft:can_stand_on_brittle_ice"

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityCanStandOnBrittleIce is experimental: turn on features.experimental in anvilconfig.json."
            )


class EntityTimeMarkerSensor(JsonComponent):
    """[EXPERIMENTAL] Runs events on this entity when named time markers fire on named world clocks. Needs the experimental flag in anvilconfig.json.

    Args:
        triggers (list[TimeMarkerSensorTrigger]): The world clock time markers to listen for, at least one. Entries identical to an earlier one are ignored by the game. Add them with `add_trigger`.
    """

    identifier = "minecraft:time_marker_sensor"

    triggers: list[TimeMarkerSensorTrigger] = json_field(default_factory=list)

    def add_trigger(
        self,
        *,
        clock: str,
        time_marker: str,
        event: str,
        filters: Filter | None = None,
        target: FilterSubject | None = None,
    ) -> "EntityTimeMarkerSensor":
        """Adds a world clock time marker to listen for, and the event to run when it fires.

        Args:
            clock (str): The name of the world clock to listen to.
            time_marker (str): The name of the time marker on the clock to listen for.
            event (str): The event to run when the time marker fires.
            filters (Filter, optional): The conditions for the event to run.
            target (FilterSubject, optional): The entity the event runs on. Game default self.
        """
        self.triggers.append(
            TimeMarkerSensorTrigger(
                clock=clock,
                time_marker=time_marker,
                on_time_marker=EventTrigger(
                    event=event, filters=filters, target=target
                ),
            )
        )
        return self

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityTimeMarkerSensor is experimental: turn on features.experimental in anvilconfig.json."
            )
        if not self.triggers:
            raise ValueError("EntityTimeMarkerSensor needs at least one trigger.")
