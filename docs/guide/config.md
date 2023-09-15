# Understanding your config.ini file

The `config.ini` file is the configuration file for your project. It contains all the information about your project, such as the project name, the namespace, the version, etc.

This is a very important file, as it is used to generate almost all the files in your project.

The `config.ini` file is divided into sections, each section containing different information about your project which you can modify.

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

### `[BUILD]`

This section contains information about the build process of the project.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `release` | `UUIDv4` | The version number of the project, used in all manifest files. | `1.0.0` | None | Yes |
| `rp_uuid` | `UUIDv4` | The uuid of the resource pack. | `Randomly generated` | None | Yes |
| `bp_uuid` | `UUIDv4` | The uuid of the behavior pack. | `Randomly generated` | None | Yes |
| `pack_uuid` | `UUIDv4` | The uuid of the world template. | `Randomly generated` | None | Yes |

### `[ANVIL]`

This section contains information about Anvil.

| Key | Type | Description | Default | Restriction | Can be changed |
| --- | ---- | ----------- | ------- | ----------- | -------------- |
| `debug` | `int(bool)` | Enables or disables generation of additional debugging features. | `0` | None | Yes |
| `scriptapi` | `int(bool)` | Enables or disables ScriptAPI support. | `0` | None | Yes |
| `pbr` | `int(bool)` | Enables or disables Physically based rendering support. | `0` | None | Yes |
| `namespace_format` | `int(bool)` | The identifier and file extension formats to be enforced. | `0` | None | Yes |
| `pascal_project_name` | `str` | Used in generation of Resource and Behavior packs. | `MP` | None | Yes |
| `last_check` | `str` | The last time Anvil checked `@Mojang/bedrock-sample` for updates. | `datetime` | None | Not advised |

## Example

```ini
[MINCRAFT]
vanilla_version = 1.20.12

[PACKAGE]
company = Namespace
namespace = namespace
project_name = my_project
display_name = My Project
project_description = My Project Essentials

[BUILD]
release = 1.0.0
rp_uuid = 00000000-0000-0000-0000-000000000000
bp_uuid = 00000000-0000-0000-0000-000000000000
pack_uuid = 00000000-0000-0000-0000-000000000000

[ANVIL]
debug = 0
scriptapi = 0
pbr = 0
namespace_format = 0
pascal_project_name = MP
last_check = 2022-04-01 00:00:00
```


## Note
> The `config.ini` file is automatically generated when you run the `anvil create` command. You can modify the `config.ini` file at any time, but be aware that some changes might have unexpected results.
> Additional information can be added to the `config.ini` file through the Anvil API at runtime. This is useful for storing information that is not used in the generation of the project.


