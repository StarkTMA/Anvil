<img src="https://starktma.net/wp-content/uploads/2022/04/logo.png" width="300" alt="Anvil Logo">

# Anvil

![Python 10](https://img.shields.io/badge/python-3.10%20%20|%20%203.11%20%20|%20%203.12-g.svg)
![Anvil Version](https://img.shields.io/badge/beta-0.7.0-yellow.svg)
![OS](https://img.shields.io/badge/OS-Windows-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## What is Anvil?

Anvil is a Minecraft Bedrock development tool designed to make creating content for Minecraft Bedrock easier and consistent. It is build around modularity and extensibility, allowing you to create your own modules and plugins to extend the functionality of Anvil.

### Requirements

To use Anvil, [**python**](https://www.python.org/downloads/) `3.10.0` or higher must be installed.

Due to Minecraft bedrock being primarily developed on Windows, Anvil is only supported on Windows.

### Features

- Develop the entire project in python, no need to dive into json files.
- Reusable modules and scripts to make development easier.
- Automatic packaging of the project into a `.mcpack`, `.mcaddon` or `.mcworld` and more.
- Automatic validation for Marketplace content.

### Installing

To install Anvil, run the following command in your terminal:

```bash
pip install mcanvil
```

### Usage

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

### Links & Resources

- [**Documentation**](https://anvil.starktma.net/) - Official docs for **anvil**.
- [**Bedrock Learn Portal**](https://learn.microsoft.com/en-gb/minecraft/creator/reference/) - Official Minecraft Bedrock Documentation.

### Latest Changes

### Version 0.7.0

### [Guidelines]

- New packaging type: Addon
- Anvil raises an error when using experimental features in packages of type Addon.
- Anvil raises an error when total block permutations exceed 10,000 in packages of type Addon, and a warning otherwise.
- Anvil raises an error when overriding a vanilla feature (items and entities, including the player) in packages of type Addon.
- All textures are now placed 2 folders deep in the RP directory, this is to avoid overriding 3rd party textures. `RP/textures/namespace/project_name/`
- Texture references are now in the format `namespace:texture_name`. This is done automatically.
- Scores are now enforced to start with `namespace.` for packages of type Addon. added a new method `get_new_score` to anvil definition to generate scores.
- Tags are now enforced to start with `namespace.` for packages of type Addon.
- Loot Tables are now placed 2 folders deep in the BP directory, this is to avoid conflicting with 3rd party loot tables. `BP/loot_tables/namespace/project_name/`.
- Functions are now placed 2 folders deep in the BP directory, this is to avoid conflicting with 3rd party functions. `BP/functions/namespace/project_name/`.
- Sound references are now in the format `namespace:sound_name`. This is done automatically.
- Materials now follow the format `namespace.material_name:base_material`.

### [ANVIL]

- Split the `core.py` file into multiple files. This shouldn't cause any issues.
- Removed the `fullns` cli option, a universal format is now enforced.
- Added `addon` cli option to set the packaging target. Can be changed from `anvilconfig.json`.
- Missing config options are now handled on runtime.
- `AddonObjects` now all have a single extension format.
- Refactored a lot of code, split a lot classes into smaller modules.
- Most of the functionalities are now required to manually import from their respective modules.
- Anvil now flags experimental entities on non experimental environments.
- Resource packs and Behavior Packs always have dependencies on each other
- Reimplemented the `get_vanilla` method in Entity clients, work with vanilla entities only. The method retrieves the latest version of the `client_entity` from the official `bedrock_samples` github repository.
- Implemented a basic caching system to store retrieved vanilla data, the cached data will be updated in case there is newer release.
- Added a new `identifier` property to the `Materials()` class.

### [Blocks]

- Added a new `BlockDefault()` component that allows you to use the blocks.json file to define block visuals. This is a workaround until `BlockUnitCube()` is out of experimental.
- `BlockGeometry()` and `BlockMaterialInstance()` are no longer required when using `BlockDefault()`.
- If a display name is not supplied using `BlockDisplayName()`, the name will be inferred from the block identifier. Not localized.

### [Items]

- If a display name is not supplied using `ItemDisplayName()`, the name will be inferred from the item identifier. Not localized.
- Added an `attachable` property to items to quickly add attachables to items.

### [Molang]

- Added `Context` to the molang module.
- Fixed an error that treated some molang expressions as string literals and wrapped them with single quotes.

### [Blockbench]

- As an effort to move towards using `.bbmodel` files natively, there has been a change to how models and textures are referenced.
  - Entities and attachables no longer require a dedicated model file, instead a referenced models must be added to the `assets/models` folder under their own name.
    - For instance, if you have an entity named `starktma:vehicle` that references a model called `truck`, you must add a model file named `truck.geo.json` to the `assets/models/actors` folder.
  - Entities and attachables no longer require a dedicated texture file, instead a referenced textures must be added to the `assets/textures` folder under their own name.
    - For instance, if you have an entity named `starktma:vehicle` that references a texture called `truck`, you must add a texture file named `truck.png` to the `assets/textures/actors` folder.
  - Entities and attachables textures and models are now placed in the same `actors` folder.
  - Entities and attachables no longer exports their models and texture into queued folders, instead everything is exported under the `actors` folder.
- Adopting blockbench files will facilitate working with assets, additional the folder structure can no longer be supported wth the new enforced guidelines due to the file path limit.

### [Components]

- Added `Tameable()` component.
