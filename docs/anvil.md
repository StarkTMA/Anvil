# Anvil — Python‑First Toolchain for Minecraft Bedrock

Anvil lets you build Bedrock addons the same way you write gameplay logic: **in code, not in JSON editors**. Write blocks, entities, items, recipes, animation controllers, and even Script API logic in clean, type‑safe Python. Run a single command and Anvil turns that code into perfectly‑validated Bedrock packs, ready for your development folder or the Marketplace submission portal.

---

## How Anvil Helps You Ship Faster

A typical Bedrock project involves hundreds of JSON fragments that must all line up with Mojang’s ever‑shifting schemas. One typo breaks everything. Anvil collapses that surface area to a single Python DSL and gives you proper IDE support autocomplete, static checks, refactors—plus Marketplace rule validation baked in. When Anvil finishes a build you know your packs load and for partners Microsoft won’t bounce the upload.

---

## Zero‑to‑Pack Workflow

1. **`anvil create <namespace> <project_name>`** scaffolds a project folder, generates all required UUIDs, and writes `anvilconfig.json`.
2. Drop assets, Blockbench models, textures, mcstructure files, sounds into the `assets` tree. Put gameplay Python and Typescript in `assets/`.
3. **`anvil build`** compiles Python ➞ JSON, optionally compiles TypeScript ➞ JavaScript, validates everything, and exports your chosen package format.

---

## Project Scaffold

```text
project/
├── assets/
│   ├── bbmodels/
│   ├── particles/
│   ├── textures/
│   ├── sounds/
│   └── structures/
├── marketing/
├── output/
├── scripts/
│   ├── javascript/
│   └── python/
├── world/
├── anvilconfig.json
├── esbuild.js
├── package.json
└── tsconfig.json
```

Source stays put; `anvil build` copies only what Bedrock needs into dev Behaviour/Resource packs.

---

## Configuration

`anvilconfig.json` is documented in the [project configuration guide](guide/config.md). That page is the single source of truth for the file layout and default values.

---

## CLI Flags

The command options used by `anvil create`, `anvil build`, and the other CLI commands are documented in the [CLI reference](guide/cli.md).

---

## Asset Pipelines

### TypeScript

When `scriptapi=true` (or `--scriptapi`) Anvil generates `package.json` and `tsconfig.json`, `esbuild.js` for you. Drop TypeScript files into `assets/scripts/javascript/` and import them freely. Anvil runs `esbuild` to bundle. Or you can use your own javascript bundler; just set `js_bundle_script` in `anvilconfig.json` to your entrypoint.

### Localization

All literal strings are stored in `localization.csv` in the project root with one column per Minecraft-supported language. Anvil compiles this into `en_US.lang` and other language files automatically.

---

## Validation & Error Handling

• **Namespacing** — `minecraft` is forbidden; namespace ≤ 8 chars; project name ≤ 16.

• **Manifest sanity** — UUID format, duplicates, required icons/marketing art, capability flags.

Any failure raises a Python exception with file‑exact context; exit code 1 indicates “build failed.”

---

## Extensibility

Place new modules in `assets/python/` and inherit from core classes (`Entity`, `Block`, `Item`, …). Mixins and helper libraries are plain Python; Anvil introspects them automatically.

---

## Packaging Targets

Use `Anvil.compile(zip=True)` or call `anvil build --zip` and set `target` in `anvilconfig.json`.

| Target  | Output                               |
| ------- | ------------------------------------ |
| `addon` | Marketplace‑ready addon ZIP.         |
| `world` | Marketplace‑ready world template ZIP |

Use `Anvil.compile(mcaddon=True)` or call `anvil build --mcaddon` to get a ready‑to‑use `.mcaddon` file.
Use `Anvil.compile(mcworld=True)` or call `anvil build --mcworld` to get a ready‑to‑use `.mcworld` file.

Icon/Marketing requirements differ per target; Anvil refuses to package until mandatory art exists.

---

## Version Support & Performance

- **Python ≥ 3.13** on **Windows 10/11** (Bedrock’s official dev OS).
- Always tracks the **latest Bedrock release**; back‑targets are intentionally unsupported.

---

## Should You Use It?

If you’re tired of JSON busy‑work and comfortable writing Python, yes. Anvil keeps you in a real programming language, auto‑validates Marketplace constraints, and ships in seconds. Otherwise, `pip install mcanvil`, scaffold, script, build, publish.
