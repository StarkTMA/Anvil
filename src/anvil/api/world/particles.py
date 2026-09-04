import json
import os

from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.config import CONFIG
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject


class Particle(AddonObject):
    _extension = ".particle.json"
    _path = os.path.join(CONFIG.RP_PATH, "particles")
    _object_type = "Particle"

    def __init__(
        self,
        particle: str,
        component: TextureComponents,
    ) -> None:
        """Create a particle with optional PBR texture set support.

        Args:
            particle (str): Name of the particle.
            component (TextureComponents): Texture components configuration for PBR.
        """
        super().__init__(particle)
        self._texture_set: TextureSet | None = None
        self._color_texture = component.color

        if not os.path.exists(
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
                != self._name
            ):
                raise ValueError(
                    f"Particle identifier mismatch: expected '{self._name}', got '{self._content['particle_effect']['description']['identifier']}'"
                )

        self._texture_set = TextureSet(self._color_texture, "particle")
        self._texture_set.set_particle_textures(component)

        self._content["particle_effect"]["description"]["basic_render_parameters"][
            "texture"
        ] = os.path.join(
            "textures",
            CONFIG.NAMESPACE,
            CONFIG.PROJECT_NAME,
            "particle",
            self._color_texture,
        )

        self._content["particle_effect"]["description"][
            "identifier"
        ] = f"{CONFIG.NAMESPACE}:{self._name}"

    def queue(self) -> "Particle":
        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue()

    def __export__(self) -> None:
        # Export texture set if configured
        if self._texture_set is not None:
            self._texture_set.queue()

        super().__export__()
