# Creating your first project

## Introduction

This guide will walk you through creating your first project with Anvil.

Open your terminal and run the following command:

``` bash
anvil create namespace my_project

[options]:
    --preview           Generates the project in Minecraft Preview com.mojang instead of release.
    --fullns            Sets the Project namespace to the full namespace.project_name
    --scriptapi         Adds dependencies support of ScriptAPI
    --pbr               Adds capabilities support of Physically based rendering
```

The command will do the following:

    - Create a folder named `my_project` in `com.mojang\minecraftWorlds`.
    - A VScode workspace will be created in your desktop.

The vscode workspace will be opened automatically, revealing a specific folder structure:

```bash
my_project
├───assets
│   ├───animations
│   ├───marketing
│   ├───models
│   │   ├───attachables
│   │   ├───blocks
│   │   └───entity
│   ├───output
│   ├───particles
│   ├───skins
│   ├───sounds
│   ├───structures
│   ├───textures
│   │   ├───attachables
│   │   ├───blocks
│   │   ├───entity
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
├───scripts
├───.gitignore
├───CHANGELOG.md
├───config.ini
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

### `scripts`

If you require any additional scripts for your project, you can place them in this folder. Not needed for the project to work.

### `.gitignore`

This file is used by git to ignore files and folders when committing changes to your repository.

By default, it will ignore python cache files.

### `CHANGELOG.md`

This file can be used to keep track of changes made to your project. Not needed for the project to work.

### `config.ini`

This is the second most important file in your project. It contains all the configuration for your project.

### `manifest.json`

This file is used by Minecraft to identify your project. It contains information such as the project name, description, version, and more. Will be regenerated when you run the anvil script.

### `my_project.py`

This is the main python script for your project. It contains all the code that will be used to generate your project. The main script must remain in the root directory of the project, additional work can be added and imported from scripts in the `scripts` folder.

### `world_behavior_packs.json`

This file is used by Minecraft to identify the behavior packs for your project. Will be regenerated when you run the anvil script.

### `world_resource_packs.json`

This file is used by Minecraft to identify the resource packs for your project. Will be regenerated when you run the anvil script.
