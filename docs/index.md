# Anvil Documentation

![](https://img.shields.io/github/v/release/starktma/anvil)
![](https://img.shields.io/github/license/starktma/anvil)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/StarkTMA/Anvil)

![Python](https://img.shields.io/badge/Python_3.15-3776AB?style=flat&logo=python&logoColor=white)

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

Anvil is a Python-first toolkit for creating Minecraft Bedrock content. This site keeps the top-level pages short and puts repeated setup details in one canonical place.

## Start Here

- [Anvil Overview](anvil.md) for the workflow and project layout.
- [CLI Reference](guide/cli.md) for `anvil init` / `anvil create`, `anvil build`, and the rest of the command set.
- [Project Configuration](guide/config.md) for `anvilconfig.json`.
- [API Reference](api/index.md) for classes, functions, and modules.

## Tutorials

Start with the three basics, then pick the topics your pack needs. Every snippet in the guides is taken from a project that compiles.

- [Add a Custom Entity](guide/adding_entity.md)
- [Add a Custom Block](guide/adding_block.md)
- [Add a Custom Item](guide/adding_item.md)
- [Animating an Entity](guide/entity_animations.md): animations, animation controllers, render controller arrays.
- [Block States, Permutations and Traits](guide/block_states.md): a lit lantern that faces its placement.
- [Spawn Rules and Loot](guide/spawning_and_loot.md): natural spawning and drops.
- [Particles and Sounds](guide/particles_and_sounds.md): particles, sound definitions, sound events, music.
- [Recipes and the Item Catalog](guide/recipes.md): shaped, shapeless, smelting, stonecutter, creative groups.
- [NPC Dialogues](guide/dialogues.md)
- [Trade Tables](guide/trade_tables.md)
- [Wearables and Attachables](guide/wearables.md): armor rendered on the player.
- [Creating a Biome](guide/custom_biome.md): generation and Vibrant Visuals.
- [Generating Features](guide/world_features.md): ores, scattered blocks, trees.
- [Using Jigsaw](guide/using_jigsaw.md): procedural structures.
- [Custom Components](guide/custom_components.md): Script API logic on blocks and items.
- [Custom Camera](guide/adding_camera.md)
- [PBR](guide/pbr.md)
- [Localization](guide/localization.md)

## Quick Workflow

1. Run `anvil init <namespace> <project_name>` (or `anvil create`) to scaffold a project.
2. Put gameplay code in `scripts/python/` and assets under `assets/`.
3. Run `anvil build` to build and export your packs.
