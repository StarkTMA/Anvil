import os
import uuid
from datetime import datetime, timedelta
from enum import StrEnum

import click
import commentjson as json
import requests
from anvil.__version__ import __version__
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (
    PREVIEW_COM_MOJANG,
    RELEASE_COM_MOJANG,
    FileExists,
    validate_namespace_project_name,
)
from anvil.lib.reports import ReportCollector
from packaging.version import Version


class ConfigSection(StrEnum):
    """Configuration sections for the anvil config file.

    Defines the main sections that can be present in the configuration file.
    """

    ANVIL = "anvil"
    BUILD = "build"
    PACKAGE = "package"
    MINECRAFT = "minecraft"


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

    DEBUG = "debug"
    SCRIPT_API = "scriptapi"
    SCRIPT_UI = "scriptui"
    PBR = "pbr"
    RANDOM_SEED = "random_seed"
    PASCAL_PROJECT_NAME = "pascal_project_name"
    LAST_CHECK = "last_check"
    EXPERIMENTAL = "experimental"
    SCRIPT_MODULE_UUID = "script_module_uuid"
    DATA_MODULE_UUID = "data_module_uuid"
    PREVIEW = "preview"
    ENTRY_POINT = "entry_point"
    JS_BUNDLE_SCRIPT = "js_bundle_script"
    MINIFY = "minify"


class ConfigPackageTarget(StrEnum):
    """Package target types for anvil projects.

    Defines the types of packages that can be created.
    """

    WORLD = "world"
    ADDON = "addon"


class Config:
    """A class used to read and write to the config.ini file."""

    def __init__(self) -> None:
        """Initializes a Config object."""
        self._config = {}
        if FileExists("anvilconfig.json"):
            with open("anvilconfig.json", "r", encoding="utf-8") as f:
                self._config = json.loads(f.read())

    def save(self):
        """Saves the anvilconfig.json file."""
        with open("anvilconfig.json", "w") as f:
            f.write(json.dumps(self._config, indent=4))

    def add_section(self, section: str) -> None:
        """Adds a section to the anvilconfig.json file.

        Parameters:
            section (str): The section to add.
        """
        self._config[section] = {}

    def has_section(self, section: str) -> bool:
        """Checks if a section exists in the anvilconfig.json file.

        Parameters:
            section (str): The section to check.

        Returns:
            bool: True if the section exists, False otherwise.
        """
        return section in self._config

    def add_option(self, section: str, option: str, value):
        """Sets a value in the anvilconfig.json file.

        Parameters:
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

        Parameters:
            section (str): The section to check the option in.
            option (str): The option to check.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        return option in self._config[section]

    def get_option(self, section, option) -> str:
        """Gets a value from the anvilconfig.json file.

        Parameters:
            section (str): The section to get the value from.
            option (str): The option to get the value from.

        Returns:
            str: The value of the option.
        """
        return self._config[section][option]


class _AnvilConfig:
    """Main configuration class for Anvil instances (singleton).

    Manages all configuration settings, paths, and initialization
    for an Anvil project instance.
    """

    _instance = None

    COMPANY: str
    NAMESPACE: str
    PROJECT_NAME: str
    DISPLAY_NAME: str
    PROJECT_DESCRIPTION: str
    RESOURCE_DESCRIPTION: str
    BEHAVIOUR_DESCRIPTION: str

    RP_PATH: str
    BP_PATH: str

    _VANILLA_VERSION: str
    _RELEASE: str
    _DEBUG: bool
    _PASCAL_PROJECT_NAME: str
    _LAST_CHECK: str
    _TARGET: str
    _RP_UUID: list[str]
    _BP_UUID: list[str]
    _PACK_UUID: str
    _SCRIPT_API: bool
    _SCRIPT_UI: bool
    _PBR: bool
    _RANDOM_SEED: bool
    _EXPERIMENTAL: bool
    _DATA_MODULE_UUID: str
    _SCRIPT_MODULE_UUID: str
    _MINIFY: bool

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(_AnvilConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.Config = Config()

        click.clear()
        click.echo(
            "\n".join(
                [
                    f"{click.style('Anvil', 'cyan')} - by StarkTMA.",
                    f"Version {click.style(__version__, 'cyan')}.",
                    f"Copyright © {datetime.now().year} {click.style('StarkTMA', 'red')}.",
                    "All rights reserved.",
                    "",
                    "",
                ]
            )
        )

        self.Report = ReportCollector()
        self.Report.add_headers()

        self._load_configs()

        # GDK Setup preparation
        self._COM_MOJANG = PREVIEW_COM_MOJANG if self._PREVIEW else RELEASE_COM_MOJANG
        self._WORLD_PATH = os.path.join(
            self._COM_MOJANG, "minecraftWorlds", self.PROJECT_NAME
        )

        self.RP_PATH = os.path.join(
            self._COM_MOJANG, "development_resource_packs", f"RP_{self.PROJECT_NAME}"
        )
        self.BP_PATH = os.path.join(
            self._COM_MOJANG, "development_behavior_packs", f"BP_{self.PROJECT_NAME}"
        )

        if datetime.now() - datetime.strptime(
            self._LAST_CHECK, "%Y-%m-%d %H:%M:%S"
        ) > timedelta(hours=24):
            self._check_new_versions()

    def _handle_config(
        self, section: ConfigSection, option: ConfigOption, prompt
    ) -> None:
        if not self.Config.has_section(section):
            self.Config.add_section(section)
        if not self.Config.has_option(section, option):
            if prompt == "input":
                prompt = input(f"Missing '{option}': ")
            self.Config.add_option(section, option, prompt)
        return self.Config.get_option(section, option)

    def _load_configs(self) -> None:
        self.NAMESPACE = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.NAMESPACE, "input"
        )
        self.PROJECT_NAME = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME, "input"
        )

        self.COMPANY = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.COMPANY, "input"
        )
        self.DISPLAY_NAME = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME, "input"
        )
        self.PROJECT_DESCRIPTION = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION, "input"
        )
        self.BEHAVIOUR_DESCRIPTION = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.BEHAVIOUR_DESCRIPTION, "input"
        )
        self.RESOURCE_DESCRIPTION = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.RESOURCE_DESCRIPTION, "input"
        )
        self._DEBUG = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.DEBUG, False
        )
        self._PASCAL_PROJECT_NAME = self._handle_config(
            ConfigSection.ANVIL,
            ConfigOption.PASCAL_PROJECT_NAME,
            "".join(x[0] for x in self.PROJECT_NAME.split("_")).upper(),
        )

        self._VANILLA_VERSION = self._handle_config(
            ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD
        )
        self._TARGET = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.TARGET, "world"
        )

        self._RELEASE = self._handle_config(
            ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0"
        )
        self._LAST_CHECK = self._handle_config(
            ConfigSection.ANVIL,
            ConfigOption.LAST_CHECK,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        self._SCRIPT_API = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.SCRIPT_API, False
        )
        self._SCRIPT_UI = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.SCRIPT_UI, False
        )
        self._PBR = self._handle_config(ConfigSection.ANVIL, ConfigOption.PBR, False)
        self._RANDOM_SEED = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.RANDOM_SEED, False
        )
        self._EXPERIMENTAL = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.EXPERIMENTAL, False
        )
        self._PREVIEW = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.PREVIEW, False
        )
        self._ENTRY_POINT = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.ENTRY_POINT, "scripts/python/main.py"
        )

        self._RP_UUID = self._handle_config(
            ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())]
        )
        self._BP_UUID = self._handle_config(
            ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())]
        )
        self._PACK_UUID = self._handle_config(
            ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4())
        )
        self._DATA_MODULE_UUID = self._handle_config(
            ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4())
        )
        if self._SCRIPT_API:
            self._SCRIPT_MODULE_UUID = self._handle_config(
                ConfigSection.BUILD, ConfigOption.SCRIPT_MODULE_UUID, str(uuid.uuid4())
            )
            self._SCRIPT_BUNDLE_SCRIPT = self._handle_config(
                ConfigSection.ANVIL, ConfigOption.JS_BUNDLE_SCRIPT, "node esbuild.js"
            )

        if self._TARGET not in ConfigPackageTarget:
            raise ValueError(
                f"Invalid package target '{self._TARGET}'. Must be one of {list(ConfigPackageTarget)}."
            )

        self._MINIFY = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.MINIFY, False
        )

        validate_namespace_project_name(
            self.NAMESPACE, self.PROJECT_NAME, self._TARGET == "addon"
        )

    def _check_new_versions(self):
        click.echo(click.style("Checking for package updates...", fg="cyan"))

        try:
            vanilla_latest_build: str = json.loads(
                requests.get(
                    "https://raw.githubusercontent.com/Mojang/bedrock-samples/version.json"
                )
            )["latest"]["version"]
        except:
            vanilla_latest_build = MANIFEST_BUILD

        try:
            latest_build: str = (
                requests.get(
                    "https://raw.githubusercontent.com/StarkTMA/Anvil/main/src/anvil/__version__.py"
                )
                .split("=")[-1]
                .strip()
            )
        except:
            latest_build = __version__

        if Version(__version__) < Version(latest_build):
            click.echo(
                click.style(
                    f"\r[INFO]: A newer anvil build were found: [{latest_build}].",
                    fg="yellow",
                )
            )
        else:
            click.echo(click.style("\r[INFO]: Anvil is up to date.", fg="green"))

        self.Config.add_option(
            ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, vanilla_latest_build
        )
        self.Config.add_option(
            ConfigSection.ANVIL,
            ConfigOption.LAST_CHECK,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )


CONFIG = _AnvilConfig()
