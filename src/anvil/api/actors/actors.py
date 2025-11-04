import os
from typing import overload

from anvil.api.actors._animations import _BPAnimations
from anvil.api.actors._component_group import _ComponentGroup, _Components, _Properties
from anvil.api.actors._events import _Event
from anvil.api.actors._render_controller import _RenderControllers
from anvil.api.actors.components import EntityInstantDespawn, EntityRideable
from anvil.api.actors.spawn_rules import SpawnRule
from anvil.api.core.core import SoundDefinition, SoundEvent
from anvil.api.core.sounds import EntitySoundEvent, SoundCategory, _SoundDescription
from anvil.api.core.textures import ItemTexturesObject
from anvil.api.logic.molang import Molang, Variable
from anvil.api.pbr.pbr import TextureSet
from anvil.api.vanilla.entities import MinecraftEntityTypes
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG, ConfigPackageTarget
from anvil.lib.enums import DamageSensor, Target
from anvil.lib.lib import MOLANG_PREFIXES
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    AddonObject,
    EntityDescriptor,
    JsonSchemes,
    MinecraftDescription,
    MinecraftEntityDescriptor,
)
from anvil.lib.translator import AnvilTranslator
from anvil.lib.types import RGB, RGBA, Vector2D

__all__ = ["Entity", "Attachable"]


class _BP_ControllerState:
    def __init__(self, state_name):
        self._state_name = state_name
        self._controller_state: dict = JsonSchemes.animation_controller_state(
            self._state_name
        )
        self._default = True

    def on_entry(self, *commands: str):
        """Events, commands or molang to preform on entry of this state.

        Args:
            *commands (str): The Events, commands or molang to preform on entry of this state.

        Returns:
            This state.
        """
        for command in commands:
            if str(command).startswith(Target.S):
                self._controller_state[self._state_name]["on_entry"].append(command)
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_entry"].append(
                    f"{command};"
                )
            else:
                self._controller_state[self._state_name]["on_entry"].append(
                    f"/{command}"
                )
        self._default = False
        return self

    def on_exit(self, *commands: str):
        """Events, commands or molang to preform on exit of this state.

        Args:
            *commands (str): The Events, commands or molang to preform on exit of this state.

        Returns:
            This state.
        """
        for command in commands:
            if str(command).startswith(Target.S.value):
                self._controller_state[self._state_name]["on_exit"].append(f"{command}")
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_exit"].append(
                    f"{command};"
                )
            else:
                self._controller_state[self._state_name]["on_exit"].append(
                    f"/{command}"
                )
        self._default = False
        return self

    def animation(self, animation: str, condition: str = None):
        """Animation short name to play during this state.

        Args:
            animation (str): The name of the animation to play.
            condition (str, optional): The condition on which this animation plays.

        Returns:
            This state.
        """
        if condition is None:
            self._controller_state[self._state_name]["animations"].append(animation)
        else:
            self._controller_state[self._state_name]["animations"].append(
                {animation: condition}
            )
        self._default = False
        return self

    def transition(self, state: str, condition: str):
        """Target state to switch to and the condition to do so.

        Parameters
        ----------
        state : str
            The name of the state to transition to.
        condition : str
            The condition that must be met for the transition to occur.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["transitions"].append(
            {state: str(condition)}
        )
        self._default = False
        return self

    @property
    def _export(self):
        return self._controller_state


class _RP_ControllerState:
    def __init__(self, actor: "_ActorClientDescription", state_name):
        self._actor = actor
        self._state_name = state_name
        self._controller_state = JsonSchemes.animation_controller_state(
            self._state_name
        )
        self._controller_state[self._state_name]["particle_effects"] = []
        self._controller_state[self._state_name]["sound_effects"] = []
        self._default = True

    @overload
    def on_entry(self, *commands: str | Molang) -> "_RP_ControllerState": ...

    @overload
    def on_entry(
        self, variable: Molang | str, value: Molang | str | int | float
    ) -> "_RP_ControllerState": ...

    def on_entry(self, *args, **kwargs) -> "_RP_ControllerState":
        """molang to preform on entry of this state.

        Parameters
        ----------
        *args : str | Molang or (variable, value)
            param args: molang commands to perform on entry of this state, or variable assignment.

        Returns
        -------
            This state.

        """
        # Handle variable assignment case: on_entry(variable, value)
        if len(args) == 2 and not kwargs:
            variable, value = args
            command = f"{variable}={value}"
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_entry"].append(
                    f"{command};"
                )
            else:
                raise RuntimeError(
                    f"Invalid variable assignment for on_entry: {command}. Only Molang commands are allowed. Resource Pack Controller State [{self._state_name}]"
                )
        # Handle commands case: on_entry(*commands)
        else:
            for command in args:
                if any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                    self._controller_state[self._state_name]["on_entry"].append(
                        f"{command};"
                    )
                else:
                    raise RuntimeError(
                        f"Invalid command for on_entry: {command}. Only Molang commands are allowed. Resource Pack Controller State [{self._state_name}]"
                    )

        self._default = False
        return self

    @overload
    def on_exit(self, *commands: str | Molang) -> "_RP_ControllerState": ...

    @overload
    def on_exit(
        self, variable: Molang | str, value: Molang | str | int | float
    ) -> "_RP_ControllerState": ...

    def on_exit(self, *args, **kwargs) -> "_RP_ControllerState":
        """molang to preform on entry of this state.

        Parameters
        ----------
        *args : str | Molang or (variable, value)
            param args: molang commands to perform on entry of this state, or variable assignment.

        Returns
        -------
            This state.

        """
        # Handle variable assignment case: on_exit(variable, value)
        if len(args) == 2 and not kwargs:
            variable, value = args
            command = f"{variable}={value}"
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_exit"].append(
                    f"{command};"
                )
            else:
                raise RuntimeError(
                    f"Invalid variable assignment for on_exit: {command}. Only Molang commands are allowed. Resource Pack Controller State [{self._state_name}]"
                )
        # Handle commands case: on_exit(*commands)
        else:
            for command in args:
                if any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                    self._controller_state[self._state_name]["on_exit"].append(
                        f"{command};"
                    )
                else:
                    raise RuntimeError(
                        f"Invalid command for on_exit: {command}. Only Molang commands are allowed. Resource Pack Controller State [{self._state_name}]"
                    )

        self._default = False
        return self

    def animation(self, animation: str, condition: str = None):
        """Animation short name to play during this state.

        Parameters
        ----------
        animation : str
            The name of the animation to play.
        condition : str , optional
            The condition on which this animation plays.

        Returns
        -------
            This state.

        """
        if condition is None:
            self._controller_state[self._state_name]["animations"].append(animation)
        else:
            self._controller_state[self._state_name]["animations"].append(
                {animation: condition}
            )
        self._default = False
        return self

    def transition(self, state: str, condition: str):
        """Target state to switch to and the condition to do so.

        Parameters
        ----------
        state : str
            The name of the state to transition to.
        condition : str
            The condition that must be met for the transition to occur.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["transitions"].append(
            {state: str(condition)}
        )
        self._default = False
        return self

    def particle(
        self,
        effect: str,
        locator: str = "root",
        pre_anim_script: str = None,
        bind_to_actor: bool = True,
    ):
        """The effect to be emitted during this state.

        Parameters
        ----------
        effect : str
            The shortname of the particle effect to be played, defined in the Client Entity.
        locator : str
            The name of a locator on the actor where the effect should be located.
        pre_anim_script : str , optional
            A molang script that will be run when the particle emitter is initialized.
        bind_to_actor : bool , optional
            Set to false to have the effect spawned in the world without being bound to an actor.

        Returns
        -------
            This state.

        """
        if not self._actor._description["description"]["particle_effects"].get(effect):
            raise RuntimeError(
                f"Particle effect '{effect}' is not defined in the Client Entity for Actor '{self._actor.name}'."
            )
        particle = {"effect": effect, "locator": locator}
        if pre_anim_script is not None:
            particle.update(
                {"pre_effect_script": f"{pre_anim_script};".replace(";;", ";")}
            )
        if bind_to_actor is False:
            particle.update({"bind_to_actor": False})
        self._controller_state[self._state_name]["particle_effects"].append(particle)
        self._default = False
        return self

    def sound_effect(
        self,
        effect: str,
        locator: str = "root",
    ):
        """Collection of sounds to trigger on entry to this animation state.

        Parameters
        ----------
        effect : str
            The shortname of the sound effect to be played, defined in the Client Entity.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["sound_effects"].append(
            {"effect": effect, "locator": locator}
        )
        self._default = False
        return self

    def blend_transition(self, blend_value: float):
        """Sets the amount of time to fade out if the animation is interrupted.

        Parameters
        ----------
        blend_value : float
            Blend out time.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["blend_transition"] = blend_value
        self._default = False
        return self

    @property
    def blend_via_shortest_path(self):
        """When blending a transition to another state, animate each euler axis through the shortest rotation, instead of by value.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["blend_via_shortest_path"] = True
        self._default = False
        return self

    @property
    def _export(self):
        return self._controller_state


class _BP_Controller:
    def __init__(self, identifier, controller_shortname):
        self._identifier = identifier
        self._controller_shortname = controller_shortname
        self._controllers = JsonSchemes.animation_controller(
            self._identifier, self._controller_shortname
        )
        self._controller_states: list[_BP_ControllerState] = []
        self._controller_namespace = f"controller.animation.{self._identifier.replace(':', '.')}.{self._controller_shortname}"
        self._states_names = []
        self._side = "Server"

    def add_state(self, state_name: str):
        self._states_names.append(state_name)
        """Adds a new state to the animation controller.
        
        Parameters
        ----------
        state_name : str
            The name of the state to add.
        
        Returns
        -------
            Animation controller state.
        
        """
        self._controller_state = _BP_ControllerState(state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state

    @property
    def _export(self):
        collected_states = []
        for state in self._controller_states:
            if not state._default:
                self._controllers[self._controller_namespace]["states"].update(
                    state._export
                )
                for tr in state._export.values():
                    if "transitions" in tr:
                        for st in tr["transitions"]:
                            collected_states.extend(st.keys())

        for state in set(collected_states):
            if state not in self._states_names:
                raise RuntimeError(
                    f"State '{state}' is referenced in transitions but not defined in the. behavior Pack Animation Controller[{self._identifier}]."
                )

        if len(self._controllers[self._controller_namespace]["states"].items()) > 0:
            return self._controllers
        return {}


class _RP_Controller(_BP_Controller):
    def __init__(self, actor: "_ActorClientDescription", name, controller_shortname):
        super().__init__(name, controller_shortname)
        self._actor = actor
        self._side = "Client"
        self._controller_states: list[_RP_ControllerState] = []

    def add_state(self, state_name: str):
        self._states_names.append(state_name)
        self._controller_state = _RP_ControllerState(self._actor, state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state


class _BP_AnimationControllers(AddonObject):
    _extension = ".bp_ac.json"
    _path = os.path.join(
        CONFIG.BP_PATH,
        "animation_controllers",
    )
    _object_type = "Behavior Pack Animation Controller"

    def __init__(self, identifier) -> None:
        super().__init__(identifier)
        self._animation_controllers = JsonSchemes.animation_controllers()
        self._controllers_list: list[_BP_Controller] = []

    def add_controller(self, controller_shortname: str) -> _BP_Controller:
        """Adds a new animation controller to the current actor with `default` as the `initial_state`.

        Parameters
        ----------
        controller_shortname : str
            The shortname of the controller you want to add.

        Returns
        -------
            Animation controller.

        """
        ctrl = _BP_Controller(self.identifier, controller_shortname)
        self._controllers_list.append(ctrl)
        return ctrl

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            for controller in self._controllers_list:
                self._animation_controllers["animation_controllers"].update(
                    controller._export
                )
            self.content(self._animation_controllers)
            return super().queue(directory=directory)


class _RP_AnimationControllers(AddonObject):
    _extension = ".rp_ac.json"
    _path = os.path.join(CONFIG.RP_PATH, "animation_controllers")
    _object_type = "Resource Pack Animation Controller"

    def __init__(self, actor: "_ActorClientDescription", name) -> None:
        super().__init__(name)
        self._actor = actor
        self._animation_controllers = JsonSchemes.animation_controllers()
        self._controllers_list: list[_RP_Controller] = []

    def add_controller(self, controller_shortname: str) -> _RP_Controller:
        """Adds a new animation controller to the current actor with `default` as the `initial_state`.

        Parameters
        ----------
        controller_shortname : str
            The shortname of the controller you want to add.

        Returns
        -------
            Animation controller.

        """
        self._animation_controller = _RP_Controller(
            self._actor, self.identifier, controller_shortname
        )
        self._controllers_list.append(self._animation_controller)
        return self._animation_controller

    def _is_populated(self):
        return len(self._controllers_list) > 0 and any(
            [len(t._controller_states) > 0 for t in [c for c in self._controllers_list]]
        )

    def queue(self, directory: str = None):
        if self._is_populated():
            for controller in self._controllers_list:
                self._animation_controllers["animation_controllers"].update(
                    controller._export
                )
            self.content(self._animation_controllers)
            return super().queue(directory=directory)


class _ActorReuseAssets:
    def __init__(self, client: "_ActorClientDescription") -> None:
        self.client = client

    def animation(
        self,
        shortname: str,
        animation_name: str,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        if animate is True:
            if condition is None:
                self.client._animate_append(shortname)
            else:
                self.client._animate_append({shortname: condition})

        self.client._description["description"]["animations"].update(
            {shortname: animation_name}
        )

    def animation_controller(
        self,
        shortname: str,
        animation_controller_name: str,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        if animate is True:
            if condition is None:
                self.client._animate_append(shortname)
            else:
                self.client._animate_append({shortname: condition})

        self.client._description["description"]["animations"].update(
            {shortname: animation_controller_name}
        )

    def texture(self, shortname: str, texture_name: str):
        self.client._description["description"]["textures"].update(
            {shortname: texture_name}
        )

    def geometry(self, shortname: str, geometry_name: str):
        self.client._description["description"]["geometry"].update(
            {shortname: geometry_name}
        )

    def particle_effect(self, shortname: str, particle_name: str):
        self.client["description"]["particle_effects"].update(
            {shortname: particle_name}
        )

    def sound_effect(self, shortname: str, sound_name: str):
        self.client._description["description"]["sound_effects"].update(
            {shortname: sound_name}
        )

    def spawn_egg(self, item_sprite: str, texture_index: int = 0):
        self.client._description["description"]["spawn_egg"] = {
            "texture": item_sprite,
            "texture_index": texture_index,
        }

    def render_controller(self, controller_name: str, condition: str = None):
        if condition is None:
            self.client._description["description"]["render_controllers"].append(
                controller_name
            )
        else:
            self.client._description["description"]["render_controllers"].append(
                {controller_name: condition}
            )


class _ActorDescription(MinecraftDescription):
    """Base class for all actor descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all actor descriptions.

        Parameters:
            name (str): The name of the actor.
            is_vanilla (bool, optional): Whether or not the actor is a vanilla actor. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._animation_controllers: _RP_AnimationControllers
        self._description["description"].update(
            {"animations": {}, "scripts": {"animate": []}}
        )

    def _animate_append(self, key: str | dict):
        """Appends a key to the animate list."""

        if key not in self._description["description"]["scripts"]["animate"]:
            self._description["description"]["scripts"]["animate"].append(key)

    def _animation_controller(
        self, controller_shortname: str, animate: bool = False, condition: str = None
    ):
        """Sets the mapping of internal animation controller references to actual animations.

        Parameters
        ----------
        controller_shortname : str
            The name of the animation controller.
        animate : bool, optional
            bool = False
        condition : str, optional
            str = None

        """

        if animate is True:
            if condition is None:
                self._animate_append(controller_shortname)
            else:
                self._animate_append({controller_shortname: condition})

        self._description["description"]["animations"].update(
            {
                controller_shortname: f"controller.animation.{CONFIG.NAMESPACE}.{self.name}.{controller_shortname}"
            }
        )

    def _animations(
        self,
        geometry_name: str,
        animation_shortname: str,
        animate: bool = False,
        condition: str = None,
    ):
        """Sets the mapping of internal animation references to actual animations.

        Parameters
        ----------
        animation_shortname : str
            The name of the animation.
        animate : bool, optional
            bool = False
        condition : str, optional
            str = None

        """

        if animate is True:
            if condition is None:
                self._animate_append(animation_shortname)
            else:
                self._animate_append({animation_shortname: condition})

        self._description["description"]["animations"].update(
            {
                animation_shortname: f"animation.{CONFIG.NAMESPACE}.{geometry_name}.{animation_shortname}"
            }
        )


class _ActorClientDescription(_ActorDescription):
    _queued_animation_controllers = set()
    _type = "entity"

    def _render_append(self, key):
        if key not in self._description["description"]["render_controllers"]:
            self._description["description"]["render_controllers"].append(key)

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client actor descriptions.

        Parameters:
            name (str): The name of the actor.
            is_vanilla (bool, optional): Whether or not the actor is a vanilla actor. Defaults to False.
            type (str, optional): The type of the actor. Defaults to "entity".
        """
        super().__init__(name, is_vanilla)
        if self._type not in ["entity", "attachables"]:
            raise RuntimeError(
                f"Invalid type '{self._type}' for actor description. Expected 'entity' or 'attachables'. Actor [{self.identifier}]"
            )

        vanilla_entity_ids = [
            getattr(MinecraftEntityTypes, method)().identifier
            for method in dir(MinecraftEntityTypes)
            if callable(getattr(MinecraftEntityTypes, method))
            and not method.startswith("_")
        ]

        if is_vanilla and self.identifier not in vanilla_entity_ids:
            raise RuntimeError(
                f"Invalid vanilla entity '{self.identifier}'. Please use a valid vanilla entity from MinecraftEntityTypes. Actor [{self.identifier}]"
            )

        self._is_dummy = False
        self._animation_controllers = _RP_AnimationControllers(self, self._name)
        self._render_controllers = _RenderControllers(self._name)
        self._texture_set: TextureSet = None

        self._description["description"].update(JsonSchemes.client_description())

    def animation_controller(
        self,
        controller_shortname: str,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation controller references to actual animations.

        Parameters:
            controller_shortname (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str| Molang, optional): The condition to animate the animation controller. Defaults to None.

        """
        self._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(
        self,
        blockbench_name: str,
        animation_name: str,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation references to actual animations.

        Parameters:
            animation_name (str): The name of the animation.
            animate (bool, optional): Whether or not to animate the animation. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation. Defaults to None.

        """
        bb = _Blockbench(blockbench_name, "actors")
        bb.animations.queue_animation(animation_name)

        self._animations(blockbench_name, animation_name, animate, condition)

        return self

    def material(self, material_id: str, material_name: str):
        """This method manages the materials for an entity.

        Parameters:
            material_id (str): The id of the material.
            material_name (str): The name of the material.

        """
        self._description["description"]["materials"].update(
            {str(material_id): str(material_name)}
        )
        return self

    def geometry(self, geometry_name: str, override_bounding_box: Vector2D = None):
        """
        This method manages the geometry for an entity.

        Parameters:
            geometry_name (str): The name of the geometry.
            override_bounding_box (Vector2D, optional): The bounding box to override the default bounding box. Defaults to None.

        Returns:
            self: Returns an instance of the class.
        """

        bb = _Blockbench(geometry_name, "actors")
        if override_bounding_box:
            bb.override_bounding_box(override_bounding_box)
        bb.model.queue_model()

        self._description["description"]["geometry"].update(
            {geometry_name: f"geometry.{CONFIG.NAMESPACE}.{geometry_name}"}
        )

        return self

    def dummy(self):
        """This method manages the dummy for an entity."""
        self._is_dummy = True
        return self

    def queryable_geometry(self, geometry_shortname: str):
        """This method manages the queryable geometry for an entity.

        Parameters:
            geometry_shortname (str): The shortname of the geometry.

        """
        if not geometry_shortname in self._description["description"]["geometry"]:
            raise RuntimeError(
                f"Queryable geometry '{geometry_shortname}' not found in entity {self.identifier}. Entity [{self.identifier}]"
            )
        self._description["description"]["queryable_geometry"] = geometry_shortname
        return self

    def texture(
        self,
        blockbench_name: str,
        color: str,
        normal: str | RGB | RGBA = None,
        height: str | RGB | RGBA = None,
        mer: str | RGB | RGBA = None,
        mers: str | RGB | RGBA = None,
    ):
        """This method manages the textures for an entity.

        Parameters:
            blockbench_name (str): The name of the texture.
            texture_name (str): The name of the texture.
        """
        bb = _Blockbench(blockbench_name, "actors")
        bb.textures.queue_texture(color)

        self._description["description"]["textures"].update(
            {
                color: os.path.join(
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "actors",
                    blockbench_name,
                    color,
                )
            }
        )

        if any(
            [
                normal,
                height,
                mer,
                mers,
            ]
        ):
            self._texture_set = TextureSet(color, "actors")
            self._texture_set.set_textures(
                blockbench_name,
                color,
                normal,
                height,
                mer,
                mers,
            )
            self._texture_set.queue()
        return self

    def script(self, variable: Variable | str, *script: Molang | str):
        """This method manages the scripts for an entity.
        Parameters:
            variable (Variable | str): The variable to set the script to.
            *script (Molang | str): The script to set the variable to.
        """
        chained_scripts = "; ".join(map(str, script))

        self._description["description"]["scripts"]["pre_animation"].append(
            f"{variable}={chained_scripts};".replace(";;", ";")
        )
        return self

    def parent_setup(self, variable: Variable | str, script: Molang | str):
        """This method manages the scripts for an entity."""
        self._description["description"]["scripts"]["parent_setup"].append(
            f"{variable}={script};".replace(";;", ";")
        )
        return self

    def init_vars(self, **vars):
        """Initializes variables for an entity.

        Examples:
            >>> Entity("example").init_vars(x=0, y=5, z=8)
        """
        for k, v in vars.items():
            Variable._set_var(k)
            self._description["description"]["scripts"]["initialize"].append(
                f"v.{k}={v};"
            )
        return self

    def scale(self, scale: Molang | str = "1"):
        """Sets the scale of the entity.

        Parameters:
            scale (str | Molang, optional): The scale of the entity. Defaults to "1".
        """
        if not scale == "1":
            self._description["description"]["scripts"].update({"scale": str(scale)})

    def should_update_bones_and_effects_offscreen(self, bool: bool = False):
        """Sets whether or not the entity should update bones and effects offscreen.

        Parameters:
            bool (bool, optional): Whether or not the entity should update bones and effects offscreen. Defaults to False.
        """
        self._description["description"]["scripts"][
            "should_update_bones_and_effects_offscreen"
        ] = str(int(bool))

    def should_update_effects_offscreen(self, bool: bool = False):
        """Sets whether or not the entity should update effects offscreen.

        Parameters:
            bool (bool, optional): Whether or not the entity should update effects offscreen. Defaults to False.
        """
        self._description["description"]["scripts"][
            "should_update_effects_offscreen"
        ] = str(int(bool))

    def scaleXYZ(
        self, x: Molang | str = "1", y: Molang | str = "1", z: Molang | str = "1"
    ):
        """Sets the scale of the entity.

        Parameters:
            x (str | Molang, optional): The x scale of the entity. Defaults to "1".
            y (str | Molang, optional): The y scale of the entity. Defaults to "1".
            z (str | Molang, optional): The z scale of the entity. Defaults to "1".
        """
        if not x == "1" or not y == "1" or not z == "1":
            self._description["description"]["scripts"]["scalex"] = str(x)
            self._description["description"]["scripts"]["scaley"] = str(y)
            self._description["description"]["scripts"]["scalez"] = str(z)

    def render_controller(self, controller_name: str, condition: str = None):
        """This method manages the render controllers for an entity.

        Parameters:
            controller_name (str): The name of the render controller.
            condition (str, optional): The condition to render the render controller. Defaults to None.

        """
        if condition is None:
            self._render_append(
                f"controller.render.{CONFIG.NAMESPACE}.{self.name}.{controller_name}"
            )
        else:
            self._render_append(
                {
                    f"controller.render.{CONFIG.NAMESPACE}.{self.name}.{controller_name}": condition
                }
            )

        return self._render_controllers.add_controller(controller_name)

    def particle_effect(self, particle_name: str, use_vanilla_texture: bool = False):
        """This method manages the particle effects for an entity.

        Parameters:
            particle_name (str): The name of the particle effect.

        """
        from anvil.api.world.particles import Particle

        self._particle_name = particle_name
        self._description["description"]["particle_effects"].update(
            {self._particle_name: f"{CONFIG.NAMESPACE}:{self._particle_name}"}
        )
        Particle(self._particle_name, use_vanilla_texture).queue()
        return self

    def sound_effect(
        self,
        sound_identifier: str,
        category: SoundCategory = SoundCategory.Neutral,
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        """This method manages the sound effects for an entity.

        Parameters:
            sound_shortname (str): The shortname of the sound effect.
            sound_path (str): The path to the sound effects from the assets/sounds folder.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.

        """
        self._description["description"]["sound_effects"].update(
            {sound_identifier: f"{CONFIG.NAMESPACE}:{sound_identifier}"}
        )

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound_identifier,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
        )

    def sound_event(
        self,
        sound_reference: str,
        sound_event: EntitySoundEvent,
        category: SoundCategory = SoundCategory.Neutral,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: int = 0,
        min_distance: int = 9999,
        variant_query: Molang = None,
        variant_map: str = None,
    ):
        """This method manages the sound events for an entity.

        Parameters:
            sound_reference (str): The identifier of the sound effect.
            sound_event (EntitySoundEvent): The sound event.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.
            volume (float, optional): The volume of the sound effect. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the sound effect. Defaults to (0.8, 1.2).
            max_distance (int, optional): The maximum distance of the sound effect. Defaults to 0.
            min_distance (int, optional): The minimum distance of the sound effect. Defaults to 9999.
            variant_query (Molang, optional): The variant query of the sound effect. Defaults to None.
            variant_map (str, optional): The variant map of the sound effect. Defaults to None.
        """
        sound_event_obj = SoundEvent()
        return sound_event_obj.add_entity_event(
            self.identifier,
            sound_reference,
            sound_event,
            category,
            volume,
            pitch,
            max_distance,
            min_distance,
            variant_query,
            variant_map,
        )

    def _export(self, directory: str = None):
        """Queues the entity for export.

        Parameters:
            directory (str, optional): The directory to export the entity to. Defaults to None.

        Raises:
            RuntimeError: If the entity does not have a geometry, texture, or render controller.
            Exception: If a geometry is reused but the entity it is reused from has not been queued yet.

        """
        if not self._is_dummy:
            if len(self._description["description"]["geometry"]) == 0:
                raise RuntimeError(
                    f"Entity {self.identifier} missing at least one geometry. Entity [{self.identifier}]"
                )

            if len(self._description["description"]["textures"]) == 0:
                raise RuntimeError(
                    f"Entity {self.identifier} missing at least one texture. Entity [{self.identifier}]"
                )

            if len(self._description["description"]["render_controllers"]) == 0:
                raise RuntimeError(
                    f"Entity {self.identifier} missing at least one render controller. Entity [{self.identifier}]"
                )

            for controller in self._render_controllers._controllers:
                controller._validate(
                    self._description["description"]["textures"].keys(),
                    self._description["description"]["geometry"].keys(),
                    self._description["description"]["materials"].keys(),
                )

            self._render_controllers.queue(directory)
            self._animation_controllers.queue(directory)

        if self._texture_set:
            self._texture_set.queue()

        if self._description["description"]["scripts"]["parent_setup"] != []:
            self._description["description"]["scripts"]["parent_setup"] = ";".join(
                self._description["description"]["scripts"]["parent_setup"]
            )

        for controller in self._animation_controllers._controllers_list:
            if controller._export == {}:
                self._description["description"]["animations"].pop(
                    controller._controller_shortname
                )
                anims: list[str | dict] = self._description["description"]["scripts"][
                    "animate"
                ]

                if controller._controller_shortname in anims:
                    anims.remove(controller._controller_shortname)
                else:
                    d = next(
                        d
                        for d in anims
                        if isinstance(d, dict) and controller._controller_shortname in d
                    )
                    anims.remove(d)

        return super()._export()


class _EntityClientDescription(_ActorClientDescription):
    """Base class for all client entity descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entity descriptions.

        Parameters:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        self._spawn_egg_texture = None
        super().__init__(name, is_vanilla)

    @property
    def EnableAttachables(self):
        """This determines if the entity should render attachables such as armor."""
        self._description["description"]["enable_attachables"] = True
        return self

    @property
    def HeldItemIgnoresLighting(self):
        """This determines if the held item should ignore lighting."""
        self._description["description"]["held_item_ignores_lighting"] = True
        return self

    @property
    def HideArmor(self):
        """This determines if the armor should be hidden."""
        self._description["description"]["hide_armor"] = True
        return self

    def spawn_egg(self, item_sprite: str, texture_index: int = 0):
        """This method adds a spawn egg texture to the entity.

        Parameters:
            item_sprite (str): The name of the item sprite.
        """
        ItemTexturesObject().add_item(item_sprite, "spawn_eggs", [item_sprite])
        self._description["description"]["spawn_egg"] = {
            "texture": f"{CONFIG.NAMESPACE}:{item_sprite}",
            "texture_index": texture_index if texture_index == 0 else {},
        }

    def spawn_egg_color(self, base_color: str, overlay_color: str):
        """This method adds a spawn egg color to the entity.

        Parameters:
            base_color (str): The base color of the spawn egg.
            overlay_color (str): The overlay color of the spawn egg.
        """
        self._description["description"]["spawn_egg"] = {
            "base_color": base_color,
            "overlay_color": overlay_color,
        }

    def _export(self, directory: str):
        """Queues the entity for export.

        Parameters:
            directory (str): The directory to export the entity to.

        """
        super()._export(directory)
        if "spawn_egg" not in self._description["description"] and not self._is_vanilla:
            self._description["description"]["spawn_egg"] = {
                "base_color": "#FFFFFF",
                "overlay_color": "#000000",
            }

        return self._description


class _AttachableClientDescription(_ActorClientDescription):
    """Base class for all client attachable descriptions."""

    _type = "attachables"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client attachable descriptions.

        Parameters:
            name (str): The name of the attachable.
            is_vanilla (bool, optional): Whether or not the attachable is a vanilla attachable. Defaults to False.
        """
        super().__init__(name, is_vanilla)

    @property
    def reuse_assets(self):
        """Whether or not the actor should reuse assets from another actor."""
        return _ActorReuseAssets(self._description)


class _EntityServerDescription(_ActorDescription):
    """Base class for all server entity descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all server entity descriptions.

        Parameters:
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
    def Summonable(self):
        """Sets whether or not we can summon this entity using commands such as /summon.

        Returns
        -------
            Entity description object.

        """
        self._description["description"]["is_summonable"] = True
        return self

    @property
    def Spawnable(self):
        """Sets whether or not this entity has a spawn egg in the creative ui.

        Returns
        -------
            Entity description object.

        """
        self._description["description"]["is_spawnable"] = True
        return self

    @property
    def Experimental(self):
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

    def RuntimeIdentifier(self, entity: "MinecraftEntityDescriptor"):
        """Sets the runtime identifier of the entity.

        Parameters:
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

    @property
    def add_property(self):
        """Adds a property to the entity."""
        return self._properties

    def spawn_category(self):
        """Sets the spawn category of the entity."""
        self._description["description"]["spawn_category"] = "none"

    @property
    def _export(self):
        """Exports the entity description."""
        self._description["description"]["properties"] = self._properties._export
        return super()._export()


class _EntityServer(AddonObject):
    """Base class for all server entities."""

    _extension = ".behavior.json"
    _path = os.path.join(CONFIG.BP_PATH, "entities")
    _object_type = "Server Entity"

    def _add_despawn_function(self):
        """Adds a despawn function to the entity."""
        self.component_group("despawn").add(EntityInstantDespawn())
        self.event("despawn").add("despawn")

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all server entities.

        Parameters:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._server_entity = JsonSchemes.entity_server()
        self._description = _EntityServerDescription(self.identifier, self._is_vanilla)
        self._animation_controllers = _BP_AnimationControllers(self.identifier)
        self._animations = _BPAnimations(self.identifier)
        self._spawn_rule = SpawnRule(self.identifier, self._is_vanilla)
        self._components = _Components()
        self._events: list[_Event] = []
        self._component_groups: list[_ComponentGroup] = []
        self._vars = []
        self._add_despawn_function()

    @property
    def description(self):
        """Returns the entity description."""
        return self._description

    @property
    def spawn_rule(self):
        """Returns the spawn rule of the entity."""
        return self._spawn_rule

    def animation_controller(
        self,
        controller_shortname: str,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation controller references to actual animations.

        Parameters:
            controller_shortname (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation controller. Defaults to None.

        """
        self._description._animation_controller(
            controller_shortname, animate, condition
        )
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(
        self,
        animation_name: str,
        loop: bool = False,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation references to actual animations.

        Parameters:
            animation_name (str): The name of the animation.
            loop (bool, optional): Whether or not the animation should loop. Defaults to False.
            animate (bool, optional): Whether or not to animate the animation. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation. Defaults to None.

        """
        self._description._animations(self._name, animation_name, animate, condition)
        return self._animations.add_animation(animation_name, loop)

    def init_vars(self, **vars):
        """Initializes variables for an entity."""
        for k, v in vars.items():
            Variable._set_var(k)
            self._vars.extend([f"v.{k}={v}"])

        return self

    def event(self, event_name: str):
        """Adds an event to the entity.

        Parameters:
            event_name (str): The name of the event.
        """
        self._events.append(_Event(event_name))
        return self._events[-1]

    @property
    def components(self):
        """Returns the components of the entity."""
        return self._components

    def component_group(self, component_group_name: str):
        """Adds a component group to the entity.

        Parameters:
            component_group_name (str): The name of the component group.

        """
        self._component_groups.append(_ComponentGroup(component_group_name))
        return self._component_groups[-1]

    def add_basic_components(self):
        """Adds basic server components to the entity.

        This includes:
            - `EntityBreathable`
            - `EntityCollisionBox`
            - `EntityDamageSensor`
            - `EntityHealth`
            - `EntityJumpStatic`
            - `EntityKnockbackResistance`
            - `EntityMovement`
            - `EntityMovementType`
            - `EntityNavigationType`
            - `EntityPhysics`
            - `EntityPushable`
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
            EntityMovementType,
            EntityNavigationType,
            EntityPhysics,
            EntityPushable,
            EntityPushThrough,
        )
        from anvil.api.logic.commands import DamageCause

        self.components.add(
            EntityJumpStatic(0),
            EntityMovementType.Basic(),
            EntityNavigationType.Walk(),
            EntityMovement(0),
            EntityPhysics(True, True),
            EntityKnockbackResistance(10000),
            EntityHealth(6),
            EntityCollisionBox(1, 1),
            EntityBreathable(),
            EntityDamageSensor().add_trigger(DamageCause.All, DamageSensor.No),
            EntityPushable(False, False),
            EntityPushThrough(1),
        )

    def queue(self, directory: str = None):
        """Queues the entity for export.

        Parameters:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        super().queue(directory=directory)

    def _export(self):
        if len(self._vars) > 0:
            self.animation_controller("variables", True).add_state("default").on_entry(
                *self._vars
            )
        self._animations.queue(directory=self._directory)
        self._animation_controllers.queue(directory=self._directory)
        self._spawn_rule.queue(directory=self._directory)

        self._server_entity["minecraft:entity"].update(self.description._export)
        self._server_entity["minecraft:entity"]["components"].update(
            self._components._export()["components"]
        )

        for event in self._events:
            self._server_entity["minecraft:entity"]["events"].update(event._export)
        for component_group in self._component_groups:
            self._server_entity["minecraft:entity"]["component_groups"].update(
                component_group._export()
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

        if self._components._has(EntityRideable) or any(
            c._has(EntityRideable) for c in self._component_groups
        ):
            AnvilTranslator().add_localization_entry(
                f"action.hint.exit.{self.identifier}", "Sneak to exit"
            )
        return super()._export()


class _EntityClient(AddonObject):
    """Base class for all client entities."""

    _extension = ".entity.json"
    _path = os.path.join(CONFIG.RP_PATH, "entity")
    _object_type = "Client Entity"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entities.

        Parameters:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._client_entity = JsonSchemes.entity_client()
        self._description = _EntityClientDescription(self.identifier, self._is_vanilla)

    @property
    def reuse_assets(self):
        """Whether or not the actor should reuse assets from another actor."""
        return _ActorReuseAssets(self._description)

    @property
    def description(self):
        """Returns the entity description."""
        return self._description

    def queue(self, directory: str = None):
        """Queues the entity for export.

        Parameters:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        self._client_entity["minecraft:client_entity"].update(
            self._description._export(directory)
        )

        self.content(self._client_entity)
        super().queue(directory=directory)


class Entity(EntityDescriptor):
    def __init__(self, name, is_vanilla=False, allow_runtime=True):
        super().__init__(name, is_vanilla, allow_runtime)

        self.server = _EntityServer(name, is_vanilla)
        self.client = _EntityClient(name, is_vanilla)

    def queue(
        self,
        directory: str = None,
        display_name: str = None,
        spawn_egg_name: str = None,
    ):
        display_name = self._display_name if display_name is None else display_name
        spawn_egg_name = (
            f"Spawn {display_name}" if spawn_egg_name is None else spawn_egg_name
        )
        if self._is_vanilla:
            directory = "vanilla"

        AnvilTranslator().add_localization_entry(
            f"entity.{self.identifier}.name", display_name
        )
        AnvilTranslator().add_localization_entry(
            f"entity.{self.identifier}<>.name", display_name
        )
        AnvilTranslator().add_localization_entry(
            f"item.spawn_egg.entity.{self.identifier}.name",
            spawn_egg_name,
        )
        self.client.queue(directory)
        self.server.queue(directory)

        CONFIG.Report.add_report(
            ReportType.ENTITY,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
            col2=[event._event_name for event in self.server._events],
        )


class Attachable(AddonObject):
    _extension = ".attachable.json"
    _path = os.path.join(CONFIG.RP_PATH, "attachables")
    _object_type = "Attachable"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes the attachable.

        Parameters:
            name (str): The name of the attachable.
        """
        super().__init__(name, is_vanilla)

        self._attachable = JsonSchemes.attachable()
        self._description = _AttachableClientDescription(self.identifier, False)

    @property
    def description(self):
        """Returns the description of the attachable."""
        return self._description

    def queue(self):
        """Queues the attachable."""

        self._attachable["minecraft:attachable"].update(self._description._export())
        self.content(self._attachable)

        CONFIG.Report.add_report(
            ReportType.ATTACHABLE,
            vanilla=self._is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
        )
        super().queue()

    def __str__(self):
        """Returns the identifier of the attachable."""
        return self.identifier
