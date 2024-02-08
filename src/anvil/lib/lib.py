"""A collection of useful functions and classes used throughout the program."""
import json as json
import os
import shutil
import subprocess
import zipfile
from datetime import datetime
from enum import StrEnum

import commentjson as commentjson

from anvil.api.types import Color
from anvil.lib.logger import Logger

from ..__version__ import __version__

APPDATA: str = os.getenv("APPDATA").rstrip("Roaming")  # type: ignore
DESKTOP: str = os.path.join(os.getenv("USERPROFILE"), "Desktop")  # type: ignore
MOLANG_PREFIXES = ("q.", "v.", "c.", "t.", "query.", "variable.", "context.", "temp.", "math.")


# --------------------------------------------------------------------------


def FileExists(path) -> bool:
    """Checks if a file exists.

    Args:
        path (_type_): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(path)


def normalize_180(angle: float | str) -> float:
    """Normalizes an angle between -180 and 180.

    Args:
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

    Args:
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

    Args:
        start (int): The starting value.
        stop (int): The ending value.
        num (float, optional): The number of values to generate. Defaults to 1.

    Returns:
        list: A list of interpolated values between start and stop.
    """
    step = (stop - start) / (num - 1)
    values = [round(start + i * step, 2) for i in range(num)]
    return values


def process_color(color: Color, add_alpha: bool = False) -> str | list[float]:
    if isinstance(color, tuple):
        if len(color) not in [3, 4]:
            raise ValueError("Color tuple must have 3 or 4 elements.")
        if len(color) == 3 and add_alpha:
            color = (*color, 255)
        return (clamp(c, 0.0, 255.0) for c in color)
    elif isinstance(color, str):
        if color[0] != "#" or len(color) not in [7, 9]:
            raise ValueError(
                "Invalid color string. Must be a hexadecimal string of 7 (RGB) or 9 (RGBA) characters including '#'."
            )
        if len(color) == 7 and add_alpha:
            color += "ff"
        return color
    else:
        raise TypeError("Color must be either a tuple of 3 or 4 integers or a hexadecimal string.")


# Legacy code, will be removed in the future.
def Defaults(type, *args):
    """Creates a file with default content. This is a legacy function and will be removed in the future.

    Args:
        type (str): The type of file to be created.

    Returns:
        dict: The file content.
    """
    match type:
        case "recipe_shaped":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shaped": {
                    "tags": ["crafting_table"],
                    "pattern": [],
                    "key": {},
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_shapeless":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["crafting_table"],
                    "ingredients": [],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_stonecutter":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["stonecutter"],
                    "ingredients": [],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_smithing_table":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["smithing_table"],
                    "ingredients": [{"item": "minecraft:netherite_ingot", "count": 1}],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_furnace":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_furnace": {
                    "tags": args[3],
                    "output": args[1],
                    "input": args[2],
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "spawn_rules":
            return {
                "format_version": "1.8.0",
                "minecraft:spawn_rules": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                        "population_control": "ambient",
                    },
                    "conditions": [],
                },
            }


def RemoveDirectory(path: str) -> None:
    """
    Removes a directory and all its contents.

    Args:
        path (str): The path to the directory to be removed.
    """


def RemoveFile(path: str) -> None:
    """
    Removes a file.

    Args:
        path (str): The path to the file to be removed.
    """
    os.remove(path)


def CopyFiles(old_dir: str, new_dir: str, target_file: str, rename: str = None) -> None:
    """
    Copies a file from one directory to another.

    Args:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
        target_file (str): The name of the file to be copied.
        rename (str, optional): The new name for the copied file. Defaults to None.
    """
    CreateDirectory(new_dir)
    if rename is None:
        shutil.copyfile(os.path.join(old_dir, target_file), os.path.join(new_dir, target_file))
    else:
        shutil.copyfile(os.path.join(old_dir, target_file), os.path.join(new_dir, rename))


def CopyFolder(old_dir: str, new_dir: str) -> None:
    """
    Copies a folder and all its contents to a new location.

    Args:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
    """
    CreateDirectory(new_dir)
    shutil.copytree(os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True)


def zipit(zip_name, dir_list: dict) -> None:
    """
    Create a ZIP archive containing multiple directories and files.

    Args:
        zip_name: The name of the ZIP archive.
        dir_list (dict): A dictionary where the keys are source directories and the values are target directories.

    Note:
        The target directories represent the structure inside the ZIP archive.
    """

    def zipdir(ziph: zipfile.ZipFile, source, target):
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    ziph.write(
                        os.path.join(root, file),
                        os.path.join(
                            target,
                            os.path.relpath(os.path.join(root, file), os.path.join(source, ".")),
                        ),
                    )
        else:
            ziph.write(
                source,
                os.path.relpath(os.path.join(target, source), os.path.join(source, "..")),
            )

    zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for source, target in dir_list.items():
        zipdir(zipf, source, target)
    zipf.close()


def CreateDirectory(path: str) -> None:
    """
    Creates a new directory.

    Args:
        path (str): The path to the new directory.
    """
    this_path = os.path.join("./", path.lstrip("/"))
    os.makedirs(this_path, exist_ok=True)


def File(name: str, content: str | dict, directory: str, mode: str, skip_tag: bool = False, *args) -> None:
    """
    Create or modify a file with the given content.

    Args:
        name (str): The name of the file.
        content: The content of the file.
        directory (str): The directory path where the file should be created or modified.
        mode (str): The file mode, either "w" (write) or "a" (append).
        skip_tag (bool, optional): Whether to skip adding the file metadata tag. Defaults to False.
        *args: Additional StrEnum.

    Note:
        The file content is converted to the appropriate format based on the file extension.
    """
    from anvil.lib.config import Config, ConfigOption, ConfigSection

    CreateDirectory(directory)
    type = name.split(".")[-1]
    out_content = ""
    file_content = content
    stamp = f"Generated with StarkTMA/Anvil {__version__}"
    time = datetime.now(datetime.now().astimezone().tzinfo).strftime("%d-%m-%Y %H:%M:%S %z")
    copyright = f"Property of {Config().get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY)}"
    path = os.path.normpath(os.path.join(directory, name))
    if mode == "w":
        match type:
            case "json" | "material" | "code-workspace":
                out_content = f"//Filename: {name}\n//{stamp}\n//{time}\n//{copyright}\n\n"
                file_content = json.dumps(content, sort_keys=False, indent=4, ensure_ascii=False)
            case "py" | "mcfunction":
                out_content = f"#Filename: {name}\n#{stamp}\n#{time}\n#{copyright}\n\n"
            case "lang":
                out_content = f"##Filename: {name}\n##{stamp}\n##{time}\n##{copyright}\n\n"
    if skip_tag:
        out_content = file_content
    else:
        out_content += file_content

    prev = ""

    if FileExists(path):
        with open(path, "r", encoding="utf-8") as file:
            prev = file.read()

    if prev.split("\n")[6::] != file_content.split("\n"):
        with open(path, mode, encoding="utf-8") as file:
            file.write(out_content)


def process_subcommand(command: str, error_handle: str = "Error"):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_handle}: {e}")


def validate_namespace_project_name(namespace: str, project_name: str, is_addon: bool = False):
    pascal_project_name = "".join(x[0] for x in project_name.split("_")).upper()

    if namespace == "minecraft":
        Logger.reserved_namespace(namespace)

    if len(namespace) > 8:
        Logger.namespace_too_long(namespace)

    if len(project_name) > 16:
        Logger.project_name_too_long(namespace)

    if is_addon:
        if not namespace.endswith(f"_{pascal_project_name.lower()}"):
            Logger.unique_namespace(f"{namespace}_{pascal_project_name.lower()}")
