import json
import os
import uuid
from datetime import datetime
from enum import StrEnum

import requests

from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (FileExists, RemoveDirectory,
                           validate_namespace_project_name)
from anvil.lib.logger import Logger
from anvil.lib.reports import ReportCollector


class ConfigSection(StrEnum):
    ANVIL = "anvil"
    BUILD = "build"
    PACKAGE = "package"
    MINECRAFT = "minecraft"


class ConfigOption(StrEnum):
    VANILLA_VERSION = "vanilla_version"
    COMPANY = "company"
    NAMESPACE = "namespace"
    PROJECT_NAME = "project_name"
    DISPLAY_NAME = "display_name"
    PROJECT_DESCRIPTION = "project_description"
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


class Config:
    """A class used to read and write to the config.ini file."""

    def __init__(self) -> None:
        """Initializes a Config object."""
        self._config = {}
        if FileExists("anvilconfig.json"):
            with open("anvilconfig.json", "r") as f:
                self._config = json.loads(f.read())

    def save(self):
        """Saves the anvilconfig.json file."""
        with open("anvilconfig.json", "w") as f:
            f.write(json.dumps(self._config, indent=4))

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

    def add_option(self, section: str, option: str, value):
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

    def get_option(self, section, option) -> str:
        """Gets a value from the anvilconfig.json file.

        Args:
            section (str): The section to get the value from.
            option (str): The option to get the value from.

        Returns:
            str: The value of the option.
        """
        return self._config[section][option]


class _AnvilConfig:
    COMPANY: str
    NAMESPACE: str
    PROJECT_NAME: str
    DISPLAY_NAME: str
    PROJECT_DESCRIPTION: str

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

    def _handle_config(self, section: ConfigSection, option: ConfigOption, prompt) -> None:
        """Handles the config of the Anvil instance.

        Args:
            section (str): The section of the config.
            option (str): The option of the config.
        """
        if not self.Config.has_section(section):
            self.Config.add_section(section)
        if not self.Config.has_option(section, option):
            if prompt == "input":
                prompt = input(f"Missing '{option}': ")
            self.Config.add_option(section, option, prompt)
            self.Logger.config_added_option(section, option)
        return self.Config.get_option(section, option)

    def _load_configs(self) -> None:
        """Loads the configs of the Anvil instance."""
        self.NAMESPACE = self._handle_config(ConfigSection.PACKAGE, ConfigOption.NAMESPACE, "input")
        self.PROJECT_NAME = self._handle_config(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME, "input")

        self.COMPANY = self._handle_config(ConfigSection.PACKAGE, ConfigOption.COMPANY, "input")
        self.DISPLAY_NAME = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME, "input"
        )
        self.PROJECT_DESCRIPTION = self._handle_config(
            ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION, "input"
        )
        self._DEBUG = self._handle_config(ConfigSection.ANVIL, ConfigOption.DEBUG, False)
        self._PASCAL_PROJECT_NAME = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.PASCAL_PROJECT_NAME, "".join(x[0] for x in self.PROJECT_NAME.split("_")).upper()
        )

        self._VANILLA_VERSION = self._handle_config(ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD)
        self._TARGET = self._handle_config(ConfigSection.PACKAGE, ConfigOption.TARGET, "world")

        self._RELEASE = self._handle_config(ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0")
        self._LAST_CHECK = self._handle_config(
            ConfigSection.ANVIL, ConfigOption.LAST_CHECK, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self._RP_UUID = self._handle_config(ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())])
        self._BP_UUID = self._handle_config(ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())])
        self._PACK_UUID = self._handle_config(ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4()))

        self._SCRIPT_API = self._handle_config(ConfigSection.ANVIL, ConfigOption.SCRIPT_API, False)
        self._SCRIPT_UI = self._handle_config(ConfigSection.ANVIL, ConfigOption.SCRIPT_UI, False)
        self._PBR = self._handle_config(ConfigSection.ANVIL, ConfigOption.PBR, False)
        self._RANDOM_SEED = self._handle_config(ConfigSection.ANVIL, ConfigOption.RANDOM_SEED, False)
        self._EXPERIMENTAL = self._handle_config(ConfigSection.ANVIL, ConfigOption.EXPERIMENTAL, False)

        if self._TARGET not in ["world", "addon"]:
            self.Logger.invalid_target(self._TARGET)

        validate_namespace_project_name(self.NAMESPACE, self.PROJECT_NAME, self._TARGET=="addon")

    def _check_new_vanilla_version(self):
        self.Logger.check_update()
        try:
            j = requests.get("https://raw.githubusercontent.com/Mojang/bedrock-samples/main/version.json")
            latest_build = json.loads(j.text)["latest"]["version"]
            RemoveDirectory(os.path.join("assets", "cache"))
        except:
            latest_build = self._VANILLA_VERSION

        if self._VANILLA_VERSION < latest_build:
            self.Logger.new_minecraft_build(self._VANILLA_VERSION, latest_build)
        else:
            self.Logger.minecraft_build_up_to_date()

        self.Config.add_option(ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, latest_build)
        self.Config.add_option(ConfigSection.ANVIL, ConfigOption.LAST_CHECK, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def __init__(self) -> None:
        self.Config = Config()

        self.Logger = Logger()
        self.Logger.header()

        self.Report = ReportCollector()
        self.Report.add_headers()

        self._load_configs()

        self.RP_PATH = os.path.join("resource_packs", f"RP_{self._PASCAL_PROJECT_NAME}")
        self.BP_PATH = os.path.join("behavior_packs", f"BP_{self._PASCAL_PROJECT_NAME}")

        if int((datetime.now() - datetime.strptime(self._LAST_CHECK, "%Y-%m-%d %H:%M:%S")).total_seconds()) > 12 * 3600:
            self._check_new_vanilla_version()