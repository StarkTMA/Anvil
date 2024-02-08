import json
import os
from enum import StrEnum

import requests
from halo import Halo
from PIL import Image

from anvil import ANVIL, CONFIG
from anvil.api.blockbench import Animation, Geometry
from anvil.api.components import Filter, InstantDespawn, Rideable, _component
from anvil.api.enums import Difficulty, Population, Target, Vibrations
from anvil.api.molang import Query, Variable
from anvil.api.types import Identifier, Molang, event
from anvil.api.vanilla import ENTITY_LIST, ITEMS_LIST, Entities
from anvil.lib.lib import MOLANG_PREFIXES, CopyFiles, File, FileExists
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription
from anvil.lib.sounds import EntitySoundEvent, SoundCategory, SoundDescription

__all__ = ["Entity", "Attachable"]


class _ActorDescription(MinecraftDescription):
    """Base class for all actor descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all actor descriptions.

        Args:
            name (str): The name of the actor.
            is_vanilla (bool, optional): Whether or not the actor is a vanilla actor. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._animation_controllers_list = []
        self._animations_list = []
        self._description["description"].update({"animations": {}, "scripts": {"animate": []}})

    def _animate_append(self, key: str | dict):
        """Appends a key to the animate list."""

        if key not in self._description["description"]["scripts"]["animate"]:
            self._description["description"]["scripts"]["animate"].append(key)

    def _animation_controller(self, controller_shortname: str, animate: bool = False, condition: str = None):
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
            {controller_shortname: f"controller.animation.{CONFIG.NAMESPACE}.{self._name}.{controller_shortname}"}
        )

    def _animations(self, geometry_name: str, animation_shortname: str, animate: bool = False, condition: str = None):
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
    _queued_models = set()
    _queued_textures = set()
    _queued_animations = set()
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
        if self._type not in ["entity", "attachables"]:
            CONFIG.Logger.client_type_unsupported(self._type, self.identifier)
        self._is_vanilla = is_vanilla
        self._animation_controllers = _RP_AnimationControllers(self._name, self._is_vanilla)
        self._render_controllers = _RenderControllers(self._name, self._is_vanilla)
        self._description["description"].update(JsonSchemes.client_description())

        self._sounds: list[SoundDescription] = []

    @property
    def dummy(self):
        """Whether or not the actor is a dummy actor. If True, Anvil will create a dummy geometry and texture for the actor."""
        dummy = Geometry("dummy")
        dummy.add_geo("dummy", (8, 8)).set_visible_bounds((2, 1.5), (0, 0.25, 0)).add_bone("root", (0, 0, 0)).add_cube(
            (0, 0, 0), (0, 0, 0), (0, 0)
        )
        dummy.queue("actors")
        CopyFiles(
            os.path.join("assets", "models", "actors"),
            os.path.join(
                "resource_packs",
                f"RP_{CONFIG._PASCAL_PROJECT_NAME}",
                "models",
                "entity",
                "actors",
            ),
            "dummy.geo.json",
        )

        self._description["description"]["geometry"].update({"dummy": f"geometry.{CONFIG.NAMESPACE}.dummy"})

        img = Image.new("RGBA", (8, 8), color=(0, 0, 0, 0))
        img.save(os.path.join("assets", "textures", "actors", "dummy.png"))
        CopyFiles(
            os.path.join("assets", "textures", "actors"),
            os.path.join(
                CONFIG.RP_PATH,
                "textures",
                CONFIG.NAMESPACE,
                CONFIG.PROJECT_NAME,
                "actors",
            ),
            "dummy.png",
        )
        self._description["description"]["textures"].update(
            {"dummy": os.path.join("textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "actors", "dummy")}
        )

        self.render_controller("dummy").geometry("dummy").textures("dummy")

    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str | Molang = None):
        """Sets the mapping of internal animation controller references to actual animations.

        Args:
            controller_shortname (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str| Molang, optional): The condition to animate the animation controller. Defaults to None.

        """
        self._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(self, geometry_name: str, animation_name: str, animate: bool = False, condition: str | Molang = None):
        """Sets the mapping of internal animation references to actual animations.

        Args:
            animation_name (str): The name of the animation.
            animate (bool, optional): Whether or not to animate the animation. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation. Defaults to None.

        """
        
        anim_namespace = f"animation.{CONFIG.NAMESPACE}.{geometry_name}.{animation_name}"

        if not anim_namespace in _ActorClientDescription._queued_animations:
            try: 
                with open(os.path.join("assets", "animations", f"{geometry_name}{Animation._extension}")) as file:
                    if anim_namespace not in file.read():
                        CONFIG.Logger.missing_animation(
                            os.path.join("assets", "animations", f"{geometry_name}{Animation._extension}"), anim_namespace
                        )
            except:
                CONFIG.Logger.file_exist_error(f"{geometry_name}{Animation._extension}", os.path.join("assets", "animations"))

            _ActorClientDescription._queued_animations.add(anim_namespace)

        self._animations(geometry_name, animation_name, animate, condition)

        return self

    def material(self, material_id: str, material_name: str):
        """This method manages the materials for an entity.

        Args:
            material_id (str): The id of the material.
            material_name (str): The name of the material.

        """
        self._description["description"]["materials"].update({material_id: material_name})
        return self

    def geometry(self, geometry_shortname: str, geometry_name: str):
        """
        This method manages the geometry for an entity.

        Args:
            geometry_shortname (str): The shortname of the geometry.
            geometry_name (str): The name of the geometry.

        Returns:
            self: Returns an instance of the class.
        """

        geo_namespace = f"geometry.{CONFIG.NAMESPACE}.{geometry_name}"
        if not geo_namespace in _ActorClientDescription._queued_models:
            try:
                with open(os.path.join("assets", "models", "actors", f"{geometry_name}.geo.json")) as file:
                    data = file.read()
                    if geo_namespace not in data:
                        CONFIG.Logger.namespace_not_in_geo(
                            os.path.join("assets", "models", "actors", f"{geometry_name}.geo.json"), geo_namespace
                        )
            except:
                CONFIG.Logger.file_exist_error(f"{geometry_name}.geo.json", os.path.join("assets", "models", "actors"))

            _ActorClientDescription._queued_models.add(geometry_name)

        self._description["description"]["geometry"].update({geometry_shortname: geo_namespace})

        return self

    def texture(self, texture_id: str, texture_name: str):
        """This method manages the textures for an entity.

        Args:
            texture_id (str): The id of the texture.
            texture_name (str): The name of the texture.

        """
        if not texture_name in _ActorClientDescription._queued_textures:
            if not FileExists(os.path.join("assets", "textures", "actors", f"{texture_name}.png")):
                CONFIG.Logger.file_exist_error(f"{texture_name}.png", os.path.join("assets", "textures", "actors"))

            self._queued_textures.add(texture_name)

        self._description["description"]["textures"].update(
            {texture_id: os.path.join("textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "actors", texture_name)}
        )

        return self

    def script(self, variable: Variable | str, script: Molang | str):
        """This method manages the scripts for an entity."""
        self._description["description"]["scripts"]["pre_animation"].append(f"{variable}={script};")
        return self

    def init_vars(self, **vars):
        """Initializes variables for an entity.

        Examples:
            >>> Entity("example").init_vars(x=0, y=5, z=8)
        """
        for k, v in vars.items():
            Variable._set_var(k)
            self._description["description"]["scripts"]["initialize"].append(f"v.{k}={v};")
        return self

    def scale(self, scale: Molang | str = "1"):
        """Sets the scale of the entity.

        Args:
            scale (str | Molang, optional): The scale of the entity. Defaults to "1".
        """
        if not scale == "1":
            self._description["description"]["scripts"].update({"scale": str(scale)})

    def render_controller(self, controller_name: str, condition: str = None):
        """This method manages the render controllers for an entity.

        Args:
            controller_name (str): The name of the render controller.
            condition (str, optional): The condition to render the render controller. Defaults to None.

        """
        if condition is None:
            self._render_append(f"controller.render.{CONFIG.NAMESPACE}.{self._name}.{controller_name}")
        else:
            self._render_append({f"controller.render.{CONFIG.NAMESPACE}.{self._name}.{controller_name}": condition})

        return self._render_controllers.add_controller(controller_name)

    def particle_effect(self, particle_name: str):
        """This method manages the particle effects for an entity.

        Args:
            particle_name (str): The name of the particle effect.

        """
        self._particle_name = particle_name
        self._description["description"]["particle_effects"].update(
            {self._particle_name: f"{CONFIG.NAMESPACE}:{self._particle_name}"}
        )
        return self

    def sound_effect(
        self,
        sound_name: str,
        sound_reference: str,
        category: SoundCategory = SoundCategory.Neutral,
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        """This method manages the sound effects for an entity.

        Args:
            sound_shortname (str): The shortname of the sound effect.
            sound_identifier (str): The identifier of the sound effect.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.

        """
        self._description["description"]["sound_effects"].update({sound_name: f"{CONFIG.NAMESPACE}:{sound_reference}"})
        sound: SoundDescription = ANVIL.definitions.register_sound_definition(
            sound_reference, category, max_distance=max_distance, min_distance=min_distance
        )
        self._sounds.append(sound)
        return sound

    def sound_event(
        self,
        sound_identifier,
        sound_event: EntitySoundEvent,
        category: SoundCategory = SoundCategory.Neutral,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: int = 0,
        min_distance: int = 9999,
    ):
        """This method manages the sound events for an entity.

        Args:
            sound_identifier (_type_): The identifier of the sound effect.
            sound_event (EntitySoundEvent): The sound event.
            category (SoundCategory, optional): The category of the sound effect. Defaults to SoundCategory.Neutral.
            volume (float, optional): The volume of the sound effect. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the sound effect. Defaults to (0.8, 1.2).

        """
        ANVIL.definitions.register_sound_event(self.identifier, sound_identifier, sound_event, volume, pitch)

        sound: SoundDescription = ANVIL.definitions.register_sound_definition(
            sound_identifier, category, max_distance=max_distance, min_distance=min_distance
        )
        self._sounds.append(sound)
        return sound

    @Halo("Retrieving vanilla entity description")
    def get_vanilla(self):
        if self.is_vanilla:
            cache_path = os.path.join("assets", "cache", f"{self.name}.entity.json")
            data = {}
            if FileExists(cache_path):
                with open(cache_path, "r") as file:
                    data = json.loads(file.read())
            else:
                retrieve = requests.get(
                    f"https://raw.githubusercontent.com/Mojang/bedrock-samples/main/resource_pack/entity/{self.name}.entity.json"
                )
                data = json.loads(retrieve.text)
            self._description["description"] = data["minecraft:client_entity"]["description"]
            if "particle_effects" not in self._description["description"]:
                self._description["description"]["particle_effects"] = {}
            File(f"{self.name}.entity.json", data, os.path.join("assets", "cache"), "w", True)

    def to_dict(self, directory: str = None):
        """Queues the entity for export.

        Args:
            directory (str, optional): The directory to export the entity to. Defaults to None.

        Raises:
            RuntimeError: If the entity does not have a geometry, texture, or render controller.
            Exception: If a geometry is reused but the entity it is reused from has not been queued yet.

        """
        from anvil.api.features import Particle

        if len(self._description["description"]["geometry"]) == 0:
            CONFIG.Logger.missing_geometry(self.identifier)

        if len(self._description["description"]["textures"]) == 0:
            CONFIG.Logger.missing_texture(self.identifier)

        if len(self._description["description"]["render_controllers"]) == 0:
            CONFIG.Logger.missing_render_controller(self.identifier)

        # TODO: Replace once a proper particle integration is added.
        if "particle_effects" in self._description["description"]:
            for particle in self._description["description"]["particle_effects"]:
                Particle(particle).queue()

        for sound in self._sounds:
            sound._export

        self._render_controllers.queue(directory)
        self._animation_controllers.queue(directory)

        return super().to_dict

    @staticmethod
    def _export():
        for model in _ActorClientDescription._queued_models:
            CopyFiles(
                os.path.join("assets", "models", "actors"),
                os.path.join(
                    CONFIG.RP_PATH,
                    "models",
                    "entity",
                    "actors"
                ),
                f"{model}.geo.json",
            )
        
        for texture in _ActorClientDescription._queued_textures:
            CopyFiles(
                os.path.join("assets", "textures", "actors"),
                os.path.join(
                    CONFIG.RP_PATH,
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "actors"
                ),
                f"{texture}.png",
            )
        
        for animation in _ActorClientDescription._queued_animations:
            CopyFiles(
                os.path.join("assets", "animations"),
                os.path.join(
                    CONFIG.RP_PATH,
                    "animations",
                    #CONFIG.NAMESPACE,
                    #CONFIG.PROJECT_NAME,
                    "actors"
                ),
                f"{animation.split(".")[2]}.animation.json",
            )


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
                CONFIG.Logger.experimental_not_allowed(self.identifier)
        else:
            CONFIG.Logger.entity_marked_as_experimental(self.identifier)

        self._description["description"]["is_experimental"] = True
        return self

    def RuntimeIdentifier(self, entity: Entities.vanilla_entity):
        """Sets the runtime identifier of the entity.

        Args:
            entity (Entities.vanilla_entity): The vanilla entity to get the runtime identifier from.
        """
        if CONFIG._TARGET != "addon":
            if not type(entity) is Entities.vanilla_entity:
                CONFIG.Logger.runtime_entity_error(entity)
            else:
                if entity._allow_runtime:
                    self._description["description"]["runtime_identifier"] = entity.identifier
                else:
                    CONFIG.Logger.runtime_entity_not_allowed(entity)
        else:
            CONFIG.Logger.runtime_not_allowed(self.identifier)

    @property
    def add_property(self):
        """Adds a property to the entity."""
        return self._properties

    @property
    def _export(self):
        """Exports the entity description."""
        self._description["description"]["properties"] = self._properties._export
        return super().to_dict


class _EntityClientDescription(_ActorClientDescription):
    """Base class for all client entity descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entity descriptions.

        Args:
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

    def spawn_egg(self, item_sprite: str):
        """This method adds a spawn egg texture to the entity.

        Args:
            item_sprite (str): The name of the item sprite.
        """
        ANVIL.definitions.register_item_textures(item_sprite, "spawn_eggs", item_sprite)
        self._description["description"]["spawn_egg"] = {"texture": f"{CONFIG.NAMESPACE}:{item_sprite}"}

    def to_dict(self, directory: str):
        """Queues the entity for export.

        Args:
            directory (str): The directory to export the entity to.

        """
        super().to_dict(directory)
        if "spawn_egg" not in self._description["description"] and not self._is_vanilla:
            self._spawn_egg_texture = list(self._description["description"]["textures"].values())[0].split("\\")[-1]
            reduced_image = Image.open(
                os.path.join(
                    "assets",
                    "textures",
                    "actors",
                    f'{self._spawn_egg_texture}.png',
                )
            ).convert("P", palette=Image.WEB)
            palette = reduced_image.getpalette()
            color_counts = (
                (
                    count,
                    "#{0:02x}{1:02x}{2:02x}".format(*palette[3 * index : 3 * index + 3]),
                )
                for count, index in reduced_image.getcolors()
            )
            most_dominant = max(color_counts, key=lambda x: x[0])[1]
            color_counts = (
                (
                    count,
                    "#{0:02x}{1:02x}{2:02x}".format(*palette[3 * index : 3 * index + 3]),
                )
                for count, index in reduced_image.getcolors()
            )
            least_dominant = min(color_counts, key=lambda x: x[0])[1]

            self._description["description"]["spawn_egg"] = {
                "base_color": most_dominant,
                "overlay_color": least_dominant,
            }
        return self._description


class _AttachableClientDescription(_ActorClientDescription):
    """Base class for all client attachable descriptions."""
    _type = "attachables"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client attachable descriptions.

        Args:
            name (str): The name of the attachable.
            is_vanilla (bool, optional): Whether or not the attachable is a vanilla attachable. Defaults to False.
        """
        super().__init__(name, is_vanilla)


class _EntityServer(AddonObject):
    """Base class for all server entities."""

    _extension = ".behavior.json"
    _path = os.path.join(CONFIG.BP_PATH, "entities")

    def _add_despawn_function(self):
        """Adds a despawn function to the entity."""
        self.component_group("despawn").add(InstantDespawn())
        self.event("despawn").add("despawn")

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all server entities.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name)
        self._is_vanilla = is_vanilla
        self._server_entity = JsonSchemes.server_entity()
        self._description = _EntityServerDescription(self._name, self._is_vanilla)
        self._animation_controllers = _BP_AnimationControllers(self._name, self._is_vanilla)
        self._animations = _BPAnimations(self._name, self._is_vanilla)
        self._spawn_rule = _SpawnRule(self._name, self._is_vanilla)
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

    def animation_controller(self, controller_shortname: str, animate: bool = False, condition: str | Molang = None):
        """Sets the mapping of internal animation controller references to actual animations.

        Args:
            controller_shortname (str): The name of the animation controller.
            animate (bool, optional): Whether or not to animate the animation controller. Defaults to False.
            condition (str | Molang, optional): The condition to animate the animation controller. Defaults to None.

        """
        self._description._animation_controller(controller_shortname, animate, condition)
        return self._animation_controllers.add_controller(controller_shortname)

    def animation(
        self,
        animation_name: str,
        loop: bool = False,
        animate: bool = False,
        condition: str | Molang = None,
    ):
        """Sets the mapping of internal animation references to actual animations.

        Args:
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

        Args:
            event_name (str): The name of the event.
        """
        self._event = _Event(event_name)
        self._events.append(self._event)
        return self._event

    @property
    def components(self):
        """Returns the components of the entity."""
        return self._components

    @property
    def identifier(self) -> str:
        return self.description.identifier

    def component_group(self, component_group_name: str):
        """Adds a component group to the entity.

        Args:
            component_group_name (str): The name of the component group.

        """
        self._component_group = _ComponentGroup(component_group_name)
        self._component_groups.append(self._component_group)
        return self._component_group

    def queue(self, directory: str = None):
        """Queues the entity for export.

        Args:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        if len(self._vars) > 0:
            self.animation_controller("variables", True).add_state("default").on_entry(*self._vars)
        self._animations.queue(directory=directory)
        self._animation_controllers.queue(directory=directory)
        self._spawn_rule.queue(directory=directory)

        self._server_entity["minecraft:entity"].update(self.description._export)
        self._server_entity["minecraft:entity"]["components"].update(self._components._export()["components"])

        for event in self._events:
            self._server_entity["minecraft:entity"]["events"].update(event._export)
        for component_group in self._component_groups:
            self._server_entity["minecraft:entity"]["component_groups"].update(component_group._export())

        self.content(self._server_entity)

        controllers = list(self._animation_controllers._animation_controllers["animation_controllers"].keys())
        cleared_items = []
        for key, controller in self._description._description["description"]["animations"].items():
            if controller.startswith("controller.") and controller not in controllers:
                cleared_items.append(key)
        
        for item in cleared_items:
            self._description._description["description"]["animations"].pop(item)
            
        if Rideable.component_namespace in json.dumps(self._server_entity):
            ANVIL.definitions.register_lang(f"action.hint.exit.{self.identifier}", "Hold shift to exit")

        super().queue(directory=directory)


class _EntityClient(AddonObject):
    """Base class for all client entities."""

    _extension = ".entity.json"
    _path = os.path.join(CONFIG.RP_PATH, "entity")

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entities.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name)
        self._is_vanilla = is_vanilla
        self._client_entity = JsonSchemes.client_entity()
        self._description = _EntityClientDescription(self._name, self._is_vanilla)

    @property
    def description(self):
        """Returns the entity description."""
        return self._description

    @property
    def identifier(self) -> str:
        return self.description.identifier

    def queue(self, directory: str = None):
        """Queues the entity for export.

        Args:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        self._client_entity["minecraft:client_entity"].update(self._description.to_dict(directory))

        self.content(self._client_entity)
        super().queue(directory=directory)


# Render Controllers
class _RenderController:
    def __init__(self, identifier, controller_name, is_vanilla):
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = CONFIG.NAMESPACE
        if is_vanilla:
            self._namespace_format = "minecraft"
        self._controller_name = controller_name
        self._controller = JsonSchemes.render_controller(CONFIG.NAMESPACE, self._identifier, self._controller_name)
        self.controller_identifier = f"controller.render.{CONFIG.NAMESPACE}.{self._identifier}.{self._controller_name}"

    def texture_array(self, array_name: str, *textures_short_names: str):
        self._controller[self.controller_identifier]["arrays"]["textures"].update(
            {f"Array.{array_name}": [f"Texture.{texture}" for texture in textures_short_names]}
        )
        return self

    def material(self, bone: str, material_shortname: str):
        self._controller[self.controller_identifier]["materials"].append(
            {bone: material_shortname if material_shortname.startswith(("v", "q")) else f"Material.{material_shortname}"}
        )
        return self

    def geometry_array(self, array_name: str, *geometries_short_names: str):
        self._controller[self.controller_identifier]["arrays"]["geometries"].update(
            {f"Array.{array_name}": [f"Geometry.{geometry}" for geometry in geometries_short_names]}
        )
        return self

    def geometry(self, short_name: str = "default"):
        if "Array" not in short_name:
            name = f"Geometry.{short_name}"
        else:
            name = short_name
        self._controller[self.controller_identifier]["geometry"] = name
        return self

    def textures(self, short_name: str = "default"):
        if "Array" not in short_name:
            name = f"Texture.{short_name}"
        else:
            name = short_name

        self._controller[self.controller_identifier]["textures"].append(name)
        return self

    def part_visibility(self, bone: str, condition: str | bool):
        self._controller[self.controller_identifier]["part_visibility"].append({bone: condition})
        return self

    def overlay_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({"overlay_color": {"a": a, "r": r, "g": g, "b": b}})
        return self

    def on_fire_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({"on_fire_color": {"a": a, "r": r, "g": g, "b": b}})
        return self

    def is_hurt_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({"is_hurt_color": {"a": a, "r": r, "g": g, "b": b}})
        return self

    def color(self, a, r, g, b):
        self._controller[self.controller_identifier].update({"color": {"a": a, "r": r, "g": g, "b": b}})
        return self

    @property
    def filter_lighting(self):
        self._controller[self.controller_identifier]["filter_lighting"] = True
        return self

    @property
    def ignore_lighting(self):
        self._controller[self.controller_identifier]["ignore_lighting"] = True
        return self

    def light_color_multiplier(self, multiplier: int):
        self._controller[self.controller_identifier]["light_color_multiplier"] = multiplier
        return self

    def uv_anim(self, offset: list[str, str], scale: list[str, str]):
        self._controller[self.controller_identifier]["uv_anim"] = {
            "offset": offset,
            "scale": scale,
        }

    @property
    def _export(self):
        if len(self._controller[self.controller_identifier]["materials"]) == 0:
            self.material("*", "default")
        return self._controller


class _RenderControllers(AddonObject):
    _extension = ".rc.json"
    _path = os.path.join(
        CONFIG.RP_PATH,
        "render_controllers",
    )

    def __init__(self, identifier: str, is_vanilla) -> None:
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._controllers: list[_RenderController] = []
        self.render_controller = JsonSchemes.render_controllers()
        super().__init__(self._identifier)

    def add_controller(self, controller_name: str):
        self._render_controller = _RenderController(self._identifier, controller_name, self._is_vanilla)
        self._controllers.append(self._render_controller)
        return self._render_controller

    def queue(self, directory: str = ""):
        if len(self._controllers) > 0:
            for controller in self._controllers:
                self.render_controller["render_controllers"].update(controller._export)
            self.content(self.render_controller)
            return super().queue(directory=directory)


# Animation Controllers
class _BP_ControllerState:
    def __init__(self, state_name):
        self._state_name = state_name
        self._controller_state: dict = JsonSchemes.animation_controller_state(self._state_name)
        self._default = True

    def on_entry(self, *commands: str):
        """Events, commands or molang to preform on entry of this state.

        Parameters
        ----------
        commands : str
            param commands: The Events, commands or molang to preform on entry of this state.

        Returns
        -------
            This state.

        """
        for command in commands:
            if str(command).startswith(Target.S):
                self._controller_state[self._state_name]["on_entry"].append(command)
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_entry"].append(f"{command};")
            else:
                self._controller_state[self._state_name]["on_entry"].append(f"/{command}")
        self._default = False
        return self

    def on_exit(self, *commands: str):
        """Events, commands or molang to preform on exit of this state.

        Parameters
        ----------
        commands : str
            param commands: The Events, commands or molang to preform on exit of this state.

        Returns
        -------
            This state.

        """
        for command in commands:
            if str(command).startswith(Target.S.value):
                self._controller_state[self._state_name]["on_exit"].append(f"{command}")
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_exit"].append(f"{command};")
            else:
                self._controller_state[self._state_name]["on_exit"].append(f"/{command}")
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
            self._controller_state[self._state_name]["animations"].append({animation: condition})
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
        self._controller_state[self._state_name]["transitions"].append({state: str(condition)})
        self._default = False
        return self

    @property
    def _export(self):
        return self._controller_state


class _RP_ControllerState:
    def __init__(self, state_name):
        self._state_name = state_name
        self._controller_state = JsonSchemes.animation_controller_state(self._state_name)
        self._controller_state[self._state_name]["particle_effects"] = []
        self._controller_state[self._state_name]["sound_effects"] = []
        self._default = True

    def on_entry(self, *commands: str):
        """Molang to preform on entry of this state.

        Parameters
        ----------
        commands : str
            param commands: Molang to preform on entry of this state.

        Returns
        -------
            This state.

        """
        for command in commands:
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_entry"].append(f"{command};")
            else:
                CONFIG.Logger.molang_only(command)
        self._default = False
        return self

    def on_exit(self, *commands: str):
        """Molang to preform on exit of this state.

        Parameters
        ----------
        commands : str
            param commands: Molang to preform on exit of this state.

        Returns
        -------
            This state.

        """
        for command in commands:
            if any(command.startswith(v) for v in MOLANG_PREFIXES):
                self._controller_state[self._state_name]["on_exit"].append(f"{command};")
            else:
                CONFIG.Logger.molang_only(command)
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
            self._controller_state[self._state_name]["animations"].append({animation: condition})
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
        self._controller_state[self._state_name]["transitions"].append({state: str(condition)})
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
        particle = {"effect": effect, "locator": locator}
        if pre_anim_script is not None:
            particle.update({"pre_effect_script": pre_anim_script})
        if bind_to_actor is False:
            particle.update({"bind_to_actor": False})
        self._controller_state[self._state_name]["particle_effects"].append(particle)
        self._default = False
        return self

    def sound_effect(self, effect: str):
        """Collection of sounds to trigger on entry to this animation state.

        Parameters
        ----------
        effect : str
            The shortname of the sound effect to be played, defined in the Client Entity.

        Returns
        -------
            This state.

        """
        self._controller_state[self._state_name]["sound_effects"].append({"effect": effect})
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
    def __init__(self, identifier, controller_shortname, is_vanilla):
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = CONFIG.NAMESPACE
        if is_vanilla:
            self._namespace_format = "minecraft"
        self._controller_shortname = controller_shortname
        self._controllers = JsonSchemes.animation_controller(CONFIG.NAMESPACE, self._identifier, self._controller_shortname)
        self._controller_states: list[_BP_ControllerState] = []
        self._controller_namespace = f"controller.animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._controller_shortname}"
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
                self._controllers[self._controller_namespace]["states"].update(state._export)
                for tr in state._export.values():
                    if "transitions" in tr:
                        for st in tr["transitions"]:
                            collected_states.extend(st.keys())

        for state in set(collected_states):
            if state not in self._states_names:
                CONFIG.Logger.missing_state(self._side, self._controller_namespace, state)
        
        if len(self._controllers[self._controller_namespace]["states"].items()) > 0:
            return self._controllers
        return {}


class _RP_Controller(_BP_Controller):
    def __init__(self, name, controller_shortname, is_vanilla):
        super().__init__(name, controller_shortname, is_vanilla)
        self._side = "Client"
        self._controller_states: list[_RP_ControllerState] = []

    def add_state(self, state_name: str):
        self._states_names.append(state_name)
        self._controller_state = _RP_ControllerState(state_name)
        self._controller_states.append(self._controller_state)
        return self._controller_state


class _BP_AnimationControllers(AddonObject):
    _extension = ".bp_ac.json"
    _path = os.path.join(
        CONFIG.BP_PATH,
        "animation_controllers",
    )

    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier)
        self._identifier = identifier
        self._is_vanilla = is_vanilla
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
        ctrl = _BP_Controller(self._name, controller_shortname, self._is_vanilla)
        self._controllers_list.append(ctrl)
        return ctrl

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            for controller in self._controllers_list:
                self._animation_controllers["animation_controllers"].update(controller._export)
            self.content(self._animation_controllers)
            return super().queue(directory=directory)


class _RP_AnimationControllers(AddonObject):
    _extension = ".rp_ac.json"
    _path = os.path.join(CONFIG.RP_PATH, "animation_controllers")

    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name)
        self._name = name
        self._is_vanilla = is_vanilla
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
        self._animation_controller = _RP_Controller(self._name, controller_shortname, self._is_vanilla)
        self._controllers_list.append(self._animation_controller)
        return self._animation_controller

    def queue(self, directory: str = None):
        if len(self._controllers_list) > 0:
            if any([len(t._controller_states) > 0 for t in [c for c in self._controllers_list]]):
                for controller in self._controllers_list:
                    self._animation_controllers["animation_controllers"].update(controller._export)
                self.content(self._animation_controllers)
                return super().queue(directory=directory)


# Animations
class _BPAnimation:
    def __init__(self, identifier, animation_short_name: str, loop: bool, is_vanilla):
        self._is_vanilla = is_vanilla
        self._identifier = identifier
        self._namespace_format = CONFIG.NAMESPACE
        if is_vanilla:
            self._namespace_format = "minecraft"
        self._animation_short_name = animation_short_name
        self._animation_length = 0.01
        self._animation = JsonSchemes.bp_animation(CONFIG.NAMESPACE, self._identifier, self._animation_short_name, loop)

    def timeline(self, timestamp: float, *commands: str):
        """Takes a timestamp and a list of events, command or molang to run at that time.

        Parameters
        ----------
        timestamp : int
            The timestamp of the event.
        commands : str
            param commands: The Events, commands or molang to run on exit of this state.

        Returns
        -------
            This animation.

        """
        if self._animation_length < timestamp:
            self._animation_length = timestamp + 0.1
        self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"][
            "animation_length"
        ] = self._animation_length
        if (
            timestamp
            not in self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"]["timeline"]
        ):
            self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"]["timeline"][
                timestamp
            ] = []
        for command in commands:
            if str(command).startswith("@s"):
                self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"]["timeline"][
                    timestamp
                ].append(f"{command}")
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"]["timeline"][
                    timestamp
                ].append(f"{command};")
            else:
                self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"]["timeline"][
                    timestamp
                ].append(f"/{command}")
        return self

    def animation_length(self, animation_length: float):
        """This function sets the length of the animation.

        Parameters
        ----------
        animation_length : int
            The length of the animation in seconds.

        Returns
        -------
            This animation.

        """
        self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"][
            "animation_length"
        ] = animation_length
        return self

    def anim_time_update(self, anim_time_update: Query):
        """
        Parameters
        ----------
        anim_time_update : int
            The length of the animation in seconds.

        Returns
        -------
            This animation.

        """
        self._animation[f"animation.{CONFIG.NAMESPACE}.{self._identifier}.{self._animation_short_name}"][
            "anim_time_update"
        ] = anim_time_update
        return self

    @property
    def _export(self):
        return self._animation


class _BPAnimations(AddonObject):
    _extension = ".animation.json"
    _path = os.path.join(CONFIG.BP_PATH, "animations")

    def __init__(self, identifier, is_vanilla) -> None:
        super().__init__(identifier)
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._animations = JsonSchemes.bp_animations()
        self._animations_list: list[_BPAnimation] = []

    def add_animation(self, animation_short_name: str, loop: bool = False):
        """Adds a new animation to the current actor.

        Parameters
        ----------
        animation_short_name : str
            The shortname of the animation you want to add.
        loop : bool, optional
            If the animation should loop or not.

        Returns
        -------
            Animation.

        """
        self._animation = _BPAnimation(self._identifier, animation_short_name, loop, self._is_vanilla)
        self._animations_list.append(self._animation)
        return self._animation

    def queue(self, directory: str = None):
        if len(self._animations_list) > 0:
            for animation in self._animations_list:
                self._animations["animations"].update(animation._export)
            self.content(self._animations)
            return super().queue(directory=directory)


# Spawn Rules
class _SpawnRuleDescription(MinecraftDescription):
    def __init__(self, spawn_rule_obj, name: str, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._spawn_rule_obj: _SpawnRule = spawn_rule_obj
        self._description["description"]["population_control"] = Population.Ambient

    def population_control(self, population: Population):
        """Setting an entity to a pool it will spawn as long as that pool hasn't reached the spawn limit.

        Parameters
        ----------
        population : Population
            Population Control
                `Animal`, `UnderwaterAnimal`, `Monster`, `Ambient`

        Returns
        -------
            Spawn Rule

        """
        self._description["description"]["population_control"] = population.value
        return self._spawn_rule_obj


class _Condition:
    def __init__(self):
        self._condition = {}

    @property
    def SpawnOnSurface(self):
        """Sets the actor to spawn on surfaces.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:spawns_on_surface": {}})
        return self

    @property
    def SpawnUnderground(self):
        """Sets the actor to spawn underground.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:spawns_underground": {}})
        return self

    @property
    def SpawnUnderwater(self):
        """Sets the actor to spawn underwater.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:spawns_underwater": {}})
        return self

    @property
    def SpawnInLava(self):
        """Sets the actor to spawn in lava.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:spawns_lava": {}})
        return self

    def SpawnsOnBlockFilter(self, *block):
        """Sets the list of blocks the actor can spawn on top of.

        Parameters
        ----------
        block : str
            Valid blocks to activate this component.

        Returns
        -------
            Spawn rule condition.

        """
        if "minecraft:spawns_on_block_filter" not in self._condition:
            self._condition.update({"minecraft:spawns_on_block_filter": []})
        self._condition["minecraft:spawns_on_block_filter"] = block
        return self

    def DensityLimit(self, surface: int = -1, underground: int = -1):
        """Sets the density limit number of this mob type to spawn.

        Parameters
        ----------
        surface : int
            The maximum number of mob of this mob type spawnable on the surface. `-1` for an unlimited number.
        underground : int
            The maximum number of mob of this mob type spawnable underground. `-1` for an unlimited number.

        Returns
        -------
            Spawn rule condition.

        """
        density = {"minecraft:density_limit": {}}
        if surface != -1:
            density["minecraft:density_limit"]["surface"] = surface
        if underground != -1:
            density["minecraft:density_limit"]["underground"] = underground
        self._condition.update(density)
        return self

    def BrightnessFilter(
        self,
        min_brightness: int = 0,
        max_brightness: int = 15,
        adjust_for_weather: bool = True,
    ):
        """This function filters the image by brightness

        Parameters
        ----------
        min_brightness : int
            The minimum light level value that allows the mob to spawn. Allowed range is (0,15)
        max_brightness : int
            The maximum light level value that allows the mob to spawn. Allowed range is (0,15)
        adjust_for_weather : bool, optional
            This determines if weather can affect the light level conditions that cause the mob to spawn (e.g. Allowing hostile mobs to spawn during the day when it rains.)

        Returns
        -------
            Spawn rule condition.

        """
        min_brightness = max(0, min_brightness)
        max_brightness = min(15, max_brightness)
        self._condition.update(
            {
                "minecraft:brightness_filter": {
                    "min": min_brightness,
                    "max": max_brightness,
                    "adjust_for_weather": adjust_for_weather,
                }
            }
        )
        return self

    def DifficultyFilter(
        self,
        min_difficulty: Difficulty = Difficulty.Easy,
        max_difficulty: Difficulty = Difficulty.Hard,
    ):
        """Sets the range of difficulties this mob type should spawn in.

        Parameters
        ----------
        min_difficulty : Difficulty
            The minimum difficulty level that this mob spawns in.
        max_difficulty : Difficulty
            The maximum difficulty level that this mob spawns in.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update(
            {
                "minecraft:difficulty_filter": {
                    "min": min_difficulty,
                    "max": max_difficulty,
                }
            }
        )
        return self

    def Weight(self, weight: int = 0):
        """The weight on how likely the spawn rule chooses this condition over other valid conditions. The higher the value the more likely it will be chosen.

        Parameters
        ----------
        weight : int
            The weight of the item.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:weight": {"default": weight}})
        return self

    def Herd(
        self,
        min_size: int = 1,
        max_size: int = 4,
        spawn_event: str = None,
        event_skip_count: int = 0,
    ):
        """Determines the herd size of this mob.

        Parameters
        ----------
        min_size : int
            The minimum number of mobs of this type that can spawn in the herd.
        max_size : int
            The maximum number of mobs of this type that can spawn in the herd.
        spawn_event : str, optional
                This is an event that can be triggered from spawning.
        event_skip_count : int, optional
            This is the number of mobs spawned before the Specifies event is triggered.

        Returns
        -------
            Spawn rule condition.

        """
        if "minecraft:herd" not in self._condition:
            self._condition.update({"minecraft:herd": []})
        self_herd = {"min_size": min_size, "max_size": max_size}
        if spawn_event != None:
            self_herd.update({"event": spawn_event, "event_skip_count": event_skip_count})
        self._condition["minecraft:herd"].append(self_herd)
        return self

    def BiomeFilter(self, filter: Filter):
        """Specifies which biomes the mob spawns in.

        Parameters
        ----------
        filter : dict
            Filter dict

        Returns
        -------
            Spawn rule condition.

        """
        if "minecraft:biome_filter" not in self._condition:
            self._condition.update({"minecraft:biome_filter": []})
        self._condition["minecraft:biome_filter"].append(filter)
        return self

    def HeightFilter(self, min: int, max: int):
        """Specifies the height range this mob spawn in.

        Parameters
        ----------
        min : int
            The minimum height that allows the mob to spawn.
        max : int
            The maximum height that allows the mob to spawn.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:height_filter": {"min": min, "max": max}})
        return self

    def WorldAgeFilter(self, min: int):
        """Specifies the minimum age of the world before this mob can spawn.

        Parameters
        ----------
        min : int
            The minimum age of the world.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:world_age_filter": {"min": min}})

        return self

    def SpawnsOnBlockPreventedFilter(self, *block):
        """Sets the list of blocks the actor should not spawn on.

        Returns
        -------
            Spawn rule condition.

        """
        if "minecraft:spawns_on_block_prevented_filter" not in self._condition:
            self._condition.update({"minecraft:spawns_on_block_prevented_filter": []})
        self._condition["minecraft:spawns_on_block_prevented_filter"] = block
        return self

    @property
    def DisallowSpawnsInBubble(self):
        """Prevents this mob from spawning in water bubbles.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:disallow_spawns_in_bubble": {}})
        return self

    def MobEventFilter(self, event: str):
        """Specifies the event to call on spawn.

        Parameters
        ----------
        event : str
            The event to call.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:mob_event_filter": {"event": event}})

        return self

    def DistanceFilter(self, min: int, max: int):
        """Specifies the distance range from a player this mob spawn in.

        Parameters
        ----------
        min : int
            The minimum distance from a player that allows the mob to spawn.
        max : int
            The maximum distance from a player that allows the mob to spawn.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:distance_filter": {"min": min, "max": max}})
        return self

    def DelayFilter(self, minimum: int, maximum: int, identifier: str, spawn_chance: int):
        """Unknown behavior.

        Parameters
        ----------
        minimum : int
            The minimum time required to use.
        maximum : int
            The maximum time required to use
        identifier : str
                The * identifier.
        spawn_chance : int
            This is spawn chance. range of (0-100)

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update(
            {
                "minecraft:delay_filter": {
                    "min": minimum,
                    "max": maximum,
                    "identifier": identifier,
                    "spawn_chance": max(min(spawn_chance, 100), 0),
                }
            }
        )

        return self

    def PermuteType(self, entity_type: str, weight: int = 10, spawn_event: str = None):
        """Sets a chance to mutate the spawned entity into another.

        Parameters
        ----------
        entity_type : str
            The entity identifier.
        weight : str
                The weight of permutation.
        spawn_event : str, optional
            The event to call on the entity spawning.

        Returns
        -------
            Spawn rule condition.

        """
        if "minecraft:permute_type" not in self._condition:
            self._condition.update({"minecraft:permute_type": []})
        self_permute_type = {"entity_type": entity_type, "weight": weight}
        if spawn_event != None:
            self_permute_type.update({"entity_type": f"{entity_type}<{spawn_event}>"})
        self._condition["minecraft:permute_type"].append(self_permute_type)
        return self

    def SpawnEvent(self, event: str = "minecraft:entity_spawned"):
        """Sets the event to call when the entity spawn in the world. By default the event called is `minecraft:entity_spawned` event without using this component.

        Parameters
        ----------
        event : str
            the event to call on entity spawn.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update({"minecraft:spawn_event": {"event": event}})
        return self

    def PlayerInVillageFilter(self, distance: int, village_border_tolerance: int):
        """Specifies the distance range the player must be from a village for this entity to spawn.

        Parameters
        ----------
        distance : int
            The distance from the village.
        village_border_tolerance : int
            The distance tolerance from the village borders.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update(
            {
                "minecraft:player_in_village_filter": {
                    "distance": distance,
                    "village_border_tolerance": village_border_tolerance,
                }
            }
        )
        return self

    def SpawnsAboveBlockFilter(self, distance: int, *block):
        """Sets the list of blocks the actor can spawn above.

        Parameters
        ----------
        distance : int
            The vertical distance to check for valid blocks.
        block : str
            Valid blocks to activate this component.

        Returns
        -------
            Spawn rule condition.

        """
        self._condition.update(
            {
                "minecraft:spawns_above_block_filter": {
                    "distance": distance,
                    "blocks": block,
                }
            }
        )
        return self

    def export(self):
        return self._condition


class _SpawnRule(AddonObject):
    _extension = ".spawn_rules.json"
    _path = os.path.join(CONFIG.BP_PATH, "spawn_rules")

    def __init__(self, identifier, is_vanilla):
        super().__init__(identifier)
        self._identifier = identifier
        self._is_vanilla = is_vanilla
        self._namespace_format = CONFIG.NAMESPACE
        if is_vanilla:
            self._namespace_format = "minecraft"
        self._description = _SpawnRuleDescription(self, self._identifier, self._is_vanilla)
        self._spawn_rule = JsonSchemes.spawn_rules()
        self._conditions = []

    @property
    def description(self):
        return self._description

    @property
    def add_condition(self):
        self._condition = _Condition()
        self._conditions.append(self._condition)
        return self._condition

    def queue(self, directory: str = None):
        if len(self._conditions) > 0:
            self._spawn_rule["minecraft:spawn_rules"].update(self._description.to_dict)
            self._spawn_rule["minecraft:spawn_rules"]["conditions"] = [condition.export() for condition in self._conditions]
            self.content(self._spawn_rule)
            return super().queue(directory=directory)


# Events
class _BaseEvent:
    def __init__(self, event_name: event):
        self._event_name = event_name
        self._event = {
            self._event_name: {
                "add": {"component_groups": []},
                "remove": {"component_groups": []},
                "queue_command": {"command": []},
                "set_property": {},
                "emit_vibration":{}
            }
        }

    def add(self, *component_groups: str):
        self._event[self._event_name]["add"]["component_groups"].extend(component_groups)
        return self

    def remove(self, *component_groups: str):
        self._event[self._event_name]["remove"]["component_groups"].extend(component_groups)
        return self

    def trigger(self, event: event):
        self._event[self._event_name]["trigger"] = event
        return self

    def set_property(self, property, value):
        self._event[self._event_name]["set_property"].update({f"{CONFIG.NAMESPACE}:{property}": value})
        return self

    def queue_command(self, *commands: str):
        self._event[self._event_name]["queue_command"]["command"].extend(cmd for cmd in commands)
        return self

    def emit_vibration(self, vibration: Vibrations):
        self._event[self._event_name]["vibration"] = vibration
        return self
    
    @property
    def _export(self):
        return self._event


class _Randomize(_BaseEvent):
    def __init__(self, parent):
        self._event = {"weight": 1, "set_property": {}}
        self._sequences: list[_Sequence] = []
        self._parent_class: _Event = parent

    def add(self, *component_groups):
        self._event.update({"add": {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({"remove": {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event: event):
        self._event.update({"trigger": event})
        return self

    def weight(self, weight: int):
        self._event.update({"weight": weight})
        return self

    def set_property(self, property, value):
        self._event["set_property"].update({f"{CONFIG.NAMESPACE}:{property}": value})
        return self

    def queue_command(self, *commands: str):
        self._event.update({"queue_command": {"command": commands}})
        return self
    
    def emit_vibration(self, vibration: Vibrations):
        self._event.update({"vibration": vibration})
        return self

    @property
    def randomize(self):
        return self._parent_class.randomize

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def _export(self):
        if len(self._sequences) > 0:
            self._event.update({"sequence": []})
            for sequence in self._sequences:
                self._event["sequence"].append(sequence._export)
        return self._event


class _Sequence(_BaseEvent):
    def __init__(self, parent_event) -> None:
        self._randomizes: list[_Randomize] = []
        self._parent_class: _Event = parent_event
        self._event = {"set_property": {}}

    def add(self, *component_groups):
        self._event.update({"add": {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({"remove": {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event: event):
        self._event.update({"trigger": event})
        return self

    def filters(self, filter: Filter):
        self._event.update({"filters": filter})
        return self

    def set_property(self, property, value):
        self._event["set_property"].update({f"{CONFIG.NAMESPACE}:{property}": value})
        return self

    def queue_command(self, *commands: str):
        self._event.update({"queue_command": {"command": commands}})
        return self
    
    def emit_vibration(self, vibration: Vibrations):
        self._event.update({"vibration": vibration})
        return self
    
    @property
    def sequence(self):
        return self._parent_class.sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    @property
    def _export(self):
        if len(self._randomizes) > 0:
            self._event.update({"randomize": []})
            for randomize in self._randomizes:
                self._event["randomize"].append(randomize._export)
        return self._event


class _Event(_BaseEvent):
    def __init__(self, event_name: event):
        super().__init__(event_name)
        self._sequences: list[_Sequence] = []
        self._randomizes: list[_Randomize] = []

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    @property
    def _export(self):
        if len(self._sequences) > 0 and len(self._randomizes) > 0:
            raise SyntaxError("Sequences and Randomizes cannot coexist in the same event.")
        if len(self._sequences) > 0:
            self._event[self._event_name].update({"sequence": []})
            for sequence in self._sequences:
                self._event[self._event_name]["sequence"].append(sequence._export)
        if len(self._randomizes) > 0:
            self._event[self._event_name].update({"randomize": []})
            for randomize in self._randomizes:
                self._event[self._event_name]["randomize"].append(randomize._export)
        return super()._export


# Components
class _Components:
    def __init__(self):
        self._component_group_name = "components"
        self._components: dict[str, _component] = {}

    def _set(self, key: str, value: _component):
        self._components[key] = value

    def _remove(self, key: str):
        self._components.pop(key)

    def _has(self, key: str):
        return key in self._components

    def add(self, *components: _component):
        for component in components:
            self._set(component.component_namespace, component)
        return self

    def remove(self, *components: _component):
        for component in components:
            self._remove(component.component_namespace)
        return self

    def overwrite(self, *components: _component):
        self._components = {}
        for component in components:
            self._set(component.component_namespace, component)

    def _export(self):
        cmp = {}
        for component in self._components.values():
            cmp.update(component)

        return {self._component_group_name: cmp}


class _ComponentGroup(_Components):
    def __init__(self, component_group_name: str):
        super().__init__()
        self._component_group_name = component_group_name
        self._components = {self._component_group_name: {}}


class _Properties:
    def __init__(self):
        self._properties = {}

    def enum(self, name: str, values: tuple[str], default: str, *, client_sync: bool = False):
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
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "int",
            "default": int(default),
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
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "float",
            "default": float(default),
            "range": [float(f) for f in range],
            "client_sync": client_sync,
        }
        return self

    def bool(self, name: str, *, default: bool = False, client_sync: bool = False):
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "bool",
            "default": default,
            "client_sync": client_sync,
        }
        return self

    @property
    def _export(self):
        return self._properties


# ========================================================================================================
class Entity:
    def _validate_name(self, name: str):
        if ":" in name:
            CONFIG.Logger.namespaces_not_allowed(name)
        if not name[0].isalpha():
            CONFIG.Logger.digits_not_allowed(name)

    def __init__(self, name: str) -> None:
        self._is_vanilla = name in ENTITY_LIST
        self._name = name if not self._is_vanilla else str(name)
        self._namespace_format = "minecraft" if self._is_vanilla else CONFIG.NAMESPACE
        self._validate_name(self._name)

        if CONFIG._TARGET == "addon" and self._is_vanilla:
            CONFIG.Logger.vanilla_override_error(self._name)

        self._server = _EntityServer(self._name, self._is_vanilla)
        self._client = _EntityClient(self._name, self._is_vanilla)

    @property
    def Server(self):
        """Server-side logic.

        Returns
        -------
            Server Entity.
        """
        return self._server

    @property
    def Client(self):
        """Client-side.

        Returns
        -------
            Client Entity.
        """
        return self._client

    @property
    def identifier(self) -> Identifier:
        """Returns the identifier of the Entity."""
        return self.Client.description.identifier

    @property
    def name(self) -> str:
        """Returns the name of the Entity."""
        return self.Client.description.name

    def add_basic_components(self):
        """Adds basic server components to the entity.

        This includes:
            - `JumpStatic`
            - `MovementType`
            - `NavigationType`
            - `Movement`
            - `Physics`
            - `KnockbackResistance`
            - `Health`
            - `CollisionBox`
            - `Breathable`
            - `DamageSensor`
            - `Pushable`
            - `PushThrough`
        """
        from anvil.api.commands import DamageCause
        from anvil.api.components import (Breathable, CollisionBox,
                                          DamageSensor, Health, JumpStatic,
                                          KnockbackResistance, Movement,
                                          MovementType, NavigationType,
                                          Physics, Pushable, PushThrough)

        self.Server.components.add(
            JumpStatic(0),
            MovementType().Basic(),
            NavigationType().Walk(),
            Movement(0),
            Physics(True, True),
            KnockbackResistance(10000),
            Health(6),
            CollisionBox(1, 1),
            Breathable(),
            DamageSensor().add_trigger(DamageCause.All, False),
            Pushable(False, False),
            PushThrough(1),
        )

    def queue(
        self,
        directory: str = None,
        display_name: str = None,
        spawn_egg_name: str = None,
    ):
        display_name = self._name.replace("_", " ").title() if display_name is None else display_name
        spawn_egg_name = f"Spawn {display_name}" if spawn_egg_name is None else spawn_egg_name
        if self._is_vanilla:
            directory = "vanilla"

        ANVIL.definitions.register_lang(f"entity.{self._namespace_format}:{self._name}.name", display_name)
        ANVIL.definitions.register_lang(f"entity.{self._namespace_format}:{self._name}<>.name", display_name)
        ANVIL.definitions.register_lang(
            f"item.spawn_egg.entity.{self._namespace_format}:{self._name}.name",
            spawn_egg_name,
        )
        self.Client.queue(directory)
        self.Server.queue(directory)

        CONFIG.Report.add_report(
            ReportType.ENTITY,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
            # col2 = [event._event_name for event in self.Server._events]
        )

    def __str__(self):
        return self.identifier


class Attachable(AddonObject):
    _extension = ".attachable.json"
    _path = os.path.join(CONFIG.RP_PATH, "attachables")

    def __init__(self, name: str) -> None:
        """Initializes the attachable.

        Args:
            name (str): The name of the attachable.
        """
        super().__init__(name)
        self._name = name
        self._is_vanilla = name in ITEMS_LIST
        self._namespace = "minecraft" if self._is_vanilla else CONFIG.NAMESPACE

        if CONFIG._TARGET == "addon" and self._is_vanilla:
            CONFIG.Logger.vanilla_override_error(self._name)

        self._attachable = JsonSchemes.attachable()
        self._description = _AttachableClientDescription(self._name, False)

    @property
    def description(self):
        """Returns the description of the attachable."""
        return self._description

    @property
    def identifier(self) -> Identifier:
        """Returns the identifier of the attachable."""
        return self.description.identifier

    @property
    def name(self) -> str:
        """Returns the name of the attachable."""
        return self.description.name

    @property
    def queue(self):
        """Queues the attachable."""

        display_name = self._name.replace("_", " ").title()

        self._attachable["minecraft:attachable"].update(self._description.to_dict())
        self.content(self._attachable)

        CONFIG.Report.add_report(
            ReportType.ATTACHABLE,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )
        super().queue()

    def __str__(self):
        """Returns the identifier of the attachable."""
        return self.identifier
