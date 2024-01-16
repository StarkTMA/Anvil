# Understanding your anvilconfig.json file

The `anvilconfig.json` file is the configuration file for your project. It contains all the information about your project, such as the project name, the namespace, the version, etc.

This is a very important file, as it is used to generate almost all the files in your project.

The `anvilconfig.json` file is divided into sections, each section containing different information about your project which you can modify.

## Sections

### `[MINCRAFT]`

This section contains information about the Minecraft version that the project is compiled for.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `vanilla_version` | `str` | The version of Minecraft that the project is compiled for. | `1.20.12` | Automatically pulled from `@Mojang/bedrock-sample` | Unnecessary |

### `[PACKAGE]`

This section contains information about your project.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `company` | `str` | The company name of the project, used in the `manifest.json` authors section | `Namespace` | None | Yes |
| `namespace` | `str`| The namespace of the project. | `namespace` | The namespace cannot exceed 8 characters. | Not advised |
| `project_name` | `str` | The name of the project. | `my_project` | The project name cannot exceed 16 characters. Changing this might have unexpected results. | Not advised |
| `display_name` | `str` | The display name of the project. | `My Project` | None | Yes |
| `project_description` | `str` | The description of the project. Used in localized text | `My Project Essentials` | None | Yes |
| `target` | `str` | The packaging target, can either be `world` or `addon` | `My Project Essentials` | None | Yes |

### `[BUILD]`

This section contains information about the build process of the project.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `release` | `UUIDv4` | The version number of the project, used in all manifest files. | `1.0.0` | None | Yes |
| `rp_uuid` | `list[UUIDv4]` | The uuid of the resource pack. | `Randomly generated` | None | Yes |
| `bp_uuid` | `list[UUIDv4]` | The uuid of the behavior pack. | `Randomly generated` | None | Yes |
| `pack_uuid` | `UUIDv4` | The uuid of the world template. | `Randomly generated` | None | Yes |

### `[ANVIL]`

This section contains information about Anvil.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `debug` | `bool` | Enables or disables generation of additional debugging features. | `false` | None | Yes |
| `scriptapi` | `bool` | Enables or disables ScriptAPI support. | `false` | None | Yes |
| `scriptui` | `bool` | Enables or disables ScriptAPI/UI support. | `false` | None | Yes |
| `pbr` | `bool` | Enables or disables Physically based rendering support. | `false` | None | Yes |
| `random_seed` | `bool` | Enables or disables random_seed support. | `false` | None | Yes |
| `pascal_project_name` | `str` | Used in generation of Resource and Behavior packs. | `MP` | None | Yes |
| `last_check` | `str` | The last time Anvil checked `@Mojang/bedrock-sample` for updates. | `datetime` | None | Not advised |

### `[NAMESPACE]`

Addition configuration options you can add. 


## Example

```json 
{
    "minecraft": {
        "vanilla_version": "1.20.50.3"
    },
    "package": {
        "company": "StarkTMA",
        "namespace": "stark_mp",
        "project_name": "my_project",
        "display_name": "My Project",
        "project_description": "My Project Packs",
        "target": "world"
    },
    "build": {
        "release": "1.0.0",
        "rp_uuid": [
            "38ec2836-ad50-49c1-bd60-479522b61cc3"
        ],
        "bp_uuid": [
            "6264fa55-70e8-4e24-a7ff-52a2c4f435ca"
        ],
        "pack_uuid": "5e9f2140-11c6-47f4-a267-25af5ad92e5a"
    },
    "anvil": {
        "debug": false,
        "scriptapi": true,
        "scriptui": true,
        "pbr": false,
        "random_seed": false,
        "pascal_project_name": "MP",
        "last_check": "2024-01-16 19:06:58",
        "experimental": false
    },
    "stark_mp": {}
}
```


## Note
> The `anvilconfig.json` file is automatically generated when you run the `anvil create` command. You can modify the `anvilconfig.json` file at any time, but be aware that some changes might have unexpected results.
> Missing keys in the `anvilconfig.json` file will be handled by Anvil when you run the main script.
> Additional information can be added to the `anvilconfig.json` file through the Anvil API at runtime. This is useful for storing information that is not used in the generation of the project.


