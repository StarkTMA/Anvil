import os
from typing import TYPE_CHECKING, overload

from anvil.api.core.enums import Target
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
)

if TYPE_CHECKING:
    from .actors import _ActorClientDescription

__all__ = ["BPAnimationControllers", "RPAnimationControllers"]


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
            elif any(str(command).startswith(v) for v in Molang.prefixes):
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
            elif any(str(command).startswith(v) for v in Molang.prefixes):
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

    def __export__(self):
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
            if any(command.startswith(v) for v in Molang.prefixes):
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
                if any(str(command).startswith(v) for v in Molang.prefixes):
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
            if any(command.startswith(v) for v in Molang.prefixes):
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
                if any(str(command).startswith(v) for v in Molang.prefixes):
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

    def __export__(self):
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

    def __export__(self):
        collected_states = []
        for state in self._controller_states:
            if not state._default:
                self._controllers[self._controller_namespace]["states"].update(
                    state.__export__()
                )
                for tr in state.__export__().values():
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


class BPAnimationControllers(AddonObject):
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
                    controller.__export__()
                )
            self.content(self._animation_controllers)
            return super().queue(directory=directory)


class RPAnimationControllers(AddonObject):
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
                    controller.__export__()
                )
            self.content(self._animation_controllers)
            return super().queue(directory=directory)
