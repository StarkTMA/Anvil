"""`KeyFrame`s, values over the day of a Vibrant Visuals setting, and the `KeyFramed` and
`KeyFramedColor` metadata that check and write them as `{"<time>": value}`."""

from dataclasses import dataclass
from typing import Any

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA, JsonSchema

from .jsontypes import COLOR_SCHEMA, InRange, JsonType

__all__ = ["KeyFrame", "KeyFramed", "KeyFramedColor"]

_TIME = InRange(0.0, 1.0)


@dataclass
class KeyFrame:
    """Represents a single keyframe for animating properties over the daily cycle.

    Attributes:
        time (float): The time of day, between 0.0 and 1.0.
        value (float | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The value at this keyframe (could be a float, RGB tuple, or Hex color).
    """

    time: float
    value: float | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255

    @classmethod
    def keyframe_dict(
        cls,
        keyframes: list["KeyFrame"],
        target_color_format=None,
    ) -> dict[str, float | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]:
        """Converts a list of KeyFrames into a dictionary suitable for Minecraft JSON.

        Each keyframe's time is formatted as a string key.

        Args:
            keyframes (list[KeyFrame]): A list of keyframe instances to convert.
            target_color_format (optional): The target color type class (e.g. HexRGB, RGB) to convert color values to.

        Returns:
            dict[str, float | HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]: A dictionary mapping time strings to their corresponding values.
        """
        from anvil.lib.lib import AnvilFormatter, AnvilValidator

        result = {}
        for k in keyframes:
            if AnvilValidator.is_color_value(k.value):
                result[str(k.time)] = AnvilFormatter.convert_color(
                    k.value, target_color_format
                )
            else:
                result[str(k.time)] = k.value
        return result


def _frames(value: Any) -> list[KeyFrame] | None:
    if isinstance(value, list) and value and isinstance(value[0], KeyFrame):
        return value
    return None


def _over_the_day(value: JsonSchema) -> JsonSchema:
    return {
        "anyOf": [
            value,
            {
                "type": "object",
                "propertyNames": {"pattern": "^(0(\\.[0-9]+)?|1(\\.0+)?)$"},
                "additionalProperties": value,
            },
        ]
    }


@dataclass(frozen=True, slots=True)
class KeyFramed(JsonType):
    """A number, or `KeyFrame`s written as `{"<time>": number}` over the day. Each time must
    be from 0.0 to 1.0.

    Args:
        minimum (float, optional): The lowest value, of the number or of every keyframe.
        maximum (float, optional): The highest value, of the number or of every keyframe.
    """

    minimum: float | None = None
    maximum: float | None = None

    def validate(self, name: str, value: Any) -> None:
        frames = _frames(value)
        values = InRange(self.minimum, self.maximum)
        if frames is None:
            values.validate(name, value)
            return
        for index, frame in enumerate(frames):
            _TIME.validate(f"{name}[{index}].time", frame.time)
            values.validate(f"{name}[{index}].value", frame.value)

    def encode(self, value: Any) -> Any:
        frames = _frames(value)
        return value if frames is None else KeyFrame.keyframe_dict(frames)

    def schema(self, inner: JsonSchema) -> JsonSchema:
        number = InRange(self.minimum, self.maximum).schema({"type": "number"})
        return _over_the_day(number)


@dataclass(frozen=True, slots=True)
class KeyFramedColor(JsonType):
    """A color in any format, or `KeyFrame`s written as `{"<time>": color}` over the day.
    Each time must be from 0.0 to 1.0. A hex color is written in full, in lower case."""

    def validate(self, name: str, value: Any) -> None:
        for index, frame in enumerate(_frames(value) or []):
            _TIME.validate(f"{name}[{index}].time", frame.time)

    def encode(self, value: Any) -> Any:
        from anvil.lib.lib import AnvilFormatter

        frames = _frames(value)
        if frames is None:
            return AnvilFormatter.convert_color(value)
        return KeyFrame.keyframe_dict(frames)

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return _over_the_day(COLOR_SCHEMA)
