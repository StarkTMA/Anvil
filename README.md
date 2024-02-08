<img src="https://starktma.net/wp-content/uploads/2022/04/logo.png" width="300" alt="Anvil Logo">

# Anvil

![Python 10](https://img.shields.io/badge/python-3.10%20%20|%20%203.11%20%20|%20%203.12-g.svg)
![Anvil Version](https://img.shields.io/badge/beta-0.7.1-yellow.svg)
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
