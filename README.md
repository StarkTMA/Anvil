# Anvil Documentation

![Python 10](https://img.shields.io/badge/python-+3.10%20%20-g.svg)
![Anvil Version](https://img.shields.io/github/v/release/StarkTMA/Anvil?label=version)
![OS](https://img.shields.io/badge/OS-Windows-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction to Anvil

Anvil is a comprehensive development toolkit designed for creating Minecraft Bedrock Edition content with ease and flexibility. Anvil aims to simplify the creation of custom Minecraft entities, blocks, commands, and more by leveraging Python and embracing a modular, component-based design philosophy.

Whether you're a seasoned Minecraft modder or just starting your journey in content development, Anvil provides you with the tools to make your creations come to life. Its features are designed to streamline workflows, enforce consistency, and offer a robust framework for handling the complexities of Minecraft content.

### Key Features

- **Modular Development**: Design blocks, entities, and features in a reusable manner to make your content scalable and easy to manage.
- **Schema Management**: Automate JSON schema creation and validation for Minecraft packs to eliminate manual errors.
- **Report Generation**: Generate detailed reports about the contents of your project, including entities, blocks, and other assets, for easy tracking and management.
- **Project Validation**: Validate your project before submission to the Minecraft Marketplace, raising any errors or warnings that need to be addressed to meet Marketplace standards.
- **Multi-Format Packaging**: Package your project into multiple formats, worlds, addons, templates and more.

## Getting Started with Anvil

### Prerequisites

To use Anvil, ensure you have the following installed:

- [**Python 3.10**](https://www.python.org/downloads/) or higher.
- **Windows OS**: Anvil is designed specifically for Windows, as Minecraft Bedrock development is primarily done on this platform.

### Installation

To install Anvil, you can use `pip`:

```bash
pip install mcanvil
```

This will install the latest version of Anvil along with its dependencies.

### Creating Your First Project

To create a new Minecraft development project with Anvil, open your terminal and run the following command:

```bash
anvil create <namespace> <project_name> [options]
```

- **namespace**: A unique identifier for your project. The namespace `minecraft` is reserved and cannot be used.
- **project_name**: The name of your project.

Optional flags include:

- `--preview`: Set up the project for Minecraft Preview.
- `--scriptapi`: Adds support for Script API dependencies.
- `--pbr`: Adds Physically Based Rendering (PBR) dependencies for enhanced graphics.
- `--random_seed` : Adds support for Random Seed Worlds, allowing for randomized world generation.
- `--addon`: Marks the package as an addon, enforcing relevant constraints.

### Example

```bash
anvil create my_ns awesome_project --scriptapi --pbr
```

This command will:

- Create a folder named `awesome_project` in your working directory.
- Set up the initial project structure, including JSON and Python files.

### Project Structure

Once you create your project, the structure will look like this:

```
awesome_project/
├── assets/
│   ├── bbmodels/
│   ├── particles/
│   ├── textures/
│   └── sounds/
├── marketing/
├── output/
├── scripts/
│   ├── javascript/
│   └── python/
├── world/
│   └── structures/
├── .gitignore
├── CHANGELOG.md
├── anvilconfig.json
├── esbuild.js
├── package.json
└── tsconfig.json
```

### Running Your Project

To test your project in Minecraft, navigate to your project folder and use the following command:

```bash
anvil run
```

This command will run your python script and generates the necessary files for your project.

---

### Links & Resources

- [**Documentation**](https://anvil.starktma.net/) - Official docs for **anvil**.
- [**Bedrock Learn Portal**](https://learn.microsoft.com/en-gb/minecraft/creator/reference/) - Official Minecraft Bedrock Documentation.

### Projects made with Anvil

<table>
  <tr>
    <td width="25%">
      <a href="https://www.minecraft.net/en-us/marketplace/pdp/starktma/enchantments-plus/7c27b1c3-40e4-4b70-87f6-ff15ab32daa1">
        <img src="https://starktma.net/wp-content/uploads/2025/10/keyart.png" alt="Enchantments Plus" width="100%"/>
      </a>
    </td>
    <td width="25%">
      <a href="https://www.minecraft.net/en-us/marketplace/pdp/honeyfrost/dinosaurs-add--on-2.1/bbc3adf7-b481-47f2-9a3d-749ae5421508">
        <img src="https://starktma.net/wp-content/uploads/2024/09/dinosaurs_addon.jpg" alt="Dinosaurs" width="100%"/>
      </a>
    </td>
    <td width="25%">
      <a href="https://www.minecraft.net/en-us/marketplace/pdp/starktma/sugar-rush/369a21ac-1f36-4629-8d70-59849c5501ec">
        <img src="https://starktma.net/wp-content/uploads/2023/11/keyart.png" alt="Sugar Rush" width="100%"/>
      </a>
    </td>
    <td width="25%">
      <a href="https://www.minecraft.net/en-us/marketplace/pdp/starktma/beyond:-platformer/f1ecf12b-1b6f-4794-a8de-24dfb82e6f25">
        <img src="https://starktma.net/wp-content/uploads/2024/10/beyond_platformer_v2.jpg" alt="Beyond: Platformers" width="100%"/>
      </a>
    </td>
  </tr>
</table>
