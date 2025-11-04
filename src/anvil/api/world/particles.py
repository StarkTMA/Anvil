import json
import os

from anvil.lib.config import CONFIG
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject


class Particle(AddonObject):
    _extension = ".particle.json"
    _path = os.path.join(CONFIG.RP_PATH, "particles")
    _object_type = "Particle"

    def __init__(self, particle_name, use_vanilla_texture: bool = False):
        super().__init__(particle_name)
        self._use_vanilla_texture = use_vanilla_texture

        if not FileExists(
            os.path.join("assets", "particles", f"{self._name}.particle.json")
        ):
            raise FileNotFoundError(
                f"Particle file '{self._name}.particle.json' does not exist in 'assets/particles'. {self._object_type}[{self._name}]"
            )

        with open(
            os.path.join("assets", "particles", f"{self._name}.particle.json"), "r"
        ) as file:
            self._content = json.loads(file.read())
            if (
                self._content["particle_effect"]["description"]["identifier"]
                != f"{CONFIG.NAMESPACE}:{self._name}"
            ):
                raise ValueError(
                    f"Particle identifier mismatch: expected '{CONFIG.NAMESPACE}:{self._name}', got '{self._content['particle_effect']['description']['identifier']}'"
                )

    def queue(self):
        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue()

    def _export(self):
        if not self._use_vanilla_texture:
            texture_path = self._content["particle_effect"]["description"][
                "basic_render_parameters"
            ]["texture"]
            texture_name = texture_path.split("/")[-1]

            if not FileExists(
                os.path.join("assets", "particles", f"{texture_name}.png")
            ):
                raise FileNotFoundError(
                    f"Texture file '{texture_name}.png' does not exist in 'assets/particles'. {self._object_type}[{self._name}]"
                )

            self._content["particle_effect"]["description"]["basic_render_parameters"][
                "texture"
            ] = os.path.join(
                "textures",
                CONFIG.NAMESPACE,
                CONFIG.PROJECT_NAME,
                "particle",
                texture_name,
            )

            CopyFiles(
                os.path.join("assets", "particles"),
                os.path.join(
                    CONFIG.RP_PATH,
                    "textures",
                    CONFIG.NAMESPACE,
                    CONFIG.PROJECT_NAME,
                    "particle",
                ),
                f"{texture_name}.png",
            )
        super()._export()
