# Creating your first project

## Introduction

This guide will walk you through creating your first project with Anvil.

Open your terminal and run the following command:

```bash
anvil create <namespace> <project_name> [options]

namespace           The namespace of the project. "minecraft" is a reserved namespace and cannot be used.
project_name        The name of the project.

[options]:
    --preview           Generates the project in Minecraft Preview com.mojang instead of release.
    --scriptapi         Adds dependencies support of ScriptAPI
    --pbr               Adds dependencies support of Physically based rendering
    --random_seed       Adds support of Random Seed Worlds.
    --addon             Sets this package as an addon, comes with many restrictions.
```

The command will do the following:

    - Create a folder named `my_project` in `com.mojang\minecraftWorlds`.
    - A VScode workspace will be created in your desktop.

The vscode workspace will be opened automatically, revealing a specific folder structure:

```bash
my_project
├───assets
│   ├───animations
│   ├───javascript
│   ├───marketing
│   ├───models
│   │   ├───actors
│   │   └───blocks
│   ├───output
│   ├───particles
│   ├───python
│   ├───skins
│   ├───sounds
│   ├───structures
│   ├───textures
│   │   ├───actors
│   │   ├───blocks
│   │   ├───environment
│   │   ├───items
│   │   ├───particle
│   │   └───ui
│   └───vanilla
├───behavior_packs
│   └───BP_MP
│       ├───texts
│       │   └───en_US.lang
│       └───manifest.json
├───resource_packs
│   └───RP_MP
│       ├───texts
│       │   └───en_US.lang
│       └───manifest.json
├───.gitignore
├───anvilconfig.json
├───CHANGELOG.md
├───manifest.json
├───my_project.py
├───world_behavior_packs.json
└───world_resource_packs.json
```

## Project Structure

### `assets`

This folder contains all the assets for your project. It is divided into subfolders for each type of asset.

This is the most important folder in your project, as it contains all the assets that will be used to generate the project.

### `behavior_packs`

This folder will host all the behavior packs for your project. This folder will be created and populated when you run the anvil script.

### `resource_packs`

This folder will host all the resource packs for your project. This folder will be created and populated when you run the anvil script.

### `.gitignore`

This file is used by git to ignore files and folders when committing changes to your repository.

By default, it will ignore python cache files and /node_modules.

### `CHANGELOG.md`

This file can be used to keep track of changes made to your project. Not needed for the project to work.

### `anvilconfig.json`

This is the second most important file in your project. It contains all the configuration for your project.

### `manifest.json`

This file is used by Minecraft to identify your project. It contains information such as the project name, description, version, and more. Will be regenerated when you run the anvil script.

### `my_project.py`

This is the main python script for your project. It contains all the code that will be used to generate your project. The main script must remain in the root directory of the project, additional work can be added and imported from scripts in the `assets/python` folder or any folder for that matter.

### `world_behavior_packs.json`

This file is used by Minecraft to identify the behavior packs for your project. Will be regenerated when you run the anvil script.

### `world_resource_packs.json`

This file is used by Minecraft to identify the resource packs for your project. Will be regenerated when you run the anvil script.
