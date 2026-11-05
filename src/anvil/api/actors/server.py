"""The behavior pack's `entities/<entity>.behavior.json`: a server entity, its description,
components, component groups and events."""

from typing import Annotated, Any, ClassVar, Literal

from anvil.api.actors.animation_controllers import (
    BPAnimationControllers,
    _ActorScripts,
    _BPAnimationController,
)
from anvil.api.actors.animations import BPAnimations, _BPAnimation
from anvil.api.actors.components import (
    EntityInstantDespawn,
    EntityPushableByBlock,
    EntityPushableByEntity,
    EntityRideable,
)
from anvil.api.actors.events import _Event
from anvil.api.actors.spawn_rules import SpawnRule
from anvil.api.core.components import ComponentGroup
from anvil.api.logic.molang import Molang, Variable
from anvil.lib.config import CONFIG, ConfigPackageTarget, Pack
from anvil.lib.format_versions import ENTITY_SERVER_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    Identifier,
    JsonFile,
    JsonObject,
    Keyed,
    json_field,
    validate_components,
)
from anvil.lib.jsonmodel.enums import DamageSensor
from anvil.lib.jsonmodel.types import SpawnCategory
from anvil.lib.translator import AnvilTranslator

__all__ = ["EntityServer"]


# region Description


class _EntityProperty(JsonObject):
    """An entity property of the project, `<namespace>:<name>`."""

    name: str = json_field(exclude=True, positional=True)
    type: Literal["enum", "int", "float", "bool"] = json_field()
    default: bool | int | float | str = json_field()
    values: list[str] | None = None
    range: tuple[int, int] | tuple[float, float] | None = None
    client_sync: bool = False


class _EntityServerDescription(JsonObject):
    """The `description` of a server entity, and its builders. Unset keys are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None
    is_spawnable: bool = json_field(default=True)
    is_summonable: bool = json_field(default=True)
    is_experimental: bool = json_field(default=False, omit_default=True)
    spawn_category: SpawnCategory | None = None
    runtime_identifier: str | None = None
    properties: Annotated[list[_EntityProperty], Keyed("name")] = json_field(
        default_factory=list, omit_default=True
    )
    animations: dict[str, str] = json_field(default_factory=dict)
    scripts: _ActorScripts = json_field(default_factory=_ActorScripts)

    _animations: list[_BPAnimation | _BPAnimationController] = json_field(
        default_factory=list, init=False, exclude=True
    )
    """The animations and controllers, in the order they were added."""

    @property
    def name(self) -> str:
        """The entity's name, without its namespace."""
        return self.identifier.name

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")
        if len(self.properties) > 32:
            raise ValueError(
                f"An entity can have at most 32 properties, it has {len(self.properties)}. "
                f"Entity [{self.identifier}]"
            )

    def _runtime_identifier(self, entity: str) -> Identifier:
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError(
                f"Using runtime is not allowed for packages of type '{CONFIG._TARGET}'. "
                f"Entity [{self.identifier}]"
            )
        if not isinstance(entity, str):
            raise TypeError(
                f"Expected a vanilla entity identifier, got {type(entity).__name__}. "
                f"Entity [{self.identifier}]"
            )
        return Identifier.parse(entity, vanilla=True, object_type="Runtime Identifier")

    def config(
        self,
        is_summonable: bool = True,
        is_spawnable: bool = True,
        is_experimental: bool = False,
        runtime_identifier: str | None = None,
        spawn_category: (
            Literal[
                "creature",
                "monster",
                "ambient",
                "axolotls",
                "water_creature",
                "water_ambient",
                "underground_water_creature",
                "misc",
            ]
            | None
        ) = None,
    ) -> "_EntityServerDescription":
        """Sets how the entity can be spawned. `is_spawnable` and `is_summonable` are always
        written, because the game treats them as False when they are missing.

        Args:
            is_summonable (bool, optional): Lets commands such as /summon spawn it.
                Defaults to True.
            is_spawnable (bool, optional): Gives it a spawn egg in the creative inventory.
                Defaults to True.
            is_experimental (bool, optional): Enables it only with the experimental toggle.
                Defaults to False.
            runtime_identifier (str, optional): The vanilla entity
                whose hard-coded behavior it takes.
            spawn_category (str, optional): The mob cap it counts toward,
                such as `creature` or `monster`. Left out when not given.
        """
        if is_experimental and CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError(
                "Experimental entities are not allowed for packages of type 'addon'. "
                f"Entity [{self.identifier}]."
            )
        self.is_summonable = is_summonable
        self.is_spawnable = is_spawnable
        self.is_experimental = is_experimental
        self.spawn_category = spawn_category
        if runtime_identifier is not None:
            self.runtime_identifier = self._runtime_identifier(runtime_identifier)
        return self

    def _add_property(self, name: str, **values: Any) -> "_EntityServerDescription":
        name = f"{CONFIG.NAMESPACE}:{name}"
        self.properties[:] = [p for p in self.properties if p.name != name]
        self.properties.append(_EntityProperty(name, **values))
        return self

    def add_enum_property(
        self,
        name: str,
        values: tuple[str, ...],
        default: str,
        *,
        client_sync: bool = False,
    ) -> "_EntityServerDescription":
        """Adds a property that holds one of some names.

        Args:
            name (str): The property name, without namespace.
            values (tuple[str, ...]): The names.
            default (str): The starting value.
            client_sync (bool, optional): Sends the value to clients. Defaults to False.
        """
        return self._add_property(
            name,
            type="enum",
            default=default,
            values=list(values),
            client_sync=client_sync,
        )

    def add_int_property(
        self,
        name: str,
        range: tuple[int, int],
        *,
        default: int | Molang = 0,
        client_sync: bool = False,
    ) -> "_EntityServerDescription":
        """Adds a property that holds a whole number.

        Args:
            name (str): The property name, without namespace.
            range (tuple[int, int]): The (min, max) values.
            default (int | Molang, optional): The starting value. Defaults to 0.
            client_sync (bool, optional): Sends the value to clients. Defaults to False.
        """
        return self._add_property(
            name,
            type="int",
            default=default if isinstance(default, Molang) else int(default),
            range=tuple(range),
            client_sync=client_sync,
        )

    def add_float_property(
        self,
        name: str,
        range: tuple[float, float],
        *,
        default: float | Molang = 0,
        client_sync: bool = False,
    ) -> "_EntityServerDescription":
        """Adds a property that holds a number.

        Args:
            name (str): The property name, without namespace.
            range (tuple[float, float]): The (min, max) values.
            default (float | Molang, optional): The starting value. Defaults to 0.
            client_sync (bool, optional): Sends the value to clients. Defaults to False.
        """
        return self._add_property(
            name,
            type="float",
            default=default if isinstance(default, Molang) else float(default),
            range=tuple(float(f) for f in range),
            client_sync=client_sync,
        )

    def add_bool_property(
        self, name: str, *, default: bool = False, client_sync: bool = False
    ) -> "_EntityServerDescription":
        """Adds a property that holds true or false.

        Args:
            name (str): The property name, without namespace.
            default (bool, optional): The starting value. Defaults to False.
            client_sync (bool, optional): Sends the value to clients. Defaults to False.
        """
        return self._add_property(
            name, type="bool", default=default, client_sync=client_sync
        )

    def animation(
        self,
        animation_name: str,
        loop: bool | None = None,
        animate: bool = False,
        condition: str | Molang | None = None,
    ) -> _BPAnimation:
        """Returns the behavior pack animation with this name, added on first use, and maps
        its short name.

        Args:
            animation_name (str): The animation's short name.
            loop (bool, optional): If it loops, set when the animation is added. Defaults to
                False.
            animate (bool, optional): Runs it all the time. Defaults to False.
            condition (str | Molang, optional): When it runs, with `animate`.
        """
        animation = next(
            (
                a
                for a in self._animations
                if isinstance(a, _BPAnimation) and a.name == animation_name
            ),
            None,
        )
        if animation is None:
            animation = _BPAnimation(
                animation_name, owner=self.identifier, loop=bool(loop)
            )
            self._animations.append(animation)
        elif loop is not None and loop != animation.loop:
            raise ValueError(
                f"Animation '{animation_name}' was added with loop={animation.loop}. "
                f"Entity [{self.identifier}]"
            )
        if animate is True:
            animation._set_animate(condition)
        return animation

    def animation_controller(
        self,
        controller_name: str,
        animate: bool = False,
        condition: str | Molang | None = None,
        initial_state: str | None = None,
    ) -> _BPAnimationController:
        """Returns the behavior pack animation controller with this name, added on first
        use, and maps its short name.

        Args:
            controller_name (str): The controller's short name.
            animate (bool, optional): Runs it all the time. Defaults to False.
            condition (str | Molang, optional): When it runs, with `animate`.
            initial_state (str, optional): The state it starts in, set when the controller is
                added. Defaults to `default`.
        """
        controller = next(
            (
                c
                for c in self._animations
                if isinstance(c, _BPAnimationController) and c.name == controller_name
            ),
            None,
        )
        if controller is None:
            controller = _BPAnimationController(
                controller_name,
                owner=self.identifier,
                initial_state=initial_state or "default",
            )
            self._animations.append(controller)
        elif initial_state is not None and initial_state != controller.initial_state:
            raise ValueError(
                f"Animation controller '{controller_name}' was added with initial state "
                f"'{controller.initial_state}'. Entity [{self.identifier}]"
            )
        if animate is True:
            controller._set_animate(condition)
        return controller

    def __prepare_export__(self, owner: JsonFile, *, root: bool = True) -> None:
        """Maps the animations and the controllers that have something to write, runs the
        animated ones, and queues their files next to the owner's."""
        self._animations = [
            entry
            for entry in self._animations
            if not (isinstance(entry, _BPAnimationController) and entry._is_empty())
        ]
        for entry in self._animations:
            self.animations[entry.name] = entry.identifier
            if entry.animate:
                self.scripts.add_animate(entry.name, entry.condition)
        BPAnimationControllers(self).queue(owner._directory)
        BPAnimations(self).queue(owner._directory)


# endregion


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


def _groups(groups: list[ComponentGroup]) -> Any:
    return {group.name: group.__payload__() for group in groups}


# endregion


class _EntityServer(JsonObject):
    """The `minecraft:entity` body."""

    description: _EntityServerDescription = json_field(
        default_factory=_EntityServerDescription
    )
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )
    component_groups: Annotated[
        list[ComponentGroup], Encoded(_groups, {"type": "object"})
    ] = json_field(default_factory=list)
    events: Annotated[list[_Event], Keyed("name")] = json_field(default_factory=list)


class _EntityServerFile(JsonObject):
    """The content of a `.behavior.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:entity")

    format_version: str = json_field(default=ENTITY_SERVER_VERSION, init=False)
    entity: _EntityServer = json_field(
        default_factory=_EntityServer, key="minecraft:entity"
    )


class EntityServer(JsonFile):
    """A server entity: its description, components, component groups and events.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/)
    """

    _document = _EntityServerFile
    _extension = ".behavior.json"
    _pack = Pack.BP
    _folder = "entities"
    _object_type = "Server Entity"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a server entity.

        Args:
            name (str): The entity's name.
            is_vanilla (bool, optional): If the entity is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)
        self._spawn_rule = SpawnRule(self.identifier, self.identifier.is_vanilla)
        self._vars: list[str] = []
        self.component_group("despawn").add(EntityInstantDespawn())
        self.event("despawn").add_component_groups(["despawn"])

    @property
    def _body(self) -> _EntityServer:
        return self._content.entity

    @property
    def description(self) -> _EntityServerDescription:
        """The description builders."""
        return self._body.description

    @property
    def spawn_rule(self) -> SpawnRule:
        """The entity's spawn rules."""
        return self._spawn_rule

    @property
    def events(self) -> list[_Event]:
        """The entity's events, in the order they were added."""
        return self._body.events

    def init_vars(self, **vars) -> "EntityServer":
        """Initializes variables when the entity is created, in a `variables` controller."""
        for k, v in vars.items():
            Variable._set_var(k)
            self._vars.append(f"v.{k}={v}")
        return self

    def event(
        self,
        event_name: (
            Literal[
                "minecraft:entity_born",
                "minecraft:entity_spawned",
                "minecraft:entity_transformed",
                "minecraft:on_prime",
            ]
            | str
        ),
    ) -> _Event:
        """Returns the event with this name, added on first use.
            - `minecraft:entity_born` runs when the entity is born from breeding.
            - `minecraft:entity_spawned` runs when the entity spawns in the world.
            - `minecraft:entity_transformed` runs when another entity transforms into it.
            - `minecraft:on_prime` runs when the entity is about to explode.

        Args:
            event_name (str): The event name.
        """
        for event in self.events:
            if event.name == event_name:
                return event
        event = _Event(event_name)
        self.events.append(event)
        return event

    @property
    def components(self) -> ComponentGroup:
        """The entity's root components."""
        return self._body.components

    def component_group(self, component_group_name: str) -> ComponentGroup:
        """Returns the component group with this name, added on first use.

        Args:
            component_group_name (str): The group name.
        """
        if component_group_name == "components":
            raise ValueError(
                "'components' is the root group. Use `entity.server.components` instead."
            )
        for group in self._body.component_groups:
            if group.name == component_group_name:
                return group
        group = ComponentGroup(name=component_group_name)
        self._body.component_groups.append(group)
        return group

    def add_basic_components(self) -> "EntityServer":
        """Adds basic server components to the entity.

        This includes:
            - `EntityBreathable`
            - `EntityCollisionBox`
            - `EntityDamageSensor`
            - `EntityHealth`
            - `EntityJumpStatic`
            - `EntityKnockbackResistance`
            - `EntityMovement`
            - `EntityMovementBasic`
            - `EntityNavigationWalk`
            - `EntityPhysics`
            - `EntityPushableByBlock`
            - `EntityPushableByEntity`
            - `EntityPushThrough`
        """
        from anvil.api.actors.components import (
            EntityBreathable,
            EntityCollisionBox,
            EntityDamageSensor,
            EntityHealth,
            EntityJumpStatic,
            EntityKnockbackResistance,
            EntityMovement,
            EntityMovementBasic,
            EntityNavigationWalk,
            EntityPhysics,
            EntityPushThrough,
        )

        self.components.add(
            EntityJumpStatic(jump_power=0),
            EntityMovementBasic(),
            EntityNavigationWalk(),
            EntityMovement(value=0),
            EntityPhysics(),
            EntityKnockbackResistance(value=1.0),
            EntityHealth(value=6),
            EntityCollisionBox(height=1, width=1),
            EntityBreathable(),
            EntityDamageSensor().add_trigger(deals_damage=DamageSensor.No),
            EntityPushableByBlock(),
            EntityPushableByEntity(),
            EntityPushThrough(value=1),
        )
        return self

    def __export__(self) -> None:
        if self._vars:
            self.animation_controller("variables", True).add_state(
                "default"
            ).add_on_entry(*self._vars)
        self.description.__prepare_export__(self)
        self._spawn_rule.queue(directory=self._directory)

        body = self._body
        validate_components(self, body.components, body.component_groups)

        if body.components.has(EntityRideable) or any(
            group.has(EntityRideable) for group in body.component_groups
        ):
            AnvilTranslator().add_localization_entry(
                f"action.hint.exit.{self.identifier}", "Sneak to exit"
            )
        return super().__export__()
