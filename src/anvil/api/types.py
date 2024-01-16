from typing import NewType


Color = NewType("Color", [tuple[int, int, int] | tuple[int, int, int, int] | str])
Seconds = NewType("Seconds", float)
Molang = NewType("Molang", str)
coordinate = NewType("coordinate", [float | str])
coordinates = NewType("tuple(x, y, z)", tuple[coordinate, coordinate, coordinate])
position = NewType("tuple(x, y, z)", tuple[coordinate, coordinate, coordinate])
rotation = NewType("tuple(ry,rx)", tuple[coordinate, coordinate])
level = NewType("tuple(lm,l)", tuple[float, float])
Component = NewType("Component", str)
Identifier = NewType("Identifier", str)
event = NewType("Event", str)
tick = NewType("Tick", int)
_range = NewType("[range]", str)
inf = 99999999999