"""Reusable field encoders for `JsonObject` fields.

An encoder is a callable `(value) -> json` that turns a field's value into its JSON form on
export. The field keeps the value as the user set it.
"""

from __future__ import annotations

import math
from functools import partial
from typing import TYPE_CHECKING, Any

from anvil.api.core.enums import BlockFaceValues
from anvil.api.core.types import (
    RGB,
    RGB255,
    RGBA,
    RGBA255,
    BlockReference,
    Color,
    Encoder,
    HexRGB,
    HexRGBA,
    ItemReference,
    NumberRange,
)
from anvil.lib.lib import clamp

if TYPE_CHECKING:
    from anvil.api.actors.components import BreedPartner
    from anvil.api.vanilla.effects import MinecraftEffects


def keyed(attribute: str) -> Encoder:
    """Writes a list of objects as a JSON object keyed by each item's `attribute`, for JSON
    whose keys are names the user picks (bones, faces). Pair it with `validators.unique`.
    """

    def encode(value: Any) -> Any:
        return {str(getattr(item, attribute)): item for item in value}

    return encode


def merged(value: Any) -> Any:
    """Writes a list of components as one JSON object keyed by each component's identifier."""
    payload: dict[str, Any] = {}
    for component in value:
        payload.update(component.__json__())
    return payload


def contents(value: Any) -> Any:
    """Writes a component container as its components only, without its name."""
    return merged(value._components)


class KeptObject(dict):
    """A JSON object written even when it is empty. Anvil drops empty objects on export, but
    some keys are switches whose empty object turns a behavior on (`"remove_on_hit": {}`).
    """


def kept(value: Any) -> Any:
    """Writes a part as an object that is kept when it has no options set, and a switch as
    `{}` when True and nothing when False.
    """
    if value is True:
        return KeptObject()
    if value is False:
        return None
    return KeptObject(value.__json__())


def bounds(low: str, high: str, *, exact: bool = False) -> Encoder:
    """Writes a `(min, max)` pair as an object with the keys `low` and `high`, smallest value
    first. A single number is written as it is, or as both ends when `exact`.
    """

    def encode(value: Any) -> Any:
        if isinstance(value, (tuple, list)):
            return {low: min(value), high: max(value)}
        if exact:
            return {low: value, high: value}
        return value

    return encode


min_max = bounds("min", "max")
range_min_max = bounds("range_min", "range_max")
xp_range = bounds("minXP", "maxXP", exact=True)
despawn_distance = bounds("min_distance", "max_distance")


# api.actors.components


def block_object(block: BlockReference) -> Any:
    """A block as `{"name": ..., "states": ...}`."""
    from anvil.lib.schemas import MinecraftBlockDescriptor

    if isinstance(block, MinecraftBlockDescriptor):
        if block.states:
            return {"name": block.identifier, "states": dict(block.states)}
        return {"name": block.identifier}
    return {"name": block}


def item_objects(items: list[ItemReference]) -> list[Any]:
    """Items as `[{"item": ...}, ...]`."""
    return [{"item": item} for item in items]


def effect_name(effect: MinecraftEffects | str) -> str:
    """An effect name without the `minecraft:` namespace."""
    return str(effect).removeprefix("minecraft:")


def effect_names(effects: list[MinecraftEffects | str]) -> list[str]:
    return [effect_name(effect) for effect in effects]


def skin_variants(skins: list[int]) -> list[Any]:
    return [{"variant": skin} for skin in skins]


def speed_from_meters(digits: int) -> Encoder:
    """Converts a speed in blocks per second to the game's speed value."""

    def convert(speed: float) -> float:
        return round(0.152 * math.sqrt(speed), digits)

    def encode(value: float | NumberRange) -> Any:
        if isinstance(value, (int, float)):
            return convert(value)
        return range_min_max((convert(value[0]), convert(value[1])))

    return encode


def loot_table(value: Any) -> Any:
    """A loot table, or its path, as `{"table": ...}`. A part is written as it is."""
    from anvil.lib.jsonmodel import JsonObject

    if isinstance(value, JsonObject):
        return value
    return {"table": value}


def effects_object(effects: list[Any]) -> Any:
    return {"effects": effects}


def pairs(pairs: list[tuple[Any, Any]]) -> Any:
    """`(key, value)` pairs as a JSON object."""
    return {str(key): str(value) for key, value in pairs}


def property_names(names: list[str]) -> list[str]:
    """Entity property names, with the project namespace where they have none."""
    from anvil.lib.config import CONFIG

    return [name if ":" in name else f"{CONFIG.NAMESPACE}:{name}" for name in names]


def component_groups(groups: list[str]) -> Any:
    return {"component_groups": groups}


def damage_sensor(value: Any) -> Any:
    if isinstance(value, bool):
        return "yes" if value else "no"
    return value


ANCHORS = ("origin", "eye_height", "middle")


def projectile_anchor(value: Any) -> Any:
    if isinstance(value, int) and not isinstance(value, bool):
        return ANCHORS[value]
    return value


def trigger(value: Any) -> Any:
    """Events as triggers: the game reads a bare event name only on some fields, so a name
    is written as `{"event": name, "target": "self"}`."""
    from anvil.api.core.components import EventTrigger
    from anvil.api.core.enums import FilterSubject

    if isinstance(value, list):
        return [trigger(item) for item in value]
    if isinstance(value, str):
        return EventTrigger(event=value, target=FilterSubject.Self)
    return value


def block_objects(blocks: list[BlockReference]) -> list[Any]:
    """Blocks as `[{"name": ..., "states": ...}, ...]`."""
    return [block_object(block) for block in blocks]


def breeds_with(partners: list["BreedPartner"]) -> dict[str, Any]:
    """The partners as `{mate: breed event}`, the form the game reads: an empty object
    without a breed event."""
    return {
        str(partner.mate_type): trigger(partner.breed_event) or {}
        for partner in partners
    }


# api.biomes.components


def color_or_map(color_maps: tuple[str, ...]):
    def encode(value: Color | str) -> str | dict[str, str]:
        if value in color_maps:
            return {"color_map": value}
        return to_hex(value)

    return encode


# api.blocks.components


def expand_faces(faces: list[BlockFaceValues]) -> list[str]:
    from anvil.api.core.enums import expand_block_face_sides

    return [str(face) for face in expand_block_face_sides(list(faces))]


# anvil.lib.lib (formerly AnvilFormatter)


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
            a = clamp(float(color[3]), 0.0, 255.0) / 255.0 if len(color) == 4 else 1.0
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


to_hex = partial(convert_color, target=HexRGB)
to_rgba = partial(convert_color, target=RGBA)
