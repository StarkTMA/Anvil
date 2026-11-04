"""The base of every feature type, and the `distribution` shared by scatter features
and feature rules.

Each feature type has its own module with three classes: `_XFeature` is the body of the
feature, `_XFeatureFile` is the document written to the file (`format_version` and the
body under its `minecraft:` key), and `XFeature` is the file class you create and build.
"""

from collections.abc import Sequence
from typing import Annotated, Any, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import AtLeastOne, Fraction, JsonFile, JsonObject, json_field


class CoordinateRange(JsonObject):
    """A random offset along one axis of a scatter, between the two ends of `extent`.

    Args:
        distribution (Literal["uniform", "gaussian", "inverse_gaussian", "triangle", "fixed_grid", "jittered_grid"]):
            How the offset is picked within `extent`.
        extent (tuple[int, int]): The lowest and highest offset, both included, from the
            position the scatter starts at.
        grid_offset (int, optional): Grid distributions only: the offset of the grid along
            this axis.
        step_size (int, optional): Grid distributions only: the distance between two steps
            of the grid.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction#coordinate-range)
    """

    distribution: Literal[
        "uniform",
        "gaussian",
        "inverse_gaussian",
        "triangle",
        "fixed_grid",
        "jittered_grid",
    ] = json_field(positional=True)
    extent: tuple[int, int] = json_field(positional=True)
    grid_offset: int | None = json_field(default=None)
    step_size: Annotated[int, AtLeastOne] | None = json_field(default=None)

    def __validate__(self) -> None:
        grid = self.distribution in ("fixed_grid", "jittered_grid")
        if not grid and (self.grid_offset is not None or self.step_size is not None):
            raise ValueError(
                f"grid_offset and step_size only apply to grid distributions, not '{self.distribution}'."
            )


class _ScatterParams(JsonObject):
    """The `distribution` of a scatter feature or a feature rule: where, how many times and
    how likely the feature is placed."""

    iterations: int | str = json_field()
    scatter_chance: Annotated[float | str | tuple[int, int], Fraction] | None = (
        json_field(default=None)
    )
    coordinate_eval_order: Literal["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"] | None = (
        json_field(default=None)
    )
    x: float | str | CoordinateRange = json_field()
    y: float | str | CoordinateRange = json_field()
    z: float | str | CoordinateRange = json_field()


class DistributionMixin:
    """Gives a scatter feature or a feature rule its `distribution()` builder."""

    def _distribution_owner(self) -> Any:
        raise NotImplementedError()

    def distribution(
        self,
        iterations: int | str,
        scatter_chance: float | tuple[int, int] | str | None,
        x: float | str | CoordinateRange,
        y: float | str | CoordinateRange,
        z: float | str | CoordinateRange,
        coordinate_eval_order: (
            Literal["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"] | None
        ) = None,
    ):
        """Sets where, how many times and how likely the feature is placed.

        Coordinates are offsets from the position the scatter starts at: a number, a Molang
        expression or a :class:`CoordinateRange`.

        Args:
            iterations (int | str): How many times the feature is placed, or a Molang
                expression that returns it.
            scatter_chance (float | tuple[int, int] | str | None): The chance that any
                iteration runs, checked once: a percentage, a `(numerator, denominator)`
                fraction or a Molang expression. None leaves it out: always.
            x (float | str | CoordinateRange): The x offset, evaluated each iteration.
            y (float | str | CoordinateRange): The y offset, evaluated each iteration.
            z (float | str | CoordinateRange): The z offset, evaluated each iteration.
            coordinate_eval_order (Literal["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"], optional):
                The order the coordinates are evaluated in, when one depends on another.
                Game default "xzy".
        """
        self._distribution_owner().set_distribution(
            _ScatterParams(
                iterations=iterations,
                scatter_chance=scatter_chance,
                coordinate_eval_order=coordinate_eval_order,
                x=x,
                y=y,
                z=z,
            )
        )
        return self


class _FeatureDescription(JsonObject):
    """The `description` of a feature."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: str | None = None

    def set_identifier(self, identifier: str) -> None:
        """Sets the `namespace:name` of the feature, its file name being the name."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("A feature needs an identifier.")


class _Feature(JsonObject, abstract=True):
    """The body every feature type starts with: its description."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: _FeatureDescription = json_field(default_factory=_FeatureDescription)


class Feature(JsonFile):
    """The base of the feature types. Create one of them, such as :class:`ScatterFeature`.

    A feature is written as its identifier wherever another file references it.
    """

    _object_type = "Feature"
    _extension = ".json"
    _pack = Pack.BP
    _folder = "features"

    def __init__(self, name: str) -> None:
        """Creates the feature file.

        Args:
            name (str): The name of the feature, also its file name. The identifier is
                `<namespace>:<name>`.

        Raises:
            TypeError: When `Feature` itself is created rather than a feature type.
        """
        super().__init__(name)
        if self._content.feature is not None:
            self._feature.description.set_identifier(self.identifier)

    def _description(self) -> _FeatureDescription:
        """A description with the feature's identifier, for a body built in one go."""
        return _FeatureDescription(identifier=self.identifier)

    @property
    def _feature(self) -> Any:
        """The body of the feature in the file."""
        return self._content.feature

    def queue(self) -> "Feature":
        """Queues the feature for export."""
        return super().queue()


def _blocks(
    blocks: Sequence[str | Block | BlockDescriptor],
) -> list[str | Block | BlockDescriptor]:
    if isinstance(blocks, str):
        raise TypeError(f"Expected a list of blocks, got the string {blocks!r}.")
    return list(blocks)
