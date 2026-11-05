# Understanding Your anvilconfig.json File

This is the canonical reference for `anvilconfig.json`. The overview pages link here instead of repeating the configuration tables.

The file defines the project name, namespace, versioning, and runtime flags that Anvil uses while generating packs and bundles.

## Sections

The options are grouped by what they are used for. Each option must be in its section.

### `[PACKAGE]`

What the project is: its identity, names, descriptions and packaging target.

| Key                    | Type  | Description                                               | Default                    | Restriction                                                             | Can be Changed |
| ---------------------- | ----- | --------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------- | -------------- |
| `company`              | `str` | Company name used in the `manifest.json` authors section. | `Namespace`                | None                                                                    | Yes            |
| `namespace`            | `str` | Namespace for the project.                                | `namespace`                | 1 to 8 lowercase letters, digits or `_`, starting with a letter.        | Not Advised    |
| `project_name`         | `str` | Name of the project.                                      | `my_project`               | 1 to 16 lowercase letters, digits or `_`, starting with a letter.       | Not Advised    |
| `display_name`         | `str` | Display name of the project.                              | `My Project`               | None                                                                    | Yes            |
| `project_description`  | `str` | Description used in localized text.                       | `My Project Packs`         | None                                                                    | Yes            |
| `behavior_description` | `str` | Description of the behavior pack.                         | `My Project behavior Pack` | None                                                                    | Yes            |
| `resource_description` | `str` | Description of the resource pack.                         | `My Project Resource Pack` | None                                                                    | Yes            |
| `target`               | `str` | Packaging target; can be `world` or `addon`.              | `world`                    | None                                                                    | Yes            |

For an addon, the namespace must end with the initials of the project name, for example `stark_mp` for `my_project`. The initials also name the packs inside the Marketplace zip.

### `[MANIFEST]`

What the pack manifests carry: the release version and the UUIDs.

| Key                    | Type           | Description                                            | Default            | Restriction | Can be Changed |
| ---------------------- | -------------- | ------------------------------------------------------ | ------------------ | ----------- | -------------- |
| `release`              | `str`          | Version number of the project, used in manifest files. | `1.0.0`            | `X.X.X`     | Yes            |
| `rp_uuid`              | `list[UUIDv4]` | UUIDs of the resource packs.                           | Randomly generated | None        | Yes            |
| `bp_uuid`              | `list[UUIDv4]` | UUIDs of the behavior packs.                           | Randomly generated | None        | Yes            |
| `pack_uuid`            | `UUIDv4`       | UUID of the world template.                            | Randomly generated | None        | Yes            |
| `data_module_uuid`     | `UUIDv4`       | UUID of the data module.                               | Randomly generated | None        | Yes            |
| `resource_module_uuid` | `UUIDv4`       | UUID of the resources module.                          | Randomly generated | None        | Yes            |
| `script_module_uuid`   | `UUIDv4`       | UUID of the script module, when `scriptapi` is on.     | Randomly generated | None        | Yes            |

### `[FEATURES]`

What the project's content uses.

| Key            | Type   | Description                                             | Default | Restriction | Can be Changed |
| -------------- | ------ | ------------------------------------------------------- | ------- | ----------- | -------------- |
| `scriptapi`    | `bool` | Enable/disable ScriptAPI support.                       | `false` | None        | Yes            |
| `scriptui`     | `bool` | Enable/disable ScriptAPI/UI support.                    | `false` | None        | Yes            |
| `pbr`          | `bool` | Enable/disable physically based rendering (PBR) support. | `false` | None        | Yes            |
| `experimental` | `bool` | Indicates if the project uses experimental features.    | `false` | None        | Yes            |
| `random_seed`  | `bool` | Enable/disable random seed support.                     | `false` | None        | Yes            |

### `[BUILD]`

How the project is built and exported. Debug output is turned on with the `--debug` build flag, not in this file.

| Key                | Type   | Description                                                                | Default           | Restriction | Can be Changed |
| ------------------ | ------ | -------------------------------------------------------------------------- | ----------------- | ----------- | -------------- |
| `preview`          | `bool` | Whether to generate the project for Minecraft release or preview versions. | `false`           | None        | Yes            |
| `entry_point`      | `str`  | The main entry point script for the project.                               | `main.py`         | None        | Yes            |
| `js_bundle_script` | `str`  | The JavaScript bundle script for the project.                              | `node esbuild.js` | None        | Yes            |
| `minify`           | `bool` | Whether to minify the JavaScript code and JSONs during the build process.  | `false`           | None        | Yes            |
| `add_stamp`        | `bool` | Whether to add the Anvil header to generated files.                        | `true`            | None        | Yes            |
| `local_export`     | `bool` | Whether to export compiled behavior and resource packs to the local `output/com.mojang` folder. Defaults to `false` on Windows and `true` on non-Windows. | `false` (Windows) / `true` (non-Windows) | None | Yes |

### `[ANVIL]`

What Anvil records on its own. You don't need to edit it.

| Key               | Type  | Description                                                   | Default    | Restriction                                         | Can be Changed |
| ----------------- | ----- | ------------------------------------------------------------- | ---------- | --------------------------------------------------- | -------------- |
| `last_check`      | `str` | Last time Anvil checked `@Mojang/bedrock-sample` for updates. | `datetime` | None                                                | Not Advised    |
| `vanilla_version` | `str` | The latest Minecraft version Anvil found.                     | `1.20.12`  | Automatically pulled from `@Mojang/bedrock-sample`. | No             |

## Example

```json
{
	"package": {
		"company": "StarkTMA",
		"namespace": "stark_mp",
		"project_name": "my_project",
		"display_name": "My Project",
		"project_description": "My Project Packs",
		"behavior_description": "My Project behavior Pack",
		"resource_description": "My Project Resource Pack",
		"target": "world"
	},
	"manifest": {
		"release": "1.0.0",
		"rp_uuid": ["00000000-0000-0000-0000-000000000000"],
		"bp_uuid": ["00000000-0000-0000-0000-000000000000"],
		"pack_uuid": "00000000-0000-0000-0000-000000000000",
		"data_module_uuid": "00000000-0000-0000-0000-000000000000",
		"resource_module_uuid": "00000000-0000-0000-0000-000000000000",
		"script_module_uuid": "00000000-0000-0000-0000-000000000000"
	},
	"features": {
		"scriptapi": true,
		"scriptui": true,
		"pbr": false,
		"experimental": false,
		"random_seed": false
	},
	"build": {
		"preview": false,
		"entry_point": "main.py",
		"js_bundle_script": "node esbuild.js",
		"minify": false,
		"add_stamp": true,
		"local_export": false
	},
	"anvil": {
		"last_check": "2024-01-16 19:06:58",
		"vanilla_version": "1.20.50.3"
	}
}
```

## Notes

- The `anvilconfig.json` file is automatically generated when you run the `anvil init` (or `anvil create`) command. You can modify the file at any time, but be cautious—some changes might have unexpected results.
- Project options that are not exposed as CLI flags during initialization (such as `pbr` and `random_seed`) are configured directly in this file under the `features` section.
- Missing keys in the `anvilconfig.json` file will be automatically handled by Anvil during runtime.
- You can add additional information to the `anvilconfig.json` file through the Anvil API. This is particularly useful for storing metadata not required during the project generation.
