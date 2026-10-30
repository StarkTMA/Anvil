"""`json_field`, which declares a `JsonObject` field, and `default_of`, a field's default."""

import dataclasses
from typing import Any

from anvil.api.core.types import DefaultFactory, Encoder, Validators


def default_of(field: dataclasses.Field) -> Any:
    """The default value of a field."""
    if field.default_factory is not dataclasses.MISSING:
        return field.default_factory()
    return field.default


def json_field(
    *,
    default: Any = dataclasses.MISSING,
    default_factory: DefaultFactory | Any = dataclasses.MISSING,
    key: str | None = None,
    validators: Validators = (),
    omit_default: bool = False,
    encoder: Encoder | None = None,
    init: bool = True,
    exclude: bool = False,
    positional: bool = False,
) -> Any:
    """Declares a `JsonObject` field.

    Parameters:
        default: The default value. `None` means the key is left out of the JSON.
        default_factory: A factory for mutable defaults such as lists.
        key: The JSON key, when it differs from the field name (for example `"minecraft:foo"`).
        validators: Checks run on export when the value is not `None`.
        omit_default: Leave the key out of the JSON while the value equals the default.
        encoder: Converts the value to its JSON form on export (for example a color to a hex
            string). The field keeps the value as the user set it.
        init: `False` for a constant the user never sets, such as a `type` discriminator.
        exclude: Keep the field out of the JSON: a constructor option that is not a JSON key,
            or state the object keeps for its own methods. Its validators still run.
        positional: The field can also be given as the first argument, like the `name` of a file.
    """
    return dataclasses.field(
        default=default,
        default_factory=default_factory,
        init=init,
        kw_only=not positional,
        metadata={
            "key": key,
            "validators": tuple(validators),
            "omit_default": omit_default,
            "encoder": encoder,
            "exclude": exclude,
        },
    )
