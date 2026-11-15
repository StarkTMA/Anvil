"""The `minecraft:search_feature`."""

from typing import Annotated, ClassVar, Literal

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import AtLeastOne, JsonObject, json_field


class _SearchVolume(JsonObject):
    """The box a search feature sweeps, as offsets from its position."""

    min: tuple[int, int, int] = json_field()
    max: tuple[int, int, int] = json_field()

    def __validate__(self) -> None:
        if any(low > high for low, high in zip(self.min, self.max)):
            raise ValueError(
                f"Search volume min {self.min} must not be above max {self.max}."
            )


class _SearchFeature(_Feature):
    """The `minecraft:search_feature` body."""

    places_feature: str = json_field()
    search_volume: _SearchVolume = json_field()
    search_axis: Literal["-x", "+x", "-y", "+y", "-z", "+z"] = json_field()
    required_successes: Annotated[int, AtLeastOne] | None = None

    def set_search_volume(
        self, min_position: tuple[int, int, int], max_position: tuple[int, int, int]
    ) -> None:
        """Sets the box searched."""
        self.search_volume = _SearchVolume(min=min_position, max=max_position)


class _SearchFeatureFile(JsonObject):
    """The content of a search feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:search_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SearchFeature | None = json_field(
        key="minecraft:search_feature", default=None
    )

    def set_feature(self, feature: _SearchFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class SearchFeature(Feature[_SearchFeatureFile]):
    """Sweeps a box, layer by layer along an axis, for positions where a feature can be
    placed, and places it when enough are found. With `-x`, positions with greater x are
    checked first.

    - Succeeds if `required_successes` positions are found (1 by default).
    - Fails if fewer are found.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_search_feature)
    """

    def __init__(
        self,
        name: str,
        places_feature: "Feature | str",
        search_axis: Literal["-x", "+x", "-y", "+y", "-z", "+z"],
        min_position: tuple[int, int, int],
        max_position: tuple[int, int, int],
        required_successes: int | None = None,
    ) -> None:
        """Creates a search feature.

        Args:
            name (str): The name of the feature, also its file name.
            places_feature (Feature | str): The feature placed.
            search_axis (Literal["-x", "+x", "-y", "+y", "-z", "+z"]): The axis the search
                sweeps along.
            min_position (tuple[int, int, int]): The corner of the box with the smallest
                offsets.
            max_position (tuple[int, int, int]): The opposite corner.
            required_successes (int, optional): How many valid positions must be found. At
                least 1.
        """
        super().__init__(name)
        self._document.set_feature(
            _SearchFeature(
                description=self._description(),
                places_feature=str(places_feature),
                search_volume=_SearchVolume(
                    min=tuple(min_position), max=tuple(max_position)
                ),
                search_axis=search_axis,
                required_successes=required_successes,
            )
        )

    def search_volume(
        self, min_position: tuple[int, int, int], max_position: tuple[int, int, int]
    ) -> "SearchFeature":
        """Sets the box searched, as offsets from the feature's position.

        Args:
            min_position (tuple[int, int, int]): The corner with the smallest offsets.
            max_position (tuple[int, int, int]): The opposite corner.
        """
        self._feature.set_search_volume(tuple(min_position), tuple(max_position))
        return self
