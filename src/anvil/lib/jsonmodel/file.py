"""`JsonFile`, the base of every JSON file an Anvil project writes to a pack."""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import TYPE_CHECKING, Any, get_args, get_origin

from anvil.lib.config import CONFIG, ConfigPackageTarget, Pack
from anvil.lib.lib import AnvilIO

from .identifier import Identifier

if TYPE_CHECKING:
    from .object import JsonObject


class JsonFile[D: JsonObject]:
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    A file type names its document, the class of its typed content, as the type argument:
    `class ShadowSettings(JsonFile[_ShadowSettingsFile])`. An abstract file base stays
    generic: `class Feature[D: JsonObject](JsonFile[D])`.

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
    _document_type: type[D]
    """The class of the file's typed content, the type argument the file type gives:
    `_document` starts as an empty one, and `__schema__()` describes the file. Abstract file
    bases have none."""
    _document: D
    """The file's typed content, written on export."""
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
            TypeError: When the class is an abstract file base, with no document type.
            ValueError: When the identifier is not valid (see `Identifier.parse`), or a vanilla
                override is not allowed.
        """
        type(self)._require_document()
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
        self._document = self._document_type()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        for base in cls.__dict__.get("__orig_bases__", ()):
            origin = get_origin(base)
            if isinstance(origin, type) and issubclass(origin, JsonFile):
                document = get_args(base)[0]
                if isinstance(document, type):
                    cls._document_type = document

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
    def _require_document(cls) -> None:
        if not hasattr(cls, "_document_type"):
            raise TypeError(
                f"{cls.__name__} is an abstract file base: create one of its file types."
            )

    @classmethod
    def __schema__(cls) -> dict[str, Any]:
        """The JSON Schema (draft 2020-12) of this file: the schema of its `_document_type`, with
        the file's type as `title` and where it is written under `x-anvil-file`.

        Raises:
            TypeError: When the class is an abstract file base, with no document type.
        """
        cls._require_document()
        file = {
            "pack": cls._pack,
            "folder": cls._folder,
            "name": cls._file_name,
            "extension": cls._extension,
        }
        schema = cls._document_type.__schema__()
        return {
            "$schema": schema.pop("$schema"),
            "title": cls._object_type,
            "x-anvil-file": {key: str(value) for key, value in file.items() if value},
            **schema,
        }

    def queue(self, directory: str | None = None) -> "JsonFile[D]":
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

        self._directory = directory if directory is not None else ""
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

        AnvilIO.file(file_name, self._document, self._path, "w")
