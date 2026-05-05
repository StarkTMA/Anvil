# CLI Reference

Anvil exposes a Click-based command line interface through the `anvil` executable. Use `anvil --help` for the main command list and `anvil <command> --help` for command-specific usage.

This page documents the commands registered in `src/anvil/cli.py` and the behavior implemented by each command module.

## Command Overview

| Command          | Alias / implementation | Project required                     | Purpose                                                            |
| ---------------- | ---------------------- | ------------------------------------ | ------------------------------------------------------------------ |
| `create`         | `init`                 | No                                   | Scaffold a new Anvil project.                                      |
| `build`          | `run`                  | Yes                                  | Build or export the configured project entry point.                |
| `clean`          | `clear`                | Yes                                  | Remove the current project's development packs.                    |
| `prof`           | `profile`              | Yes                                  | Record a performance trace for the current project.                |
| `process-sounds` | `sounds`               | No, but `assets/sounds` should exist | Normalize and re-encode audio files in place.                      |
| `loopback`       | `lb`                   | No                                   | Enable Minecraft UWP loopback access and open the local test page. |

## `create` / `init`

Scaffolds a new project and writes the base configuration, pack folders, and starter files.

```bash
anvil create <namespace> <project_name> [--preview] [--scriptapi] [--addon] [--vscode]
```

### Arguments

| Argument       | Description                                 |
| -------------- | ------------------------------------------- |
| `namespace`    | Project namespace. `minecraft` is reserved. |
| `project_name` | Project folder and package name.            |

### Options

| Option        | Effect                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `--preview`   | Generate the project for the Minecraft Preview `com.mojang` paths.                                    |
| `--scriptapi` | Add Script API support, generate JavaScript scaffolding, and install the Script API npm dependencies. |
| `--addon`     | Mark the project as an addon and apply addon-specific restrictions.                                   |
| `--vscode`    | Generate a VS Code workspace and launch it after scaffolding.                                         |

### What it creates

- `anvilconfig.json` with the project metadata and build settings.
- A starter `scripts/python/main.py` entry point.
- The project directories under `assets/`, `scripts/`, `world/`, `marketing/`, and `output/`.
- `.gitignore`, `CHANGELOG.md`, and `.github/workflows/release.yml`.
- When `--scriptapi` is enabled, `package.json`, `tsconfig.json`, `esbuild.js`, `scripts/javascript/constants.ts`, and `scripts/javascript/main.ts` are also created.
- When `--vscode` is enabled, the project gets a `.code-workspace` file and a `.vscode/launch.json` file for debugging.

### Notes

- The command validates the namespace and project name before creating anything.
- After scaffolding, the command switches into the new project directory and saves the generated config.
- If `--scriptapi` is enabled, Anvil installs `@minecraft/server`, `@minecraft/server-ui`, `@minecraft/vanilla-data`, `@starktma/minecraft-utils`, and `esbuild`.

## `run` / `build`

Builds or exports the configured project entry point from `anvilconfig.json` with the current Python interpreter. Use `anvil build` in examples.

```bash
anvil build [--js-only] [--noarch] [--nocompile] [--mcaddon] [--mcworld] [--zip] [--tech-notes] [--workflow]
```

### Behavior

- Reads the entry point from `anvilconfig.json`.
- Launches that entry point using the same interpreter that started `anvil`.
- Appends any selected flags to the entry script unchanged.

### Options

| Option         | Effect                                                                        |
| -------------- | ----------------------------------------------------------------------------- |
| `--js-only`    | Forward a request to skip archive work where the entry point supports it.     |
| `--noarch`     | Forward a request to skip archive work where the entry point supports it.     |
| `--nocompile`  | Forward a request to skip compilation work where the entry point supports it. |
| `--mcaddon`    | Forward a request to build a Minecraft addon package.                         |
| `--mcworld`    | Forward a request to build a Minecraft world package.                         |
| `--zip`        | Forward a request to build a ZIP archive.                                     |
| `--tech-notes` | Forward a request to generate technical notes.                                |
| `--workflow`   | Forward a request to refresh the GitHub workflow.                             |

### Notes

- The command requires a valid `anvilconfig.json` in the current directory.
- If the entry point is missing, Anvil prints a warning and exits without building.
- The top-level CLI does not package files directly. It delegates the build logic to the project entry script.

## `clean` / `clear`

Deletes the current project's development packs from the matching Minecraft `com.mojang` folders.

```bash
anvil clean
```

### Behavior

- Resolves the current project name and preview setting from `anvilconfig.json`.
- Searches for the development resource pack and development behavior pack for that project.
- Shows the detected paths and asks for confirmation before deleting anything.

### Notes

- If no development packs are found, the command exits cleanly.
- This command is useful when you want a clean export before the next build.

## `prof` / `profile`

Records a Speedscope-compatible performance trace for the current project.

```bash
anvil prof
```

### Behavior

- Reads the configured entry point from `anvilconfig.json`.
- Runs `py-spy record` against the project entry point.
- Writes the trace to `output/anvil_trace.json`.

### Notes

- This command requires `py-spy` to be available on `PATH`.
- If the project configuration is missing or incomplete, the command exits early with a warning.

## `process-sounds` / `sounds`

Batch processes audio files in `assets/sounds`, converts them to `.ogg`, and overwrites the originals.

```bash
anvil sounds [--target-lufs <value>] [--sample-rate <value>] [--quality <value>]
```

### Options

| Option          | Default | Effect                   |
| --------------- | ------- | ------------------------ |
| `--target-lufs` | `-18`   | Target loudness in LUFS. |
| `--sample-rate` | `32000` | Output sample rate.      |
| `--quality`     | `0`     | Vorbis quality level.    |

### Behavior

- Recursively walks `assets/sounds`.
- Processes `.wav`, `.mp3`, and `.ogg` files.
- Normalizes loudness, resamples the audio, and writes the result back as `.ogg`.
- Prompts before starting because the operation overwrites source files.

### Notes

- This command is destructive.
- It requires `ffmpeg` to be installed and available on `PATH`.

## `loopback` / `lb`

Enables Minecraft UWP loopback access and opens the local loopback test page.

```bash
anvil lb
```

### Behavior

- Runs `CheckNetIsolation LoopbackExempt -a -n="Microsoft.MinecraftUWP_8wekyb3d8bbwe"`.
- Opens `http://localhost:7003/` in the default browser.

### Notes

- This command is specific to Windows and Minecraft UWP.
- It is meant to remove the local network restriction that blocks loopback testing.

## Common Usage Patterns

```bash
anvil create my_ns awesome_project --scriptapi --vscode
anvil build --mcaddon
anvil clean
anvil sounds --target-lufs -16 --quality 2
anvil lb
```

## Practical Notes

- `create` can be run in an empty folder.
- `run`, `clean`, and `prof` expect a valid Anvil project in the current directory.
- `process-sounds` and `clean` can modify or delete files, so they prompt before doing work.
- `profile` and `process-sounds` depend on external tools, not just Python packages.
