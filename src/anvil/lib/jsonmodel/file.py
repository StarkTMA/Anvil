"""`JsonFile`, the base of every JSON file an Anvil project writes to a pack."""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from anvil.api.core.types import JsonSchema
from anvil.lib.config import CONFIG, ConfigPackageTarget, Pack
from anvil.lib.lib import AnvilIO

from .identifier import Identifier

if TYPE_CHECKING:
    from .object import JsonObject


class JsonFile:
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    Attributes:
        name (str): The name of the addon object.
        is_vanilla (bool): Indicates if the object is from vanilla Minecraft.
        object_type (str, optional): The type of the addon object.
    """

    _extension = ".json"
    _pack: Pack | None = None
    _folder = ""
    _object_type = "addon_object"
    _queued = False
    _document: ClassVar[type[JsonObject] | None] = None
    """The typed content of the file. When set, `_content` starts as an empty document and
    `__schema__()` describes the file."""
    _file_name: str | None = None
    """The file's name when it is not the identifier's name, such as `global`."""

    def __init__(
        self, name: str, is_vanilla: bool = False, *, identifier: str | None = None
    ) -> None:
        """
        Constructs all the necessary attributes for the JsonFile object.

        Args:
            name (str): The file name. Without `identifier`, it is also the identifier, and the
                file is named after the identifier's name.
            is_vanilla (bool, optional): If the file overrides a vanilla definition. Packages
                of type addon cannot.
            identifier (str, optional): The identifier the file writes, when it is not the
                file name.

        Raises:
            ValueError: When the identifier is not valid (see `Identifier.parse`), or a vanilla
                override is not allowed.
        """
        if is_vanilla and CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError(
                f"Overriding vanilla features is not allowed for packages of type "
                f"'{CONFIG._TARGET}'. {self._object_type}[{name}]"
            )
        self._identifier = Identifier.parse(
            name if identifier is None else identifier,
            vanilla=is_vanilla,
            object_type=self._object_type,
        )
        if identifier is not None:
            self._file_name = name
        if CONFIG._DEBUG:
            self._created_from = traceback.format_stack()[:-1]

        self._directory = ""
        self._content = self._document() if self._document else {}

    @property
    def identifier(self) -> Identifier:
        """The file's identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """The identifier's name, without its namespace."""
        return self.identifier.name

    def __str__(self) -> str:
        return self.identifier

    @classmethod
    def __schema__(cls) -> JsonSchema:
        """The JSON Schema (draft 2020-12) of this file: the schema of its `_document`, with
        the file's type as `title` and where it is written under `x-anvil-file`.

        Raises:
            TypeError: If the file has no typed `_document` yet.
        """
        if cls._document is None:
            raise TypeError(f"{cls.__name__} is not typed yet, so it has no schema.")
        file = {
            "pack": cls._pack,
            "folder": cls._folder,
            "name": cls._file_name,
            "extension": cls._extension,
        }
        schema = cls._document.__schema__()
        return {
            "$schema": schema.pop("$schema"),
            "title": cls._object_type,
            "x-anvil-file": {key: str(value) for key, value in file.items() if value},
            **schema,
        }

    def content(self, content) -> "JsonFile":
        """
        Sets the content of the addon object and returns the object.

        Args:
            content (any): The content to be set for the addon object.

        Returns:
            self: The instance of the current JsonFile.
        """
        self._content = content
        return self

    def queue(self, directory: str | None = None) -> "JsonFile":
        """
        Queues the addon object for processing and logs the event.

        Args:
            directory (str, optional): The directory of the addon object.

        Returns:
            self: The instance of the current JsonFile.
        """
        from anvil.api.core.core import ANVIL

        if self._queued:
            return self

        self._directory = directory if not directory is None else ""
        self._queued = True
        ANVIL.__queue__(self)
        return self

    @property
    def _path(self) -> Path:
        """The folder the object is written to: its folder in its pack, then its directory."""
        return self._pack_path / self._folder / self._directory

    @property
    def _pack_path(self) -> Path:
        """The folder of the pack the object is written to."""
        return CONFIG.RP_PATH if self._pack == Pack.RP else CONFIG.BP_PATH

    def __export__(self) -> None:
        """
        Exports the addon object after potentially shortening its content and replacing backslashes.
        Logs the event and writes the object to a file.
        """
        file_name = f"{self._file_name or self.identifier.name}{self._extension}"
        path = (self._path / file_name).relative_to(self._pack_path).as_posix()
        if len(path) > 96:
            raise ValueError(
                f"Relative file path [{path}] has [{len(path)}] characters, but cannot be more than [96] characters."
            )

        AnvilIO.file(file_name, self._content, self._path, "w")
