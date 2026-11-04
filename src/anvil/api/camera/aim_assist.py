"""Aim assist presets and categories, used by a camera preset's aim assist."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from anvil.lib.config import Pack
from anvil.lib.format_versions import AIM_ASSIST_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    JsonValue,
    Kept,
    Keyed,
    json_field,
)

_PRESETS_FOLDER = Path("cameras", "presets")


class _AimAssistItemSetting(JsonValue):
    """One entry of `item_settings`: the category used while the item is held.

    Args:
        item (str): The item identifier.
        category (str): The aim assist category name.
    """

    item: str = json_field(exclude=True)
    category: str = json_field()


class _AimAssistPreset(JsonObject):
    """The `minecraft:aim_assist_preset` object. Unset keys are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None
    item_settings: Annotated[list[_AimAssistItemSetting], Keyed("item")] = json_field(
        default_factory=list, omit_default=True
    )
    default_item_settings: str | None = None
    hand_settings: str | None = None
    exclusion_list: list[str] = json_field(default_factory=list, omit_default=True)
    liquid_targeting_list: list[str] = json_field(
        default_factory=list, omit_default=True
    )

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the preset's identifier, already parsed by the file."""
        self.identifier = identifier

    def add_item_setting(self, item: str, category: str) -> None:
        """Uses `category` while `item` is held. Setting an item again replaces its category."""
        self.item_settings = [
            setting for setting in self.item_settings if setting.item != item
        ]
        self.item_settings.append(_AimAssistItemSetting(item=item, category=category))

    def set_default_item_settings(self, category: str) -> None:
        """Sets the category used for items not in `item_settings`."""
        self.default_item_settings = category

    def set_hand_settings(self, category: str) -> None:
        """Sets the category used with an empty hand."""
        self.hand_settings = category

    def set_exclusion_list(self, exclusions: list[str]) -> None:
        """Sets the blocks and entities aim assist never targets."""
        self.exclusion_list = list(exclusions)

    def set_liquid_targeting_list(self, targets: list[str]) -> None:
        """Sets the items that target liquids while held."""
        self.liquid_targeting_list = list(targets)

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The aim assist preset has no identifier.")


class _AimAssistPresetFile(JsonObject):
    """The content of an aim assist preset file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:aim_assist_preset",
    )

    format_version: str = json_field(default=AIM_ASSIST_VERSION, init=False)
    preset: _AimAssistPreset = json_field(
        key="minecraft:aim_assist_preset", default_factory=_AimAssistPreset
    )


class AimAssistPreset(JsonFile):
    """An aim assist preset: which category is used for each held item, and what aim assist
    never targets. Camera presets use one through `CameraPreset.aim_assist`, the
    `/aimassist` command by its identifier.

    Written to the behavior pack's `cameras/presets/` folder.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/aimassistpresets)
    """

    _document = _AimAssistPresetFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = _PRESETS_FOLDER
    _object_type = "Aim Assist Preset"

    def __init__(self, name: str) -> None:
        """Initializes the Aim Assist Preset.

        Args:
            name (str): The preset's name, also its file name. The identifier is
                `<namespace>:<name>`.
        """
        super().__init__(name)
        self._content.preset.set_identifier(self.identifier)

    def item_setting(self, item: str, category: str) -> "AimAssistPreset":
        """Uses an aim assist category while an item is held.

        Args:
            item (str): The item identifier.
            category (str): The name of a category in `AimAssistCategories`.
        """
        self._content.preset.add_item_setting(item, category)
        return self

    def default_item_settings(self, category: str) -> "AimAssistPreset":
        """Sets the aim assist category for items not given an `item_setting`.

        Args:
            category (str): The category name.
        """
        self._content.preset.set_default_item_settings(category)
        return self

    def hand_settings(self, category: str) -> "AimAssistPreset":
        """Sets the aim assist category used when the player holds nothing.

        Args:
            category (str): The category name.
        """
        self._content.preset.set_hand_settings(category)
        return self

    def exclusion_list(self, exclusions: list[str]) -> "AimAssistPreset":
        """Sets the entities and blocks aim assist ignores.

        Args:
            exclusions (list[str]): The block and entity identifiers to exclude, such as
                `"minecraft:bedrock"`.
        """
        self._content.preset.set_exclusion_list(exclusions)
        return self

    def liquid_targeting_list(self, targets: list[str]) -> "AimAssistPreset":
        """Sets the items that are allowed to target liquids.

        Args:
            targets (list[str]): The item identifiers that target liquids while held, such
                as `"minecraft:bucket"`.
        """
        self._content.preset.set_liquid_targeting_list(targets)
        return self

    def queue(self) -> "AimAssistPreset":
        """Queues the aim assist preset for export."""
        return super().queue()


class _AimAssistPriority(JsonValue):
    """One block or entity of a category's priorities, written as `identifier: priority`.

    Args:
        identifier (str): The block or entity identifier.
        priority (int): The priority. Larger numbers are preferred.
    """

    identifier: str = json_field(exclude=True)
    priority: int = json_field()


class _AimAssistCategoryPriorities(JsonObject):
    """The `priorities` of a category. Unset keys are left out."""

    entity_default: int | None = None
    block_default: int | None = None
    entities: Annotated[list[_AimAssistPriority], Keyed("identifier")] = json_field(
        default_factory=list, omit_default=True
    )
    blocks: Annotated[list[_AimAssistPriority], Keyed("identifier")] = json_field(
        default_factory=list, omit_default=True
    )

    def set_entity_default(self, priority: int) -> None:
        """Sets the priority of entities not in `entities`."""
        self.entity_default = priority

    def set_block_default(self, priority: int) -> None:
        """Sets the priority of blocks not in `blocks`."""
        self.block_default = priority

    def add_entity(self, entity: str, priority: int) -> None:
        """Sets an entity's priority, replacing an earlier one."""
        self.entities = [item for item in self.entities if item.identifier != entity]
        self.entities.append(_AimAssistPriority(identifier=entity, priority=priority))

    def add_block(self, block: str, priority: int) -> None:
        """Sets a block's priority, replacing an earlier one."""
        self.blocks = [item for item in self.blocks if item.identifier != block]
        self.blocks.append(_AimAssistPriority(identifier=block, priority=priority))


class AimAssistCategory(JsonObject):
    """An aim assist category: the targeting priority of blocks and entities. Made by
    `AimAssistCategories.add_category`.

    Args:
        name (str): The category name, used by `AimAssistPreset`.
    """

    name: str = json_field(positional=True)
    priorities: Annotated[_AimAssistCategoryPriorities, Kept] = json_field(
        default_factory=_AimAssistCategoryPriorities
    )

    def entity_default(self, value: int) -> "AimAssistCategory":
        """Sets the priority of entities without their own priority.

        Args:
            value (int): The priority.
        """
        self.priorities.set_entity_default(value)
        return self

    def block_default(self, value: int) -> "AimAssistCategory":
        """Sets the priority of blocks without their own priority.

        Args:
            value (int): The priority.
        """
        self.priorities.set_block_default(value)
        return self

    def block_priority(self, block: str, priority: int) -> "AimAssistCategory":
        """Sets the priority of a block.

        Args:
            block (str): The block identifier.
            priority (int): The priority. Larger numbers are preferred.
        """
        self.priorities.add_block(block, priority)
        return self

    def entity_priority(self, entity: str, priority: int) -> "AimAssistCategory":
        """Sets the priority of an entity.

        Args:
            entity (str): The entity identifier.
            priority (int): The priority. Larger numbers are preferred.
        """
        self.priorities.add_entity(entity, priority)
        return self


class _AimAssistCategoryList(JsonObject):
    """The `minecraft:aim_assist_categories` object."""

    categories: list[AimAssistCategory] = json_field(default_factory=list)

    def add_category(self, category: AimAssistCategory) -> None:
        """Adds a category. Two categories cannot share a name."""
        if any(item.name == category.name for item in self.categories):
            raise ValueError(f"Aim assist category '{category.name}' already exists.")
        self.categories.append(category)


class _AimAssistCategoriesFile(JsonObject):
    """The content of `cameras/presets/categories.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:aim_assist_categories",
    )

    format_version: str = json_field(default=AIM_ASSIST_VERSION, init=False)
    categories: _AimAssistCategoryList = json_field(
        key="minecraft:aim_assist_categories", default_factory=_AimAssistCategoryList
    )


class AimAssistCategories(JsonFile):
    """The aim assist categories of the pack, written next to the aim assist presets as
    `categories.json`. Only one category is active at a time, chosen by the held item.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/aimassistpresets#aim-assist-categories)
    """

    _document = _AimAssistCategoriesFile
    _extension = ".json"
    _pack = Pack.BP
    _folder = _PRESETS_FOLDER
    _object_type = "Aim Assist Categories"

    def __init__(self) -> None:
        """Initializes the Aim Assist Categories file."""
        super().__init__("categories")

    def add_category(self, category: str) -> AimAssistCategory:
        """Adds an aim assist category and returns it.

        Args:
            category (str): The category name.
        """
        part = AimAssistCategory(category)
        self._content.categories.add_category(part)
        return part

    def queue(self) -> "AimAssistCategories":
        """Queues the aim assist categories for export."""
        return super().queue()
