"""Experimental entity filters. They need `features.experimental` in anvilconfig.json."""

from anvil.api.core.filters import Filter as _Filter
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel.enums import FilterOperation, FilterSubject

__all__ = ["Filter"]


def _require_experimental(test: str) -> None:
    if not CONFIG._EXPERIMENTAL:
        raise ValueError(
            f"Filter.{test} is experimental: turn on features.experimental in anvilconfig.json."
        )


class Filter(_Filter):
    """Entity filters, with the experimental tests. Has every public `Filter` test too."""

    @classmethod
    def speed(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ) -> "Filter":
        """[EXPERIMENTAL] Tests the subject entity's speed in meters per second.
        Needs the experimental flag in anvilconfig.json.

        Args:
            value (float): Speed in meters per second.
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Example:
            Filter.speed(4.0, operator=FilterOperation.Greater)
        """
        _require_experimental("speed")
        return cls("speed", subject, operator, None, value)

    @classmethod
    def horizontal_speed(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ) -> "Filter":
        """[EXPERIMENTAL] Tests the subject entity's horizontal speed in meters per second.
        Needs the experimental flag in anvilconfig.json.

        Args:
            value (float): Horizontal speed in meters per second.
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Example:
            Filter.horizontal_speed(0.0)
        """
        _require_experimental("horizontal_speed")
        return cls("horizontal_speed", subject, operator, None, value)

    @classmethod
    def vertical_speed(
        cls,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ) -> "Filter":
        """[EXPERIMENTAL] Tests the subject entity's signed vertical speed in meters per second. Positive moves up, negative moves down.
        Needs the experimental flag in anvilconfig.json.

        Args:
            value (float): Signed vertical speed in meters per second.
            subject (FilterSubject, optional): Subject to test. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use. Defaults to FilterOperation.Equals.

        Example:
            Filter.vertical_speed(0.0, operator=FilterOperation.Less)
        """
        _require_experimental("vertical_speed")
        return cls("vertical_speed", subject, operator, None, value)
