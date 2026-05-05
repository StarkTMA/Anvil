# Understanding Your anvilconfig.json File

This is the canonical reference for `anvilconfig.json`. The overview pages link here instead of repeating the configuration tables.

The file defines the project name, namespace, versioning, and runtime flags that Anvil uses while generating packs and bundles.

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
| `project_description`  | `str` | Description used in localized text.                       | `My Project Packs`         | None                                                                    | Yes            |
| `behavior_description` | `str` | Description of the behavior pack.                         | `My Project behavior Pack` | None                                                                    | Yes            |
| `resource_description` | `str` | Description of the resource pack.                         | `My Project Resource Pack` | None                                                                    | Yes            |
| `target`               | `str` | Packaging target; can be `world` or `addon`.              | `world`                    | None                                                                    | Yes            |

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
		"rp_uuid": ["00000000-0000-0000-0000-000000000000"],
		"bp_uuid": ["00000000-0000-0000-0000-000000000000"],
		"pack_uuid": "00000000-0000-0000-0000-000000000000",
		"data_module_uuid": "00000000-0000-0000-0000-000000000000",
		"script_module_uuid": "00000000-0000-0000-0000-000000000000"
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
	}
}
```

## Notes

- The `anvilconfig.json` file is automatically generated when you run the `anvil create` command. You can modify the file at any time, but be cautious—some changes might have unexpected results.
- Missing keys in the `anvilconfig.json` file will be automatically handled by Anvil during runtime.
- You can add additional information to the `anvilconfig.json` file through the Anvil API. This is particularly useful for storing metadata not required during the project generation.
