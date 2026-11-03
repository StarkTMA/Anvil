import os

from anvil.api.actors.animation_controllers import (
    RPAnimationControllers,
)
from anvil.api.actors.render_controller import RenderControllers
from anvil.api.core.core import SoundDefinition, SoundEvent
from anvil.api.core.enums import EntitySoundEvent, SoundCategory
from anvil.api.core.types import Vector2D
from anvil.api.logic.molang import Molang, Variable
from anvil.api.models.animations import _Animation
from anvil.api.models.geometry import Geometry
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.api.vanilla.entities import vanilla_entity_ids
from anvil.lib.blockbench import _Blockbench, _BlockBenchSource
from anvil.lib.config import CONFIG
from anvil.lib.schemas import (
    JsonSchemes,
    MinecraftDescription,
)
from anvil.lib.translator import AnvilTranslator


class _ActorDescription(MinecraftDescription):
    """Base class for all actor descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all actor descriptions.

        Args:
            name (str): The name of the actor.
            is_vanilla (bool, optional): Whether or not the actor is a vanilla actor. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._animation_controllers: RPAnimationControllers
        self._description["description"].update(
            {"animations": {}, "scripts": {"animate": []}}
        )

    def _animate_append(self, key: str | dict):
        """Appends a key to the animate list."""

        if key not in self._description["description"]["scripts"]["animate"]:
            self._description["description"]["scripts"]["animate"].append(key)

    def _animation_controller(
        self, controller_name: str, animate: bool = False, condition: str = None
    ):
        """Sets the mapping of internal animation controller references to actual animations.

        Parameters
        ----------
        controller_name : str
            The name of the animation controller.
        animate : bool, optional
            bool = False
        condition : str, optional
            str = None

        """

        if animate is True:
            if condition is None:
                self._animate_append(controller_name)
            else:
                self._animate_append({controller_name: condition})

        self._description["description"]["animations"].update(
            {
                controller_name: f"controller.animation.{CONFIG.NAMESPACE}.{self.name}.{controller_name}"
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

        self._animation_reference(
            animation_shortname,
            f"animation.{CONFIG.NAMESPACE}.{geometry_name}.{animation_shortname}",
            animate,
            condition,
        )

    def _animation_reference(
        self,
        shortname: str,
        identifier: str,
        animate: bool = False,
        condition: str = None,
    ):
        """Maps `shortname` to the animation `identifier`, and animates it if asked."""
        if animate is True:
            if condition is None:
                self._animate_append(shortname)
            else:
                self._animate_append({shortname: condition})

        self._description["description"]["animations"].update({shortname: identifier})


class _ActorClientDescription(_ActorDescription):
    _queued_animation_controllers = set()
    _type = "entity"

    def _render_append(self, key):
        if key not in self._description["description"]["render_controllers"]:
            self._description["description"]["render_controllers"].append(key)

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client actor descriptions.

        Args:
            name (str): The name of the actor.
            is_vanilla (bool, optional): Whether or not the actor is a vanilla actor. Defaults to False.
            type (str, optional): The type of the actor. Defaults to "entity".
        """
        super().__init__(name, is_vanilla)
        if self._type not in ["entity", "attachable"]:
            raise RuntimeError(
                f"Invalid type '{self._type}' for actor description. Expected 'entity' or 'attachables'. Actor [{self.identifier}]"
            )

        if is_vanilla and self.identifier not in vanilla_entity_ids():
            raise RuntimeError(
                f"Invalid vanilla entity '{self.identifier}'. Please use a valid vanilla entity from MinecraftEntityTypes. Actor [{self.identifier}]"
            )

        self._is_dummy = False
        self._animation_controllers = RPAnimationControllers(self, self._name)
        self._render_controllers = RenderControllers(self._name, self._type)
        self._texture_set: TextureSet = None

        self._description["description"].update(JsonSchemes.client_description())

    def animation_controller(
        self,
        controller_name: str,
        animate: bool = False,
        condition: str | Molang = None,
        initial_state: str = "default",
    ):
        """Sets the mapping of internal animation controller references to actual animations.

        Args:
            controller_name (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str| Molang, optional): The condition to animate the animation controller. Defaults to None.
            initial_state (str, optional): The initial state of the animation controller. Defaults to "default".
        """
        self._animation_controller(controller_name, animate, condition)
        return self._animation_controllers.add_controller(
            controller_name, initial_state
        )

    def animation(
        self,
        blockbench: str | _Animation,
        animation_name: str | None = None,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation references to actual animations.

        Args:
            blockbench (str | Animation): The Blockbench model holding the animation, or an Animation built in code (then leave `animation_name` out; its name is the shortname).
            animation_name (str, optional): The name of the animation in the Blockbench model.
            animate (bool, optional): Whether or not to animate the animation. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation. Defaults to None.

        """
        if isinstance(blockbench, _Animation):
            if animation_name is not None:
                raise TypeError(
                    "Pass either an Animation, or a Blockbench model name and an animation name, not both."
                )
            animation = blockbench
            animation.file.queue(_BlockBenchSource.ACTOR)
            self._animation_reference(
                animation.name, animation.identifier, animate, condition
            )
            return self

        if animation_name is None:
            raise TypeError(
                "animation_name is required when referencing a Blockbench model."
            )

        bb = _Blockbench(blockbench, _BlockBenchSource.ACTOR)
        bb.animations.queue_animation(animation_name)

        self._animations(blockbench, animation_name, animate, condition)

        return self

    def material(self, name: str, material: str):
        """This method manages the materials for an entity.

        Args:
            name (str): The id of the material.
            material (str): The name of the material.

        """
        self._description["description"]["materials"].update({str(name): str(material)})
        return self

    def geometry(
        self, geometry_name: str | Geometry, override_bounding_box: Vector2D = None
    ):
        """
        This method manages the geometry for an entity.

        Args:
            geometry_name (str | Geometry): The name of the Blockbench model, or a Geometry built in code (its name is the shortname).
            override_bounding_box (Vector2D, optional): The bounding box to override the default bounding box. Defaults to None.

        Returns:
            self: Returns an instance of the class.
        """
        if isinstance(geometry_name, Geometry):
            geometry = geometry_name
            if override_bounding_box:
                geometry.set_visible_bounds(*override_bounding_box)
            geometry.queue(_BlockBenchSource.ACTOR)
            self._description["description"]["geometry"].update(
                {geometry.name: geometry.geometry_identifier}
            )
            return self

        bb = _Blockbench(geometry_name, _BlockBenchSource.ACTOR)
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

        Args:
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
        blockbench: str,
        component: TextureComponents,
    ):
        """This method manages the textures for an entity.

        Args:
            blockbench (str): The name of the texture.
            texture_name (str): The name of the texture.
        """
        bb = _Blockbench(blockbench, _BlockBenchSource.ACTOR)
        bb.textures.queue_texture(component.color)

        self._description["description"]["textures"].update(
            {
                component.color: os.path.join(
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "actors",
                    blockbench,
                    component.color,
                )
            }
        )

        if component.has_aux():
            self._texture_set = TextureSet(component.color, _BlockBenchSource.ACTOR)
            self._texture_set.set_blockbench_textures(blockbench, component)
            self._texture_set.queue()
        return self

    def script(self, variable: Variable | Molang, *script: Molang | str):
        """This method manages the scripts for an entity.
        Args:
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
            f"{variable}={str(script)};".replace(";;", ";")
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

    def scale(self, scale: Molang | str = 1):
        """Sets the scale of the entity.

        Args:
            scale (str | Molang, optional): The scale of the entity. Defaults to "1".
        """
        if not (isinstance(scale, (str, Molang)) or isinstance(scale, (int, float))):
            raise TypeError("Entity scale must be one of (str, Molang, int float).")
        if scale != 1:
            self._description["description"]["scripts"]["scale"] = scale

    def should_update_bones_and_effects_offscreen(self, value: bool = False):
        """Sets whether or not the entity should update bones and effects offscreen.

        Args:
            value (bool, optional): Whether or not the entity should update bones and effects offscreen. Defaults to False.
        """
        self._description["description"]["scripts"][
            "should_update_bones_and_effects_offscreen"
        ] = str(int(value))

    def should_update_effects_offscreen(self, value: bool = False):
        """Sets whether or not the entity should update effects offscreen.

        Args:
            value (bool, optional): Whether or not the entity should update effects offscreen. Defaults to False.
        """
        self._description["description"]["scripts"][
            "should_update_effects_offscreen"
        ] = str(int(value))

    def scaleXYZ(
        self, x: Molang | str = "1", y: Molang | str = "1", z: Molang | str = "1"
    ):
        """Sets the scale of the entity.

        Args:
            x (str | Molang, optional): The x scale of the entity. Defaults to "1".
            y (str | Molang, optional): The y scale of the entity. Defaults to "1".
            z (str | Molang, optional): The z scale of the entity. Defaults to "1".
        """
        if x != "1" or y != "1" or z != "1":
            self._description["description"]["scripts"]["scalex"] = str(x)
            self._description["description"]["scripts"]["scaley"] = str(y)
            self._description["description"]["scripts"]["scalez"] = str(z)

    def hide_held_items(self, expression: Molang | str | bool = True):
        """Sets the hide_held_items script expression. When this Molang expression evaluates to a non-zero value, it hides any items held by the entity.

        Args:
            expression (str | Molang | bool, optional): The Molang expression or boolean. Defaults to True.
        """
        if isinstance(expression, bool):
            val = str(int(expression))
        else:
            val = str(expression)

        self._description["description"]["scripts"]["hide_held_items"] = val

    def render_controller(self, controller_name: str, condition: str = None):
        """This method manages the render controllers for an entity.

        Args:
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

    def particle_effect(self, particle: str, component: TextureComponents):
        """This method manages the particle effects for an entity.

        Args:
            particle (str): The name of the particle effect.

        """
        from anvil.api.world.particles import Particle

        self._description["description"]["particle_effects"].update(
            {particle: f"{CONFIG.NAMESPACE}:{particle}"}
        )
        Particle(particle, component).queue()
        return self

    def sound_effect(
        self,
        sound: str,
        category: SoundCategory = SoundCategory.Neutral,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str = None,
    ):
        """This method manages the sound effects for an entity.

        Args:
            sound_shortname (str): The shortname of the sound effect.
            sound_path (str): The path to the sound effects from the assets/sounds folder.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            subtitle (str, optional): The subtitle of the sound effect. Defaults to None.
        """
        if not isinstance(category, SoundCategory):
            raise ValueError(
                f"Invalid sound category '{category}' for sound effect '{sound}' in entity {self.identifier}. Entity [{self.identifier}]"
            )

        self._description["description"]["sound_effects"].update(
            {sound: f"{CONFIG.NAMESPACE}:{sound}"}
        )

        key = f"subtitle.generic.{sound}"

        if subtitle is not None:
            AnvilTranslator().add_localization_entry(key, subtitle)

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
            subtitle=key if subtitle else None,
        )

    def sound_event(
        self,
        sound_reference: str,
        sound_event: EntitySoundEvent,
        category: SoundCategory = SoundCategory.Neutral,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float | None = None,
        min_distance: float | None = None,
        variant_query: Molang = None,
        variant_map: str = None,
        subtitle: str = None,
    ):
        """This method manages the sound events for an entity.

        Args:
            sound_reference (str): The identifier of the sound effect.
            sound_event (EntitySoundEvent): The sound event.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.
            volume (float, optional): The volume of the sound effect. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the sound effect. Defaults to (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            variant_query (Molang, optional): The variant query of the sound effect. Defaults to None.
            variant_map (str, optional): The variant map of the sound effect. Defaults to None.
            subtitle (str, optional): The subtitle of the sound effect. Defaults to None.
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
            subtitle,
        )

    def __export__(self, directory: str = None):
        """Queues the entity for export.

        Args:
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

            for controller in self._render_controllers._controllers.values():
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
            if controller.__export__() == {}:
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

        return super().__export__()
