import json
import os

from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.config import CONFIG
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject


class ParticlesNotRegisteredError(RuntimeError):
    pass


class ParticleNotFoundError(FileNotFoundError):
    def __init__(self, particle_name: str):
        super().__init__(
            f"Could not fine '{particle_name}.particle.json' in 'assets/particles'. {Particle._object_type}[{particle_name}]"
        )


class ParticleReferencedNotFoundError(FileNotFoundError):
    def __init__(self, source_name: str, reference_name: str):
        super().__init__(
            f"Could not fine '{reference_name}.particle.json', referenced by {source_name}. {Particle._object_type}[{source_name}]"
        )


class ParticleNameMismatch(ParticlesNotRegisteredError):
    def __init__(self, particle_name: str, found_id: str):
        super().__init__(f"Expected '{particle_name}', found '{found_id}'")


class Particle(AddonObject):
    _non_queued_particles: set[str] = set()
    _queued_particles: set[str] = set()
    _extension = ".particle.json"
    _path = os.path.join(CONFIG.RP_PATH, "particles")
    _object_type = "Particle"

    def _check_event_particles(self):
        events: dict = self._content["particle_effect"].get("events", None)
        if not events:
            return

        for event in events.values():
            component = event.get("particle_effect", None)

            if not component:
                continue

            id: str = component.get("effect")
            if id.startswith("minecraft:"):
                continue

            name = id.split(":")[-1]
            target_path = os.path.join("assets", "particles", f"{name}.particle.json")
            self._check_reference_file_exists(target_path, name)

            if not name in Particle._queued_particles:
                Particle._non_queued_particles.add(name)

            event["particle_effect"]["effect"] = f"{CONFIG.NAMESPACE}:{name}"

    def _check_file_exists(self, source_path, particle_name):
        if not os.path.exists(source_path):
            raise ParticleNotFoundError(particle_name)

    def _check_reference_file_exists(self, source_path, reference_name):
        if not os.path.exists(source_path):
            raise ParticleReferencedNotFoundError(self._name, reference_name)

    def _load_file_content(self, source_path):
        with open(source_path, "r") as file:
            self._content = json.loads(file.read())

    def _set_particle_id_texture(self, texture_name: str):
        texture_path = os.path.join(
            "textures",
            CONFIG.NAMESPACE,
            CONFIG.PROJECT_NAME,
            "particle",
            texture_name,
        )
        self._content["particle_effect"]["description"]["basic_render_parameters"][
            "texture"
        ] = texture_path

        self._content["particle_effect"]["description"][
            "identifier"
        ] = f"{CONFIG.NAMESPACE}:{self.name}"

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
        source_path = os.path.join("assets", "particles", f"{particle}.particle.json")
        self._check_file_exists(source_path, particle)

        super().__init__(particle)
        self._load_file_content(source_path)

        source_id = self._content["particle_effect"]["description"]["identifier"]
        if source_id != particle:
            raise ParticleNameMismatch(particle, source_id)

        self._texture_set = TextureSet(component.color, "particle")
        self._texture_set.set_particle_textures(component)

        self._set_particle_id_texture(component.color)
        self._check_event_particles()

    def queue(self) -> "Particle":
        if self.name in Particle._non_queued_particles:
            Particle._non_queued_particles.remove(self.name)
        Particle._queued_particles.add(self.name)

        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue()

    def __export__(self) -> None:
        if self._texture_set is not None:
            self._texture_set.queue()

        super().__export__()

    def __check_errors__():
        if len(Particle._non_queued_particles) == 0:
            return

        raise ParticlesNotRegisteredError(
            f"The following particles were referenced in particle events but were never queued. [{" ".join(Particle._non_queued_particles)}]"
        )
