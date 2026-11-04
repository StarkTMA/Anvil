"""Tests for particles read into their typed document."""

import orjson
import pytest
from PIL import Image

from anvil.api.world.particles import Particle, _ParticleDocument
from anvil.lib import config
from anvil.lib.jsonmodel import JsonFile
from anvil.lib.lib import AnvilIO

_SMOKE = {
    "format_version": "1.10.0",
    "particle_effect": {
        "description": {
            "identifier": "smoke",
            "basic_render_parameters": {
                "material": "particles_alpha",
                "texture": "textures/particle/particles",
            },
        },
        "curves": {
            "variable.fade": {
                "type": "linear",
                "input": "v.particle_age",
                "horizontal_range": "v.particle_lifetime",
                "nodes": [1, 0],
            }
        },
        "events": {
            "puff": {"particle_effect": {"effect": "spark", "type": "particle"}},
            "boom": {"sound_effect": {"event_name": "random.explode"}},
        },
        "components": {
            "minecraft:emitter_rate_instant": {"num_particles": 8},
            "minecraft:emitter_lifetime_once": {"active_time": 1},
            "minecraft:emitter_shape_sphere": {"radius": 0.5, "direction": "outwards"},
            "minecraft:particle_initial_speed": "math.random(1, 2)",
            "minecraft:particle_lifetime_expression": {"max_lifetime": 2},
            "minecraft:particle_lifetime_events": {"expiration_event": "puff"},
            "minecraft:particle_appearance_billboard": {
                "size": [0.2, "v.fade * 0.2"],
                "facing_camera_mode": "lookat_xyz",
                "uv": {"texture_width": 128, "texture_height": 128, "uv": [0, 0]},
            },
            "minecraft:particle_appearance_tinting": {
                "color": {"gradient": {"0.0": "#ffffffff"}, "interpolant": "v.fade"}
            },
            "minecraft:particle_appearance_lighting": {},
        },
    },
}


def test_particle_document_round_trips():
    document = _ParticleDocument.__from_json__(_SMOKE)
    components = document.particle_effect.components
    assert components.emitter_rate_instant.num_particles == 8
    assert components.particle_appearance_billboard.size == (0.2, "v.fade * 0.2")
    assert AnvilIO._normalize_json_like(document) == _SMOKE


@pytest.fixture
def particles(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Particle, "_queued_particles", set())
    monkeypatch.setattr(Particle, "_non_queued_particles", set())
    folder = tmp_path / "assets" / "particles"
    folder.mkdir(parents=True)
    Image.new("RGBA", (16, 16)).save(folder / "smoke.png")

    def write(name, content):
        (folder / f"{name}.particle.json").write_bytes(orjson.dumps(content))

    return write


def test_particle_reads_its_file_and_renames_references(particles):
    from anvil.api.pbr.texture_set import TextureComponents

    spark = orjson.loads(orjson.dumps(_SMOKE))
    spark["particle_effect"]["description"]["identifier"] = "spark"
    del spark["particle_effect"]["events"]
    particles("smoke", _SMOKE)
    particles("spark", spark)

    with config.override(NAMESPACE="testns"):
        smoke = Particle("smoke", TextureComponents(color="smoke"))
        exported = AnvilIO._normalize_json_like(smoke._content)
    effect = exported["particle_effect"]
    assert effect["description"]["identifier"] == "testns:smoke"
    assert effect["description"]["basic_render_parameters"]["texture"] == (
        "textures/testns/test/particle/smoke"
    )
    assert effect["events"]["puff"]["particle_effect"]["effect"] == "testns:spark"
    assert Particle._non_queued_particles == {"spark"}
    assert isinstance(smoke, JsonFile)


def test_particle_refuses_an_unknown_component(particles):
    from anvil.api.pbr.texture_set import TextureComponents

    broken = orjson.loads(orjson.dumps(_SMOKE))
    broken["particle_effect"]["components"]["minecraft:emitter_rate_magic"] = {}
    particles("smoke", broken)
    with pytest.raises(ValueError, match="minecraft:emitter_rate_magic"):
        Particle("smoke", TextureComponents(color="smoke"))
