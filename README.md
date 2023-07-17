# Anvil -  a Minecraft bedrock content development tool

-----

![Anvil Status](https://img.shields.io/badge/status-beta-yellow.svg)
![Anvil Version](https://img.shields.io/badge/release-0.4.2-blue.svg)
![Python 10](https://img.shields.io/badge/python-3.10-g.svg)
![Python 11](https://img.shields.io/badge/python-3.11-g.svg)


### Requirements

To use Anvil, [**python**](https://www.python.org/downloads/) `3.10.0` or higher must be installed.

### Installation

To install Anvil, run the following command in your terminal:

```bash 
pip install anvil
```

### Usage

```bash
anvil create <namespace> <project_name> [options]

namespace           The namespace of the project. "minecraft" is a reserved namespace and cannot be used.
project_name        The name of the project.

[options]:
    --preview           Generates the project in Minecraft Preview com.mojang instead of release.
    --fullns            Sets the Project namespace to the full namespace.project_name
    --scriptapi         Adds dependencies support of ScriptAPI
    --pbr               Adds dependencies support of Physically based rendering
```

### Links & Resources

* [**Documentation**](https:///) - Official docs for **anvil**.
* [**Bedrock Learn Portal**](https://learn.microsoft.com/en-gb/minecraft/creator/reference/) - Official Minecraft Bedrock Documentation.