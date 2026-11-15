import orjson
import pytest

from anvil.api.biomes.components import (
    BiomeClimate,
    BiomeCreatureSpawnProbability,
    BiomeHumidity,
    BiomeMapTints,
    BiomeMountainParameters,
    BiomeMultiNoiseGenerationRules,
    BiomeNoiseGradient,
    BiomeOverworldGenerationRules,
    BiomeOverworldHeight,
    BiomePartiallyFrozen,
    BiomeReplaceBiomes,
    BiomeReplacement,
    BiomeSubSurfaceBuilder,
    BiomeSurfaceBuilder,
    BiomeSurfaceMaterialAdjustments,
    BiomeTags,
    BiomeVillageType,
    GrassTint,
    MesaSurface,
    NoiseBlockSpecifier,
    NoiseDescriptor,
    OverworldSurface,
    Surface,
)
from anvil.api.vanilla.biomes import MinecraftBiomeTypes
from anvil.lib.jsonmodel import ComponentPlacement, Identifier, JsonComponent
from anvil.lib.jsonmodel.enums import Dimension
from anvil.lib.lib import AnvilIO


@pytest.fixture(autouse=True)
def anvil_project(tmp_path, monkeypatch):
    """Block descriptors read the project config, so run each test in a minimal project."""
    (tmp_path / "anvilconfig.json").write_bytes(
        orjson.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    import anvil.lib.config as config

    config.use(None)


def test_new_biomes():
    assert MinecraftBiomeTypes.SulfurCaves == "minecraft:sulfur_caves"


def test_biome_components():
    sb = BiomeSurfaceBuilder()
    assert sb.identifier == "minecraft:surface_builder"

    ssb = BiomeSubSurfaceBuilder()
    assert ssb.identifier == "minecraft:subsurface_builder"

    ng = BiomeNoiseGradient()
    ng.set_type(builder_type="minecraft:noise_gradient")
    assert ng.type == "minecraft:noise_gradient"
    with pytest.raises(ValueError):
        _export(ng.set_type(builder_type="minecraft:not_a_builder"))

    stone = Identifier.parse("minecraft:stone", vanilla=True)
    ng.add_noise_block_specifier(
        specifier=NoiseBlockSpecifier(block=stone, range=(-0.5, 0.5))
    )
    assert len(ng.noise_block_specifiers) == 1
    assert _export(ng.noise_block_specifiers[0])["range"] == {"min": -0.5, "max": 0.5}
    with pytest.raises(ValueError):
        _export(NoiseBlockSpecifier(block=stone, range=(-1.5, 0.5)))


def test_noise_descriptor():
    nd = NoiseDescriptor(name="test_noise", first_octave=4, amplitudes=[1.0, 0.5, 0.25])
    assert _export(nd) == {
        "name": "test_noise",
        "first_octave": 4,
        "amplitudes": [1.0, 0.5, 0.25],
    }

    for bad in (
        NoiseDescriptor(name=123, first_octave=4, amplitudes=[1.0]),
        NoiseDescriptor(name="test", first_octave="4", amplitudes=[1.0]),
        NoiseDescriptor(name="test", first_octave=4, amplitudes=[]),
        NoiseDescriptor(name="test", first_octave=4, amplitudes=["not_a_number"]),
    ):
        with pytest.raises((TypeError, ValueError)):
            _export(bad)


def test_noise_block_specifier():
    stone = Identifier.parse("minecraft:stone", vanilla=True)
    dirt = Identifier.parse("minecraft:dirt", vanilla=True)

    assert _export(NoiseBlockSpecifier(block=stone, threshold=0.5)) == {
        "threshold": 0.5,
        "block": "minecraft:stone",
    }
    assert _export(
        NoiseBlockSpecifier(block=dirt, range=(-0.5, 0.5), noise="custom_noise")
    ) == {
        "noise": "custom_noise",
        "range": {"min": -0.5, "max": 0.5},
        "block": "minecraft:dirt",
    }

    for bad in (
        NoiseBlockSpecifier(block=stone, range=(-1.1, 0.9)),
        NoiseBlockSpecifier(block=stone, range=(0.1, 1.1)),
        NoiseBlockSpecifier(block=stone),
    ):
        with pytest.raises(ValueError):
            _export(bad)
    with pytest.raises(TypeError):
        NoiseBlockSpecifier(stone, threshold=0.5)


def test_biome_noise_gradient():
    nd = NoiseDescriptor(name="test_noise", first_octave=4, amplitudes=[1.0, 0.5, 0.25])
    stone = Identifier.parse("minecraft:stone", vanilla=True)
    dirt = Identifier.parse("minecraft:dirt", vanilla=True)
    nbs1 = NoiseBlockSpecifier(block=stone, threshold=0.5)
    nbs2 = NoiseBlockSpecifier(block=dirt, range=(0.1, 0.9), noise="custom_noise")

    ng = BiomeNoiseGradient()
    ng.set_noise_descriptor(noise_descriptor=nd)
    ng.set_noise_block_specifiers(specifiers=[nbs1, nbs2])
    ng.set_non_replaceable_blocks(blocks=[stone])

    serialized = AnvilIO._normalize_json_like(ng)
    assert serialized == {
        "minecraft:noise_gradient": {
            "noise_descriptor": {
                "name": "test_noise",
                "first_octave": 4,
                "amplitudes": [1.0, 0.5, 0.25],
            },
            "noise_block_specifiers": [
                {
                    "threshold": 0.5,
                    "block": "minecraft:stone",
                },
                {
                    "noise": "custom_noise",
                    "range": {"min": 0.1, "max": 0.9},
                    "block": "minecraft:dirt",
                },
            ],
            "non_replaceable_blocks": ["minecraft:stone"],
        }
    }

    ng2 = BiomeNoiseGradient()
    ng2.add_noise_block_specifier(specifier=nbs1).add_noise_block_specifier(
        specifier=nbs2
    )
    assert ng2.noise_block_specifiers == [nbs1, nbs2]
    with pytest.raises(TypeError):
        _export(
            BiomeNoiseGradient().add_noise_block_specifier(specifier="not a specifier")
        )

    assert AnvilIO._normalize_json_like(BiomeNoiseGradient()) == {
        "minecraft:noise_gradient": {}
    }


def test_surface_builder_noise_gradient():
    nd = NoiseDescriptor(name="test_noise", first_octave=4, amplitudes=[1.0, 0.5, 0.25])
    stone = Identifier.parse("minecraft:stone", vanilla=True)
    dirt = Identifier.parse("minecraft:dirt", vanilla=True)
    nbs1 = NoiseBlockSpecifier(block=stone, threshold=0.5)
    nbs2 = NoiseBlockSpecifier(block=dirt, range=(0.1, 0.9), noise="custom_noise")

    sb = BiomeSurfaceBuilder()
    sb.set_noise_gradient_builder(
        noise_descriptor=nd,
        noise_block_specifiers=[nbs1, nbs2],
        non_replaceable_blocks=[stone],
    )
    serialized_sb = AnvilIO._normalize_json_like(sb)
    assert serialized_sb == {
        "minecraft:surface_builder": {
            "builder": {
                "type": "minecraft:noise_gradient",
                "noise_descriptor": {
                    "name": "test_noise",
                    "first_octave": 4,
                    "amplitudes": [1.0, 0.5, 0.25],
                },
                "noise_block_specifiers": [
                    {
                        "threshold": 0.5,
                        "block": "minecraft:stone",
                    },
                    {
                        "noise": "custom_noise",
                        "range": {"min": 0.1, "max": 0.9},
                        "block": "minecraft:dirt",
                    },
                ],
                "non_replaceable_blocks": ["minecraft:stone"],
            }
        }
    }


def _export(component):
    return AnvilIO._normalize_json_like(component)


def _overworld_materials():
    return dict(
        foundation_material=Identifier.parse("minecraft:stone", vanilla=True),
        mid_material=Identifier.parse("minecraft:dirt", vanilla=True),
        sea_floor_material=Identifier.parse("minecraft:gravel", vanilla=True),
        sea_material=Identifier.parse("minecraft:water", vanilla=True),
        top_material=Identifier.parse("minecraft:grass_block", vanilla=True),
    )


ALL_BIOME_COMPONENTS = [
    BiomeSurfaceBuilder,
    BiomeSubSurfaceBuilder,
    BiomeClimate,
    BiomeCreatureSpawnProbability,
    BiomeHumidity,
    BiomeMapTints,
    BiomeMountainParameters,
    BiomeMultiNoiseGenerationRules,
    BiomeOverworldGenerationRules,
    BiomeOverworldHeight,
    BiomePartiallyFrozen,
    BiomeReplaceBiomes,
    BiomeSurfaceMaterialAdjustments,
    BiomeNoiseGradient,
    BiomeTags,
    BiomeVillageType,
]


@pytest.mark.parametrize("component", ALL_BIOME_COMPONENTS)
def test_biome_components_are_json_components(component):
    assert issubclass(component, JsonComponent)
    assert not hasattr(component, "format_version")
    assert component.identifier.startswith("minecraft:")
    assert component._placement == ComponentPlacement.ANY


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
@pytest.mark.parametrize("component", ALL_BIOME_COMPONENTS)
def test_biome_components_refuse_positional_arguments(component):
    with pytest.raises(TypeError):
        _export(component(1))


def test_surface_builder_overworld_variants():
    sb = BiomeSurfaceBuilder().set_overworld_builder(
        **_overworld_materials(), sea_floor_depth=7
    )
    assert isinstance(sb.builder, OverworldSurface)
    assert _export(sb) == {
        "minecraft:surface_builder": {
            "builder": {
                "type": "minecraft:overworld",
                "foundation_material": "minecraft:stone",
                "mid_material": "minecraft:dirt",
                "top_material": "minecraft:grass_block",
                "sea_floor_material": "minecraft:gravel",
                "sea_material": "minecraft:water",
                "sea_floor_depth": 7,
            }
        }
    }

    sb.set_frozen_ocean_builder(**_overworld_materials())
    assert _export(sb)["minecraft:surface_builder"]["builder"]["type"] == (
        "minecraft:frozen_ocean"
    )

    sb.set_swamp_builder(**_overworld_materials(), max_puddle_depth_below_sea_level=3)
    builder = _export(sb)["minecraft:surface_builder"]["builder"]
    assert builder["type"] == "minecraft:swamp"
    assert builder["max_puddle_depth_below_sea_level"] == 3

    sb.set_mesa_builder(
        **_overworld_materials(),
        clay_material=Identifier.parse("minecraft:clay", vanilla=True),
        hard_clay_material=Identifier.parse("minecraft:hardened_clay", vanilla=True),
        bryce_pillars=True,
    )
    assert isinstance(sb.builder, MesaSurface)
    builder = _export(sb)["minecraft:surface_builder"]["builder"]
    assert builder["type"] == "minecraft:mesa"
    assert builder["bryce_pillars"] is True
    assert "has_forest" not in builder


def test_surface_builder_validation():
    with pytest.raises(ValueError):
        _export(
            BiomeSurfaceBuilder().set_overworld_builder(
                **_overworld_materials(), sea_floor_depth=200
            )
        )
    materials = _overworld_materials()
    materials["top_material"] = "minecraft:grass_block"
    with pytest.raises(TypeError):
        _export(BiomeSurfaceBuilder().set_overworld_builder(**materials))
    with pytest.raises(TypeError):
        _export(BiomeSurfaceBuilder(builder={"type": "minecraft:the_end"}))
    with pytest.raises(TypeError, match="abstract"):
        _export(Surface())
    with pytest.raises(TypeError):
        _export(OverworldSurface(type="minecraft:mesa", **_overworld_materials()))


def test_surface_builder_capped_and_end():
    stone = Identifier.parse("minecraft:stone", vanilla=True)
    sb = BiomeSubSurfaceBuilder().set_capped_builder(
        beach_material=stone,
        ceiling_materials=[stone],
        floor_materials=[stone],
        foundation_material=stone,
        sea_material=Identifier.parse("minecraft:lava", vanilla=True),
    )
    builder = _export(sb)["minecraft:subsurface_builder"]["builder"]
    assert builder["type"] == "minecraft:capped"
    assert builder["ceiling_materials"] == ["minecraft:stone"]

    sb.set_end_builder()
    assert _export(sb) == {
        "minecraft:subsurface_builder": {"builder": {"type": "minecraft:the_end"}}
    }


def test_biome_climate():
    climate = BiomeClimate(
        temperature=0.8, downfall=0.4, snow_accumulation=[0.0, 0.125]
    )
    assert _export(climate) == {
        "minecraft:climate": {
            "temperature": 0.8,
            "downfall": 0.4,
            "snow_accumulation": [0.0, 0.125],
        }
    }
    assert _export(BiomeClimate()) == {"minecraft:climate": {}}
    with pytest.raises(ValueError):
        _export(BiomeClimate(temperature=51))
    with pytest.raises(ValueError):
        _export(BiomeClimate(downfall=1.5))
    with pytest.raises(ValueError):
        _export(BiomeClimate(snow_accumulation=[0.5]))
    with pytest.raises(ValueError):
        _export(BiomeClimate(snow_accumulation=[0.5, 2.0]))
    with pytest.raises(AttributeError, match="read-only"):
        climate.temperature = 1.0
    assert climate.temperature == 0.8


def test_biome_spawn_probability_and_humidity():
    assert _export(BiomeCreatureSpawnProbability(probability=0.1)) == {
        "minecraft:creature_spawn_probability": {"probability": 0.1}
    }
    with pytest.raises(ValueError):
        _export(BiomeCreatureSpawnProbability(probability=0.8))

    assert _export(BiomeHumidity(is_humid=False)) == {
        "minecraft:humidity": {"is_humid": False}
    }
    with pytest.raises(TypeError):
        _export(BiomeHumidity(is_humid=1))


def test_biome_map_tints_writes_hex_color():
    tints = BiomeMapTints(
        foliage=(1.0, 0.0, 0.0), grass=GrassTint(tint=(0.0, 1.0, 0.0))
    )
    exported = _export(tints)["minecraft:map_tints"]
    assert exported["foliage"].lower() == "#ff0000"
    assert exported["grass"]["tint"].lower() == "#00ff00"
    assert tints.foliage == (1.0, 0.0, 0.0)
    with pytest.raises(TypeError):
        _export(BiomeMapTints(grass={"tint": "#00ff00"}))


def test_biome_mountain_parameters_writes_material():
    stone = Identifier.parse("minecraft:stone", vanilla=True)
    mountain = (
        BiomeMountainParameters()
        .set_steep_material_adjustment(material=stone, north_slopes=True)
        .set_top_slide(enabled=False)
    )
    assert _export(mountain) == {
        "minecraft:mountain_parameters": {
            "steep_material_adjustment": {
                "material": "minecraft:stone",
                "north_slopes": True,
            },
            "top_slide": {"enabled": False},
        }
    }
    with pytest.raises(TypeError):
        _export(
            mountain.set_steep_material_adjustment(material=stone, east_slopes="yes")
        )
    with pytest.raises(TypeError):
        _export(mountain.set_top_slide(enabled="no"))


def test_deprecated_biome_components():
    with pytest.warns(DeprecationWarning):
        rules = BiomeMultiNoiseGenerationRules(target_temperature=0.5, weight=2)
    assert _export(rules) == {
        "minecraft:multinoise_generation_rules": {
            "target_temperature": 0.5,
            "weight": 2,
        }
    }
    with pytest.warns(DeprecationWarning):
        assert _export(BiomeOverworldGenerationRules()) == {
            "minecraft:overworld_generation_rules": {}
        }


def test_biome_overworld_height():
    with pytest.warns(DeprecationWarning):
        by_params = BiomeOverworldHeight(noise_params=(0.1, 0.2))
        by_type = BiomeOverworldHeight(noise_type="ocean")
        with pytest.raises(ValueError):
            _export(BiomeOverworldHeight(noise_params=(0.1, 0.2), noise_type="ocean"))
        with pytest.raises(ValueError):
            _export(BiomeOverworldHeight(noise_type="volcano"))
        with pytest.raises(ValueError):
            _export(BiomeOverworldHeight(noise_params=(0.1,)))
    assert _export(by_params) == {
        "minecraft:overworld_height": {"noise_params": [0.1, 0.2]}
    }
    assert _export(by_type) == {"minecraft:overworld_height": {"noise_type": "ocean"}}


def test_biome_replace_biomes():
    replace = BiomeReplaceBiomes()
    assert _export(replace) == {"minecraft:replace_biomes": {}}
    replace.add_replacement(
        targets=[MinecraftBiomeTypes.Plains], amount=0.5, noise_frequency_scale=2.0
    )
    assert isinstance(replace.replacements[0], BiomeReplacement)
    assert _export(replace) == {
        "minecraft:replace_biomes": {
            "replacements": [
                {
                    "targets": ["minecraft:plains"],
                    "amount": 0.5,
                    "noise_frequency_scale": 2.0,
                    "dimension": "minecraft:overworld",
                }
            ]
        }
    }
    with pytest.raises(ValueError):
        _export(
            BiomeReplaceBiomes().add_replacement(
                targets=[], amount=0.5, noise_frequency_scale=2.0
            )
        )
    with pytest.raises(ValueError):
        _export(
            BiomeReplaceBiomes().add_replacement(
                targets=["plains"], amount=0, noise_frequency_scale=2.0
            )
        )
    with pytest.raises(ValueError):
        _export(
            BiomeReplaceBiomes().add_replacement(
                targets=["plains"], amount=0.5, noise_frequency_scale=200
            )
        )
    with pytest.raises(ValueError):
        _export(
            BiomeReplaceBiomes().add_replacement(
                targets=["plains"],
                amount=0.5,
                noise_frequency_scale=2.0,
                dimension=Dimension.TheEnd,
            )
        )


def test_biome_surface_material_adjustments():
    adjustments = BiomeSurfaceMaterialAdjustments()
    assert _export(adjustments) == {"minecraft:surface_material_adjustments": {}}
    adjustments.add_adjustment(
        height_range=(0, 64),
        noise_range=(-0.5, 0.5),
        noise_frequency_scale=0.5,
        top_material=Identifier.parse("minecraft:sand", vanilla=True),
    )
    assert _export(adjustments) == {
        "minecraft:surface_material_adjustments": {
            "adjustments": [
                {
                    "height_range": [0, 64],
                    "noise_frequency_scale": 0.5,
                    "noise_range": [-0.5, 0.5],
                    "materials": {"top_material": "minecraft:sand"},
                }
            ]
        }
    }
    with pytest.raises(ValueError):
        _export(
            BiomeSurfaceMaterialAdjustments().add_adjustment(height_range=(0, 64, 128))
        )
    with pytest.raises(TypeError):
        _export(
            BiomeSurfaceMaterialAdjustments().add_adjustment(
                top_material="minecraft:sand"
            )
        )


def test_biome_tags_and_village_type():
    assert _export(BiomeTags(tags=["forest", "rare"])) == {
        "minecraft:tags": {"tags": ["forest", "rare"]}
    }
    with pytest.raises(TypeError):
        _export(BiomeTags(tags=["forest", 3]))

    assert _export(BiomeVillageType(type="desert")) == {
        "minecraft:village_type": {"type": "desert"}
    }
    with pytest.raises(ValueError):
        _export(BiomeVillageType(type="jungle"))
    with pytest.raises(TypeError):
        _export(BiomeVillageType())
    with pytest.raises(TypeError):
        _export(BiomeVillageType("desert"))


def test_builder_fields_are_read_only():
    sb = BiomeSurfaceBuilder().set_end_builder()
    with pytest.raises(AttributeError, match="read-only"):
        sb.builder = None
    with pytest.raises(AttributeError, match="read-only"):
        sb.builder.type = "minecraft:mesa"
    replace = BiomeReplaceBiomes().add_replacement(
        targets=["plains"], amount=0.5, noise_frequency_scale=2.0
    )
    with pytest.raises(AttributeError, match="read-only"):
        replace.replacements[0].amount = 0.9


def test_biome_partially_frozen_is_an_empty_marker():
    assert _export(BiomePartiallyFrozen()) == {"minecraft:partially_frozen": {}}


def test_biome_overworld_generation_rules_fields():
    with pytest.warns(DeprecationWarning):
        rules = BiomeOverworldGenerationRules(
            generate_for_climates=[("medium", 1), ("warm", 2)],
            hills_transformation="minecraft:forest_hills",
            mutate_transformation=[("minecraft:flower_forest", 1)],
        )
    assert _export(rules) == {
        "minecraft:overworld_generation_rules": {
            "generate_for_climates": [["medium", 1], ["warm", 2]],
            "hills_transformation": "minecraft:forest_hills",
            "mutate_transformation": [["minecraft:flower_forest", 1]],
        }
    }
    with pytest.warns(DeprecationWarning), pytest.raises(ValueError):
        _export(BiomeOverworldGenerationRules(generate_for_climates=[("medium",)]))


def test_replacement_allows_nether_and_height_range_allows_molang():
    replace = BiomeReplaceBiomes().add_replacement(
        targets=["basalt_deltas"],
        amount=0.3,
        noise_frequency_scale=1.0,
        dimension=Dimension.Nether,
    )
    assert (
        _export(replace)["minecraft:replace_biomes"]["replacements"][0]["dimension"]
        == "minecraft:nether"
    )
    with pytest.raises(ValueError):
        _export(
            BiomeReplaceBiomes().add_replacement(
                targets=["plains"],
                amount=0.3,
                noise_frequency_scale=1.0,
                dimension=Dimension.TheEnd,
            )
        )

    adjustments = BiomeSurfaceMaterialAdjustments().add_adjustment(
        height_range=("variable.sea_level", 120),
        top_material=Identifier.parse("minecraft:sand", vanilla=True),
    )
    assert _export(adjustments)["minecraft:surface_material_adjustments"][
        "adjustments"
    ][0]["height_range"] == ["variable.sea_level", 120]


def test_client_biome_components():
    from anvil.api.biomes.components import (
        BiomeClientFogAppearance,
        BiomeClientFoliageAppearance,
        BiomeClientGrassAppearance,
        BiomeClientMusic,
        BiomeClientPrecipitation,
        BiomeClientSkyColor,
        BiomeClientWaterAppearance,
    )

    assert _export(BiomeClientSkyColor(sky_color=(1.0, 0.0, 0.0))) == {
        "minecraft:sky_color": {"sky_color": "#ff0000"}
    }
    assert _export(BiomeClientWaterAppearance(surface_color="#62529e")) == {
        "minecraft:water_appearance": {"surface_color": "#62529e"}
    }
    assert _export(BiomeClientFoliageAppearance(color="birch")) == {
        "minecraft:foliage_appearance": {"color": {"color_map": "birch"}}
    }
    assert _export(BiomeClientGrassAppearance(color="#00ff00")) == {
        "minecraft:grass_appearance": {"color": "#00ff00"}
    }
    assert _export(
        BiomeClientFogAppearance(fog_identifier="minecraft:fog_the_end")
    ) == {"minecraft:fog_appearance": {"fog_identifier": "minecraft:fog_the_end"}}
    with pytest.raises(ValueError):
        _export(BiomeClientWaterAppearance(surface_opacity=1.5))
    with pytest.raises(ValueError):
        _export(BiomeClientMusic(volume_multiplier=2))
    with pytest.raises(ValueError, match="at most one"):
        _export(BiomeClientPrecipitation(ash=0.1, white_ash=0.2))


def test_biome_client_builders_and_components_mix():
    from anvil.api.biomes.client import BiomeClient
    from anvil.api.biomes.components import (
        BiomeClientFogAppearance,
        BiomeClientSkyColor,
        BiomeClientWaterAppearance,
    )

    client = BiomeClient("test_biome")
    client.sky_color("#ff0000").water_appearance("#62529e")
    client.components.add(
        BiomeClientFogAppearance(fog_identifier="minecraft:fog_the_end")
    )

    assert client.components.has(BiomeClientSkyColor)
    assert client.components.has(BiomeClientFogAppearance)
    water = next(
        c for c in client.components if isinstance(c, BiomeClientWaterAppearance)
    )
    assert water.surface_opacity == 0.8


def _check_file(file):
    jsonschema = pytest.importorskip("jsonschema")
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._document)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


@pytest.fixture
def no_write(monkeypatch):
    """Exports files without writing them."""
    monkeypatch.setattr("anvil.lib.jsonmodel.file.AnvilIO.file", lambda *a, **k: None)


def test_biome_sides_refuse_the_other_sides_components(no_write):
    from anvil.api.biomes.client import BiomeClient
    from anvil.api.biomes.components import BiomeClientSkyColor
    from anvil.api.biomes.server import BiomeServer

    server = BiomeServer("test_biome")
    server.components.add(BiomeClientSkyColor(sky_color="#ff0000"))
    with pytest.raises(ValueError, match="client biome component"):
        server.__export__()

    client = BiomeClient("test_biome")
    client.components.add(BiomeHumidity(is_humid=True))
    with pytest.raises(ValueError, match="server biome component"):
        client.__export__()


def test_biome_server_file():
    from anvil.api.biomes.server import BiomeServer

    server = BiomeServer("test_biome")
    server.components.add(BiomeClimate(temperature=0.8, downfall=0.4))
    server.components.add(BiomeTags(tags=["custom", "overworld"]))
    assert server.identifier == "test:test_biome"
    assert _check_file(server) == {
        "format_version": server._document.format_version,
        "minecraft:biome": {
            "description": {"identifier": "test:test_biome"},
            "components": {
                "minecraft:climate": {"temperature": 0.8, "downfall": 0.4},
                "minecraft:tags": {"tags": ["custom", "overworld"]},
            },
        },
    }
    assert BiomeServer.__schema__()["x-anvil-file"] == {
        "pack": "behavior_pack",
        "folder": "biomes",
        "extension": ".biome.json",
    }


def test_biome_client_file():
    from anvil.api.biomes.client import BiomeClient

    client = BiomeClient("test_biome")
    client.sky_color("#80a0ff").grass_appearance("swamp_grass").precipitation(ash=0.5)
    assert _check_file(client) == {
        "format_version": client._document.format_version,
        "minecraft:client_biome": {
            "description": {"identifier": "test:test_biome"},
            "components": {
                "minecraft:sky_color": {"sky_color": "#80a0ff"},
                "minecraft:grass_appearance": {"color": {"color_map": "swamp_grass"}},
                "minecraft:precipitation": {"ash": 0.5},
            },
        },
    }
    assert BiomeClient.__schema__()["x-anvil-file"]["pack"] == "resource_pack"


def test_biome_files_are_empty_by_default():
    """Empty components are left out, as the file shortener always dropped them."""
    from anvil.api.biomes.client import BiomeClient
    from anvil.api.biomes.server import BiomeServer

    assert _check_file(BiomeServer("plains", True))["minecraft:biome"] == {
        "description": {"identifier": "minecraft:plains"}
    }
    assert _check_file(BiomeClient("plains", True))["minecraft:client_biome"] == {
        "description": {"identifier": "minecraft:plains"}
    }


def test_biome_object(monkeypatch):
    from anvil.api.biomes.biomes import Biome
    from anvil.api.biomes.client import BiomeClient
    from anvil.api.biomes.server import BiomeServer
    from anvil.lib import config

    biome = Biome("mushroom_caves")
    assert biome.identifier == "test:mushroom_caves"
    assert biome.name == "mushroom_caves"
    assert str(biome) == "test:mushroom_caves"
    assert biome._server is None and biome._client is None

    assert isinstance(biome.server, BiomeServer)
    assert biome.server is biome.server
    assert biome.server.identifier == "test:mushroom_caves"
    assert biome.server.description.identifier == "test:mushroom_caves"
    assert biome._client is None

    queued = []
    monkeypatch.setattr(
        BiomeServer, "queue", lambda self, directory=None: queued.append(self)
    )
    monkeypatch.setattr(
        BiomeClient, "queue", lambda self, directory=None: queued.append(self)
    )
    assert biome.queue() is biome
    assert queued == [biome._server]

    vanilla = Biome(MinecraftBiomeTypes.Plains, True)
    assert vanilla.identifier == "minecraft:plains"
    assert isinstance(vanilla.client, BiomeClient)
    assert vanilla.client.identifier.is_vanilla
    with config.override(_TARGET="addon", NAMESPACE="test_t"):
        with pytest.raises(ValueError, match="partial overrides"):
            Biome(MinecraftBiomeTypes.Plains, True)
