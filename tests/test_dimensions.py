import jsonschema
import pytest

from anvil.api.biomes.components import BiomeClimate
from anvil.api.dimension import (
    DimensionClouds,
    DimensionConfiguration,
    DimensionDefaultBiome,
    DimensionHeight,
)
from anvil.lib import config
from anvil.lib.config import ConfigPackageTarget
from anvil.lib.jsonmodel.enums import Dimension
from anvil.lib.lib import AnvilIO


@pytest.fixture(autouse=True)
def world_project():
    with config.override(_TARGET=ConfigPackageTarget.WORLD):
        yield


def _exported(file):
    return AnvilIO._normalize_json_like(file._document)


def test_overworld_components():
    overworld = DimensionConfiguration(Dimension.Overworld)
    overworld.components.add(
        DimensionHeight(min_y=-64, height_range=384),
        DimensionDefaultBiome(biome="minecraft:plains"),
        DimensionClouds(height=192),
    )
    assert _exported(overworld) == {
        "format_version": "1.26.50",
        "minecraft:dimension": {
            "description": {"identifier": "minecraft:overworld"},
            "components": {
                "minecraft:dimension_height": {"min_y": -64, "height_range": 384},
                "minecraft:default_biome": {"biome": "minecraft:plains"},
                "minecraft:clouds": {"height": 192},
            },
        },
    }
    assert overworld.identifier.is_vanilla
    jsonschema.validate(_exported(overworld), DimensionConfiguration.__schema__())


def test_nether_is_void():
    nether = DimensionConfiguration(Dimension.Nether)
    assert _exported(nether)["minecraft:dimension"]["components"] == {
        "minecraft:generation": {"generator_type": "void"}
    }


@pytest.mark.parametrize(
    "component",
    [
        lambda: DimensionHeight(min_y=-64, height_range=100),
        lambda: DimensionHeight(min_y=-64, height_range=2048),
        lambda: DimensionHeight(min_y=-600, height_range=384),
        lambda: DimensionClouds(height=600),
    ],
)
def test_bad_components_raise_on_export(component):
    with pytest.raises(ValueError):
        AnvilIO._normalize_json_like(component())


def test_only_dimension_components():
    overworld = DimensionConfiguration(Dimension.Overworld)
    overworld.components.add(BiomeClimate(temperature=1))
    with pytest.raises(ValueError, match="not a dimension component"):
        overworld.__export__()


def test_dimensions_refused_in_addons():
    with config.override(_TARGET=ConfigPackageTarget.ADDON, NAMESPACE="test_t"):
        with pytest.raises(ValueError):
            DimensionConfiguration(Dimension.Overworld)
