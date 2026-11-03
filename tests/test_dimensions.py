import jsonschema
import pytest

from anvil.api.core.enums import Dimension
from anvil.lib import config
from anvil.lib.config import ConfigPackageTarget
from anvil.lib.lib import AnvilIO


@pytest.fixture(autouse=True)
def world_project():
    with config.override(_TARGET=ConfigPackageTarget.WORLD):
        yield


def _exported(file):
    return AnvilIO._normalize_json_like(file._content)


def test_overworld_bounds():
    from anvil.api.world.dimensions import DimensionConfiguration

    overworld = DimensionConfiguration(Dimension.Overworld).height_bounds((-128, 256))
    assert _exported(overworld) == {
        "format_version": "1.18.0",
        "minecraft:dimension": {
            "description": {"identifier": "minecraft:overworld"},
            "components": {"minecraft:dimension_bounds": {"min": -128, "max": 256}},
        },
    }
    assert overworld.identifier.is_vanilla
    jsonschema.validate(_exported(overworld), DimensionConfiguration.__schema__())


def test_nether_is_void():
    from anvil.api.world.dimensions import DimensionConfiguration

    nether = DimensionConfiguration(Dimension.Nether)
    assert _exported(nether)["minecraft:dimension"]["components"] == {
        "minecraft:generation": {"generator_type": "void"}
    }
    with pytest.raises(ValueError, match="Only the Overworld"):
        nether.height_bounds((-64, 320))


@pytest.mark.parametrize("bounds", [(-127, 256), (256, -128), (-528, 256)])
def test_bad_bounds_raise_on_export(bounds):
    from anvil.api.world.dimensions import DimensionConfiguration

    overworld = DimensionConfiguration(Dimension.Overworld).height_bounds(bounds)
    with pytest.raises(ValueError):
        _exported(overworld)


def test_dimensions_refused_in_addons():
    from anvil.api.world.dimensions import DimensionConfiguration

    with config.override(_TARGET=ConfigPackageTarget.ADDON, NAMESPACE="test_t"):
        with pytest.raises(RuntimeError):
            DimensionConfiguration(Dimension.Overworld)
