import os
from typing import Literal

from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


class _RenderController:
    def _validate(
        self, textures: list[str], geometries: list[str], materials: list[str]
    ):
        controller = self._controller[self.controller_identifier]
        controller_textures = controller.get("textures", [])
        controller_arrays = controller.get("arrays", {}).get("textures", {})

        def log_invalid_texture(texture):
            texture_ext = texture.split(".")[-1]
            if texture_ext not in textures:
                raise RuntimeError(
                    f"Texture {texture} not found in entity {self._identifier}. Render controller [{self._identifier}]"
                )

        for texture in controller_textures:
            if texture.startswith("Texture."):
                log_invalid_texture(texture)

        for array in controller_arrays:
            for texture in controller_arrays.get(array.split("[")[0], []):
                log_invalid_texture(texture)

        for geometry in self._controller[self.controller_identifier]["geometry"]:
            if (
                geometry.startswith("Geometry.")
                and geometry.split(".")[-1] not in geometries
            ):
                raise RuntimeError(
                    f"Geometry {geometry} not found in entity {self._identifier}. Render controller [{self._identifier}]"
                )
            elif (
                geometry.startswith("Array.")
                and geometry.split(".")[-1]
                not in self._controller[self.controller_identifier]["arrays"][
                    "geometries"
                ][geometry]
            ):
                raise RuntimeError(
                    f"Geometry {geometry} not found in entity {self._identifier}. [{self._identifier}]"
                )

        for material in self._controller[self.controller_identifier]["materials"]:
            if list(material.values())[0].split(".")[-1] not in materials:
                raise RuntimeError(
                    f"Material {list(material.values())[0]} not found in entity {self._identifier}. Render controller [{self._identifier}]"
                )

    def __init__(self, identifier, controller_name):
        self._identifier = identifier
        self._controller_name = controller_name
        self._controller = JsonSchemes.render_controller(
            self._identifier, self._controller_name
        )
        self.controller_identifier = f"controller.render.{self._identifier.replace(':', '.')}.{self._controller_name}"

    def texture_array(self, array_name: str, *textures_short_names: str):
        self._controller[self.controller_identifier]["arrays"]["textures"].update(
            {
                f"Array.{array_name}": [
                    f"Texture.{texture}" for texture in textures_short_names
                ]
            }
        )
        return self

    def material(self, bone: Literal["*"] | str, material_shortname: str):
        self._controller[self.controller_identifier]["materials"].append(
            {
                bone: (
                    material_shortname
                    if material_shortname.startswith(("v", "q"))
                    else f"Material.{material_shortname}"
                )
            }
        )
        return self

    def geometry_array(self, array_name: str, *geometries_short_names: str):
        self._controller[self.controller_identifier]["arrays"]["geometries"].update(
            {
                f"Array.{array_name}": [
                    f"Geometry.{geometry}" for geometry in geometries_short_names
                ]
            }
        )
        return self

    def geometry(self, short_name):
        if "Array" not in short_name:
            name = f"Geometry.{short_name}"
        else:
            name = short_name
        self._controller[self.controller_identifier]["geometry"] = name
        return self

    def textures(self, short_name):
        if "Array" not in short_name:
            name = f"Texture.{short_name}"
        else:
            name = short_name

        self._controller[self.controller_identifier]["textures"].append(name)
        return self

    def part_visibility(self, bone: str, condition: str | bool):
        self._controller[self.controller_identifier]["part_visibility"].append(
            {bone: condition}
        )
        return self

    def overlay_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update(
            {"overlay_color": {"a": a, "r": r, "g": g, "b": b}}
        )
        return self

    def on_fire_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update(
            {"on_fire_color": {"a": a, "r": r, "g": g, "b": b}}
        )
        return self

    def is_hurt_color(self, a, r, g, b):
        self._controller[self.controller_identifier].update(
            {"is_hurt_color": {"a": a, "r": r, "g": g, "b": b}}
        )
        return self

    def color(self, a, r, g, b):
        self._controller[self.controller_identifier].update(
            {"color": {"a": a, "r": r, "g": g, "b": b}}
        )
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
        self._controller[self.controller_identifier][
            "light_color_multiplier"
        ] = multiplier
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
    _object_type = "Render Controller"

    def __init__(self, identifier: str) -> None:
        self._controllers: list[_RenderController] = []
        self.render_controller = JsonSchemes.render_controllers()
        super().__init__(identifier)

    def add_controller(self, controller_name: str):
        self._render_controller = _RenderController(self.identifier, controller_name)
        self._controllers.append(self._render_controller)
        return self._render_controller

    def queue(self, directory: str = ""):
        if len(self._controllers) > 0:
            for controller in self._controllers:
                self.render_controller["render_controllers"].update(controller._export)
            self.content(self.render_controller)
            return super().queue(directory=directory)
