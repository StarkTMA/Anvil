"""A collection of useful functions and classes used throughout the program."""

import inspect
import json as json
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime
from enum import StrEnum

import commentjson as commentjson

from anvil.lib.types import Color

from ..__version__ import __version__

APPDATA: str = os.getenv("APPDATA")
APPDATA_LOCAL: str = os.getenv("LOCALAPPDATA")

RELEASE_COM_MOJANG = os.path.join(
    APPDATA_LOCAL,
    "Packages",
    "Microsoft.MinecraftUWP_8wekyb3d8bbwe",
    "LocalState",
    "games",
    "com.mojang",
)
PREVIEW_COM_MOJANG = os.path.join(
    APPDATA, "Minecraft Bedrock Preview", "Users", "Shared", "games", "com.mojang"
)

DESKTOP: str = os.path.join(os.getenv("USERPROFILE"), "Desktop")
MOLANG_PREFIXES = (
    "q.",
    "v.",
    "c.",
    "t.",
    "query.",
    "variable.",
    "context.",
    "temp.",
    "math.",
)
IMAGE_EXTENSIONS_PRIORITY = [".tga", ".png", ".jpg", ".jpeg"]


# --------------------------------------------------------------------------


def FileExists(path) -> bool:
    """Checks if a file exists.

    Parameters:
        path (_type_): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(path)


def normalize_180(angle: float | str) -> float:
    """Normalizes an angle between -180 and 180.

    Parameters:
        angle (float): The angle to be normalized.

    Returns:
        float: The normalized angle.
    """
    if isinstance(angle, float):
        return round((angle + 540) % 360 - 180)
    else:
        return angle


def clamp(value: float, _min: float, _max: float) -> float:
    """
    Clamps a value between a minimum and maximum limit.

    Parameters:
        value (float): The value to be clamped.
        _min (float): The lower limit.
        _max (float): The upper limit.

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
    values = [round(start + i * step, 2) for i in range(num)]
    return values


def process_color(Color: Color, add_alpha: bool = False) -> str | list[float]:
    """Processes color values from different formats.

    Args:
        Color (Color): The color to process, can be tuple or hex string.
        add_alpha (bool, optional): Whether to add alpha channel if missing. Defaults to False.

    Returns:
        str | list[float]: Processed color in the appropriate format.

    Raises:
        ValueError: If color format is invalid.
        TypeError: If color type is not supported.
    """
    if isinstance(Color, tuple):
        if len(Color) not in [3, 4]:
            raise ValueError("Color tuple must have 3 or 4 elements.")
        if len(Color) == 3 and add_alpha:
            Color = (*Color, 255)
        return (clamp(c, 0.0, 255.0) for c in Color)
    elif isinstance(Color, str):
        if Color[0] != "#" or len(Color) not in [7, 9]:
            raise ValueError(
                "Invalid Color string. Must be a hexadecimal string of 7 (RGB) or 9 (RGBA) characters including '#'."
            )
        if len(Color) == 7 and add_alpha:
            Color += "ff"
        return Color
    else:
        raise TypeError(
            "Color must be either a tuple of 3 or 4 integers or a hexadecimal string."
        )


def RemoveDirectory(path: str) -> None:
    """
    Removes a directory and all its contents.

    Parameters:
        path (str): The path to the directory to be removed.
    """

    shutil.rmtree(path, ignore_errors=True)


def RemoveFile(path: str) -> None:
    """
    Removes a file.

    Parameters:
        path (str): The path to the file to be removed.
    """
    os.remove(path)


def CopyFiles(old_dir: str, new_dir: str, target_file: str, rename: str = None) -> None:
    """
    Copies a file from one directory to another.

    Parameters:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
        target_file (str): The name of the file to be copied.
        rename (str, optional): The new name for the copied file. Defaults to None.
    """
    CreateDirectory(new_dir)
    if rename is None:
        shutil.copyfile(
            os.path.join(old_dir, target_file), os.path.join(new_dir, target_file)
        )
    else:
        shutil.copyfile(
            os.path.join(old_dir, target_file), os.path.join(new_dir, rename)
        )


def CopyFolder(old_dir: str, new_dir: str) -> None:
    """
    Copies a folder and all its contents to a new location.

    Parameters:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
    """
    CreateDirectory(new_dir)
    shutil.copytree(
        os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True
    )


def MoveFolder(old_dir: str, new_dir: str) -> None:
    """
    Moves a folder and all its contents to a new location.

    Parameters:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
    """
    CreateDirectory(new_dir)
    shutil.move(os.path.realpath(old_dir), os.path.realpath(new_dir))


def zipit(zip_name, dir_list: dict) -> None:
    """
    Create a ZIP archive containing multiple directories and files.

    Parameters:
        zip_name: The name of the ZIP archive.
        dir_list (dict): A dictionary where the keys are source directories and the values are target directories.

    Note:
        The target directories represent the structure inside the ZIP archive.
    """

    excluded_extensions = [".js.map"]

    def zipdir(ziph: zipfile.ZipFile, source, target):
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    if any(file.endswith(ext) for ext in excluded_extensions):
                        continue
                    ziph.write(
                        os.path.join(root, file),
                        os.path.join(
                            target,
                            os.path.relpath(
                                os.path.join(root, file), os.path.join(source, ".")
                            ),
                        ),
                    )
        else:
            ziph.write(
                source,
                os.path.relpath(
                    os.path.join(target, source), os.path.join(source, "..")
                ),
            )

    zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for source, target in dir_list.items():
        zipdir(zipf, source, target)
    zipf.close()


def CreateDirectory(path: str) -> None:
    """
    Creates a new directory.

    Parameters:
        path (str): The path to the new directory.
    """
    this_path = os.path.join("./", path.lstrip("/"))
    os.makedirs(this_path, exist_ok=True)


def File(
    name: str,
    content: str | dict,
    directory: str,
    mode: str,
    skip_tag: bool = False,
    **parameters,
) -> None:
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
    from anvil.lib.config import Config, ConfigOption, ConfigSection

    CreateDirectory(directory)
    type = name.split(".")[-1]
    out_content = ""
    file_content = content
    stamp = f"Generated with StarkTMA/Anvil {__version__}"
    time = datetime.now(datetime.now().astimezone().tzinfo).strftime(
        "%d-%m-%Y %H:%M:%S %z"
    )
    copyright = f"Property of {Config().get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY)}"
    path = os.path.normpath(os.path.join(directory, name))
    oneline = Config().get_option(ConfigSection.ANVIL, ConfigOption.MINIFY)
    if mode == "w":
        match type:
            case "json" | "material" | "code-workspace":
                out_content = (
                    f"//Filename: {name}\n//{stamp}\n//{time}\n//{copyright}\n\n"
                )
                file_content = json.dumps(
                    content,
                    sort_keys=False,
                    indent=4 if not oneline else None,
                    ensure_ascii=False,
                )
            case "py" | "mcfunction":
                out_content = f"#Filename: {name}\n#{stamp}\n#{time}\n#{copyright}\n\n"
            case "lang":
                out_content = (
                    f"##Filename: {name}\n##{stamp}\n##{time}\n##{copyright}\n\n"
                )
    if skip_tag:
        out_content = file_content
    else:
        out_content += file_content

    with open(path, mode, encoding="utf-8") as file:
        file.write(out_content)


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


def validate_namespace_project_name(
    namespace: str, project_name: str, is_addon: bool = False
):
    """Validates namespace and project name according to Minecraft addon requirements.

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
        if not namespace.endswith(f"_{pascal_project_name.lower()}"):
            raise ValueError(
                f"Every namespace must be unique to the pack. For this pack it should be {namespace}."
            )


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
