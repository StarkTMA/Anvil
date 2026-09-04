# Anvil Documentation

![](https://img.shields.io/github/v/release/starktma/anvil)
![](https://img.shields.io/github/license/starktma/anvil)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/StarkTMA/Anvil)

![Python](https://img.shields.io/badge/Python_3.13-3776AB?style=flat&logo=python&logoColor=white)

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

- [Add a Custom Entity](guide/adding_entity.md)
- [Add a Custom Block](guide/adding_block.md)
- [Add a Custom Item](guide/adding_item.md)
- [Custom Components](guide/custom_components.md)
- [Localization](guide/localization.md)
- [Trade Tables](guide/trade_tables.md)
- [Using Jigsaw](guide/using_jigsaw.md)
- [PBR](guide/pbr.md)

## Quick Workflow

1. Run `anvil init <namespace> <project_name>` (or `anvil create`) to scaffold a project.
2. Put gameplay code in `scripts/python/` and assets under `assets/`.
3. Run `anvil build` to build and export your packs.
