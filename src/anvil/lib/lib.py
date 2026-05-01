"""A collection of useful functions and classes used throughout the program."""

import inspect
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime
from enum import StrEnum
from typing import Any, Dict, List

import click
import commentjson
import orjson
import requests
from packaging.version import Version

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, Color, HexRGB, HexRGBA
from anvil.lib.format_versions import MANIFEST_BUILD

from ..__version__ import __version__

if os.name != "nt":
    raise OSError(
        "Anvil is only supported on Windows due to its reliance on Minecraft Bedrock's file structure and APIs."
    )

USERPORFILE: str = os.getenv("USERPROFILE", os.path.expanduser("~"))
APPDATA: str = os.getenv("APPDATA", os.path.join(USERPORFILE, "AppData", "Roaming"))

RELEASE_COM_MOJANG = os.path.join(
    APPDATA, "Minecraft Bedrock", "Users", "Shared", "games", "com.mojang"
)
PREVIEW_COM_MOJANG = os.path.join(
    APPDATA, "Minecraft Bedrock Preview", "Users", "Shared", "games", "com.mojang"
)

DESKTOP: str = os.path.join(USERPORFILE, "Desktop")
IMAGE_EXTENSIONS_PRIORITY = [".tga", ".png", ".jpg", ".jpeg"]


class Directory:
    @classmethod
    def create(cls, path: str):
        """
        Creates a new directory.

        Parameters:
            path (str): The path to the new directory.
        """
        this_path = os.path.join("./", path.lstrip("/"))
        os.makedirs(this_path, exist_ok=True)

    @classmethod
    def copy_files(
        cls, old_dir: str, new_dir: str, target_file: str, rename: str | None = None
    ):
        """
        Copies a file from one directory to another.

        Parameters:
            old_dir (str): The path to the source directory.
            new_dir (str): The path to the destination directory.
            target_file (str): The name of the file to be copied.
            rename (str | None, optional): The new name for the copied file. Defaults to None.
        """
        cls.create(new_dir)
        if rename is None:
            shutil.copyfile(
                os.path.join(old_dir, target_file), os.path.join(new_dir, target_file)
            )
        else:
            shutil.copyfile(
                os.path.join(old_dir, target_file), os.path.join(new_dir, rename)
            )

    @classmethod
    def copy_folder(cls, old_dir: str, new_dir: str):
        """
        Copies a folder and all its contents to a new location.

        Parameters:
            old_dir (str): The path to the source directory.
            new_dir (str): The path to the destination directory.
        """
        cls.create(new_dir)
        shutil.copytree(
            os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True
        )

    @classmethod
    def move_folder(cls, old_dir: str, new_dir: str) -> None:
        """
        Moves a folder and all its contents to a new location.

        Parameters:
            old_dir (str): The path to the source directory.
            new_dir (str): The path to the destination directory.
        """
        cls.create(new_dir)
        shutil.move(os.path.realpath(old_dir), os.path.realpath(new_dir))


class AnvilIO:
    _FILE_TYPE_COMMENT = {
        "json": "//",
        "material": "//",
        "code-workspace": "//",
        "py": "#",
        "mcfunction": "#",
        "lang": "##",
    }
    _BLOCK_DESCRIPTOR_NAMES = frozenset({"MinecraftBlockDescriptor", "Block"})
    _IDENTIFIER_NAMES = frozenset(
        {
            "MinecraftItemDescriptor",
            "MinecraftEntityDescriptor",
            "MinecraftBiomeDescriptor",
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

            for key, item in value.items():
                key_str = key if isinstance(key, str) else str(key)
                shortened_value = cls._normalize_json_like(item)
                if cls._should_keep_shortened_value(key_str, shortened_value):
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

        from anvil.api.core.components import Component

        if isinstance(value, Component):
            return cls._normalize_json_like(value.__export_dict__())

        if isinstance(value, type) and issubclass(value, Component):
            return cls._normalize_json_like(value.__component_identifier__())

        class_name = value.__class__.__name__

        if class_name in cls._BLOCK_DESCRIPTOR_NAMES:
            return cls._normalize_json_like(value.descriptor())

        if class_name in cls._IDENTIFIER_NAMES:
            return cls._normalize_json_like(value.identifier)

        if class_name == "LootTable":
            return cls._normalize_json_like(value.table_path)

        if class_name == "_UIElement":
            return cls._normalize_json_like(value.queue())

        return value

    @classmethod
    def _dump_json_like(cls, content, minify: bool = False) -> bytes:
        option = 0 if minify else orjson.OPT_INDENT_2
        normalized = cls._normalize_json_like(content)
        return orjson.dumps(normalized, option=option)

    @classmethod
    def _get_file_stamp(cls, name: str, type: str, company: str) -> str:
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

        return "\n".join(prefix + line for line in stamp) + "\n\n"

    @classmethod
    def _parse_json_like(
        cls, content: str | bytes | Dict | List, minify: bool = False
    ) -> bytes:
        return cls._dump_json_like(content, minify=minify)

    @classmethod
    def file(
        cls,
        name: str,
        content: str | bytes | Dict | List,
        directory: str,
        mode: str,
        skip_tag: bool = False,
        **parameters,
    ):
        """
        Create or modify a file with the given content.

        Parameters:
            name (str): The name of the file.
            content: The content of the file.
            directory (str): The directory path where the file should be created or modified.
            mode (str): The file mode, either "w" (write) or "a" (append).
            skip_tag (bool, optional): Whether to skip adding the file metadata tag. Defaults to False.
            *Parameters: Additional StrEnum.

        Note:
            The file content is converted to the appropriate format based on the file extension.
        """

        from anvil.lib.config import CONFIG

        Directory.create(directory)
        path = os.path.normpath(os.path.join(directory, name))
        type = name.split(".")[-1]

        if type in ["json", "material", "code-workspace"]:
            content = cls._parse_json_like(content, minify=CONFIG._MINIFY)

        if not skip_tag:
            file_stamp = cls._get_file_stamp(name, type, CONFIG.COMPANY)
            if isinstance(content, bytes):
                content = file_stamp.encode("utf-8") + content
            else:
                content = file_stamp + str(content)

        if isinstance(content, bytes):
            binary_mode = mode if "b" in mode else f"{mode}b"
            with open(path, binary_mode) as file:
                file.write(content)
            return

        with open(path, mode, encoding="utf-8") as file:
            file.write(content)


class AnvilArchive:
    _EXCLUDED_EXTENSIONS = {".js.map"}
    _STORED_EXTENSIONS = {}
    _FAST_COMPRESS_LEVEL = 3

    @classmethod
    def write_entry(
        cls, ziph: zipfile.ZipFile, file_path: str, archive_path: str
    ) -> None:
        extension = os.path.splitext(file_path)[1].lower()
        if extension in cls._EXCLUDED_EXTENSIONS:
            return

        if extension in cls._STORED_EXTENSIONS:
            ziph.write(file_path, archive_path, compress_type=zipfile.ZIP_STORED)
            return

        ziph.write(
            file_path,
            archive_path,
            compress_type=zipfile.ZIP_DEFLATED,
            compresslevel=cls._FAST_COMPRESS_LEVEL,
        )

    @classmethod
    def from_mapping(cls, zip_name, dir_list: dict) -> None:
        """
        Create a ZIP archive containing multiple directories and files.

        Parameters:
            zip_name: The name of the ZIP archive.
            dir_list (dict): A dictionary where the keys are source directories and the values are target directories.

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
                if os.path.isdir(source):
                    source_root = os.path.realpath(source)
                    for root, _, files in os.walk(source_root):
                        for file_name in files:
                            file_path = os.path.join(root, file_name)
                            relative_path = os.path.relpath(file_path, source_root)
                            archive_path = os.path.join(target, relative_path)
                            cls.write_entry(zipf, file_path, archive_path)
                else:
                    archive_path = os.path.join(target, os.path.basename(source))
                    cls.write_entry(zipf, source, archive_path)

    @classmethod
    def marketplace_zip(cls):
        from anvil.lib.config import CONFIG, ConfigPackageTarget

        Directory.create("output")

        content_structure = {
            os.path.join("output", "Store Art"): os.path.join("Store Art"),
            os.path.join("output", "Marketing Art"): os.path.join("Marketing Art"),
        }

        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            ZIP_RP_PATH = os.path.join(
                "Content",
                "resource_packs",
                f"RP_{CONFIG._PASCAL_PROJECT_NAME}",
            )
            ZIP_BP_PATH = os.path.join(
                "Content",
                "behavior_packs",
                f"BP_{CONFIG._PASCAL_PROJECT_NAME}",
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
                    CONFIG.RP_PATH: os.path.join(
                        "Content",
                        "world_template",
                        "resource_packs",
                        f"RP_{CONFIG._PASCAL_PROJECT_NAME}",
                    ),
                    CONFIG.BP_PATH: os.path.join(
                        "Content",
                        "world_template",
                        "behavior_packs",
                        f"BP_{CONFIG._PASCAL_PROJECT_NAME}",
                    ),
                    os.path.join(CONFIG._WORLD_PATH, "texts"): os.path.join(
                        "Content", "world_template", "texts"
                    ),
                    os.path.join(CONFIG._WORLD_PATH, "level.dat"): os.path.join(
                        "Content", "world_template"
                    ),
                    os.path.join(CONFIG._WORLD_PATH, "levelname.txt"): os.path.join(
                        "Content", "world_template"
                    ),
                    os.path.join(CONFIG._WORLD_PATH, "manifest.json"): os.path.join(
                        "Content", "world_template"
                    ),
                    os.path.join(CONFIG._WORLD_PATH, "world_icon.jpeg"): os.path.join(
                        "Content", "world_template"
                    ),
                    os.path.join(
                        CONFIG._WORLD_PATH, "world_behavior_packs.json"
                    ): os.path.join("Content", "world_template"),
                    os.path.join(
                        CONFIG._WORLD_PATH, "world_resource_packs.json"
                    ): os.path.join("Content", "world_template"),
                }
            )
            if not CONFIG._RANDOM_SEED:
                content_structure.update(
                    {
                        os.path.join(CONFIG._WORLD_PATH, "db"): os.path.join(
                            "Content", "world_template", "db"
                        ),
                    }
                )

        AnvilArchive.from_mapping(
            os.path.join("output", f"{CONFIG.PROJECT_NAME}.zip"),
            content_structure,
        )

    @classmethod
    def mcworld(cls):
        from anvil.api.core.core import CONFIG

        Directory.create("output")

        content_structure = {
            CONFIG.RP_PATH: os.path.join("resource_packs", f"RP_{CONFIG.PROJECT_NAME}"),
            CONFIG.BP_PATH: os.path.join("behavior_packs", f"BP_{CONFIG.PROJECT_NAME}"),
            os.path.join(CONFIG._WORLD_PATH, "texts"): "texts",
            os.path.join(CONFIG._WORLD_PATH, "level.dat"): "",
            os.path.join(CONFIG._WORLD_PATH, "levelname.txt"): "",
            os.path.join(CONFIG._WORLD_PATH, "manifest.json"): "",
            os.path.join(CONFIG._WORLD_PATH, "world_icon.jpeg"): "",
            os.path.join(CONFIG._WORLD_PATH, "world_behavior_packs.json"): "",
            os.path.join(CONFIG._WORLD_PATH, "world_resource_packs.json"): "",
        }

        AnvilArchive.from_mapping(
            os.path.join("output", f"{CONFIG.PROJECT_NAME}.mcworld"),
            content_structure,
        )

    @classmethod
    def mcaddon(cls) -> None:
        from anvil.api.core.core import CONFIG

        Directory.create("output")

        content_structure = {
            CONFIG.RP_PATH: f"RP_{CONFIG.PROJECT_NAME}",
            CONFIG.BP_PATH: f"BP_{CONFIG.PROJECT_NAME}",
        }

        AnvilArchive.from_mapping(
            os.path.join("output", f"{CONFIG.PROJECT_NAME}.mcaddon"),
            content_structure,
        )


class AnvilFormatter:
    @staticmethod
    def _normalize_min_max(
        value: Any,
        name: str,
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
        name: str,
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
        name: str,
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
        name: str,
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


class AnvilValidator:
    @classmethod
    def validate_namespace_project_name(
        cls, namespace: str, project_name: str, is_addon: bool = False
    ):
        """Validates namespace and project name according to Minecraft requirements.

        Args:
            namespace (str): The namespace to validate.
            project_name (str): The project name to validate.
            is_addon (bool, optional): Whether this is for an addon. Defaults to False.

        Raises:
            ValueError: If validation fails for any requirement.
        """
        pascal_project_name = "".join(x[0] for x in project_name.split("_")).upper()

        if namespace == "minecraft":
            raise ValueError(
                "The namespace 'minecraft' is reserved and cannot be used for custom packs. Please choose a different namespace."
            )

        if len(namespace) > 8:
            raise ValueError(
                f"Namespace must be 8 characters or less. '{namespace}' is {len(namespace)} characters long."
            )

        if len(project_name) > 16:
            raise ValueError(
                f"Project name must be 16 characters or less. '{project_name}' is {len(project_name)} characters long."
            )

        if is_addon:
            model_name = f"{namespace}_{pascal_project_name}"
            if not namespace.endswith(f"_{pascal_project_name.lower()}"):
                raise ValueError(
                    f"Every namespace must be unique to the pack ending with project name initials. For this pack it should be {model_name}."
                )

    @classmethod
    def check_new_versions(cls):
        click.echo(click.style("Checking for package updates...", fg="cyan"))

        try:
            request = requests.get(
                "https://raw.githubusercontent.com/Mojang/bedrock-samples/refs/heads/main/version.json"
            )
            vanilla_latest_build: str = commentjson.loads(request.text)["latest"][
                "version"
            ]
        except Exception:
            click.echo(
                click.style(
                    "[WARN]: Could not fetch latest Minecraft version.", fg="yellow"
                )
            )
            vanilla_latest_build = MANIFEST_BUILD

        try:
            request = requests.get(
                "https://raw.githubusercontent.com/StarkTMA/Anvil/main/src/anvil/__version__.py"
            )
            latest_build: str = (
                request.text.split("=")[-1].strip().strip('"').strip("'")
            )

            if Version(__version__) < Version(latest_build):
                click.echo(
                    click.style(
                        f"\r[INFO]: A newer anvil build were found: [{latest_build}].",
                        fg="green",
                    )
                )
            else:
                click.echo(click.style("\r[INFO]: Anvil is up to date.", fg="green"))

        except Exception:
            click.echo(
                click.style(
                    "[WARN]: Could not fetch latest Anvil version.", fg="yellow"
                )
            )
            latest_build = __version__

        return vanilla_latest_build, latest_build


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


# --------------------------------------------------------------------------


def clamp(value: float | int, _min: float | int, _max: float | int) -> float | int:
    """
    Clamps a value between a minimum and maximum limit.

    Parameters:
        value (float | int): The value to be clamped.
        _min (float | int): The lower limit.
        _max (float | int): The upper limit.

    Returns:
        float: The clamped value.
    """
    return max(min(_max, value), _min)


def frange(start: int, stop: int, num: float = 1):
    """
    Generate a list of interpolated float values between start and stop.

    Parameters:
        start (int): The starting value.
        stop (int): The ending value.
        num (float, optional): The number of values to generate. Defaults to 1.

    Returns:
        list: A list of interpolated values between start and stop.
    """
    step = (stop - start) / (num - 1)
    values = [round(start + i * step, 2) for i in range(int(num))]
    return values


def process_subcommand(command: str, error_handle: str = "Error"):
    """Executes a subprocess command with error handling.

    Args:
        command (str): The command to execute.
        error_handle (str, optional): Error message prefix. Defaults to "Error".
    """
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_handle}: {e}")


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


def extract_ids_from_factory_class(cls) -> set[str]:
    _IDENT_RE = re.compile(r'["\'](minecraft:[a-z0-9_]+)["\']')
    ids: set[str] = set()
    for _, fn in inspect.getmembers(cls, predicate=inspect.isfunction):
        try:
            src = inspect.getsource(fn)
        except OSError:
            # Builtins / C-extensions or unavailable source; skip cleanly
            continue
        ids.update(m.group(1) for m in _IDENT_RE.finditer(src))
    return ids


def convert_color(
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
    # Type validation first
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
            raise ValueError("Color tuple/list must have 3 (RGB) or 4 (RGBA) elements")
        is_str = False
    else:
        raise TypeError(
            f"Unsupported color type: {type(color).__name__}. Expected str, tuple, or list."
        )

    # Determine target from source if not specified
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

    # Parse input color to normalized RGBA (0-1 range with alpha)
    if is_str:
        # Expand short hex format (#RGB or #RGBA) to full format
        if len(hex_color) in [3, 4]:
            hex_color = "".join([c * 2 for c in hex_color])

        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        a = int(hex_color[6:8], 16) / 255.0 if len(hex_color) == 8 else 1.0
    else:
        # Determine if values are in 0-1 or 0-255 range
        max_val = float(max(color[:3]))

        if max_val > 1.0:
            # Assume 0-255 range
            r = clamp(float(color[0]), 0.0, 255.0) / 255.0
            g = clamp(float(color[1]), 0.0, 255.0) / 255.0
            b = clamp(float(color[2]), 0.0, 255.0) / 255.0
            a = clamp(float(color[3]), 0.0, 255.0) / 255.0 if len(color) == 4 else 1.0
        else:
            # Assume 0-1 range
            r = clamp(float(color[0]), 0.0, 1.0)
            g = clamp(float(color[1]), 0.0, 1.0)
            b = clamp(float(color[2]), 0.0, 1.0)
            a = clamp(float(color[3]), 0.0, 1.0) if len(color) == 4 else 1.0

    # Convert to target format
    if convert_target in (HexRGB, HexRGBA):
        # Convert to hex (pre-compute once)
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
