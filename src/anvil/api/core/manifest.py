"""The resource and behavior pack manifests, and their pack settings."""

from typing import Annotated, ClassVar, Literal, Sequence

from anvil.lib.config import CONFIG, ConfigPackageTarget, Pack
from anvil.lib.format_versions import (
    MANIFEST_BUILD,
    MANIFEST_BUILD_PREVIEW,
    MANIFEST_VERSION,
    MODULE_MINECRAFT_SERVER,
    MODULE_MINECRAFT_SERVER_PREVIEW,
    MODULE_MINECRAFT_SERVER_UI,
    MODULE_MINECRAFT_SERVER_UI_PREVIEW,
)
from anvil.lib.jsonmodel import JsonFile, JsonObject, Length, Positive, json_field
from anvil.lib.translator import AnvilTranslator

__all__ = ["ManifestRP", "ManifestBP"]


# region Parts


class _ManifestHeader(JsonObject):
    """The `header` of a manifest: what the game shows of the pack and how it finds it."""

    description: str = json_field(default="pack.description")
    name: str = json_field(default="pack.name")
    uuid: str = json_field()
    version: str = json_field()
    min_engine_version: str = json_field()
    pack_scope: Literal["world", "global", "any"] | None = None

    def set_pack_scope(self, pack_scope: Literal["world", "global", "any"]) -> None:
        """Sets where the pack can be applied."""
        self.pack_scope = pack_scope


class _ManifestModule(JsonObject):
    """One of the pack's `modules`. Unset keys are left out."""

    type: Literal["resources", "data", "script", "world_template", "client_data"] = (
        json_field()
    )
    uuid: str = json_field()
    version: str = json_field()
    description: str | None = None
    language: Literal["javascript"] | None = None
    entry: str | None = None


class _ManifestDependency(JsonObject):
    """One of the pack's `dependencies`: another pack by its UUID, or a script module by
    its name."""

    uuid: str | None = None
    module_name: str | None = None
    version: str = json_field()

    def __validate__(self) -> None:
        if (self.uuid is None) == (self.module_name is None):
            raise ValueError("A dependency needs either a uuid or a module_name.")


class _ManifestMetadata(JsonObject):
    """The `metadata` of a manifest. Unset keys are left out."""

    authors: Annotated[list[str], Length(minimum=1)] = json_field()
    license: str | None = None
    url: str | None = None
    product_type: Literal["addon"] | None = None

    def set_product_type(self, product_type: Literal["addon"]) -> None:
        """Sets the context the pack is made for."""
        self.product_type = product_type


class _LabelSetting(JsonObject):
    """A read-only text in the pack settings."""

    type: Literal["label"] = json_field(default="label", init=False)
    text: str = json_field()


class _ToggleSetting(JsonObject):
    """A switch in the pack settings."""

    type: Literal["toggle"] = json_field(default="toggle", init=False)
    name: str = json_field()
    text: str = json_field()
    default: bool = json_field()


class _SliderSetting(JsonObject):
    """A slider in the pack settings."""

    type: Literal["slider"] = json_field(default="slider", init=False)
    name: str = json_field()
    text: str = json_field()
    min: float = json_field()
    max: float = json_field()
    step: Annotated[float, Positive] = json_field()
    default: float = json_field()

    def __validate__(self) -> None:
        if self.min >= self.max:
            raise ValueError(
                f"Slider '{self.name}': min '{self.min}' must be less than max '{self.max}'."
            )
        if not self.min <= self.default <= self.max:
            raise ValueError(
                f"Slider '{self.name}': default '{self.default}' must be between min "
                f"'{self.min}' and max '{self.max}'."
            )


class _DropdownOption(JsonObject):
    """One option of a dropdown."""

    name: str = json_field()
    text: str = json_field()


class _DropdownSetting(JsonObject):
    """A dropdown in the pack settings."""

    type: Literal["dropdown"] = json_field(default="dropdown", init=False)
    name: str = json_field()
    text: str = json_field()
    options: Annotated[list[_DropdownOption], Length(minimum=1)] = json_field()
    default: str = json_field()

    def __validate__(self) -> None:
        if self.default not in [option.name for option in self.options]:
            raise ValueError(
                f"Dropdown '{self.name}': default '{self.default}' is not one of its options."
            )


class _Manifest(JsonObject):
    """The content of a pack's `manifest.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "header",
        "modules",
    )

    format_version: int = json_field(default=MANIFEST_VERSION, init=False)
    header: _ManifestHeader | None = None
    modules: list[_ManifestModule] = json_field(default_factory=list)
    dependencies: list[_ManifestDependency] = json_field(
        default_factory=list, omit_default=True
    )
    capabilities: list[
        Literal[
            "chemistry", "editorExtension", "experimental_custom_ui", "raytraced", "pbr"
        ]
    ] = json_field(default_factory=list, omit_default=True)
    metadata: _ManifestMetadata | None = None
    settings: list[
        _LabelSetting | _ToggleSetting | _SliderSetting | _DropdownSetting
    ] = json_field(default_factory=list, omit_default=True)

    def set_header(self, uuid: str, version: str, min_engine_version: str) -> None:
        """Sets the pack's UUID, version and the game version it is made for."""
        self.header = _ManifestHeader(
            uuid=uuid, version=version, min_engine_version=min_engine_version
        )

    def add_module(
        self,
        type: Literal["resources", "data", "script", "world_template", "client_data"],
        uuid: str,
        version: str,
        *,
        language: Literal["javascript"] | None = None,
        entry: str | None = None,
    ) -> None:
        """Adds a module."""
        self.modules.append(
            _ManifestModule(
                type=type, uuid=uuid, version=version, language=language, entry=entry
            )
        )

    def add_pack_dependency(self, uuid: str, version: str) -> None:
        """Depends on another pack."""
        self.dependencies.append(_ManifestDependency(uuid=uuid, version=version))

    def add_module_dependency(self, module_name: str, version: str) -> None:
        """Depends on a script module, such as `@minecraft/server`."""
        self.dependencies.append(
            _ManifestDependency(module_name=module_name, version=version)
        )

    def add_capability(
        self,
        capability: Literal[
            "chemistry", "editorExtension", "experimental_custom_ui", "raytraced", "pbr"
        ],
    ) -> None:
        """Enables an optional feature."""
        if capability not in self.capabilities:
            self.capabilities.append(capability)

    def set_metadata(self, authors: list[str]) -> None:
        """Sets the authors of the pack."""
        self.metadata = _ManifestMetadata(authors=authors)

    def add_setting(
        self,
        setting: _LabelSetting | _ToggleSetting | _SliderSetting | _DropdownSetting,
    ) -> None:
        """Adds a pack setting. Two settings cannot share a name."""
        name = getattr(setting, "name", None)
        if name is not None and any(
            getattr(existing, "name", None) == name for existing in self.settings
        ):
            raise ValueError(f"Setting ID '{name}' is already used.")
        self.settings.append(setting)

    def count_settings(self, kind: type[JsonObject]) -> int:
        """How many settings of a kind the manifest has."""
        return sum(isinstance(setting, kind) for setting in self.settings)

    def __validate__(self) -> None:
        if self.header is None or self.metadata is None:
            raise ValueError("The manifest has no header or metadata.")


# endregion
# region Settings


class _ManifestSettings:
    """Adds pack settings to a manifest, shown in the game's pack settings screen. Their
    texts are localized as `pack.manifest.setting.<kind>_<n>`. Get it from
    `ManifestRP().settings` or `ManifestBP().settings`.
    """

    def __init__(self, manifest: "ManifestRP | ManifestBP") -> None:
        if MANIFEST_VERSION < 3:
            raise RuntimeError(
                "Settings labels are only supported in manifest version 3 and above."
            )
        self.manifest = manifest

    @property
    def _document(self) -> _Manifest:
        return self.manifest._content

    def _text(self, kind: str, text: str) -> str:
        key = f"pack.manifest.setting.{kind}"
        AnvilTranslator().add_localization_entry(key, text)
        return key

    def label(self, label: str) -> "_ManifestSettings":
        """Adds a read-only text.

        Args:
            label (str): The text.
        """
        count = self._document.count_settings(_LabelSetting)
        self._document.add_setting(
            _LabelSetting(text=self._text(f"label_{count}", label))
        )
        return self

    def toggle(self, id: str, text: str, default: bool = True) -> "_ManifestSettings":
        """Adds a switch, read with `Query.IsPackSettingEnabled(id)`.

        Args:
            id (str): The setting's name, written as `<namespace>:<id>`.
            text (str): The text shown next to it.
            default (bool, optional): Its value until the player changes it. Defaults to True.
        """
        count = self._document.count_settings(_ToggleSetting)
        self._document.add_setting(
            _ToggleSetting(
                name=f"{CONFIG.NAMESPACE}:{id}",
                text=self._text(f"toggle_{count}", text),
                default=default,
            )
        )
        return self

    def slider(
        self, id: str, text: str, min: float, max: float, step: float, default: float
    ) -> "_ManifestSettings":
        """Adds a slider, read with `Query.GetPackSetting(id)`.

        Args:
            id (str): The setting's name, written as `<namespace>:<id>`.
            text (str): The text shown next to it.
            min (float): The lowest value, below `max`.
            max (float): The highest value.
            step (float): The step between two values, above 0.
            default (float): Its value until the player changes it, from `min` to `max`.
        """
        count = self._document.count_settings(_SliderSetting)
        self._document.add_setting(
            _SliderSetting(
                name=f"{CONFIG.NAMESPACE}:{id}",
                text=self._text(f"slider_{count}", text),
                min=min,
                max=max,
                step=step,
                default=default,
            )
        )
        return self

    def dropdown(
        self, id: str, text: str, options: Sequence[tuple[str, str]], default: str
    ) -> "_ManifestSettings":
        """Adds a dropdown, read with `Query.IsPackSettingSelected(id, option)`.

        Args:
            id (str): The setting's name, written as `<namespace>:<id>`.
            text (str): The text shown next to it.
            options (Sequence[tuple[str, str]]): Each option as `(name, text)`.
            default (str): The name of the option selected until the player changes it.
        """
        count = self._document.count_settings(_DropdownSetting)
        prefix = f"dropdown_{count}"
        self._document.add_setting(
            _DropdownSetting(
                name=f"{CONFIG.NAMESPACE}:{id}",
                text=self._text(prefix, text),
                options=[
                    _DropdownOption(
                        name=name, text=self._text(f"{prefix}.option_{index}", label)
                    )
                    for index, (name, label) in enumerate(options)
                ],
                default=default,
            )
        )
        return self


# endregion
# region Manifests


class _PackManifest(JsonFile):
    """What both pack manifests share. Each is a singleton."""

    _document = _Manifest
    _extension = ".json"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _set_up(self, own_uuid: str, module: str, module_uuid: str, other_uuid: str):
        super().__init__("manifest")
        version = CONFIG._RELEASE
        self._content.set_header(
            own_uuid,
            version,
            MANIFEST_BUILD if not CONFIG._PREVIEW else MANIFEST_BUILD_PREVIEW,
        )
        self._content.add_module(module, module_uuid, version)
        self._content.add_pack_dependency(other_uuid, version)
        self._content.set_metadata([CONFIG.COMPANY])
        self._initialized = True

    @property
    def settings(self) -> _ManifestSettings:
        """Adds pack settings to the manifest."""
        return _ManifestSettings(self)

    def _setting_names(
        self, kind: Literal["toggle", "slider", "dropdown"]
    ) -> list[str]:
        """The names of the manifest's settings of a kind."""
        return [
            setting.name for setting in self._content.settings if setting.type == kind
        ]

    def _dropdown_options(self, name: str) -> list[str] | None:
        """The option names of a dropdown, or None when there is no such dropdown."""
        for setting in self._content.settings:
            if isinstance(setting, _DropdownSetting) and setting.name == name:
                return [option.name for option in setting.options]
        return None

    def _addon_target(self) -> None:
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            self._content.header.set_pack_scope("world")
            self._content.metadata.set_product_type("addon")


class ManifestRP(_PackManifest):
    """The resource pack's `manifest.json`. It depends on the behavior pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/addonsreference/packmanifest)
    """

    _instance = None
    _pack = Pack.RP
    _object_type = "Resource Pack Manifest"

    def __init__(self) -> None:
        """Initializes a ManifestRP instance."""
        if not hasattr(self, "_initialized"):
            self._set_up(
                CONFIG._RP_UUID[0],
                "resources",
                CONFIG._RESOURCE_MODULE_UUID,
                CONFIG._BP_UUID[0],
            )

    def queue(self) -> "ManifestRP":
        """Queues the manifest for export."""
        if self._queued:
            return self
        if CONFIG.PBR:
            self._content.add_capability("pbr")
        self._addon_target()
        return super().queue()


class ManifestBP(_PackManifest):
    """The behavior pack's `manifest.json`. It depends on the resource pack, and on the
    script modules when the project uses the Script API.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/addonsreference/packmanifest)
    """

    _instance = None
    _pack = Pack.BP
    _object_type = "Behavior Pack Manifest"

    def __init__(self) -> None:
        """Initializes a ManifestBP instance."""
        if not hasattr(self, "_initialized"):
            self._set_up(
                CONFIG._BP_UUID[0],
                "data",
                CONFIG._DATA_MODULE_UUID,
                CONFIG._RP_UUID[0],
            )

    def queue(self) -> "ManifestBP":
        """Queues the manifest for export."""
        if self._queued:
            return self
        if CONFIG._SCRIPT_API:
            preview = CONFIG._PREVIEW and CONFIG._EXPERIMENTAL
            self._content.add_module(
                "script",
                CONFIG._SCRIPT_MODULE_UUID,
                CONFIG._RELEASE,
                language="javascript",
                entry="scripts/main.js",
            )
            self._content.add_module_dependency(
                "@minecraft/server",
                MODULE_MINECRAFT_SERVER_PREVIEW if preview else MODULE_MINECRAFT_SERVER,
            )
            if CONFIG._SCRIPT_UI:
                self._content.add_module_dependency(
                    "@minecraft/server-ui",
                    (
                        MODULE_MINECRAFT_SERVER_UI_PREVIEW
                        if preview
                        else MODULE_MINECRAFT_SERVER_UI
                    ),
                )
        self._addon_target()
        return super().queue()


# endregion
