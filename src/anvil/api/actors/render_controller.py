"""The resource pack's `render_controllers/<actor>.rc.json`: what an entity or attachable
renders, its geometry, materials and textures."""

from collections.abc import Sequence
from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Literal

from anvil.api.logic.molang import Molang
from anvil.lib.config import Pack
from anvil.lib.format_versions import RENDER_CONTROLLER_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    JsonValue,
    Keyed,
    json_field,
)

if TYPE_CHECKING:
    from anvil.api.actors.client import _ActorClientDescription


# region Parts


class _RenderArray(JsonValue):
    """An array of references, `Array.<name>`, picked from by a Molang index."""

    name: str = json_field(exclude=True, positional=True)
    items: list[str] = json_field(default_factory=list, positional=True)


class _RenderArrays(JsonObject):
    """The arrays of a render controller. Unset keys are left out."""

    textures: Annotated[list[_RenderArray], Keyed("name")] | None = None
    geometries: Annotated[list[_RenderArray], Keyed("name")] | None = None
    materials: Annotated[list[_RenderArray], Keyed("name")] | None = None

    def add(
        self, kind: Literal["textures", "geometries", "materials"], array: _RenderArray
    ) -> None:
        """Adds an array, replacing one with the same name."""
        current = [a for a in getattr(self, kind) or [] if a.name != array.name]
        setattr(self, kind, current + [array])


class _BoneValue(JsonValue):
    """A value for the bones matching `bone`, written as `{bone: value}`."""

    bone: str = json_field(exclude=True, positional=True)
    value: str | bool | float = json_field(positional=True)

    def __json__(self) -> Any:
        return {self.bone: self.value}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": "object",
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": {"type": ["string", "boolean", "number"]},
        }


class _RenderColor(JsonObject):
    """A color, each channel a number from 0 to 1 or Molang."""

    r: float | str = json_field()
    g: float | str = json_field()
    b: float | str = json_field()
    a: float | str = json_field()


class _UVAnim(JsonObject):
    """The texture offset and scale, each channel a number or Molang."""

    offset: tuple[float | str, float | str] = json_field()
    scale: tuple[float | str, float | str] = json_field()


# endregion


# region Controller


class _RenderController(JsonObject):
    """A render controller of an entity or attachable, `controller.render.<actor>.<name>`.
    The actor's client description lists it, with its condition when it has one.

    Its builders refer to the textures, geometries and materials of the actor's client
    description by short name. Unset keys are left out; with no material, every bone uses
    the `default` material.
    """

    name: str = json_field(exclude=True, positional=True)
    owner: Identifier = json_field(exclude=True)
    """The actor identifier."""
    actor_type: Literal["entity", "attachable"] = json_field(
        default="entity", exclude=True
    )
    condition: str | bool | None = json_field(default=None, exclude=True)
    """When the actor's client description renders the controller, Molang."""

    arrays: _RenderArrays | None = None
    geometry: str | None = None
    materials: list[_BoneValue] | None = None
    textures: list[str] | None = None
    part_visibility: list[_BoneValue] | None = None
    color: _RenderColor | None = None
    overlay_color: _RenderColor | None = None
    on_fire_color: _RenderColor | None = None
    is_hurt_color: _RenderColor | None = None
    filter_lighting: bool | None = None
    ignore_lighting: bool | None = None
    light_color_multiplier: float | str | None = None
    uv_anim: _UVAnim | None = None

    @property
    def identifier(self) -> str:
        """The controller's identifier, `controller.render.<namespace>.<actor>.<name>`."""
        return f"controller.render.{self.owner.replace(':', '.')}.{self.name}"

    @property
    def reference(self) -> str | dict[str, str | bool]:
        """How the client description lists the controller: its identifier, or
        `{identifier: condition}`."""
        if self.condition is None:
            return self.identifier
        return {self.identifier: self.condition}

    def _set_condition(self, condition: str | bool | None) -> None:
        if condition is not None:
            self.condition = condition

    def _array(
        self,
        kind: Literal["textures", "geometries", "materials"],
        name: str,
        items: list[str],
    ) -> Molang:
        variable = Molang().__query__("array", name)
        if self.arrays is None:
            self.arrays = _RenderArrays()
        self.arrays.add(kind, _RenderArray(str(variable), items))
        return variable

    def material(self, bone: str, material_shortname: str) -> "_RenderController":
        """Adds the material of the bones matching `bone`. A later entry overrides an
        earlier one.

        Args:
            bone (str): The bone name, `*` being a wildcard: `*`, `TailA`, `*Saddle*`.
            material_shortname (str): The material's short name in the client description,
                or Molang, such as an array indexed by a query.
        """
        value = (
            material_shortname
            if isinstance(material_shortname, Molang)
            else Molang().__query__("material", material_shortname)
        )
        self.materials = (self.materials or []) + [_BoneValue(bone, value)]
        return self

    def texture_array(
        self,
        array_name: str,
        textures_short_names: Sequence[str],
        query: Molang | str | None = None,
    ) -> "_RenderController":
        """Adds an array of textures. With a query, also adds the texture it picks.

        Args:
            array_name (str): The array name.
            textures_short_names (Sequence[str]): The textures' short names.
            query (Molang | str, optional): The index into the array.
        """
        variable = self._array(
            "textures", array_name, [f"Texture.{t}" for t in textures_short_names]
        )
        if query is not None:
            self.textures = (self.textures or []) + [variable[query]]
        return self

    def geometry_array(
        self,
        array_name: str,
        geometries_short_names: Sequence[str],
        query: Molang | str | None = None,
    ) -> "_RenderController":
        """Adds an array of geometries. With a query, also sets the geometry it picks.

        Args:
            array_name (str): The array name.
            geometries_short_names (Sequence[str]): The geometries' short names.
            query (Molang | str, optional): The index into the array.
        """
        variable = self._array(
            "geometries",
            array_name,
            [f"Geometry.{g}" for g in geometries_short_names],
        )
        if query is not None:
            self.geometry = variable[query]
        return self

    def material_array(
        self,
        array_name: str,
        materials_short_names: Sequence[str],
        bone: str | None = None,
        query: Molang | str | None = None,
    ) -> "_RenderController":
        """Adds an array of materials. With a bone and a query, also adds the material it
        picks for the bone.

        Args:
            array_name (str): The array name.
            materials_short_names (Sequence[str]): The materials' short names.
            bone (str, optional): The bones the picked material is for.
            query (Molang | str, optional): The index into the array.
        """
        variable = self._array(
            "materials",
            array_name,
            [str(Molang().__query__("material", m)) for m in materials_short_names],
        )
        if bone is not None and query is not None:
            self.material(bone, variable[query])
        return self

    def set_geometry(self, short_name: str) -> "_RenderController":
        """Sets the geometry.

        Args:
            short_name (str): The geometry's short name, or an array reference
                (`Array.<name>[...]`).
        """
        self.geometry = (
            short_name if "Array" in short_name else f"Geometry.{short_name}"
        )
        return self

    def add_texture(self, short_name: str) -> "_RenderController":
        """Adds a texture layer.

        Args:
            short_name (str): The texture's short name, or a reference starting with
                `Texture.` or `Array.`.
        """
        if not any(prefix in short_name for prefix in ("Texture.", "Array.")):
            short_name = f"Texture.{short_name}"
        self.textures = (self.textures or []) + [short_name]
        return self

    def add_part_visibility(
        self, bone: str, condition: Molang | str | bool
    ) -> "_RenderController":
        """Shows or hides the bones matching `bone`. A later entry overrides an earlier one.

        Args:
            bone (str): The bone name, `*` being a wildcard.
            condition (Molang | str | bool): Shown when true.
        """
        self.part_visibility = (self.part_visibility or []) + [
            _BoneValue(bone, condition)
        ]
        return self

    def set_color(self, a, r, g, b) -> "_RenderController":
        """Sets the tint color, each channel 0 to 1 or Molang."""
        self.color = _RenderColor(r=r, g=g, b=b, a=a)
        return self

    def set_overlay_color(self, a, r, g, b) -> "_RenderController":
        """Sets the overlay color, each channel 0 to 1 or Molang."""
        self.overlay_color = _RenderColor(r=r, g=g, b=b, a=a)
        return self

    def set_on_fire_color(self, a, r, g, b) -> "_RenderController":
        """Sets the color while on fire, each channel 0 to 1 or Molang."""
        self.on_fire_color = _RenderColor(r=r, g=g, b=b, a=a)
        return self

    def set_is_hurt_color(self, a, r, g, b) -> "_RenderController":
        """Sets the color while hurt, each channel 0 to 1 or Molang."""
        self.is_hurt_color = _RenderColor(r=r, g=g, b=b, a=a)
        return self

    def set_filter_lighting(self, enabled: bool = True) -> "_RenderController":
        """Sets if the lighting is filtered."""
        self.filter_lighting = enabled
        return self

    def set_ignore_lighting(self, enabled: bool = True) -> "_RenderController":
        """Sets if the lighting is ignored, so the actor renders at full brightness."""
        self.ignore_lighting = enabled
        return self

    def set_light_color_multiplier(
        self, multiplier: float | str
    ) -> "_RenderController":
        """Sets the multiplier of the light color."""
        self.light_color_multiplier = multiplier
        return self

    def set_uv_anim(
        self,
        offset: tuple[float | Molang | str, float | Molang | str],
        scale: tuple[float | Molang | str, float | Molang | str],
    ) -> "_RenderController":
        """Animates the texture by offset and scale. Entities only.

        Args:
            offset (tuple): The (u, v) offset.
            scale (tuple): The (u, v) scale.
        """
        if self.actor_type == "attachable":
            raise ValueError(
                "UV Animation is not supported for attachables. Error in render controller "
                f"[{self.identifier}]"
            )
        self.uv_anim = _UVAnim(offset=tuple(offset), scale=tuple(scale))
        return self

    def _validate(
        self,
        textures: Sequence[str],
        geometries: Sequence[str],
        materials: Sequence[str],
    ) -> None:
        """Checks the references against the client description's short names."""

        def check(reference: str, kind: str, names: Sequence[str]) -> None:
            if reference.lower().startswith(f"{kind}.") and (
                reference.split(".")[-1] not in names
            ):
                raise ValueError(
                    f"{kind.capitalize()} {reference} not found in actor {self.owner}. "
                    f"Render controller [{self.identifier}]"
                )

        arrays = self.arrays or _RenderArrays()
        for texture in self.textures or []:
            check(texture, "texture", textures)
        for array in arrays.textures or []:
            for texture in array.items:
                check(texture, "texture", textures)
        if self.geometry is not None:
            check(self.geometry, "geometry", geometries)
        for array in arrays.geometries or []:
            for geometry in array.items:
                check(geometry, "geometry", geometries)
        for material in self.materials or []:
            check(str(material.value), "material", materials)
        for array in arrays.materials or []:
            for material in array.items:
                check(material, "material", materials)

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        if "materials" not in payload:
            payload["materials"] = [
                _BoneValue("*", Molang().__query__("material", "default"))
            ]
        return payload


# endregion


# region File


class _RenderControllersFile(JsonObject):
    """The content of a `.rc.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "render_controllers")

    format_version: str = json_field(default=RENDER_CONTROLLER_VERSION, init=False)
    render_controllers: Annotated[list[_RenderController], Keyed("identifier")] = (
        json_field(default_factory=list)
    )


class RenderControllers(JsonFile):
    """The render controllers of an entity or attachable, built at export from its client
    description, which holds them (`render_controller()` adds them).

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/animations/animationrendercontroller)
    """

    _document = _RenderControllersFile
    _extension = ".rc.json"
    _pack = Pack.RP
    _folder = "render_controllers"
    _object_type = "Render Controller"

    def __init__(self, source: "_ActorClientDescription") -> None:
        """Creates the render controllers file of an actor, at export.

        Args:
            source (_ActorClientDescription): The actor's client description, which holds
                the render controllers.
        """
        super().__init__(source.name)
        self._source = source

    def queue(self, directory: str = "") -> "RenderControllers | None":
        """Queues the render controllers for export, when the actor has any."""
        self._content = self._document(
            render_controllers=list(self._source._render_controllers)
        )
        if self._content.render_controllers:
            return super().queue(directory=directory)
        return None


# endregion
