"""Builds `anvil.api.vanilla` from scratch out of the vanilla metadata in Mojang's
bedrock-samples repository, at a release tag chosen by hand.

```
python tools/update_vanilla.py v1.26.50.4
```

The whole module is deleted and rewritten on every run. Mojang's metadata has no tags
or potion types, so those lists are kept by hand below.

Releases: https://github.com/Mojang/bedrock-samples/tags
"""

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.request import urlopen

METADATA_URL = "https://raw.githubusercontent.com/Mojang/bedrock-samples/{tag}/metadata/vanilladata_modules/mojang-{name}.json"
VANILLA = Path(__file__).resolve().parent.parent / "src" / "anvil" / "api" / "vanilla"

ITEM_TAGS = [
    "minecraft:arrow",
    "minecraft:banner",
    "minecraft:boat",
    "minecraft:boats",
    "minecraft:bookshelf_books",
    "minecraft:chainmail_tier",
    "minecraft:coals",
    "minecraft:copper_tier",
    "minecraft:crimson_stems",
    "minecraft:decorated_pot_sherds",
    "minecraft:diamond_tier",
    "minecraft:digger",
    "minecraft:door",
    "minecraft:golden_tier",
    "minecraft:hanging_actor",
    "minecraft:hanging_sign",
    "minecraft:horse_armor",
    "minecraft:iron_tier",
    "minecraft:is_armor",
    "minecraft:is_axe",
    "minecraft:is_cooked",
    "minecraft:is_fish",
    "minecraft:is_food",
    "minecraft:is_hoe",
    "minecraft:is_meat",
    "minecraft:is_minecart",
    "minecraft:is_pickaxe",
    "minecraft:is_shovel",
    "minecraft:is_sword",
    "minecraft:is_tool",
    "minecraft:is_trident",
    "minecraft:leather_tier",
    "minecraft:lectern_books",
    "minecraft:leaves",
    "minecraft:logs",
    "minecraft:logs_that_burn",
    "minecraft:mangrove_logs",
    "minecraft:music_disc",
    "minecraft:netherite_tier",
    "minecraft:planks",
    "minecraft:sand",
    "minecraft:sign",
    "minecraft:soul_fire_base_blocks",
    "minecraft:spawn_egg",
    "minecraft:stone_bricks",
    "minecraft:stone_crafting_materials",
    "minecraft:stone_tier",
    "minecraft:stone_tool_materials",
    "minecraft:transform_materials",
    "minecraft:transform_templates",
    "minecraft:transformable_items",
    "minecraft:trim_templates",
    "minecraft:trimmable_armors",
    "minecraft:vibration_damper",
    "minecraft:warped_stems",
    "minecraft:wooden_slabs",
    "minecraft:wooden_tier",
    "minecraft:wool",
    "minecraft:egg",
    "minecraft:chest_boat",
    "minecraft:harness",
    "minecraft:is_shears",
    "minecraft:is_spear",
    "minecraft:metal_nuggets",
    "minecraft:nautilus_armor",
    "minecraft:piglin_loved",
    "minecraft:piglin_repellents",
    "minecraft:trim_materials",
    "minecraft:sulfur_cube_archetype_explosive",
    "minecraft:sulfur_cube_archetype_bouncy",
    "minecraft:sulfur_cube_archetype_regular",
    "minecraft:sulfur_cube_archetype_slow_flat",
    "minecraft:sulfur_cube_archetype_fast_flat",
    "minecraft:sulfur_cube_archetype_light",
    "minecraft:sulfur_cube_archetype_fast_sliding",
    "minecraft:sulfur_cube_archetype_slow_sliding",
    "minecraft:sulfur_cube_archetype_sticky",
    "minecraft:sulfur_cube_archetype_high_resistance",
]

BLOCK_TAGS = [
    "wood",
    "log",
    "oak",
    "spruce",
    "birch",
    "jungle",
    "acacia",
    "dark_oak",
    "trapdoors",
    "one_way_collidable",
    "pumpkin",
    "plant",
    "stone",
    "metal",
    "diamond_pick_diggable",
    "gold_pick_diggable",
    "iron_pick_diggable",
    "stone_pick_diggable",
    "wood_pick_diggable",
    "dirt",
    "sand",
    "gravel",
    "grass",
    "snow",
    "rail",
    "water",
    "mob_spawner",
    "lush_plants_replaceable",
    "azalea_log_replaceable",
    "not_feature_replaceable",
    "text_sign",
    "minecraft:crop",
    "fertilize_area",
    "minecraft:leaves",
    "minecraft:cornerable_stairs",
    "minecraft:has_fence_connections",
    "minecraft:diamond_tier_destructible",
    "minecraft:iron_tier_destructible",
    "minecraft:is_axe_item_destructible",
    "minecraft:is_hatchet_item_destructible",
    "minecraft:is_item_tier_destructible",
    "minecraft:is_hoe_item_destructible",
    "minecraft:is_mace_item_destructible",
    "minecraft:is_pickaxe_item_destructible",
    "minecraft:is_shears_item_destructible",
    "minecraft:is_shovel_item_destructible",
    "minecraft:is_sword_item_destructible",
    "minecraft:netherite_tier_destructible",
    "minecraft:stone_tier_destructible",
]

BIOME_TAGS = [
    "animal",
    "basalt_deltas",
    "beach",
    "bee_habitat",
    "birch",
    "caves",
    "cherry_grove",
    "cold",
    "crimson_forest",
    "dark_oak",
    "deep",
    "deep_dark",
    "desert",
    "dripstone_caves",
    "edge",
    "extreme_hills",
    "fast_fishing",
    "flower_forest",
    "forest",
    "frozen",
    "frozen_peaks",
    "grove",
    "high_seas",
    "hills",
    "ice",
    "ice_plains",
    "jagged_peaks",
    "jungle",
    "lakes",
    "lukewarm",
    "lush_caves",
    "mangrove_swamp",
    "mega",
    "mesa",
    "monster",
    "mooshroom_island",
    "mountain",
    "mutated",
    "nether",
    "nether_wastes",
    "netherwart_forest",
    "no_legacy_worldgen",
    "ocean",
    "overworld",
    "overworld_generation",
    "plains",
    "plateau",
    "rare",
    "river",
    "roofed",
    "savanna",
    "shore",
    "slime",
    "snowy_slopes",
    "soulsand_valley",
    "spawn_endermen",
    "spawn_few_piglins",
    "spawn_few_zombified_piglins",
    "spawn_ghast",
    "spawn_magma_cubes",
    "spawn_many_magma_cubes",
    "spawn_piglin",
    "spawn_zombified_piglin",
    "stone",
    "surface_mineshaft",
    "swamp",
    "swamp_water_huge_mushroom",
    "taiga",
    "the_end",
    "warm",
    "warped_forest",
]

POTION_EFFECT_TYPES = [
    "minecraft:awkward",
    "minecraft:fire_resistance",
    "minecraft:harming",
    "minecraft:healing",
    "minecraft:infested",
    "minecraft:invisibility",
    "minecraft:leaping",
    "minecraft:long_fire_resistance",
    "minecraft:long_invisibility",
    "minecraft:long_leaping",
    "minecraft:long_mundane",
    "minecraft:long_nightvision",
    "minecraft:long_poison",
    "minecraft:long_regeneration",
    "minecraft:long_slow_falling",
    "minecraft:long_slowness",
    "minecraft:long_strength",
    "minecraft:long_swiftness",
    "minecraft:long_turtle_master",
    "minecraft:long_water_breathing",
    "minecraft:long_weakness",
    "minecraft:mundane",
    "minecraft:nightvision",
    "minecraft:oozing",
    "minecraft:poison",
    "minecraft:regeneration",
    "minecraft:slow_falling",
    "minecraft:slowness",
    "minecraft:strength",
    "minecraft:strong_harming",
    "minecraft:strong_healing",
    "minecraft:strong_leaping",
    "minecraft:strong_poison",
    "minecraft:strong_regeneration",
    "minecraft:strong_slowness",
    "minecraft:strong_strength",
    "minecraft:strong_swiftness",
    "minecraft:strong_turtle_master",
    "minecraft:swiftness",
    "minecraft:thick",
    "minecraft:turtle_master",
    "minecraft:water",
    "minecraft:water_breathing",
    "minecraft:weakness",
    "minecraft:weaving",
    "minecraft:wind_charged",
    "minecraft:wither",
]

POTION_LIQUID_TYPES = ["Consume", "ThrownLingering", "ThrownSplash"]

POTION_TYPES = [
    "water",
    "awkward",
    "mundane",
    "thick",
    "healing",
    "regeneration",
    "swiftness",
    "strength",
    "harming",
    "poison",
    "slowness",
    "weakness",
    "water_breathing",
    "fire_resistance",
    "nightvision",
    "invisibility",
    "leaping",
    "slow_falling",
    "turtle_master",
    "wither",
    "strong_healing",
    "strong_harming",
    "long_leaping",
    "strong_leaping",
    "long_nightvision",
    "long_poison",
    "strong_poison",
    "long_regeneration",
    "strong_regeneration",
    "long_slowness",
    "strong_slowness",
    "long_strength",
    "strong_strength",
    "long_swiftness",
    "strong_swiftness",
    "long_turtle_master",
    "strong_turtle_master",
    "long_water_breathing",
    "long_fire_resistance",
    "long_invisibility",
    "long_slow_falling",
    "long_weakness",
    "strong_wither",
]

SNAKE = """def _to_snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\\1_\\2", s)
    s = re.sub(r"([a-z\\d])([A-Z])", r"\\1_\\2", s)
    s = re.sub(r"([a-zA-Z])(\\d+)", r"\\1_\\2", s)
    return s.lower()
"""


def fetch(tag: str, name: str) -> list[dict]:
    with urlopen(METADATA_URL.format(tag=tag, name=name)) as response:
        return json.load(response)["data_items"]


def pascal(identifier: str) -> str:
    return "".join(
        part[:1].upper() + part[1:] for part in identifier.split(":")[-1].split("_")
    )


def snake(name: str) -> str:
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    name = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", name)
    name = re.sub(r"([a-zA-Z])(\d+)", r"\1_\2", name)
    return name.lower()


def keyword(state: str) -> str:
    return state.replace(":", "_")


def literal(values: list) -> str:
    return f"Literal[{', '.join(json.dumps(value) for value in values)}]"


def state_type(state: dict) -> str:
    values = [value["value"] for value in state["values"]]
    if state["type"] == "bool":
        return "bool"
    return literal(sorted(values) if state["type"] == "int" else values)


def enum(name: str, doc: str, values: list[str] | dict[str, str]) -> str:
    if isinstance(values, list):
        values = {pascal(value): value for value in values}
    members = "\n".join(f'    {member} = "{value}"' for member, value in values.items())
    return f'class {name}(StrEnum):\n    """{doc}"""\n\n{members}\n'


def name_map(identifiers: list[str]) -> dict[str, str]:
    """Factory names whose identifier can't be derived back from the name."""
    return {pascal(i): i for i in identifiers if f"minecraft:{snake(pascal(i))}" != i}


def factory_module(
    descriptor: str,
    make: str,
    mapping: dict[str, str],
    module: str,
    ids: str,
) -> str:
    return f"""import re

from {module} import {descriptor}

_NAMES: dict[str, str] = {json.dumps(mapping, indent=4)}


{SNAKE}

def _make_factory(name: str):
    identifier = _NAMES.get(name, f"minecraft:{{_to_snake(name)}}")

    def factory() -> {descriptor}:
        return {make}

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {{identifier}}"
    return factory


def __getattr__(name: str):
    from anvil.api.vanilla.{ids} import vanilla_{ids[:-1]}_ids

    identifier = _NAMES.get(name, f"minecraft:{{_to_snake(name)}}")
    if name.startswith("_") or identifier not in vanilla_{ids[:-1]}_ids():
        raise AttributeError(f"module {{__name__!r}} has no attribute {{name!r}}")
    func = _make_factory(name)
    globals()[name] = func
    return func
"""


def potion_signature() -> str:
    return f"""def Potion(
    potion_addition: {literal(POTION_TYPES)} | None = None,
) -> Identifier"""


def blocks(tag: str, files: dict[str, str]) -> None:
    with urlopen(METADATA_URL.format(tag=tag, name="blocks")) as response:
        metadata = json.load(response)
    states = {state["name"]: state for state in metadata["block_properties"]}
    blocks = metadata["data_items"]
    identifiers = [block["name"] for block in blocks]
    if name_map(identifiers):
        raise ValueError(f"Block names don't round trip: {name_map(identifiers)}")

    stub = [
        "from enum import StrEnum",
        "from typing import Literal, TypedDict, Unpack",
        "",
        "from anvil.api.blocks.descriptor import BlockDescriptor",
        "from anvil.lib.jsonmodel import Identifier",
        "",
        enum(
            "BlockStateKeys",
            "Every vanilla block state name.",
            {pascal(keyword(s)): s for s in sorted(states)},
        ),
    ]
    for block in blocks:
        if block["properties"]:
            stub.append(f"class {pascal(block['name'])}States(TypedDict, total=False):")
            for state in sorted(p["name"] for p in block["properties"]):
                stub.append(f"    {keyword(state)}: {state_type(states[state])} | None")
            stub.append("")
    for block in blocks:
        name = pascal(block["name"])
        if block["properties"]:
            stub.append(
                f"def {name}(**states: Unpack[{name}States]) -> Identifier | BlockDescriptor: ..."
            )
        else:
            stub.append(f"def {name}() -> Identifier: ...")
    files["factories/minecraft_blocks.pyi"] = "\n".join(stub) + "\n"

    keys = {keyword(s): s for s in sorted(states) if ":" in s}
    files["factories/minecraft_blocks.py"] = f"""import re
from typing import Any

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.jsonmodel import Identifier

_STATE_KEYS: dict[str, str] = {json.dumps(keys, indent=4)}


{SNAKE}

def _make_factory(name: str):
    identifier = f"minecraft:{{_to_snake(name)}}"

    def factory(**states: Any) -> Identifier | BlockDescriptor:
        states = {{_STATE_KEYS.get(k, k): v for k, v in states.items() if v is not None}}
        name = Identifier.parse(identifier, vanilla=True)
        if states:
            return BlockDescriptor(name=name, states=states)
        return name

    factory.__name__ = name
    factory.__qualname__ = name
    factory.__doc__ = f"Factory for {{identifier}}"
    return factory


def __getattr__(name: str):
    from anvil.api.vanilla.blocks import vanilla_block_ids

    if name.startswith("_") or f"minecraft:{{_to_snake(name)}}" not in vanilla_block_ids():
        raise AttributeError(f"module {{__name__!r}} has no attribute {{name!r}}")
    func = _make_factory(name)
    globals()[name] = func
    return func
"""
    listed = "".join(f'        "{i}",\n' for i in identifiers)
    files["blocks.py"] = (
        "from enum import StrEnum\n\n"
        "from .factories import minecraft_blocks as MinecraftBlockTypes\n\n\n"
        f"def vanilla_block_ids() -> list[str]:\n    return [\n{listed}    ]\n\n\n"
        + enum("MinecraftBlockTags", "Vanilla block tags.", BLOCK_TAGS)
    )


def items(tag: str, files: dict[str, str]) -> None:
    identifiers = [item["name"] for item in fetch(tag, "items")]
    stub = [
        "from typing import Literal",
        "",
        "from anvil.lib.jsonmodel import Identifier",
        "",
    ]
    for identifier in identifiers:
        if identifier == "minecraft:potion":
            stub.append(potion_signature() + ": ...")
        else:
            stub.append(f"def {pascal(identifier)}() -> Identifier: ...")
    files["factories/minecraft_items.pyi"] = "\n".join(stub) + "\n"

    runtime = factory_module(
        "Identifier",
        "Identifier.parse(identifier, vanilla=True)",
        name_map(identifiers),
        "anvil.lib.jsonmodel",
        "items",
    )
    runtime = runtime.replace(
        "import re\n",
        "import re\nfrom typing import Literal\n",
        1,
    ).replace(
        "\n\n_NAMES",
        f"""


{potion_signature()}:
    if potion_addition is not None:
        return Identifier.parse(
            "minecraft:potion_type", vanilla=True, data=potion_addition
        )
    return Identifier.parse("minecraft:potion", vanilla=True)


_NAMES""",
        1,
    )
    files["factories/minecraft_items.py"] = runtime
    listed = "".join(
        f'        "{i}",\n' for i in [*identifiers, "minecraft:potion_type"]
    )
    files["items.py"] = (
        "from enum import StrEnum\n\n"
        "from .factories import minecraft_items as MinecraftItemTypes\n\n"
        '__all__ = ["MinecraftItemTypes", "MinecraftItemTags", "vanilla_item_ids"]\n\n\n'
        f"def vanilla_item_ids() -> list[str]:\n    return [\n{listed}    ]\n\n\n"
        + enum("MinecraftItemTags", "Vanilla item tags.", ITEM_TAGS)
    )


def entities(tag: str, files: dict[str, str]) -> None:
    identifiers = [entity["name"] for entity in fetch(tag, "entities")]
    stub = [
        "from anvil.lib.jsonmodel import Identifier",
        "",
    ]
    stub += [f"def {pascal(i)}() -> Identifier: ..." for i in identifiers]
    files["factories/minecraft_entities.pyi"] = "\n".join(stub) + "\n"
    files["factories/minecraft_entities.py"] = factory_module(
        "Identifier",
        "Identifier.parse(identifier, vanilla=True)",
        name_map(identifiers),
        "anvil.lib.jsonmodel",
        "entities",
    )
    listed = "".join(f'        "{i}",\n' for i in identifiers)
    files["entities.py"] = (
        "from .factories import minecraft_entities as MinecraftEntityTypes\n\n\n"
        f"def vanilla_entity_ids() -> list[str]:\n    return [\n{listed}    ]\n"
    )


def members(tag: str, name: str) -> dict[str, str]:
    """Mojang gives a `value` where the identifier differs from the name, such as
    `minecraft:bow_infinity` written as `minecraft:infinity`."""
    return {
        pascal(entry["name"]): entry.get("value", entry["name"])
        for entry in fetch(tag, name)
    }


def write(files: dict[str, str]) -> None:
    try:
        import black
    except ImportError:
        black = None
    shutil.rmtree(VANILLA, ignore_errors=True)
    for relative, source in files.items():
        path = VANILLA / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if black and source:
            source = black.format_str(
                source, mode=black.Mode(is_pyi=path.suffix == ".pyi")
            )
        path.write_bytes(source.replace("\n", "\r\n").encode("utf-8"))
        print(f"Wrote {path}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    tag = sys.argv[1]
    files = {
        "__init__.py": f'"""Vanilla data from Mojang/bedrock-samples {tag}."""\n',
        "factories/__init__.py": "",
    }
    blocks(tag, files)
    items(tag, files)
    entities(tag, files)
    files["biomes.py"] = (
        "from enum import StrEnum\n\n\n"
        + enum(
            "MinecraftBiomeTypes", "Vanilla biome identifiers.", members(tag, "biomes")
        )
        + "\n\n"
        + enum("MinecraftBiomeTags", "Vanilla biome tags.", BIOME_TAGS)
    )
    files["effects.py"] = (
        "from enum import StrEnum\n\n\n"
        + enum(
            "MinecraftPotionEffectTypes", "Vanilla potion types.", POTION_EFFECT_TYPES
        )
        + "\n\n"
        + enum(
            "MinecraftPotionLiquidTypes",
            "Vanilla potion deliveries.",
            POTION_LIQUID_TYPES,
        )
        + "\n\n"
        + enum(
            "MinecraftEffects", "Vanilla effect identifiers.", members(tag, "effects")
        )
    )
    files["enchantments.py"] = "from enum import StrEnum\n\n\n" + enum(
        "MinecraftEnchantments",
        "Vanilla enchantment identifiers.",
        members(tag, "enchantments"),
    )
    files["features.py"] = "from enum import StrEnum\n\n\n" + enum(
        "MinecraftStructureTypes",
        "Vanilla structure identifiers.",
        members(tag, "features"),
    )
    write(files)


if __name__ == "__main__":
    main()
