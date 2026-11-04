import jsonschema
import pytest

from anvil.lib import config
from anvil.lib.lib import AnvilIO


def _exported(file):
    return AnvilIO._normalize_json_like(file._content)


@pytest.fixture
def structures(tmp_path, monkeypatch):
    (tmp_path / "assets" / "structures" / "sub").mkdir(parents=True)
    (tmp_path / "assets" / "structures" / "house.mcstructure").touch()
    (tmp_path / "assets" / "structures" / "sub" / "tower.mcstructure").touch()
    monkeypatch.chdir(tmp_path)


def test_processor_list():
    from anvil.api.blocks.descriptor import BlockDescriptor
    from anvil.api.vanilla.blocks import MinecraftBlockTypes as Blocks
    from anvil.api.world.structures import _JigsawStructureProcess
    from anvil.lib.jsonmodel import Identifier

    processor = _JigsawStructureProcess("ruins")
    processor.add_block_ignore_processor([Blocks.Air(), "minecraft:stone"])
    capped = processor.add_capped_processor((2, 6))
    capped.add_block_rule().set_output_state(Blocks.Air())
    rule = processor.add_block_rule()
    rule.input_predicate.random_block_match(Blocks.Cobblestone(), 0.3)
    rule.location_predicate.block_state_match(
        BlockDescriptor(
            name=Identifier.parse("minecraft:oak_log", vanilla=True),
            states={"pillar_axis": "y"},
        )
    )
    rule.block_entity_modifier.append_loot("loot_tables/chest.json")
    rule.set_output_state(Blocks.MossyCobblestone())

    exported = _exported(processor)
    assert exported["minecraft:processor_list"] == {
        "description": {"identifier": f"{config.CONFIG.NAMESPACE}:ruins"},
        "processors": [
            {
                "processor_type": "minecraft:block_ignore",
                "blocks": ["minecraft:air", "minecraft:stone"],
            },
            {
                "processor_type": "minecraft:capped",
                "delegate": {
                    "processor_type": "minecraft:rule",
                    "rules": [{"output_state": "minecraft:air"}],
                },
                "limit": {"type": "uniform", "min_inclusive": 2, "max_inclusive": 6},
            },
            {
                "processor_type": "minecraft:rule",
                "rules": [
                    {
                        "input_predicate": {
                            "predicate_type": "minecraft:random_block_match",
                            "block": "minecraft:cobblestone",
                            "probability": 0.3,
                        },
                        "location_predicate": {
                            "predicate_type": "minecraft:blockstate_match",
                            "block_state": {
                                "name": "minecraft:oak_log",
                                "states": {"pillar_axis": "y"},
                            },
                        },
                        "output_state": "minecraft:mossy_cobblestone",
                        "block_entity_modifier": {
                            "type": "minecraft:append_loot",
                            "loot_table": "loot_tables/chest.json",
                        },
                    }
                ],
            },
        ],
    }
    jsonschema.validate(exported, _JigsawStructureProcess.__schema__())


def test_predicate_builder_replaces_the_previous_test():
    from anvil.api.world.structures import _JigsawStructureProcess

    rule = _JigsawStructureProcess("swap").add_block_rule()
    rule.input_predicate.random_block_match("minecraft:dirt", 0.5)
    rule.input_predicate.tag_match("stone")
    assert rule.input_predicate.__json__() == {
        "predicate_type": "minecraft:tag_match",
        "tag": "stone",
    }


@pytest.mark.parametrize(
    "build, message",
    [
        (lambda r: r.input_predicate.block_match("minecraft:dirt"), "output state"),
        (
            lambda r: (
                r.input_predicate.random_block_match("minecraft:dirt", 1.5),
                r.set_output_state("minecraft:air"),
            ),
            "must be from 0",
        ),
        (
            lambda r: (
                r.position_predicate.axis_aligned_linear_pos(0.5, 0.2, 0, 4, "x"),
                r.set_output_state("minecraft:air"),
            ),
            "greater than min_chance",
        ),
    ],
)
def test_invalid_rules_raise_on_export(build, message):
    from anvil.api.world.structures import _JigsawStructureProcess

    processor = _JigsawStructureProcess("invalid")
    build(processor.add_block_rule())
    with pytest.raises(ValueError, match=message):
        _exported(processor)


def test_capped_processor_takes_one_delegate():
    from anvil.api.world.structures import _JigsawStructureProcess

    capped = _JigsawStructureProcess("capped").add_capped_processor(3)
    capped.add_block_ignore_processor(["minecraft:air"])
    with pytest.raises(ValueError, match="single delegate"):
        capped.add_block_rule()


def test_template_pool_elements(structures):
    from anvil.api.features import AggregateFeature
    from anvil.api.world.structures import JigsawStructureTemplatePool

    pool = JigsawStructureTemplatePool("village", fallback="test_t:empty")
    processor = pool.add_structure_element("sub/tower", "village_processor", weight=3)
    pool.add_structure_element("house", projection="terrain_matching")
    pool.add_structure_element(AggregateFeature("flowers"))
    pool.add_structure_element(None, weight=2)

    namespace = config.CONFIG.NAMESPACE
    exported = _exported(pool)
    assert exported["minecraft:template_pool"]["elements"] == [
        {
            "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{namespace}/sub/tower",
                "processors": processor.identifier,
                "projection": "rigid",
            },
            "weight": 3,
        },
        {
            "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{namespace}/house",
                "projection": "terrain_matching",
            },
            "weight": 1,
        },
        {
            "element": {
                "element_type": "minecraft:feature_pool_element",
                "feature": f"{namespace}:flowers",
            },
            "weight": 1,
        },
        {"element": {"element_type": "minecraft:empty_pool_element"}, "weight": 2},
    ]
    assert exported["minecraft:template_pool"]["fallback"] == "test_t:empty"
    jsonschema.validate(exported, JigsawStructureTemplatePool.__schema__())


def test_structure_set_and_jigsaw(structures):
    from anvil.api.core.filters import Filter
    from anvil.api.world.structures import (
        JigsawStructureSet,
        JigsawStructureTemplatePool,
        _JigsawStructure,
    )

    pool = JigsawStructureTemplatePool("start")
    first = JigsawStructureSet(
        "ruins", separation=4, spacing=12, spread_type="triangular"
    )
    other = JigsawStructureSet("other", separation=2, spacing=10)
    jigsaw = first.add_jigsaw_structure(
        "ruin", pool, 3, (10, 4), "surface_structures", weight=2
    )
    jigsaw.add_biome_filters(Filter.has_biome_tag("beach")).dimension_padding(3, 4)
    jigsaw.max_distance_from_center(80).add_direct_pool_alias("a:x", "a:y")
    group = jigsaw.add_random_group_pool_alias().add_group(1)
    group.add_random_pool_alias("a:z").add_target("a:w", 2)

    assert other._structures == []
    namespace = config.CONFIG.NAMESPACE
    structure_set = _exported(first)["minecraft:structure_set"]
    assert structure_set["placement"]["spread_type"] == "triangular"
    assert structure_set["structures"] == [
        {"structure": f"{namespace}:ruin", "weight": 2}
    ]

    exported = _exported(jigsaw)
    body = exported["minecraft:jigsaw"]
    assert body["start_height"] == {
        "type": "uniform",
        "min": {"above_bottom": 4},
        "max": {"below_top": 10},
    }
    assert body["dimension_padding"] == {"bottom": 3, "top": 4}
    assert body["max_distance_from_center"] == {"horizontal": 80}
    assert body["pool_aliases"] == [
        {"type": "direct", "alias": "a:x", "target": "a:y"},
        {
            "type": "random_group",
            "groups": [
                {
                    "data": [
                        {
                            "type": "random",
                            "alias": "a:z",
                            "targets": [{"data": "a:w", "weight": 2}],
                        }
                    ],
                    "weight": 1,
                }
            ],
        },
    ]
    jsonschema.validate(exported, _JigsawStructure.__schema__())
    jsonschema.validate(_exported(first), JigsawStructureSet.__schema__())


@pytest.mark.parametrize(
    "build, message",
    [
        (
            lambda pool, s: s.add_jigsaw_structure("deep", pool, 25, 0, "lakes"),
            "from 0 to 20",
        ),
        (lambda pool, s: s, "less than half"),
    ],
)
def test_invalid_structures_raise_on_export(structures, build, message):
    from anvil.api.world.structures import (
        JigsawStructureSet,
        JigsawStructureTemplatePool,
    )

    pool = JigsawStructureTemplatePool("start")
    structure_set = JigsawStructureSet("bad", separation=6, spacing=12)
    with pytest.raises(ValueError, match=message):
        _exported(build(pool, structure_set))
