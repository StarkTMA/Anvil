"""A collection of useful functions and classes used throughout the program."""

import inspect
import json
import os
import re
import shutil
import subprocess
import zipfile
from datetime import datetime

import commentjson as commentjson
from anvil.lib.types import RGB, RGB255, RGBA, RGBA255, Color, HexRGB, HexRGBA

from ..__version__ import __version__

APPDATA: str = os.getenv("APPDATA")
APPDATA_LOCAL: str = os.getenv("LOCALAPPDATA")

RELEASE_COM_MOJANG = os.path.join(
    APPDATA, "Minecraft Bedrock", "Users", "Shared", "games", "com.mojang"
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


class PrettyPrintedEncoder(json.JSONEncoder):
    def __init__(self, *args, max_width=88, indent=4, **kwargs):
        super().__init__(*args, indent=indent, **kwargs)
        self.max_width = max_width
        self._indent_str = " " * indent

    def encode(self, o, _level=0):
        if isinstance(o, (list, tuple)):
            items = [self.encode(v, _level + 1) for v in o]
            inline = f"[{', '.join(items)}]"
            if len(inline) <= self.max_width - _level * self.indent:
                return inline
            inner = ",\n".join(self._indent_str * (_level + 1) + i for i in items)
            return f"[\n{inner}\n{self._indent_str * _level}]"

        elif isinstance(o, dict):
            items = [
                f"{json.dumps(str(k))}: {self.encode(v, _level + 1)}"
                for k, v in o.items()
            ]
            inline = f"{{ {', '.join(items)} }}"
            if len(inline) <= self.max_width - _level * self.indent:
                return inline
            inner = ",\n".join(self._indent_str * (_level + 1) + i for i in items)
            return f"{{\n{inner}\n{self._indent_str * _level}}}"

        else:
            return json.dumps(o)


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
                    cls=PrettyPrintedEncoder,
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


def convert_color(
    color: Color,
    target: RGB | RGBA | RGB255 | RGBA255 | HexRGB | HexRGBA | None = None,
) -> RGB | RGBA | RGB255 | RGBA255 | HexRGB | HexRGBA:
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
    if target is None:
        if is_str:
            target = HexRGBA if len(hex_color) in [4, 8] else HexRGB
        else:
            max_val = max(color[:3])
            has_alpha = len(color) == 4
            target = (
                RGBA255
                if has_alpha and max_val > 1.0
                else RGB255 if max_val > 1.0 else RGBA if has_alpha else RGB
            )

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
        max_val = max(color[:3])

        if max_val > 1.0:
            # Assume 0-255 range
            r = clamp(color[0], 0.0, 255.0) / 255.0
            g = clamp(color[1], 0.0, 255.0) / 255.0
            b = clamp(color[2], 0.0, 255.0) / 255.0
            a = clamp(color[3], 0.0, 255.0) / 255.0 if len(color) == 4 else 1.0
        else:
            # Assume 0-1 range
            r = clamp(color[0], 0.0, 1.0)
            g = clamp(color[1], 0.0, 1.0)
            b = clamp(color[2], 0.0, 1.0)
            a = clamp(color[3], 0.0, 1.0) if len(color) == 4 else 1.0

    # Convert to target format
    if target in (HexRGB, HexRGBA):
        # Convert to hex (pre-compute once)
        hex_r = int(round(r * 255))
        hex_g = int(round(g * 255))
        hex_b = int(round(b * 255))
        hex_a = int(round(a * 255))

        return (
            f"#{hex_r:02x}{hex_g:02x}{hex_b:02x}{hex_a:02x}"
            if target is HexRGBA
            else f"#{hex_r:02x}{hex_g:02x}{hex_b:02x}"
        )

    elif target is RGB:
        return (r, g, b)

    elif target is RGBA:
        return (r, g, b, a)

    elif target is RGB255:
        return (r * 255.0, g * 255.0, b * 255.0)

    elif target is RGBA255:
        return (r * 255.0, g * 255.0, b * 255.0, a * 255.0)

    else:
        raise ValueError(f"Unsupported target format: {target}")
