import json
import os

from anvil import CONFIG
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject


class Particle(AddonObject):
    _extension = ".particle.json"
    _path = os.path.join(CONFIG.BP_PATH, "particles")

    def __init__(self, particle_name, use_vanilla_texture: bool = False):
        super().__init__(particle_name)
        self._name = particle_name
        self._use_vanilla_texture = use_vanilla_texture

        if not FileExists(os.path.join("assets", "particles", f"{self._name}.particle.json")):
            CONFIG.Logger.file_exist_error(f"{self._name}.particle.json", os.path.join("assets", "particles"))

        with open(os.path.join("assets", "particles", f"{self._name}.particle.json"), "r") as file:
            self._content = json.loads(file.read())
            if self._content["particle_effect"]["description"]["identifier"] != f"{CONFIG.NAMESPACE}:{self._name}":
                CONFIG.Logger.namespace_not_valid(self._content["particle_effect"]["description"]["identifier"])

    def queue(self):
        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue("particles")

    def _export(self):
        if not self._use_vanilla_texture:
            texture_path = self._content["particle_effect"]["description"]["basic_render_parameters"]["texture"]
            texture_name = texture_path.split("/")[-1]
            self._content["particle_effect"]["description"]["basic_render_parameters"]["texture"] = os.path.join(
                CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "particle", texture_name
            )

            if not FileExists(os.path.join("assets", "particles", f"{texture_name}.png")):
                CONFIG.Logger.file_exist_error(f"{texture_name}.png", os.path.join("assets", "particles"))

            CopyFiles(
                os.path.join("assets", "particles"),
                os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "particle"),
                f"{texture_name}.png",
            )

        CopyFiles(
            os.path.join("assets", "particles"),
            os.path.join(CONFIG.RP_PATH, "particles"),
            f"{self._name}.particle.json",
        )
