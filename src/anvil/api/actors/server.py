from typing import Literal
from warnings import deprecated

from anvil.api.actors.animation_controllers import (
    BPAnimationControllers,
    _BP_Controller,
)
from anvil.api.actors.animations import BPAnimations, _BPAnimation
from anvil.api.actors.components import (
    EntityInstantDespawn,
    EntityPushableByBlock,
    EntityPushableByEntity,
    EntityRideable,
)
from anvil.api.actors.description import _ActorDescription
from anvil.api.actors.events import _Event
from anvil.api.actors.spawn_rules import SpawnRule
from anvil.api.core.components import ComponentGroup
from anvil.api.core.enums import DamageSensor
from anvil.api.logic.molang import Molang, Variable
from anvil.lib.config import CONFIG, ConfigPackageTarget, Pack
from anvil.lib.jsonmodel import encoders, validate_components
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
    MinecraftEntityDescriptor,
)
from anvil.lib.translator import AnvilTranslator

__all__ = ["EntityServer"]


class _Properties:
    def _enforce_count_limit(self):
        if len(self._properties) > 32:
            raise ValueError(
                "Cannot have more than 32 properties in a component group."
            )

    def __init__(self):
        self._properties = {}

    def enum(
        self, name: str, values: tuple[str], default: str, *, client_sync: bool = False
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "enum",
            "default": default,
            "values": values,
            "client_sync": client_sync,
        }
        return self

    def int(
        self,
        name: str,
        range: tuple[int, int],
        *,
        default: int = 0,
        client_sync: bool = False,
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "int",
            "default": default if isinstance(default, Molang) else int(default),
            "range": range,
            "client_sync": client_sync,
        }
        return self

    def float(
        self,
        name: str,
        range: tuple[float, float],
        *,
        default: float = 0,
        client_sync: bool = False,
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "float",
            "default": float(default),
            "range": [float(f) for f in range],
            "client_sync": client_sync,
        }
        return self

    def bool(self, name: str, *, default: bool = False, client_sync: bool = False):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "bool",
            "default": default,
            "client_sync": client_sync,
        }
        return self

    def __iter__(self):
        return iter(self._properties.keys())

    def __export__(self):
        return self._properties


class _EntityServerDescription(_ActorDescription):
    """Base class for all server entity descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all server entity descriptions.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._properties = _Properties()
        self._description["description"].update(
            {
                "properties": {},
            }
        )

    @property
    @deprecated(
        "The Summonable property is deprecated and will be removed in a future version. Please use the config method instead.",
    )
    def Summonable(self) -> "_EntityServerDescription":
        """Sets whether or not we can summon this entity using commands such as /summon.

        Returns
        -------
            Entity description object.

        """
        self._description["description"]["is_summonable"] = True
        return self

    @property
    @deprecated(
        "The Spawnable property is deprecated and will be removed in a future version. Please use the config method instead.",
    )
    def Spawnable(self) -> "_EntityServerDescription":
        """Sets whether or not this entity has a spawn egg in the creative ui.

        Returns
        -------
            Entity description object.

        """
        self._description["description"]["is_spawnable"] = True
        return self

    @property
    @deprecated(
        "The Experimental property is deprecated and will be removed in a future version. Please use the config method instead.",
    )
    def Experimental(self) -> "_EntityServerDescription":
        """Sets whether or not this entity is experimental. Experimental entities are only enabled when the experimental toggle is enabled.

        Returns
        -------
            Entity description object.

        """
        if CONFIG._EXPERIMENTAL:
            if CONFIG._TARGET == "addon":
                raise RuntimeError(
                    f"Experimental entities are not allowed for packages of type 'addon'. Entity [{self.identifier}]."
                )

        self._description["description"]["is_experimental"] = True
        return self

    @deprecated(
        "The RuntimeIdentifier property is deprecated and will be removed in a future version. Please use the config method instead.",
    )
    def RuntimeIdentifier(
        self, entity: "MinecraftEntityDescriptor"
    ) -> "_EntityServerDescription":
        """Sets the runtime identifier of the entity.

        Args:
            entity (MinecraftEntityDescriptor): The vanilla entity to get the runtime identifier from.
        """
        if CONFIG._TARGET != ConfigPackageTarget.ADDON:
            if type(entity) is MinecraftEntityDescriptor:
                if entity._allow_runtime:
                    self._description["description"][
                        "runtime_identifier"
                    ] = entity.identifier
                else:
                    raise RuntimeError(
                        f"Entity {entity.identifier} does not allow runtime identifier usage. Entity [{self.identifier}]."
                    )
            else:
                raise TypeError(
                    f"Expected Entity, got {type(entity).__name__}. Entity [{self.identifier}]"
                )
        else:
            raise RuntimeError(
                f"Using runtime is not allowed for packages of type '{CONFIG._TARGET}'. Entity [{self.identifier}]"
            )
        return self

    def config(
        self,
        is_summonable: bool = True,
        is_spawnable: bool = True,
        is_experimental: bool = False,
        runtime_identifier: "MinecraftEntityDescriptor" = None,
        spawn_category: str = "misc",
    ) -> "_EntityServerDescription":
        """Sets the config of the entity.

        Args:
            is_summonable (bool, optional): Whether or not we can summon this entity using commands such as /summon. Defaults to True.
            is_spawnable (bool, optional): Whether or not this entity has a spawn egg in the creative ui. Defaults to True.
            is_experimental (bool, optional): Whether or not this entity is experimental. Experimental entities are only enabled when the experimental toggle is enabled. Defaults to False.
            runtime_identifier (MinecraftEntityDescriptor, optional): The vanilla entity to get the runtime identifier from. Defaults to None.
            spawn_category (str, optional): The spawn category of the entity. Defaults to "misc".
        """
        self._description["description"]["is_summonable"] = is_summonable
        self._description["description"]["is_spawnable"] = is_spawnable
        self._description["description"]["is_experimental"] = is_experimental
        self._description["description"]["spawn_category"] = spawn_category
        if runtime_identifier is not None:
            if CONFIG._TARGET != ConfigPackageTarget.ADDON:
                if type(runtime_identifier) is MinecraftEntityDescriptor:
                    if runtime_identifier._allow_runtime:
                        self._description["description"][
                            "runtime_identifier"
                        ] = runtime_identifier.identifier
                    else:
                        raise RuntimeError(
                            f"Entity {runtime_identifier.identifier} does not allow runtime identifier usage. Entity [{self.identifier}]."
                        )
                else:
                    raise TypeError(
                        f"Expected Entity, got {type(runtime_identifier).__name__}. Entity [{self.identifier}]"
                    )
            else:
                raise RuntimeError(
                    f"Using runtime is not allowed for packages of type '{CONFIG._TARGET}'. Entity [{self.identifier}]"
                )
        return self

    @property
    def add_property(self) -> "_Properties":
        """Adds a property to the entity."""
        return self._properties

    def spawn_category(self) -> "_EntityServerDescription":
        """Sets the spawn category of the entity."""
        self._description["description"]["spawn_category"] = "none"
        return self

    def __export__(self) -> dict:
        """Exports the entity description."""
        self._description["description"]["properties"] = self._properties.__export__()
        return super().__export__()


class EntityServer(AddonObject):
    """Base class for all server entities."""

    _extension = ".behavior.json"
    _pack = Pack.BP
    _folder = "entities"
    _object_type = "Server Entity"

    def _add_despawn_function(self):
        """Adds a despawn function to the entity."""
        self.component_group("despawn").add(EntityInstantDespawn())
        self.event("despawn").add(["despawn"])

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all server entities.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._server_entity = JsonSchemes.entity_server()
        self._description = _EntityServerDescription(self.identifier, self._is_vanilla)
        self._animation_controllers = BPAnimationControllers(self.identifier)
        self._animations = BPAnimations(self.identifier)
        self._spawn_rule = SpawnRule(self.name, self._is_vanilla)
        self._components = ComponentGroup(name="components")
        self._events: dict[str, _Event] = {}
        self._component_groups: list[ComponentGroup] = []
        self._vars = []
        self._add_despawn_function()

    @property
    def description(self) -> "_EntityServerDescription":
        """Returns the entity description."""
        return self._description

    @property
    def spawn_rule(self) -> "SpawnRule":
        """Returns the spawn rule of the entity."""
        return self._spawn_rule

    def animation_controller(
        self,
        controller_name: str,
        animate: bool = False,
        condition: str | Molang = None,
        initial_state: str = "default",
    ) -> "_BP_Controller":
        """Sets the mapping of internal animation controller references to actual animations.

        Args:
            controller_name (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation controller. Defaults to None.

        """
        self._description._animation_controller(controller_name, animate, condition)
        return self._animation_controllers.add_controller(
            controller_name, initial_state
        )

    def animation(
        self,
        animation_name: str,
        loop: bool = False,
        animate: bool = False,
        condition: str | Molang = None,
    ) -> "_BPAnimation":
        """Sets the mapping of internal animation references to actual animations.

        Args:
            animation_name (str): The name of the animation.
            loop (bool, optional): Whether or not the animation should loop. Defaults to False.
            animate (bool, optional): Whether or not to animate the animation. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation. Defaults to None.

        """
        self._description._animations(self._name, animation_name, animate, condition)
        return self._animations.add_animation(animation_name, loop)

    def init_vars(self, **vars) -> "EntityServer":
        """Initializes variables for an entity."""
        for k, v in vars.items():
            Variable._set_var(k)
            self._vars.extend([f"v.{k}={v}"])

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
    ) -> "_Event":
        """Adds an event to the entity.
            - `minecraft:entity_born` triggers an event call on an entity when the entity is born via breeding.
            - `minecraft:entity_spawned` triggers an event call on an entity when the entity is spawned in the world.
            - `minecraft:entity_transformed` triggers an event call on an entity when transformed into another entity.
            - `minecraft:on_prime` triggers an event call on an entity when the entity is set to explode.

        Args:
            event_name (str): The name of the event.
        """
        if event_name in self._events:
            return self._events[event_name]

        self._events[event_name] = _Event(event_name)
        return self._events[event_name]

    @property
    def components(self) -> "ComponentGroup":
        """Returns the components of the entity."""
        return self._components

    def component_group(self, component_group_name: str) -> "ComponentGroup":
        """Returns the component group with this name, added on first use.

        Args:
            component_group_name (str): The name of the component group.

        """
        if component_group_name == "components":
            raise ValueError(
                "'components' is the root group. Use `entity.server.components` instead."
            )
        for group in self._component_groups:
            if group.name == component_group_name:
                return group
        self._component_groups.append(ComponentGroup(name=component_group_name))
        return self._component_groups[-1]

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

    def queue(self, directory: str = None) -> "EntityServer":
        """Queues the entity for export.

        Args:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        super().queue(directory=directory)

    def __export__(self) -> None:
        if len(self._vars) > 0:
            self.animation_controller("variables", True).add_state("default").on_entry(
                *self._vars
            )
        self._animations.queue(directory=self._directory)
        self._animation_controllers.queue(directory=self._directory)
        self._spawn_rule.queue(directory=self._directory)

        validate_components(self, self._components, self._component_groups)

        self._server_entity["minecraft:entity"].update(self.description.__export__())
        self._server_entity["minecraft:entity"]["components"].update(
            encoders.contents(self._components)
        )

        for event in self._events.values():
            self._server_entity["minecraft:entity"]["events"].update(event.__export__())

        self._server_entity["minecraft:entity"]["component_groups"].update(
            encoders.merged(self._component_groups)
        )

        self.content(self._server_entity)

        controllers = list(
            self._animation_controllers._animation_controllers[
                "animation_controllers"
            ].keys()
        )
        cleared_items = []
        for key, controller in self._description._description["description"][
            "animations"
        ].items():
            if controller.startswith("controller.") and controller not in controllers:
                cleared_items.append(key)

        for item in cleared_items:
            self._description._description["description"]["animations"].pop(item)

        if self._components.has(EntityRideable) or any(
            c.has(EntityRideable) for c in self._component_groups
        ):
            AnvilTranslator().add_localization_entry(
                f"action.hint.exit.{self.identifier}", "Sneak to exit"
            )
        return super().__export__()
