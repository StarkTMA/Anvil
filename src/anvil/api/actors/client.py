"""The resource pack's `entity/<entity>.entity.json`: how a client entity renders, and the
`description` builders it shares with the item client (attachable)."""

from pathlib import PurePosixPath
from typing import Annotated, ClassVar, Literal

from anvil.api.actors.animation_controllers import (
    RPAnimationControllers,
    _ActorScripts,
    _RPAnimationController,
)
from anvil.api.actors.render_controller import RenderControllers, _RenderController
from anvil.api.core.core import SoundDefinition, SoundEvent
from anvil.api.logic.molang import Molang, Variable
from anvil.api.models.animations import _Animation
from anvil.api.models.geometry import Geometry
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.api.textures import ItemTexturesObject
from anvil.lib.blockbench import _Blockbench, _BlockBenchSource
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import ENTITY_CLIENT_VERSION
from anvil.lib.jsonmodel import (
    Hex,
    Identifier,
    JsonFile,
    JsonObject,
    NonNegative,
    json_field,
)
from anvil.lib.jsonmodel.enums import EntitySoundEvent, SoundCategory
from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.translator import AnvilTranslator

__all__ = ["EntityClient"]


# region Scripts


class _ActorClientScripts(_ActorScripts):
    """The `scripts` of a client description. Unset keys are left out."""

    pre_animation: list[str] = json_field(default_factory=list)
    initialize: list[str] = json_field(default_factory=list)
    parent_setup: str | None = None
    scale: float | str | None = None
    scalex: str | None = None
    scaley: str | None = None
    scalez: str | None = None
    should_update_bones_and_effects_offscreen: str | None = None
    should_update_effects_offscreen: str | None = None
    hide_held_items: str | None = None

    def add_pre_animation(self, expression: str) -> "_ActorClientScripts":
        """Adds Molang run before each animation update."""
        self.pre_animation.append(expression)
        return self

    def add_initialize(self, expression: str) -> "_ActorClientScripts":
        """Adds Molang run when the actor is created."""
        self.initialize.append(expression)
        return self

    def add_parent_setup(self, expression: str) -> "_ActorClientScripts":
        """Adds Molang setting variables of the parent, the actor holding this one."""
        self.parent_setup = (self.parent_setup or "") + expression
        return self

    def set_scale(self, scale: float | str) -> "_ActorClientScripts":
        """Sets the actor's scale."""
        self.scale = scale
        return self

    def set_scale_xyz(self, x: str, y: str, z: str) -> "_ActorClientScripts":
        """Sets the actor's scale on each axis."""
        self.scalex = x
        self.scaley = y
        self.scalez = z
        return self

    def set_should_update_bones_and_effects_offscreen(
        self, value: str
    ) -> "_ActorClientScripts":
        """Sets if the actor's bones and effects update while it is off screen."""
        self.should_update_bones_and_effects_offscreen = value
        return self

    def set_should_update_effects_offscreen(self, value: str) -> "_ActorClientScripts":
        """Sets if the actor's effects update while it is off screen."""
        self.should_update_effects_offscreen = value
        return self

    def set_hide_held_items(self, value: str) -> "_ActorClientScripts":
        """Hides the items the actor holds while the expression is not zero."""
        self.hide_held_items = value
        return self


# endregion


# region Actor Description


class _ActorAnimation(JsonObject):
    """A model animation the actor maps by its short name: one from a Blockbench model or
    built in code."""

    name: str = json_field(exclude=True, positional=True)
    identifier: str = json_field(exclude=True)
    animate: bool = json_field(default=False, exclude=True)
    """Runs all the time, or while `condition` is true."""
    condition: str | None = json_field(default=None, exclude=True)


class _ActorClientDescription(JsonObject, abstract=True):
    """The `description` of a client entity or attachable, and its builders. Unset keys
    are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)
    _type: ClassVar[Literal["entity", "attachable"]] = "entity"

    identifier: Identifier | None = None
    materials: dict[str, str] = json_field(
        default_factory=lambda: {"default": "entity_alphatest"}
    )
    textures: dict[str, str] = json_field(default_factory=dict)
    geometry: dict[str, str] = json_field(default_factory=dict)
    queryable_geometry: str | None = None
    particle_effects: dict[str, str] = json_field(default_factory=dict)
    sound_effects: dict[str, str] = json_field(default_factory=dict)
    animations: dict[str, str] = json_field(default_factory=dict)
    scripts: _ActorClientScripts = json_field(default_factory=_ActorClientScripts)
    render_controllers: list[str | dict[str, str | bool]] = json_field(
        default_factory=list
    )

    _animations: list[_ActorAnimation | _RPAnimationController] = json_field(
        default_factory=list, init=False, exclude=True
    )
    """The animations and controllers, in the order they were added."""
    _render_controllers: list[_RenderController] = json_field(
        default_factory=list, init=False, exclude=True
    )
    _is_dummy: bool = json_field(default=False, init=False, exclude=True)

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    @property
    def name(self) -> str:
        """The actor's name, without its namespace."""
        return self.identifier.name

    @property
    def _owner(self) -> Identifier:
        """The identifier the actor's controllers are named after: its name in the
        project's namespace, so a vanilla actor's controllers belong to the project."""
        return Identifier.parse(self.name)

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")
        for controller in self._animations:
            if not isinstance(controller, _RPAnimationController):
                continue
            for state in controller.states:
                for particle in state.particle_effects or []:
                    if particle.effect not in self.particle_effects:
                        raise ValueError(
                            f"Particle effect '{particle.effect}' is not defined in the "
                            f"Client Entity for Actor '{self.name}'."
                        )

    def animation_controller(
        self,
        controller_name: str,
        animate: bool = False,
        condition: str | Molang | None = None,
        initial_state: str | None = None,
    ) -> _RPAnimationController:
        """Returns the resource pack animation controller with this name, added on first
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
                if isinstance(c, _RPAnimationController) and c.name == controller_name
            ),
            None,
        )
        if controller is None:
            controller = _RPAnimationController(
                controller_name,
                owner=self._owner,
                initial_state=initial_state or "default",
            )
            self._animations.append(controller)
        elif initial_state is not None and initial_state != controller.initial_state:
            raise ValueError(
                f"Animation controller '{controller_name}' was added with initial state "
                f"'{controller.initial_state}'. Actor [{self.identifier}]"
            )
        if animate is True:
            controller._set_animate(condition)
        return controller

    def animation(
        self,
        blockbench: str | _Animation,
        animation_name: str | None = None,
        animate: bool = False,
        condition: str | Molang | None = None,
    ) -> "_ActorClientDescription":
        """Maps an animation's short name to an animation.

        Args:
            blockbench (str | Animation): The Blockbench model holding the animation, or an
                Animation built in code (then leave `animation_name` out; its name is the
                short name).
            animation_name (str, optional): The animation's name in the Blockbench model.
            animate (bool, optional): Runs it all the time. Defaults to False.
            condition (str | Molang, optional): When it runs, with `animate`.
        """
        if isinstance(blockbench, _Animation):
            if animation_name is not None:
                raise TypeError(
                    "Pass either an Animation, or a Blockbench model name and an animation "
                    "name, not both."
                )
            blockbench.file.queue(_BlockBenchSource.ACTOR)
            name, identifier = blockbench.name, blockbench.identifier
        elif animation_name is None:
            raise TypeError(
                "animation_name is required when referencing a Blockbench model."
            )
        else:
            bb = _Blockbench(blockbench, _BlockBenchSource.ACTOR)
            bb.animations.queue_animation(animation_name)
            name = animation_name
            identifier = f"animation.{CONFIG.NAMESPACE}.{blockbench}.{animation_name}"
        animation = _ActorAnimation(
            name,
            identifier=identifier,
            animate=animate,
            condition=None if condition is None else str(condition),
        )
        for index, entry in enumerate(self._animations):
            if isinstance(entry, _ActorAnimation) and entry.name == name:
                self._animations[index] = animation
                break
        else:
            self._animations.append(animation)
        return self

    def add_material(self, name: str, material: str) -> "_ActorClientDescription":
        """Maps a material's short name to a material.

        Args:
            name (str): The short name, `default` being the one render controllers use.
            material (str): The material, such as `entity_alphatest`.
        """
        self.materials[name] = material
        return self

    def add_geometry(
        self,
        geometry_name: str | Geometry,
        override_bounding_box: tuple[float, float] | None = None,
    ) -> "_ActorClientDescription":
        """Adds a geometry, by its short name.

        Args:
            geometry_name (str | Geometry): The Blockbench model, or a Geometry built in code
                (its name is the short name).
            override_bounding_box (tuple[float, float], optional): Replaces the model's
                visible bounds.
        """
        if isinstance(geometry_name, Geometry):
            geometry = geometry_name
            if override_bounding_box:
                geometry.set_visible_bounds(*override_bounding_box)
            geometry.queue(_BlockBenchSource.ACTOR)
            self.geometry[geometry.name] = geometry.geometry_identifier
            return self

        bb = _Blockbench(geometry_name, _BlockBenchSource.ACTOR)
        if override_bounding_box:
            bb.override_bounding_box(override_bounding_box)
        bb.model.queue_model()
        self.geometry[geometry_name] = f"geometry.{CONFIG.NAMESPACE}.{geometry_name}"
        return self

    def set_dummy(self) -> "_ActorClientDescription":
        """Marks the actor as having nothing to render: it needs no geometry, texture or
        render controller."""
        self._is_dummy = True
        return self

    def set_queryable_geometry(
        self, geometry_shortname: str
    ) -> "_ActorClientDescription":
        """Sets the geometry other actors can query.

        Args:
            geometry_shortname (str): The geometry's short name.
        """
        if geometry_shortname not in self.geometry:
            raise ValueError(
                f"Queryable geometry '{geometry_shortname}' not found in entity "
                f"{self.identifier}. Entity [{self.identifier}]"
            )
        self.queryable_geometry = geometry_shortname
        return self

    def add_texture(
        self, blockbench: str, component: TextureComponents
    ) -> "_ActorClientDescription":
        """Adds a texture of a Blockbench model, by its color texture's name.

        Args:
            blockbench (str): The Blockbench model.
            component (TextureComponents): The texture and its PBR layers.
        """
        bb = _Blockbench(blockbench, _BlockBenchSource.ACTOR)
        bb.textures.queue_texture(component.color)
        path = PurePosixPath(
            "textures",
            CONFIG.NAMESPACE,
            CONFIG.PROJECT_NAME,
            "actors",
            blockbench,
            component.color,
        )
        self.textures[component.color] = path.as_posix()

        if component.has_aux():
            texture_set = TextureSet(component.color, _BlockBenchSource.ACTOR)
            texture_set.set_blockbench_textures(blockbench, component)
            texture_set.queue()
        return self

    def add_script(
        self, variable: Variable | Molang, *script: Molang | str
    ) -> "_ActorClientDescription":
        """Sets a variable before each animation update.

        Args:
            variable (Variable | Molang): The variable.
            *script (Molang | str): The expressions, chained.
        """
        chained_scripts = "; ".join(map(str, script))
        self.scripts.add_pre_animation(
            f"{variable}={chained_scripts};".replace(";;", ";")
        )
        return self

    def add_parent_setup(
        self, variable: Variable | str, script: Molang | str
    ) -> "_ActorClientDescription":
        """Sets a variable of the parent, the actor holding this one."""
        self.scripts.add_parent_setup(f"{variable}={str(script)};".replace(";;", ";"))
        return self

    def init_vars(self, **vars) -> "_ActorClientDescription":
        """Initializes variables when the actor is created.

        Examples:
            >>> entity.client.description.init_vars(x=0, y=5, z=8)
        """
        for k, v in vars.items():
            Variable._set_var(k)
            self.scripts.add_initialize(f"v.{k}={v};")
        return self

    def set_scale(self, scale: Molang | str | float) -> "_ActorClientDescription":
        """Sets the actor's scale.

        Args:
            scale (Molang | str | float): The scale.
        """
        if not isinstance(scale, (str, Molang, int, float)):
            raise TypeError("Entity scale must be one of (str, Molang, int float).")
        self.scripts.set_scale(scale)
        return self

    def set_scale_xyz(
        self, x: Molang | str | float, y: Molang | str | float, z: Molang | str | float
    ) -> "_ActorClientDescription":
        """Sets the actor's scale on each axis."""
        self.scripts.set_scale_xyz(str(x), str(y), str(z))
        return self

    def set_should_update_bones_and_effects_offscreen(
        self, value: bool = True
    ) -> "_ActorClientDescription":
        """Sets if the actor's bones and effects update while it is off screen."""
        self.scripts.set_should_update_bones_and_effects_offscreen(str(int(value)))
        return self

    def set_should_update_effects_offscreen(
        self, value: bool = True
    ) -> "_ActorClientDescription":
        """Sets if the actor's effects update while it is off screen."""
        self.scripts.set_should_update_effects_offscreen(str(int(value)))
        return self

    def set_hide_held_items(
        self, expression: Molang | str | bool = True
    ) -> "_ActorClientDescription":
        """Hides the items the actor holds while the expression is not zero.

        Args:
            expression (Molang | str | bool, optional): The expression. Defaults to True.
        """
        value = (
            str(int(expression)) if isinstance(expression, bool) else str(expression)
        )
        self.scripts.set_hide_held_items(value)
        return self

    def render_controller(
        self, controller_name: str, condition: str | bool | None = None
    ) -> _RenderController:
        """Returns the render controller with this name, added on first use. The
        description lists it, with its condition.

        Args:
            controller_name (str): The controller's short name.
            condition (str | bool, optional): When it renders, Molang.
        """
        controller = next(
            (c for c in self._render_controllers if c.name == controller_name), None
        )
        if controller is None:
            controller = _RenderController(
                controller_name,
                owner=self._owner,
                actor_type=self._type,
                condition=condition,
            )
            self._render_controllers.append(controller)
        else:
            controller._set_condition(condition)
        return controller

    def particle_effect(
        self, particle: str, component: TextureComponents
    ) -> "_ActorClientDescription":
        """Adds a particle effect of the project, by its short name.

        Args:
            particle (str): The particle's name.
            component (TextureComponents): The particle's texture.
        """
        from anvil.api.world.particles import Particle

        self.particle_effects[particle] = f"{CONFIG.NAMESPACE}:{particle}"
        Particle(particle, component).queue()
        return self

    def sound_effect(
        self,
        sound: str,
        category: SoundCategory = SoundCategory.Neutral,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
    ):
        """Adds a sound effect of the project, by its short name, and returns its sound
        definition.

        Args:
            sound (str): The sound's name.
            category (SoundCategory, optional): Its category. Defaults to Neutral.
            max_distance (float, optional): The distance it is no longer heard at.
            min_distance (float, optional): The distance it starts to fade at.
            subtitle (str, optional): Its subtitle.
        """
        if not isinstance(category, SoundCategory):
            raise ValueError(
                f"Invalid sound category '{category}' for sound effect '{sound}' in entity "
                f"{self.identifier}. Entity [{self.identifier}]"
            )
        self.sound_effects[sound] = f"{CONFIG.NAMESPACE}:{sound}"

        key = f"subtitle.generic.{sound}"
        if subtitle is not None:
            AnvilTranslator().add_localization_entry(key, subtitle)

        return SoundDefinition().sound_reference(
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
        variant_query: Molang | None = None,
        variant_map: str | None = None,
        subtitle: str | None = None,
    ):
        """Plays a sound on one of the actor's sound events, and returns the sound event.

        Args:
            sound_reference (str): The sound's name.
            sound_event (EntitySoundEvent): The event.
            category (SoundCategory, optional): Its category. Defaults to Neutral.
            volume (float, optional): Its volume. Defaults to 1.0.
            pitch (tuple[float, float], optional): Its pitch range. Defaults to (0.8, 1.2).
            max_distance (float, optional): The distance it is no longer heard at.
            min_distance (float, optional): The distance it starts to fade at.
            variant_query (Molang, optional): The query picking a variant.
            variant_map (str, optional): The variant map.
            subtitle (str, optional): Its subtitle.
        """
        return SoundEvent().add_entity_event(
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

    def __prepare_export__(self, owner: JsonFile, *, root: bool = True) -> None:
        """Maps the animations and the controllers that have something to write, runs the
        animated ones, lists the render controllers, checks the description and queues
        the files it uses next to the owner's.

        Raises:
            ValueError: The actor has no geometry, texture or render controller.
        """
        self._animations = [
            entry
            for entry in self._animations
            if not (isinstance(entry, _RPAnimationController) and entry._is_empty())
        ]
        for entry in self._animations:
            self.animations[entry.name] = entry.identifier
            if entry.animate:
                self.scripts.add_animate(entry.name, entry.condition)
        self.render_controllers = [c.reference for c in self._render_controllers]
        RPAnimationControllers(self).queue(owner._directory)
        if not self._is_dummy:
            for kind, present in (
                ("geometry", self.geometry),
                ("texture", self.textures),
                ("render controller", self.render_controllers),
            ):
                if not present:
                    raise ValueError(
                        f"Entity {self.identifier} missing at least one {kind}. "
                        f"Entity [{self.identifier}]"
                    )
            for controller in self._render_controllers:
                controller._validate(
                    list(self.textures), list(self.geometry), list(self.materials)
                )
            RenderControllers(self).queue(owner._directory)


# endregion


# region Entity Description


class _SpawnEgg(JsonObject):
    """The spawn egg of an entity: a texture, or two colors written as `#rrggbb`. Unset keys
    are left out."""

    texture: str | None = None
    texture_index: Annotated[int, NonNegative] | None = None
    base_color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None
    ) = None
    overlay_color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, Hex] | None
    ) = None


class _EntityClientDescription(_ActorClientDescription):
    """The `description` of a client entity, and its builders. Unset keys are left out."""

    enable_attachables: bool | None = None
    held_item_ignores_lighting: bool | None = None
    hide_armor: bool | None = None
    held_item_scale: float | str | None = None
    spawn_egg: _SpawnEgg | None = None

    def set_enable_attachables(self, value: bool = True) -> "_EntityClientDescription":
        """Sets if the entity renders attachables, such as armor."""
        self.enable_attachables = value
        return self

    def set_held_item_ignores_lighting(
        self, value: bool = True
    ) -> "_EntityClientDescription":
        """Renders the held item at full brightness."""
        self.held_item_ignores_lighting = value
        return self

    def set_hide_armor(self, value: bool = True) -> "_EntityClientDescription":
        """Hides the entity's armor."""
        self.hide_armor = value
        return self

    def set_spawn_egg(
        self, texture: TextureComponents, texture_index: int | None = None
    ) -> "_EntityClientDescription":
        """Gives the spawn egg an item texture.

        Args:
            texture (TextureComponents): The texture.
            texture_index (int, optional): The texture's index. Left out unless given.
        """
        if texture is None:
            raise ValueError("TextureComponents must be provided")

        ItemTexturesObject().add_item(texture.color, [texture.color])
        texture_set = TextureSet(texture.color, _BlockBenchSource.ITEM)
        texture_set.set_item_textures(texture)
        texture_set.queue()

        self.spawn_egg = _SpawnEgg(
            texture=f"{CONFIG.NAMESPACE}:{texture.color}",
            texture_index=texture_index,
        )
        return self

    def set_spawn_egg_color(
        self,
        base_color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
        overlay_color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
    ) -> "_EntityClientDescription":
        """Colors the spawn egg. Any color format is written as `#rrggbb`.

        Args:
            base_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The base color,
                such as `#FFFFFF` or `(255, 255, 255)`.
            overlay_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The spots'
                color.
        """
        self.spawn_egg = _SpawnEgg(base_color=base_color, overlay_color=overlay_color)
        return self

    def set_held_item_scale(
        self, scale: Molang | str | float = 1
    ) -> "_EntityClientDescription":
        """Sets the scale of the held item.

        Args:
            scale (Molang | str | float, optional): The scale. Defaults to 1.
        """
        if scale != 1:
            self.held_item_scale = scale
        return self

    def __prepare_export__(self, owner: JsonFile, *, root: bool = True) -> None:
        super().__prepare_export__(owner)
        if self.spawn_egg is None and not self.identifier.is_vanilla:
            self.set_spawn_egg_color("#FFFFFF", "#000000")


# endregion


class _ClientEntity(JsonObject):
    """The `minecraft:client_entity` body."""

    description: _EntityClientDescription = json_field(
        default_factory=_EntityClientDescription
    )


class _ClientEntityFile(JsonObject):
    """The content of a `.entity.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:client_entity",
    )

    format_version: str = json_field(default=ENTITY_CLIENT_VERSION, init=False)
    client_entity: _ClientEntity = json_field(
        default_factory=_ClientEntity, key="minecraft:client_entity"
    )


class EntityClient(JsonFile):
    """A client entity: its geometry, textures, materials, animations and render
    controllers.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/cliententitydocumentation/cliententitydocumentationintroduction)
    """

    _document = _ClientEntityFile
    _extension = ".entity.json"
    _pack = Pack.RP
    _folder = "entity"
    _object_type = "Client Entity"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a client entity.

        Args:
            name (str): The entity's name.
            is_vanilla (bool, optional): If the entity is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _EntityClientDescription:
        """The description builders."""
        return self._content.client_entity.description

    def __export__(self) -> None:
        self.description.__prepare_export__(self)
        return super().__export__()
