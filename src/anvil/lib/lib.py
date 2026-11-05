"""A collection of useful functions and classes used throughout the program."""

import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any

import click
import orjson
import requests

from anvil.lib.format_versions import MANIFEST_BUILD

from ..__version__ import __version__

if TYPE_CHECKING:
    from anvil.lib.jsonmodel.types import Color


def validate_platform() -> None:
    """Validates that Anvil is running on a supported platform.

    Only Linux, macOS, and Windows are supported.
    """
    if sys.platform not in ("win32", "darwin") and not sys.platform.startswith("linux"):
        raise OSError(
            f"Anvil only supports Windows, macOS, and Linux (current platform: '{sys.platform}')."
        )


validate_platform()


USERPROFILE: Path = Path(os.getenv("USERPROFILE", Path.home()))
APPDATA: Path = Path(os.getenv("APPDATA", USERPROFILE / "AppData" / "Roaming"))

RELEASE_COM_MOJANG: Path = (
    APPDATA / "Minecraft Bedrock" / "Users" / "Shared" / "games" / "com.mojang"
)
PREVIEW_COM_MOJANG: Path = (
    APPDATA / "Minecraft Bedrock Preview" / "Users" / "Shared" / "games" / "com.mojang"
)

DESKTOP: Path = USERPROFILE / "Desktop"
OUTPUT = Path("output")
"""The project's output folder, for packages and local exports."""
IMAGE_EXTENSIONS_PRIORITY = [".tga", ".png", ".jpg", ".jpeg"]


class Directory:
    @classmethod
    def create(cls, path: str | Path):
        """
        Creates a new directory, with its missing parents.

        Args:
            path (str | Path): The path to the new directory. A relative path is relative to
                the current folder.
        """
        Path(path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def copy_files(
        cls,
        old_dir: str | Path,
        new_dir: str | Path,
        target_file: str,
        rename: str | None = None,
    ):
        """
        Copies a file from one directory to another.

        Args:
            old_dir (str | Path): The path to the source directory.
            new_dir (str | Path): The path to the destination directory.
            target_file (str): The name of the file to be copied.
            rename (str | None, optional): The new name for the copied file. Defaults to None.
        """
        cls.create(new_dir)
        shutil.copyfile(
            Path(old_dir) / target_file, Path(new_dir) / (rename or target_file)
        )

    @classmethod
    def copy_folder(cls, old_dir: str | Path, new_dir: str | Path):
        """
        Copies a folder and all its contents to a new location.

        Args:
            old_dir (str | Path): The path to the source directory.
            new_dir (str | Path): The path to the destination directory.
        """
        cls.create(new_dir)
        shutil.copytree(
            Path(old_dir).resolve(), Path(new_dir).resolve(), dirs_exist_ok=True
        )

    @classmethod
    def move_folder(cls, old_dir: str | Path, new_dir: str | Path) -> None:
        """
        Moves a folder and all its contents to a new location.

        Args:
            old_dir (str | Path): The path to the source directory.
            new_dir (str | Path): The path to the destination directory.
        """
        cls.create(new_dir)
        shutil.move(Path(old_dir).resolve(), Path(new_dir).resolve())


class AnvilIO:
    _FILE_TYPE_COMMENT = {
        "json": "//",
        "material": "//",
        "code-workspace": "//",
        "py": "#",
        "mcfunction": "#",
        "lang": "##",
    }
    _IDENTIFIER_NAMES = frozenset(
        {
            "Biome",
            "Block",
            "Item",
            "Entity",
        }
    )

    @staticmethod
    def _should_keep_shortened_value(key: str, value) -> bool:
        if ":" in key:
            return True
        return value not in ({}, [], None, "None", "")

    @classmethod
    def _normalize_json_like(cls, value: Any) -> Any:
        if value is None or isinstance(value, (bool, int, float)):
            return value

        if isinstance(value, dict):
            shortened = {}

            from anvil.lib.jsonmodel.jsontypes import KeptObject

            for key, item in value.items():
                key_str = str(key)
                shortened_value = cls._normalize_json_like(item)
                if isinstance(item, KeptObject) or cls._should_keep_shortened_value(
                    key_str, shortened_value
                ):
                    shortened[key_str] = shortened_value

            return shortened

        if isinstance(value, list):
            shortened = []

            for item in value:
                shortened_value = cls._normalize_json_like(item)
                if shortened_value != []:
                    shortened.append(shortened_value)

            return shortened

        if isinstance(value, tuple):
            return [cls._normalize_json_like(item) for item in value]

        if isinstance(value, StrEnum):
            return value.value

        if isinstance(value, str):
            return value.replace("\\", "/")

        from anvil.api.core.filters import Filter

        if isinstance(value, Filter):
            return cls._normalize_json_like(value.__export_dict__())

        from anvil.lib.jsonmodel import JsonComponent, JsonObject

        if isinstance(value, JsonObject):
            return cls._normalize_json_like(value.__json__())

        if isinstance(value, type) and issubclass(value, JsonComponent):
            return cls._normalize_json_like(value.identifier)

        class_name = value.__class__.__name__

        if class_name in cls._IDENTIFIER_NAMES:
            return cls._normalize_json_like(value.identifier)

        if class_name == "LootTable":
            return cls._normalize_json_like(value.table_path)

        return value

    @classmethod
    def _dump_json_like(cls, content, minify: bool = False) -> bytes:
        option = 0 if minify else orjson.OPT_INDENT_2
        normalized = cls._normalize_json_like(content)
        return orjson.dumps(normalized, option=option)

    @classmethod
    def _get_file_stamp(cls, name: str, type: str, company: str, minify: bool) -> str:
        prefix = cls._FILE_TYPE_COMMENT.get(type, "//")
        time = datetime.now(datetime.now().astimezone().tzinfo).strftime(
            "%d-%m-%Y %H:%M:%S %z"
        )

        stamp = [
            f"Filename: {name}",
            f"Generated with StarkTMA/Anvil {__version__}",
            f"Time: {time}",
            f"Property of {company}",
        ]

        if minify:
            return "".join(prefix + line for line in stamp) + "\n"
        else:
            return "\n".join(prefix + line for line in stamp) + "\n\n"

    @classmethod
    def _parse_json_like(
        cls, content: str | bytes | dict | list, minify: bool = False
    ) -> bytes:
        return cls._dump_json_like(content, minify=minify)

    @classmethod
    def file(
        cls,
        name: str,
        content: str | bytes | dict | list,
        directory: str | Path,
        mode: str,
    ):
        """
        Create or modify a file with the given content.

        Args:
            name (str): The name of the file.
            content (Any): The content of the file.
            directory (str | Path): The folder where the file is created or modified.
            mode (str): The file mode, either "w" (write) or "a" (append).

        Note:
            The file content is converted to the appropriate format based on the file extension.
        """

        from anvil.lib.config import CONFIG

        STAMP_EXCLUDE = [
            "package.json",
            "tsconfig.json",
        ]

        Directory.create(directory)
        path = Path(directory) / name
        type = name.split(".")[-1]

        if type in ["json", "material", "code-workspace"]:
            content = cls._parse_json_like(
                content, minify=CONFIG._MINIFY or "--minify" in sys.argv
            )

        if CONFIG._ADD_STAMP and not type == "yml" and name not in STAMP_EXCLUDE:
            file_stamp = cls._get_file_stamp(
                name,
                type,
                CONFIG.COMPANY,
                minify=CONFIG._MINIFY or "--minify" in sys.argv,
            )

            if isinstance(content, bytes):
                content = file_stamp.encode("utf-8") + content
            else:
                content = file_stamp + str(content)

        if isinstance(content, bytes):
            binary_mode = mode if "b" in mode else f"{mode}b"
            with path.open(binary_mode) as file:
                file.write(content)
            return

        with path.open(mode, encoding="utf-8") as file:
            file.write(content)


class AnvilArchive:
    _EXCLUDED_EXTENSIONS = {".js.map"}
    _STORED_EXTENSIONS = {}
    _FAST_COMPRESS_LEVEL = 3

    @classmethod
    def write_entry(
        cls, ziph: zipfile.ZipFile, file_path: Path, archive_path: PurePosixPath
    ) -> None:
        file_name = file_path.name.lower()
        if any(file_name.endswith(ext) for ext in cls._EXCLUDED_EXTENSIONS):
            return

        if file_path.suffix.lower() in cls._STORED_EXTENSIONS:
            ziph.write(
                file_path, archive_path.as_posix(), compress_type=zipfile.ZIP_STORED
            )
            return

        ziph.write(
            file_path,
            archive_path.as_posix(),
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=cls._FAST_COMPRESS_LEVEL,
        )

    @classmethod
    def from_mapping(cls, zip_name: Path, dir_list: dict[Path, PurePosixPath]) -> None:
        """
        Create a ZIP archive containing multiple directories and files.

        Args:
            zip_name (Path): The ZIP archive to write.
            dir_list (dict[Path, PurePosixPath]): The folders and files to add, each mapped to
                the folder it goes in inside the archive.

        Note:
            The target directories represent the structure inside the ZIP archive.
        """

        with zipfile.ZipFile(
            zip_name,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=cls._FAST_COMPRESS_LEVEL,
        ) as zipf:
            for source, target in dir_list.items():
                if source.is_dir():
                    source_root = source.resolve()
                    for root, _, files in source_root.walk():
                        for file_name in files:
                            file_path = root / file_name
                            relative_path = file_path.relative_to(source_root)
                            archive_path = target / relative_path.as_posix()
                            cls.write_entry(zipf, file_path, archive_path)
                else:
                    cls.write_entry(zipf, source, target / source.name)

    @classmethod
    def marketplace_zip(cls):
        from anvil.lib.config import CONFIG, ConfigPackageTarget

        Directory.create(OUTPUT)

        content_structure = {
            OUTPUT / "Store Art": PurePosixPath("Store Art"),
            OUTPUT / "Marketing Art": PurePosixPath("Marketing Art"),
        }

        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            ZIP_RP_PATH = PurePosixPath(
                "Content", "resource_packs", f"RP_{CONFIG._PASCAL_PROJECT_NAME}"
            )
            ZIP_BP_PATH = PurePosixPath(
                "Content", "behavior_packs", f"BP_{CONFIG._PASCAL_PROJECT_NAME}"
            )
            content_structure.update(
                {
                    CONFIG.RP_PATH: ZIP_RP_PATH,
                    CONFIG.BP_PATH: ZIP_BP_PATH,
                }
            )

        else:
            content_structure.update(
                {
                    CONFIG.RP_PATH: PurePosixPath(
                        "Content",
                        "world_template",
                        "resource_packs",
                        f"RP_{CONFIG._PASCAL_PROJECT_NAME}",
                    ),
                    CONFIG.BP_PATH: PurePosixPath(
                        "Content",
                        "world_template",
                        "behavior_packs",
                        f"BP_{CONFIG._PASCAL_PROJECT_NAME}",
                    ),
                    CONFIG._WORLD_PATH
                    / "texts": PurePosixPath("Content", "world_template", "texts"),
                    CONFIG._WORLD_PATH
                    / "level.dat": PurePosixPath("Content", "world_template"),
                    CONFIG._WORLD_PATH
                    / "levelname.txt": PurePosixPath("Content", "world_template"),
                    CONFIG._WORLD_PATH
                    / "manifest.json": PurePosixPath("Content", "world_template"),
                    CONFIG._WORLD_PATH
                    / "world_icon.jpeg": PurePosixPath("Content", "world_template"),
                    CONFIG._WORLD_PATH
                    / "world_behavior_packs.json": PurePosixPath(
                        "Content", "world_template"
                    ),
                    CONFIG._WORLD_PATH
                    / "world_resource_packs.json": PurePosixPath(
                        "Content", "world_template"
                    ),
                }
            )
            if not CONFIG._RANDOM_SEED:
                content_structure.update(
                    {
                        CONFIG._WORLD_PATH
                        / "db": PurePosixPath("Content", "world_template", "db"),
                    }
                )

        AnvilArchive.from_mapping(
            OUTPUT / f"{CONFIG.PROJECT_NAME}.zip",
            content_structure,
        )

    @classmethod
    def mcworld(cls):
        from anvil.api.core.core import CONFIG

        Directory.create(OUTPUT)

        content_structure = {
            CONFIG.RP_PATH: PurePosixPath(
                "resource_packs", f"RP_{CONFIG.PROJECT_NAME}"
            ),
            CONFIG.BP_PATH: PurePosixPath(
                "behavior_packs", f"BP_{CONFIG.PROJECT_NAME}"
            ),
            CONFIG._WORLD_PATH / "texts": PurePosixPath("texts"),
            CONFIG._WORLD_PATH / "db": PurePosixPath("db"),
            CONFIG._WORLD_PATH / "level.dat": PurePosixPath(),
            CONFIG._WORLD_PATH / "levelname.txt": PurePosixPath(),
            CONFIG._WORLD_PATH / "manifest.json": PurePosixPath(),
            CONFIG._WORLD_PATH / "world_icon.jpeg": PurePosixPath(),
            CONFIG._WORLD_PATH / "world_behavior_packs.json": PurePosixPath(),
            CONFIG._WORLD_PATH / "world_resource_packs.json": PurePosixPath(),
        }

        AnvilArchive.from_mapping(
            OUTPUT / f"{CONFIG.PROJECT_NAME}.mcworld",
            content_structure,
        )

    @classmethod
    def mcaddon(cls) -> None:
        from anvil.api.core.core import CONFIG

        Directory.create(OUTPUT)

        content_structure = {
            CONFIG.RP_PATH: PurePosixPath(f"RP_{CONFIG.PROJECT_NAME}"),
            CONFIG.BP_PATH: PurePosixPath(f"BP_{CONFIG.PROJECT_NAME}"),
        }

        AnvilArchive.from_mapping(
            OUTPUT / f"{CONFIG.PROJECT_NAME}.mcaddon",
            content_structure,
        )


class AnvilFormatter:
    @staticmethod
    def _normalize_min_max(
        value: Any,
        name: str = "value",
        *,
        value_types: tuple[type, ...] = (int, float),
        clamp_min: int | float | None = None,
        clamp_max: int | float | None = None,
    ) -> tuple[int | float, int | float]:
        if (
            not isinstance(value, (tuple, list))
            or len(value) != 2
            or not all(isinstance(item, value_types) for item in value)
        ):
            value_names = " or ".join(value_type.__name__ for value_type in value_types)
            raise ValueError(
                f"{name} must be a tuple or list of 2 {value_names} values"
            )

        minimum, maximum = value
        if minimum > maximum:
            minimum, maximum = maximum, minimum
        if clamp_min is not None:
            minimum = max(clamp_min, minimum)
            maximum = max(clamp_min, maximum)
        if clamp_max is not None:
            minimum = min(clamp_max, minimum)
            maximum = min(clamp_max, maximum)

        return minimum, maximum

    @classmethod
    def min_max_dict(
        cls,
        value: Any,
        name: str = "value",
        *,
        value_types: tuple[type, ...] = (int, float),
        clamp_min: int | float | None = None,
        clamp_max: int | float | None = None,
    ) -> dict[str, Any]:
        minimum, maximum = cls._normalize_min_max(
            value,
            name,
            value_types=value_types,
            clamp_min=clamp_min,
            clamp_max=clamp_max,
        )
        return {"min": minimum, "max": maximum}

    @classmethod
    def min_max_list(
        cls,
        value: Any,
        name: str = "value",
        *,
        value_types: tuple[type, ...] = (int, float),
        clamp_min: int | float | None = None,
        clamp_max: int | float | None = None,
    ) -> list[Any]:
        minimum, maximum = cls._normalize_min_max(
            value,
            name,
            value_types=value_types,
            clamp_min=clamp_min,
            clamp_max=clamp_max,
        )
        return [minimum, maximum]

    @classmethod
    def range_min_max_dict(
        cls,
        value: float | int | tuple[float | int, float | int],
        name: str = "value",
        *,
        value_types: tuple[type, ...] = (int, float),
        clamp_min: int | float | None = None,
        clamp_max: int | float | None = None,
    ) -> dict[str, Any]:
        if isinstance(value, (float, int)):
            value = (value, value)

        minimum, maximum = cls._normalize_min_max(
            value,
            name,
            value_types=value_types,
            clamp_min=clamp_min,
            clamp_max=clamp_max,
        )
        return {"range_min": minimum, "range_max": maximum}

    @classmethod
    def convert_color(
        cls,
        color: Color,
        target: Color | None = None,
    ) -> Color:
        """Converts a color from any supported format to the target format.

        Supported input formats:
        - Hex string: "#RRGGBB", "#RRGGBBAA", "#RGB", or "#RGBA" (short format)
        - RGB/RGBA (0-1): tuple of 3 or 4 floats in range [0, 1]
        - RGB255/RGBA255 (0-255): tuple of 3 or 4 ints in range [0, 255]

        Args:
            color (Color): The input color in any supported format.
            target: The target color type (RGB, RGBA, RGB255, RGBA255, HexRGB, or HexRGBA).
                    If None, returns normalized version of input format.

        Returns:
            Color: The color converted to the target format.

        Raises:
            ValueError: If the color format is invalid or cannot be determined.
            TypeError: If the color type is not supported.

        Examples:
            >>> convert_color("#FF0000", RGB)
            (1.0, 0.0, 0.0)
            >>> convert_color("#F00", RGB)
            (1.0, 0.0, 0.0)
            >>> convert_color("#F00")  # No target, normalizes to full hex
            "#ff0000"
            >>> convert_color((1.0, 0.0, 0.0), HexRGB)
            "#ff0000"
            >>> convert_color((1.0, 0.0, 0.0), HexRGBA)
            "#ff0000ff"
            >>> convert_color((255, 0, 0), RGB)
            (1.0, 0.0, 0.0)
            >>> convert_color((0.5, 0.5, 0.5), RGBA)
            (0.5, 0.5, 0.5, 1.0)
            >>> convert_color((128, 64, 32))  # No target, normalizes to RGB255
            (128.0, 64.0, 32.0)
        """
        from anvil.lib.jsonmodel.types import (
            RGB,
            RGB255,
            RGBA,
            RGBA255,
            HexRGB,
            HexRGBA,
        )

        if isinstance(color, str):
            if not color.startswith("#"):
                raise ValueError("Hex color must start with '#'")
            hex_color = color.lstrip("#")
            if len(hex_color) not in [3, 4, 6, 8]:
                raise ValueError(
                    "Hex color must be 3 (#RGB), 4 (#RGBA), 6 (#RRGGBB), or 8 (#RRGGBBAA) characters after '#'"
                )
            is_str = True
        elif isinstance(color, (tuple, list)):
            if len(color) not in [3, 4]:
                raise ValueError(
                    "Color tuple/list must have 3 (RGB) or 4 (RGBA) elements"
                )
            is_str = False
        else:
            raise TypeError(
                f"Unsupported color type: {type(color).__name__}. Expected str, tuple, or list."
            )

        convert_target = None
        if target is None:
            if is_str:
                convert_target = HexRGBA if len(hex_color) in [4, 8] else HexRGB
            else:
                max_val = float(max(color[:3]))
                has_alpha = len(color) == 4
                convert_target = (
                    RGBA255
                    if has_alpha and max_val > 1.0
                    else RGB255 if max_val > 1.0 else RGBA if has_alpha else RGB
                )
        else:
            convert_target = target

        if is_str:
            if len(hex_color) in [3, 4]:
                hex_color = "".join([c * 2 for c in hex_color])

            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            a = int(hex_color[6:8], 16) / 255.0 if len(hex_color) == 8 else 1.0
        else:
            max_val = float(max(color[:3]))

            if max_val > 1.0:
                r = clamp(float(color[0]), 0.0, 255.0) / 255.0
                g = clamp(float(color[1]), 0.0, 255.0) / 255.0
                b = clamp(float(color[2]), 0.0, 255.0) / 255.0
                a = (
                    clamp(float(color[3]), 0.0, 255.0) / 255.0
                    if len(color) == 4
                    else 1.0
                )
            else:
                r = clamp(float(color[0]), 0.0, 1.0)
                g = clamp(float(color[1]), 0.0, 1.0)
                b = clamp(float(color[2]), 0.0, 1.0)
                a = clamp(float(color[3]), 0.0, 1.0) if len(color) == 4 else 1.0

        if convert_target in (HexRGB, HexRGBA):
            hex_r = int(round(r * 255))
            hex_g = int(round(g * 255))
            hex_b = int(round(b * 255))
            hex_a = int(round(a * 255))

            return (
                f"#{hex_r:02x}{hex_g:02x}{hex_b:02x}{hex_a:02x}"
                if convert_target is HexRGBA
                else f"#{hex_r:02x}{hex_g:02x}{hex_b:02x}"
            )

        elif convert_target is RGB:
            return (r, g, b)

        elif convert_target is RGBA:
            return (r, g, b, a)

        elif convert_target is RGB255:
            return (int(r * 255), int(g * 255), int(b * 255))

        elif convert_target is RGBA255:
            return (int(r * 255), int(g * 255), int(b * 255), int(a * 255))

        else:
            raise ValueError(f"Unsupported target format: {convert_target}")


class AnvilValidator:
    @classmethod
    def check_new_versions(cls):
        click.echo(click.style("Checking for package updates...", fg="cyan"))
        outdated_packages: list[dict[str, str]] = []

        try:
            res = subprocess.run(
                "npm outdated --json",
                shell=True,
                capture_output=True,
                text=True,
            )
            if res.stdout and res.stdout.strip():
                try:
                    npm_data = orjson.loads(res.stdout)
                    for pkg_name, pkg_info in npm_data.items():
                        if isinstance(pkg_info, dict):
                            outdated_packages.append(
                                {
                                    "name": pkg_name,
                                    "type": "npm",
                                    "current": str(pkg_info.get("current", "N/A")),
                                    "latest": str(
                                        pkg_info.get(
                                            "latest", pkg_info.get("wanted", "N/A")
                                        )
                                    ),
                                }
                            )
                except orjson.JSONDecodeError:
                    for line in res.stdout.splitlines():
                        parts = line.split()
                        if len(parts) >= 4 and not line.startswith("Package"):
                            outdated_packages.append(
                                {
                                    "name": parts[0],
                                    "type": "npm",
                                    "current": parts[1],
                                    "latest": parts[3],
                                }
                            )
        except (OSError, subprocess.SubprocessError):
            pass

        try:
            res = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
            )
            if res.stdout and res.stdout.strip():
                try:
                    pip_data = orjson.loads(res.stdout)
                    for pkg in pip_data:
                        if (
                            isinstance(pkg, dict)
                            and "mcanvil" in pkg.get("name", "").lower()
                        ):
                            outdated_packages.append(
                                {
                                    "name": pkg.get("name", "mcanvil"),
                                    "type": "pip",
                                    "current": str(pkg.get("version", "N/A")),
                                    "latest": str(pkg.get("latest_version", "N/A")),
                                }
                            )
                except orjson.JSONDecodeError:
                    for line in res.stdout.splitlines():
                        if "mcanvil" in line.lower():
                            parts = line.split()
                            if len(parts) >= 3:
                                outdated_packages.append(
                                    {
                                        "name": parts[0],
                                        "type": "pip",
                                        "current": parts[1],
                                        "latest": parts[2],
                                    }
                                )
        except (OSError, subprocess.SubprocessError):
            pass

        if outdated_packages:
            pkg_w = max(len("Package"), max(len(p["name"]) for p in outdated_packages))
            type_w = max(len("Type"), max(len(p["type"]) for p in outdated_packages))
            curr_w = max(
                len("Current"), max(len(p["current"]) for p in outdated_packages)
            )
            late_w = max(
                len("Latest"), max(len(p["latest"]) for p in outdated_packages)
            )

            header = f"{'Package':<{pkg_w}}  {'Type':<{type_w}}  {'Current':<{curr_w}}  {'Latest':<{late_w}}"
            separator = f"{'-' * pkg_w}  {'-' * type_w}  {'-' * curr_w}  {'-' * late_w}"
            click.echo(click.style(header, fg="yellow", bold=True))
            click.echo(click.style(separator, fg="bright_black"))

            for p in outdated_packages:
                name_str = click.style(f"{p['name']:<{pkg_w}}", fg="cyan")
                type_str = click.style(f"{p['type']:<{type_w}}", fg="magenta")
                curr_str = click.style(f"{p['current']:<{curr_w}}", fg="red")
                late_str = click.style(f"{p['latest']:<{late_w}}", fg="green")
                click.echo(f"{name_str}  {type_str}  {curr_str}  {late_str}")
        else:
            click.echo(click.style("[INFO]: All packages are up to date.", fg="green"))

        try:
            request = requests.get(
                "https://raw.githubusercontent.com/Mojang/bedrock-samples/refs/heads/main/version.json"
            )
            vanilla_latest_build: str = orjson.loads(request.text)["latest"]["version"]
        except (requests.RequestException, orjson.JSONDecodeError, KeyError, TypeError):
            click.echo(
                click.style(
                    "[WARN]: Could not fetch latest Minecraft version.", fg="yellow"
                )
            )
            vanilla_latest_build = MANIFEST_BUILD

        return vanilla_latest_build, __version__

    @classmethod
    def is_color_value(cls, value) -> bool:
        """
        Check if a value is a color value (not a texture file name).
        Returns True for RGB/RGBA tuples and hex color strings.
        Returns False for texture file names (plain strings without # prefix).
        """
        if value is None:
            return False

        if (
            isinstance(value, (tuple, list))
            and len(value) in (3, 4)
            and any(
                [
                    all(isinstance(c, int) and 0 <= c <= 255 for c in value),
                    all(isinstance(c, float) and 0.0 <= c <= 1.0 for c in value),
                ]
            )
        ):
            return True

        if isinstance(value, str) and value.startswith("#"):
            hex_val = value[1:]
            if len(hex_val) in (3, 4, 6, 8) and all(
                c in "0123456789abcdefABCDEF" for c in hex_val
            ):
                return True

        return False


class AnvilDisplay:
    @staticmethod
    def copyright():
        click.clear()
        click.echo(
            "\n".join(
                [
                    f"{click.style('Anvil', 'cyan')} - by StarkTMA.",
                    f"Version {click.style(__version__, 'cyan')}.",
                    f"Copyright © {datetime.now().year} {click.style('StarkTMA', 'red')}.",
                    "All rights reserved.",
                    "",
                ]
            )
        )

    @staticmethod
    def project_display(display_name: str, target: str, preview: bool):
        click.echo(
            "\n".join(
                [
                    f"Project: {display_name}.",
                    f"Target: {'Add-On' if target == 'addon' else 'World'}.",
                    f"Minecraft: {"Release" if not preview else "Preview"}.",
                    "",
                ]
            )
        )


def clamp(value: float | int, _min: float | int, _max: float | int) -> float | int:
    """
    Clamps a value between a minimum and maximum limit.

    Args:
        value (float | int): The value to be clamped.
        _min (float | int): The lower limit.
        _max (float | int): The upper limit.

    Returns:
        float: The clamped value.
    """
    return max(min(_max, value), _min)


def frange(start: int, stop: int, num: float = 1) -> list[float]:
    """
    Generate a list of interpolated float values between start and stop.

    Args:
        start (int): The starting value.
        stop (int): The ending value.
        num (float, optional): The number of values to generate. Defaults to 1.

    Returns:
        list[float]: A list of interpolated values between start and stop.
    """
    step = (stop - start) / (num - 1)
    values = [round(start + i * step, 2) for i in range(int(num))]
    return values


def process_subcommand(
    command: str, error_handle: str = "Error", exit_on_error: bool = False
):
    """Executes a subprocess command with error handling.

    Args:
        command (str): The command to execute.
        error_handle (str, optional): Error message prefix. Defaults to "Error".
        exit_on_error (bool, optional): Exit with the subprocess return code on
            failure instead of continuing (needed for CI so a failed build fails the job).
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"{error_handle}: {e}", fg="red"), err=True)
        if exit_on_error:
            sys.exit(e.returncode or 1)


def salt_from_str(s: str) -> int:
    """Generates a hash value from a string for use as a random seed.

    Args:
        s (str): The input string to hash.

    Returns:
        int: A hash value derived from the input string.
    """
    h = 0
    for ch in s:
        h = (h * 131 + ord(ch)) % 1_000_000
    return h
