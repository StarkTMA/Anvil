# Anvil Documentation

Anvil is a Python-first toolkit for creating Minecraft Bedrock content. This site keeps the top-level pages short and puts repeated setup details in one canonical place.

## Start Here

- [Anvil Overview](anvil.md) for the workflow and project layout.
- [CLI Reference](guide/cli.md) for `anvil create`, `anvil build`, and the rest of the command set.
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

1. Run `anvil create <namespace> <project_name>` to scaffold a project.
2. Put gameplay code in `scripts/python/` and assets under `assets/`.
3. Run `anvil build` to build and export your packs.
