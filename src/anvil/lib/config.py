import copy
import re
import sys
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import MISSING, dataclass, field, fields, replace
from datetime import datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any

import click
import orjson

from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (
    PREVIEW_COM_MOJANG,
    RELEASE_COM_MOJANG,
    AnvilDisplay,
    AnvilValidator,
)
from anvil.lib.reports import ReportCollector


class ConfigSection(StrEnum):
    """The sections of `anvilconfig.json`.

    - `package`: what the project is: its namespace, names, descriptions and target.
    - `manifest`: what the pack manifests carry: the release version and the UUIDs.
    - `features`: what the project's content uses: Script API, Script UI, PBR,
      experimental features and the world's random seed.
    - `build`: how the project is built and exported.
    - `anvil`: what Anvil records on its own: the last version check and the latest
      vanilla version it found.
    """

    PACKAGE = "package"
    MANIFEST = "manifest"
    FEATURES = "features"
    BUILD = "build"
    ANVIL = "anvil"


class ConfigOption(StrEnum):
    """Configuration options available in the anvil config file.

    Defines all the configuration keys that can be set in various sections
    of the configuration file.
    """

    VANILLA_VERSION = "vanilla_version"
    COMPANY = "company"
    NAMESPACE = "namespace"
    PROJECT_NAME = "project_name"
    DISPLAY_NAME = "display_name"
    PROJECT_DESCRIPTION = "project_description"
    RESOURCE_DESCRIPTION = "resource_description"
    BEHAVIOUR_DESCRIPTION = "behavior_description"

    TARGET = "target"

    RELEASE = "release"
    BP_UUID = "bp_uuid"
    RP_UUID = "rp_uuid"
    PACK_UUID = "pack_uuid"

    SCRIPT_API = "scriptapi"
    SCRIPT_UI = "scriptui"
    PBR = "pbr"
    RANDOM_SEED = "random_seed"
    LAST_CHECK = "last_check"
    EXPERIMENTAL = "experimental"
    SCRIPT_MODULE_UUID = "script_module_uuid"
    DATA_MODULE_UUID = "data_module_uuid"
    RESOURCE_MODULE_UUID = "resource_module_uuid"
    PREVIEW = "preview"
    ENTRY_POINT = "entry_point"
    JS_BUNDLE_SCRIPT = "js_bundle_script"
    MINIFY = "minify"
    ADD_STAMP = "add_stamp"
    LOCAL_EXPORT = "local_export"


class Pack(StrEnum):
    """The packs an Anvil project writes files to."""

    RP = "resource_pack"
    BP = "behavior_pack"


class ConfigPackageTarget(StrEnum):
    """Package target types for anvil projects.

    Defines the types of packages that can be created.
    """

    WORLD = "world"
    ADDON = "addon"


CONFIG_FILE = Path("anvilconfig.json")
"""The project's config file, in the current folder."""


class Config:
    """A class used to read and write to the config.ini file."""

    def __init__(self, allow_missing: bool = False) -> None:
        """Initializes a Config object."""
        self._config: dict[str, Any] = {}
        if CONFIG_FILE.exists():
            self._config = orjson.loads(CONFIG_FILE.read_bytes())
        elif not allow_missing:
            click.echo(
                click.style(
                    "Not a valid anvil project. run 'anvil --help' for more info.",
                    fg="red",
                )
            )
            exit(1)

    def save(self):
        """Saves the anvilconfig.json file."""
        with CONFIG_FILE.open("wb") as f:
            f.write(
                orjson.dumps(
                    self._config, option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS
                )
            )

    def add_section(self, section: str) -> None:
        """Adds a section to the anvilconfig.json file.

        Args:
            section (str): The section to add.
        """
        self._config[section] = {}

    def has_section(self, section: str) -> bool:
        """Checks if a section exists in the anvilconfig.json file.

        Args:
            section (str): The section to check.

        Returns:
            bool: True if the section exists, False otherwise.
        """
        return section in self._config

    def add_option(
        self,
        section: str,
        option: str,
        value: str | bool | int | float | list[str | bool | int | float],
    ) -> None:
        """Sets a value in the anvilconfig.json file.

        Args:
            section (str): The section to set the value in.
            option (str): The option to set the value in.
            value (Any): The value to set.
        """
        if not self.has_section(section):
            self.add_section(section)

        self._config[section][option] = value
        self.save()

    def has_option(self, section: str, option: str) -> bool:
        """Checks if an option exists in the anvilconfig.json file.

        Args:
            section (str): The section to check the option in.
            option (str): The option to check.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        return option in self._config[section]

    def get_option(self, section: ConfigSection, option: ConfigOption) -> Any:
        """Gets a value from the anvilconfig.json file.

        Args:
            section (ConfigSection): The section to get the value from.
            option (ConfigOption): The option to get the value from.

        Returns:
            Any: The value of the option.
        """
        return self._config[section][option]


def _initials(project_name: str) -> str:
    return "".join(x[0] for x in project_name.split("_")).upper()


NAMESPACE_PATTERN = re.compile(r"(?!minecraft$)[a-z][a-z0-9_]{0,7}")
"""A project namespace: 1 to 8 lowercase letters, digits or `_`, starting with a letter, and
not `minecraft`."""

PROJECT_NAME_PATTERN = re.compile(r"[a-z][a-z0-9_]{0,15}")
"""A project name: 1 to 16 lowercase letters, digits or `_`, starting with a letter."""


def validate_namespace_project_name(
    namespace: str, project_name: str, is_addon: bool = False
) -> None:
    """Validates the namespace and project name against `NAMESPACE_PATTERN` and
    `PROJECT_NAME_PATTERN`. An addon's namespace must also end with `_` and the project
    name's initials, `stark_mp` for `my_project`.

    Args:
        namespace (str): The namespace to validate.
        project_name (str): The project name to validate.
        is_addon (bool, optional): Whether this is for an addon. Defaults to False.

    Raises:
        ValueError: If validation fails for any requirement.
    """
    if not NAMESPACE_PATTERN.fullmatch(namespace):
        raise ValueError(
            f"Invalid namespace '{namespace}'. A namespace is 1 to 8 lowercase letters, digits "
            "or '_', starts with a letter, and cannot be 'minecraft'."
        )

    if not PROJECT_NAME_PATTERN.fullmatch(project_name):
        raise ValueError(
            f"Invalid project name '{project_name}'. A project name is 1 to 16 lowercase "
            "letters, digits or '_', and starts with a letter."
        )

    initials = _initials(project_name).lower()
    if is_addon and not re.fullmatch(rf"[a-z0-9_]+_{initials}", namespace):
        raise ValueError(
            f"Invalid namespace '{namespace}'. An addon's namespace must end with the project "
            f"name's initials, for example '{namespace.split('_')[0]}_{initials}'."
        )


def _option(
    section: ConfigSection,
    name: ConfigOption,
    default: Any = MISSING,
    *,
    factory: Any = MISSING,
    script: bool = False,
) -> Any:
    """A setting read from the `name` option of the `section` section of `anvilconfig.json`.

    Args:
        section (ConfigSection): The section the option is in.
        name (ConfigOption): The option.
        default (Any, optional): The value when the option is missing. Without a default or
            a factory, the option is required.
        factory (Callable, optional): Makes the value when the option is missing.
        script (bool, optional): The option is only written to the file for projects that
            use the Script API.
    """
    return field(
        default=default,
        default_factory=factory,
        metadata={"section": section, "name": name, "script": script},
    )


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass(kw_only=True)
class AnvilConfig:
    """The settings of an Anvil project, read from its `anvilconfig.json`.

    It only holds values: building one never prompts, prints, writes a file or uses the
    network. `load_project` does that work for the project in the current folder.

    `CONFIG` is the shared instance. It loads the project in the current folder the
    first time one of its settings is read.
    """

    NAMESPACE: str = _option(ConfigSection.PACKAGE, ConfigOption.NAMESPACE)
    PROJECT_NAME: str = _option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME)
    COMPANY: str = _option(ConfigSection.PACKAGE, ConfigOption.COMPANY)
    DISPLAY_NAME: str = _option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME)
    PROJECT_DESCRIPTION: str = _option(
        ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION
    )
    BEHAVIOUR_DESCRIPTION: str = _option(
        ConfigSection.PACKAGE, ConfigOption.BEHAVIOUR_DESCRIPTION
    )
    RESOURCE_DESCRIPTION: str = _option(
        ConfigSection.PACKAGE, ConfigOption.RESOURCE_DESCRIPTION
    )
    _TARGET: str = _option(ConfigSection.PACKAGE, ConfigOption.TARGET, "world")

    _RELEASE: str = _option(ConfigSection.MANIFEST, ConfigOption.RELEASE, "1.0.0")
    _RP_UUID: list[str] = _option(
        ConfigSection.MANIFEST, ConfigOption.RP_UUID, factory=lambda: [_new_uuid()]
    )
    _BP_UUID: list[str] = _option(
        ConfigSection.MANIFEST, ConfigOption.BP_UUID, factory=lambda: [_new_uuid()]
    )
    _PACK_UUID: str = _option(
        ConfigSection.MANIFEST, ConfigOption.PACK_UUID, factory=_new_uuid
    )
    _DATA_MODULE_UUID: str = _option(
        ConfigSection.MANIFEST, ConfigOption.DATA_MODULE_UUID, factory=_new_uuid
    )
    _RESOURCE_MODULE_UUID: str = _option(
        ConfigSection.MANIFEST, ConfigOption.RESOURCE_MODULE_UUID, factory=_new_uuid
    )
    _SCRIPT_MODULE_UUID: str = _option(
        ConfigSection.MANIFEST,
        ConfigOption.SCRIPT_MODULE_UUID,
        factory=_new_uuid,
        script=True,
    )

    _SCRIPT_API: bool = _option(ConfigSection.FEATURES, ConfigOption.SCRIPT_API, False)
    _SCRIPT_UI: bool = _option(ConfigSection.FEATURES, ConfigOption.SCRIPT_UI, False)
    PBR: bool = _option(ConfigSection.FEATURES, ConfigOption.PBR, False)
    _RANDOM_SEED: bool = _option(
        ConfigSection.FEATURES, ConfigOption.RANDOM_SEED, False
    )
    _EXPERIMENTAL: bool = _option(
        ConfigSection.FEATURES, ConfigOption.EXPERIMENTAL, False
    )

    _PREVIEW: bool = _option(ConfigSection.BUILD, ConfigOption.PREVIEW, False)
    _ENTRY_POINT: str = _option(
        ConfigSection.BUILD, ConfigOption.ENTRY_POINT, "scripts/python/main.py"
    )
    _SCRIPT_BUNDLE_SCRIPT: str = _option(
        ConfigSection.BUILD,
        ConfigOption.JS_BUNDLE_SCRIPT,
        "node esbuild.js",
        script=True,
    )
    _MINIFY: bool = _option(ConfigSection.BUILD, ConfigOption.MINIFY, False)
    _ADD_STAMP: bool = _option(ConfigSection.BUILD, ConfigOption.ADD_STAMP, True)
    _LOCAL_EXPORT: bool = _option(
        ConfigSection.BUILD,
        ConfigOption.LOCAL_EXPORT,
        factory=lambda: sys.platform != "win32",
    )

    _LAST_CHECK: str = _option(
        ConfigSection.ANVIL, ConfigOption.LAST_CHECK, factory=_now
    )
    _VANILLA_VERSION: str = _option(
        ConfigSection.ANVIL, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD
    )

    Report: ReportCollector = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        if len(self._RELEASE.split(".")) > 3:
            raise ValueError(
                "Invalid release version, must be in format X.X.X. Read more at https://semver.org/"
            )
        if self._TARGET not in ConfigPackageTarget:
            raise ValueError(
                f"Invalid package target '{self._TARGET}'. Must be one of {list(ConfigPackageTarget)}."
            )
        self._LOCAL_EXPORT = bool(self._LOCAL_EXPORT) or sys.platform != "win32"
        validate_namespace_project_name(
            self.NAMESPACE, self.PROJECT_NAME, self._TARGET == ConfigPackageTarget.ADDON
        )
        self.Report = ReportCollector()
        self.Report.add_headers()

    def __getattr__(self, name: str) -> Any:
        if self is not CONFIG or self.__dict__ or name.startswith("__"):
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
        use(load_project())
        return getattr(self, name)

    @classmethod
    def from_dict(cls, data: dict[str, dict[str, Any]]) -> "AnvilConfig":
        """Reads the settings of a project from the content of its `anvilconfig.json`.

        Args:
            data (dict): The `package`, `manifest`, `features`, `build` and `anvil` sections. Missing
                options other than the package ones get their default.

        Raises:
            ValueError: A package option is missing, the release is not X.X.X, or the target
                is unknown.
        """
        values = {}
        for option in fields(cls):
            if not option.metadata:
                continue
            section, name = option.metadata["section"], option.metadata["name"]
            if name in data.get(section, {}):
                values[option.name] = data[section][name]
            elif option.default is MISSING and option.default_factory is MISSING:
                raise ValueError(
                    f"Missing '{name}' in the '{section}' section of anvilconfig.json."
                )
        return cls(**values)

    @classmethod
    def from_file(cls, path: str | Path = "anvilconfig.json") -> "AnvilConfig":
        """Reads the settings of the project whose `anvilconfig.json` is at `path`.

        Args:
            path (str | Path, optional): The config file. Defaults to the one in the current
                folder.
        """
        return cls.from_dict(orjson.loads(Path(path).read_bytes()))

    @property
    def _DEBUG(self) -> bool:
        """If the build was started with `--debug`."""
        return "--debug" in sys.argv

    @property
    def _PASCAL_PROJECT_NAME(self) -> str:
        """The initials of the project name, `sugar_rush` as `SR`."""
        return _initials(self.PROJECT_NAME)

    @property
    def _COM_MOJANG(self) -> Path:
        """The `com.mojang` folder the packs are exported to."""
        if self._LOCAL_EXPORT:
            return Path.cwd() / "output" / "com.mojang"
        return PREVIEW_COM_MOJANG if self._PREVIEW else RELEASE_COM_MOJANG

    @property
    def RP_PATH(self) -> Path:
        """The development resource pack folder."""
        return (
            self._COM_MOJANG / "development_resource_packs" / f"RP_{self.PROJECT_NAME}"
        )

    @property
    def BP_PATH(self) -> Path:
        """The development behavior pack folder."""
        return (
            self._COM_MOJANG / "development_behavior_packs" / f"BP_{self.PROJECT_NAME}"
        )

    @property
    def _WORLD_PATH(self) -> Path:
        """The development world folder."""
        return self._COM_MOJANG / "minecraftWorlds" / self.PROJECT_NAME


CONFIG: AnvilConfig = object.__new__(AnvilConfig)


def load_project() -> AnvilConfig:
    """Loads the project in the current folder.

    Asks for the missing package options, writes them and the defaults of other missing
    options to `anvilconfig.json`, shows the project banner, checks for new versions
    once a day and, when run with `--clean`, deletes the development packs.

    Returns:
        AnvilConfig: The project's settings.
    """
    file = Config()
    options = [option for option in fields(AnvilConfig) if option.metadata]
    for option in options:
        section, name = option.metadata["section"], option.metadata["name"]
        if option.default is MISSING and option.default_factory is MISSING:
            if name not in file._config.get(section, {}):
                file.add_option(section, name, input(f"Missing '{name}': "))

    config = AnvilConfig.from_dict(file._config)
    for option in options:
        section, name = option.metadata["section"], option.metadata["name"]
        if option.metadata["script"] and not config._SCRIPT_API:
            continue
        if name not in file._config.get(section, {}):
            file.add_option(section, name, getattr(config, option.name))

    AnvilDisplay.copyright()
    AnvilDisplay.project_display(config.DISPLAY_NAME, config._TARGET, config._PREVIEW)

    if datetime.now() - datetime.strptime(
        config._LAST_CHECK, "%Y-%m-%d %H:%M:%S"
    ) > timedelta(hours=24):
        vanilla_latest_build, latest_build = AnvilValidator.check_new_versions()
        file.add_option(
            ConfigSection.ANVIL, ConfigOption.VANILLA_VERSION, vanilla_latest_build
        )
        file.add_option(ConfigSection.ANVIL, ConfigOption.LAST_CHECK, _now())

    if "--clean" in sys.argv:
        from anvil.api.core.core import clean_old_dev

        clean_old_dev(config)

    return config


def use(config: AnvilConfig | None) -> None:
    """Makes `CONFIG` hold the settings of `config`.

    Args:
        config (AnvilConfig | None): The settings. None empties `CONFIG`, so it loads the
            project in the current folder on the next read.
    """
    CONFIG.__dict__.clear()
    if config is not None:
        CONFIG.__dict__.update(config.__dict__)


@contextmanager
def override(config: AnvilConfig | None = None, **values: Any) -> Iterator[AnvilConfig]:
    """Changes the settings in `CONFIG` for the length of a `with` block.

    Args:
        config (AnvilConfig, optional): The settings to use. Defaults to the current ones.
        **values: Settings to change, by attribute name, such as `PBR=True`.

    Yields:
        AnvilConfig: `CONFIG`.
    """
    previous = copy.copy(CONFIG)
    use(replace(config if config is not None else CONFIG, **values))
    try:
        yield CONFIG
    finally:
        use(previous)
