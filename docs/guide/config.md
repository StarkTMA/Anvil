# Understanding Your anvilconfig.json File

The `anvilconfig.json` file is the main configuration file for your project. It defines key details about your project, including the project name, namespace, version, and more.

This file is crucial for your project's setup as it is used to generate most of the files in your project. The `anvilconfig.json` is divided into sections, each providing specific configuration options you can modify to suit your project's requirements.

## Sections

### `[MINECRAFT]`

This section defines the Minecraft version that your project targets.

| Key               | Type  | Description                                              | Default   | Restriction                                         | Can be Changed |
| ----------------- | ----- | -------------------------------------------------------- | --------- | --------------------------------------------------- | -------------- |
| `vanilla_version` | `str` | The Minecraft version for which the project is compiled. | `1.20.12` | Automatically pulled from `@Mojang/bedrock-sample`. | No             |

### `[PACKAGE]`

This section contains metadata about your project.

| Key                    | Type  | Description                                               | Default                    | Restriction                                                             | Can be Changed |
| ---------------------- | ----- | --------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------- | -------------- |
| `company`              | `str` | Company name used in the `manifest.json` authors section. | `Namespace`                | None                                                                    | Yes            |
| `namespace`            | `str` | Namespace for the project.                                | `namespace`                | Must not exceed 8 characters.                                           | Not Advised    |
| `project_name`         | `str` | Name of the project.                                      | `my_project`               | Must not exceed 16 characters. Changing might cause unexpected results. | Not Advised    |
| `display_name`         | `str` | Display name of the project.                              | `My Project`               | None                                                                    | Yes            |
| `project_description`  | `str` | Description used in localized text.                       | `My Project Essentials`    | None                                                                    | Yes            |
| `behavior_description` | `str` | Description of the behavior pack.                         | `My Project behavior Pack` | None                                                                    | Yes            |
| `resource_description` | `str` | Description of the resource pack.                         | `My Project Resource Pack` | None                                                                    | Yes            |
| `target`               | `str` | Packaging target; can be `world` or `addon`.              | `My Project Packs`         | None                                                                    | Yes            |

### `[BUILD]`

This section defines information related to the build process.

| Key                  | Type           | Description                                            | Default            | Restriction | Can be Changed |
| -------------------- | -------------- | ------------------------------------------------------ | ------------------ | ----------- | -------------- |
| `release`            | `UUIDv4`       | Version number of the project, used in manifest files. | `1.0.0`            | None        | Yes            |
| `rp_uuid`            | `list[UUIDv4]` | UUIDs of the resource packs.                           | Randomly generated | None        | Yes            |
| `bp_uuid`            | `list[UUIDv4]` | UUIDs of the behavior packs.                           | Randomly generated | None        | Yes            |
| `pack_uuid`          | `UUIDv4`       | UUID of the world template.                            | Randomly generated | None        | Yes            |
| `data_module_uuid`   | `UUIDv4`       | UUID of the data module.                               | Randomly generated | None        | Yes            |
| `script_module_uuid` | `UUIDv4`       | UUID of the script module.                             | Randomly generated | None        | Yes            |

### `[ANVIL]`

This section contains settings related to the Anvil tool.

| Key                   | Type   | Description                                                                | Default           | Restriction | Can be Changed |
| --------------------- | ------ | -------------------------------------------------------------------------- | ----------------- | ----------- | -------------- |
| `debug`               | `bool` | Enable/disable additional debugging features.                              | `false`           | None        | Yes            |
| `scriptapi`           | `bool` | Enable/disable ScriptAPI support.                                          | `false`           | None        | Yes            |
| `scriptui`            | `bool` | Enable/disable ScriptAPI/UI support.                                       | `false`           | None        | Yes            |
| `pbr`                 | `bool` | Enable/disable physically based rendering (PBR) support.                   | `false`           | None        | Yes            |
| `random_seed`         | `bool` | Enable/disable random seed support.                                        | `false`           | None        | Yes            |
| `pascal_project_name` | `str`  | Name used for generating Resource and behavior packs.                      | `MP`              | None        | Yes            |
| `last_check`          | `str`  | Last time Anvil checked `@Mojang/bedrock-sample` for updates.              | `datetime`        | None        | Not Advised    |
| `experimental`        | `bool` | Indicates if the project uses experimental features.                       | `false`           | None        | Yes            |
| `preview`             | `bool` | Whether to generate the project for Minecraft release or preview versions. | `false`           | None        | Yes            |
| `entry_point`         | `str`  | The main entry point script for the project.                               | `main.py`         | None        | Yes            |
| `js_bundle_script`    | `str`  | The JavaScript bundle script for the project.                              | `node esbuild.js` | None        | Yes            |
| `minify`              | `bool` | Whether to minify the JavaScript code and JSONs during the build process.  | `false`           | None        | Yes            |

### `[NAMESPACE]`

Additional configuration options you can add.

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
		"target": "world",
		"behavior_description": "My Project behavior Pack",
		"resource_description": "My Project Resource Pack"
	},
	"build": {
		"release": "1.0.0",
		"rp_uuid": ["38ec2836-ad50-49c1-bd60-479522b61cc3"],
		"bp_uuid": ["6264fa55-70e8-4e24-a7ff-52a2c4f435ca"],
		"pack_uuid": "5e9f2140-11c6-47f4-a267-25af5ad92e5a"
        "data_module_uuid": "b0c8f1d2-3c4e-4a5b-9f6d-7e8f9a0b1c2d",
        "script_module_uuid": "d1e2f3a4-5b6c-7d8e-9f0a-b1c2d3e4f5g6"
	},
	"anvil": {
		"debug": false,
		"scriptapi": true,
		"scriptui": true,
		"pbr": false,
		"random_seed": false,
		"pascal_project_name": "MP",
		"last_check": "2024-01-16 19:06:58",
		"experimental": false,
        "preview": false,
		"entry_point": "main.py",
		"js_bundle_script": "node esbuild.js",
		"minify": false
	},
	"stark_mp": {}
}
```

## Notes

- The `anvilconfig.json` file is automatically generated when you run the `anvil create` command. You can modify the file at any time, but be cautious—some changes might have unexpected results.
- Missing keys in the `anvilconfig.json` file will be automatically handled by Anvil during runtime.
- You can add additional information to the `anvilconfig.json` file through the Anvil API. This is particularly useful for storing metadata not required during the project generation.
