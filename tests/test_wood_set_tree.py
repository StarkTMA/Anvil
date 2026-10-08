from unittest.mock import MagicMock
import pytest
import anvil.lib.config

mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"
mock_config.NAMESPACE = "test"
mock_config.PROJECT_NAME = "test"
anvil.lib.config.CONFIG = mock_config

from anvil.api.blocks import components as block_components
from anvil.api.core.core import ANVIL
from anvil.api.features import WeightedRandomFeature
from anvil.kit.blocks.wood_set import WoodBlock, create_wood_set
from anvil.kit.blocks.wood_set.blocks import sapling


@pytest.fixture(autouse=True)
def mock_material(monkeypatch):
    monkeypatch.setattr(
        block_components.BlockMaterialInstance, "add_instance", lambda self, spec: self
    )
    monkeypatch.setattr(
        "anvil.api.core.textures.ItemTexturesObject.add_item",
        lambda self, *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "anvil.api.pbr.texture_set.TextureSet.set_item_textures",
        lambda self, *args, **kwargs: None,
    )


def _tree_of(block) -> str:
    components = block.server.components.__export__()["components"]
    (params,) = [v for k, v in components.items() if k.endswith(":wood_set_sapling")]
    return params["tree_feature"]


def test_sapling_grows_the_tree_it_is_given():
    ANVIL._objects_list.clear()
    feature = WeightedRandomFeature("my_tree")
    block = sapling.create("rotten", {"log", "leaves", "sapling"}, feature)
    assert _tree_of(block) == feature.identifier

    # An identifier works too
    block = sapling.create("rotten", {"log", "leaves", "sapling"}, "test:other_tree")
    assert _tree_of(block) == "test:other_tree"


def test_the_kit_makes_no_trees_of_its_own():
    ANVIL._objects_list.clear()
    sapling.create("rotten", {"log", "leaves", "sapling"}, "test:my_tree")
    queued = [
        o
        for o in ANVIL._objects_list
        if getattr(o, "_object_type", None) in ("Feature", "Feature Rule")
    ]
    assert queued == []


def test_wood_set_with_saplings_requires_a_tree():
    ANVIL._objects_list.clear()
    with pytest.raises(ValueError, match="tree"):
        create_wood_set("rotten")
    with pytest.raises(ValueError, match="tree"):
        create_wood_set("rotten", WoodBlock.DOOR)
