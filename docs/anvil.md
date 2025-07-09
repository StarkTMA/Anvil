# Anvil — Python‑First Toolchain for Minecraft Bedrock

Anvil lets you build Bedrock addons the same way you write gameplay logic: **in code, not in JSON editors**. Write blocks, entities, items, recipes, animation controllers, and even Script API logic in clean, type‑safe Python. Run a single command and Anvil turns that code into perfectly‑validated Bedrock packs, ready for your development folder or the Marketplace submission portal.

---

## How Anvil Helps You Ship Faster

A typical Bedrock project involves hundreds of JSON fragments that must all line up with Mojang’s ever‑shifting schemas. One typo breaks everything. Anvil collapses that surface area to a single Python DSL and gives you proper IDE support—autocomplete, static checks, refactors—plus Marketplace rule validation baked in. When Anvil finishes a build you know your packs load and for partners Microsoft won’t bounce the upload.

---

## Zero‑to‑Pack Workflow

1. **`anvil create <namespace> <project_name>`** scaffolds a project folder, generates all required UUIDs, and writes `anvilconfig.json`.
2. Drop assets—Blockbench models, textures, mcstructure files, sounds, Script API code—into the `assets` tree. Put gameplay Python in `assets/python/`.
3. **`anvil run`** compiles Python ➞ JSON, optionally compiles TypeScript ➞ JavaScript, validates everything, and exports your chosen package format.

---

## Project Scaffold

```text
project_name/
└─ assets/
   ├─ bbmodels/
   ├─ javascript/
   ├─ marketing/
   ├─ particles/
   ├─ python/
   ├─ skins/
   ├─ sounds/
   ├─ world/
   ├─ textures/
   │  ├─ environment/
   │  ├─ items/
   │  └─ ui/
   └─ output/   # build artefacts land here
```

Source stays put; `anvil run` copies only what Bedrock needs into dev Behaviour/Resource packs.

---

## `anvilconfig.json` Reference

All project metadata lives in one file and auto‑propagates—no duplicated strings.

| Section           | Keys                                                                                                                                                                                  | Purpose / Restrictions                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **`[MINECRAFT]`** | `vanilla_version`                                                                                                                                                                     | Target engine version. Auto‑pulled, read‑only.               |
| **`[PACKAGE]`**   | `company`, `namespace` (≤ 8 chars), `project_name` (≤ 16 chars), `display_name`, `project_description`, `behavior_description`, `resource_description`, `target` (`world` or `addon`) | Marketplace metadata.                                        |
| **`[BUILD]`**     | `release` (semver), `rp_uuid[]`, `bp_uuid[]`, `pack_uuid`, `data_module_uuid`, `script_module_uuid`                                                                                   | Identity & versioning. Missing IDs regenerate automatically. |
| **`[ANVIL]`**     | `debug`, `scriptapi`, `scriptui`, `pbr`, `random_seed`, `pascal_project_name`, `last_check`, `experimental`, `preview`                                                                | Feature toggles.                                             |
| **`[NAMESPACE]`** | _(reserved for future per‑namespace overrides)_                                                                                                                                       |                                                              |

---

## anv Flags

| Flag            | Action                                                              |
| --------------- | ------------------------------------------------------------------- |
| `--preview`     | Target Minecraft Preview paths instead of release.                  |
| `--scriptapi`   | Enable Script API; compiles sources from `assets/javascript/`.      |
| `--scriptui`    | Same, but for the UI module.                                        |
| `--pbr`         | Insert the PBR capability token and copy normal/spec maps.          |
| `--random_seed` | Enables procedural‐world hooks; limits packaging to dynamic worlds. |
| `--addon`       | Force addon mode; extra Marketplace naming constraints apply.       |

`--help` and `--version` behave conventionally.

---

## Asset Pipelines

### TypeScript

When `scriptapi=true` (or `--scriptapi`) Anvil invokes **`tsc`**. A default `tsconfig.json` is placed at project root; override it freely—Anvil respects your settings.

### PBR

When `pbr=true` (or `--pbr`) Anvil copies Blockbench PBR textures (suffixes `_nrm`, `_spc`) and injects the capability tag so Bedrock loads them without manual JSON edits.

### Localization

All literal strings are dumped into `texts/en_US.lang` with autogenerated keys. Register custom keys via `ANVIL.definitions.register_lang`. Run **`anvil translate`** to auto‑fill every Bedrock locale via Google Translate, then tweak as needed.

---

## Validation & Error Handling

• **Namespacing** — `minecraft` is forbidden; namespace ≤ 8 chars; project name ≤ 16.

• **Component ranges** — numeric arguments are clamped or hard‑failed when outside Mojang bounds.

• **Manifest sanity** — UUID format, duplicates, required icons/marketing art, capability flags.

Any failure raises a Python exception with file‑exact context; exit code 1 indicates “build failed.”

---

## Extensibility

Place new modules in `assets/python/` and inherit from core classes (`Entity`, `Block`, `Item`, …). Mixins and helper libraries are plain Python; Anvil introspects them automatically. Define post‑build hooks with `@anvil.hook` decorators when you need custom packaging logic.

---

## Packaging Targets

Call `ANVIL.package_zip()` and set `target` in `anvilconfig.json`.

| Target  | Output                               |
| ------- | ------------------------------------ |
| `addon` | Marketplace‑ready addon ZIP.         |
| `world` | Marketplace‑ready world template ZIP |

Call `ANVIL.mcaddon()` to get a ready‑to‑use `.mcaddon` file, which is a ZIP containing both resource and behavior packs.
Call `ANVIL.mcworld()` to get a ready‑to‑use `.mcworld` file, which is a ZIP containing the world template and its resource and behavior packs.
Call `ANVIL.generate_technical_notes()` to generate a `technical_notes.pdf` file with all the project Entities, Blocks, Items, Recipes, sounds, and more, for easy reference.

Icon/Marketing requirements differ per target; Anvil refuses to package until mandatory art exists.

---

## Version Support & Performance

- **Python ≥ 3.10** on **Windows 10/11** (Bedrock’s official dev OS).
- Always tracks the **latest Bedrock release**; back‑targets are intentionally unsupported.

---

## Current Gaps

Several new entity components and commands are stubbed; Contributions are welcome—open a PR.

---

## Licence

Anvil is released under **GPL v3**. No proprietary code, no bundled assets.

---

## Should You Use It?

If you’re tired of JSON busy‑work and comfortable writing Python, yes. Anvil keeps you in a real programming language, auto‑validates Marketplace constraints, and ships in seconds. If you prefer visual node editors or must target old Bedrock versions, look elsewhere. Otherwise, `pip install mcanvil`, scaffold, script, run—done.
