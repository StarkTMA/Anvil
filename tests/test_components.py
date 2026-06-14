import sys
from unittest.mock import MagicMock

# Set up mock config to avoid exit(1) during class definition imports
mock_config = MagicMock()
mock_config.BP_PATH = "dummy_bp_path"
mock_config.RP_PATH = "dummy_rp_path"

import anvil.lib.config
anvil.lib.config.CONFIG = mock_config

import pytest
from anvil.api.actors.components import EntityProjectile

def test_entity_projectile_defaults():
    proj = EntityProjectile()
    # Check default structure. By default, fields equal to defaults aren't added to the serialized dict.
    assert proj._component == {"on_hit": {}}

def test_entity_projectile_new_properties():
    proj = EntityProjectile(
        hit_nearest_passenger=True,
        ignored_entities=["minecraft:player", "minecraft:cow"],
        isolated_physics=False,
        owner_launch_immunity_ticks=10,
        reflect_immunity=2.5,
    )
    comp = proj._component
    assert comp["hit_nearest_passenger"] is True
    assert comp["ignored_entities"] == ["minecraft:player", "minecraft:cow"]
    assert comp["isolated_physics"] is False
    assert comp["owner_launch_immunity_ticks"] == 10
    assert comp["reflect_immunity"] == 2.5
