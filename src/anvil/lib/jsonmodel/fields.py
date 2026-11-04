"""`json_field`, which declares a `JsonObject` field."""

import dataclasses
from collections.abc import Callable
from typing import Any


def json_field(
    *,
    default: Any = dataclasses.MISSING,
    default_factory: Callable[[], Any] | Any = dataclasses.MISSING,
    key: str | None = None,
    omit_default: bool = False,
    init: bool = True,
    exclude: bool = False,
    positional: bool = False,
) -> Any:
    """Declares a `JsonObject` field. The annotation says what the field accepts and how it is
    written; metadata in `Annotated` adds bounds and JSON shapes (see `jsontypes`).

    Args:
        default: The default value. `None` means the key is left out of the JSON.
        default_factory: A factory for mutable defaults such as lists.
        key: The JSON key, when it differs from the field name (for example `"minecraft:foo"`).
        omit_default: Leave the key out of the JSON while the value equals the default.
        init: `False` for a constant the user never sets, such as a `type` discriminator.
        exclude: Keep the field out of the JSON: a constructor option that is not a JSON key,
            or state the object keeps for its own methods. Its annotation is still checked.
        positional: The field can also be given as the first argument, like the `name` of a file.
    """
    return dataclasses.field(
        default=default,
        default_factory=default_factory,
        init=init,
        kw_only=not positional,
        metadata={"key": key, "omit_default": omit_default, "exclude": exclude},
    )
