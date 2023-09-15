Anvil is a Minecraft Bedrock development tool designed to make creating content for Minecraft Bedrock easier and consistent. It is build around modularity and extensibility, allowing you to create your own modules and plugins to extend the functionality of Anvil.

Anvil leverages the power of [**Python**](https://www.python.org/downloads/) at automating repetitive tasks and generating code for you, so you can focus on the important stuff.

The design philosophy of Anvil is to be as modular as possible, where the entire project can be entirely generated using the python script and its assets.

## Requirements
To use Anvil, [**python**](https://www.python.org/downloads/) `3.10.0` or higher must be installed.

Due to Minecraft bedrock being primarily developed on Windows, the file paths are Windows specific, so Anvil is only supported on Windows.

## Installing
To install Anvil, run the following command in your terminal:

```bash
pip install anvil
```

This should install Anvil and all of its dependencies.

## Usage
```bash
anvil create <namespace> <project_name> [options]

namespace           The namespace of the project. "minecraft" is a reserved namespace and cannot be used.
project_name        The name of the project.

[options]:
    --preview           Generates the project in Minecraft Preview com.mojang instead of release.
    --fullns            Sets the Project namespace to the full namespace.project_name
    --scriptapi         Adds dependencies support of ScriptAPI
    --pbr               Adds capabilities support of Physically based rendering
```