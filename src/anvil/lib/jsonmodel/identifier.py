"""`Identifier`, the `namespace:name` of everything in a pack, and the one place names are
parsed and checked.

`Identifier.parse(text, vanilla=...)` also checks the namespace: `minecraft` for what Minecraft
defines, the project namespace (`CONFIG.NAMESPACE`) for what the pack adds.
"""

from __future__ import annotations

import re

__all__ = ["Identifier", "NAME_PATTERN", "VANILLA_NAMESPACE"]

VANILLA_NAMESPACE = "minecraft"
"""The namespace of everything Minecraft defines."""

NAME_PATTERN = re.compile(
    r"(?:(?P<namespace>[a-z][a-z0-9_]*):)?(?P<name>[a-z_][a-z0-9_./-]*)"
)
"""`name` or `namespace:name`. A namespace starts with a letter, a name cannot start with a digit."""


class Identifier(str):
    """A `namespace:name`, or `namespace:name:data`.

    It is a `str` of that text, so it compares, formats and is written to JSON as the text,
    and it also has its parts as `namespace`, `name` and `data`.

    Args:
        namespace (str): The namespace.
        name (str): The name.
        data (str | int, optional): Data after the name, as in `minecraft:potion_type:long_swiftness`.
    """

    namespace: str
    name: str
    data: str | None

    def __new__(
        cls, namespace: str, name: str, data: str | int | None = None
    ) -> Identifier:
        text = f"{namespace}:{name}" if data is None else f"{namespace}:{name}:{data}"
        identifier = super().__new__(cls, text)
        identifier.namespace = namespace
        identifier.name = name
        identifier.data = None if data is None else str(data)
        return identifier

    @classmethod
    def parse(
        cls,
        text: str,
        *,
        vanilla: bool = False,
        data: str | int | None = None,
        object_type: str = "Name",
    ) -> Identifier:
        """Parses `name` or `namespace:name`. A name without a namespace gets the project
        namespace, `CONFIG.NAMESPACE`.

        Args:
            text (str): The name, with or without its namespace.
            vanilla (bool, optional): True when it must be in the `minecraft` namespace, False
                when it must be in the project namespace. Defaults to False.
            data (str | int, optional): Data written after the name.
            object_type (str, optional): What the name is for, used in the errors.

        Raises:
            ValueError: When the text is not a valid name, or its namespace is not the one
                `vanilla` asks for.
        """
        from anvil.lib.config import CONFIG

        if isinstance(text, Identifier) and data is None:
            identifier = text
        else:
            match = NAME_PATTERN.fullmatch(str(text))
            if match is None:
                raise ValueError(
                    f"Invalid name [{text}]. Use 'name' or 'namespace:name', with lowercase "
                    f"letters, digits, '_', '.', '-' or '/'. A name cannot start with a digit, "
                    f"and a namespace must start with a letter. {object_type}[{text}]"
                )
            identifier = cls(
                match["namespace"] or CONFIG.NAMESPACE, match["name"], data
            )
        namespace = VANILLA_NAMESPACE if vanilla else CONFIG.NAMESPACE
        if identifier.namespace != namespace:
            kind = "vanilla" if vanilla else "custom"
            raise ValueError(
                f"Invalid namespace '{identifier.namespace}'. A {kind} identifier is "
                f"'{namespace}:name'. {object_type}[{text}]"
            )
        return identifier

    @property
    def is_vanilla(self) -> bool:
        """If the identifier is in the `minecraft` namespace."""
        return self.namespace == VANILLA_NAMESPACE

    @property
    def display_name(self) -> str:
        """The name as title case words, `ruby_ore` as `Ruby Ore`."""
        return self.name.replace("_", " ").title()

    def __reduce__(self):
        return (Identifier, (self.namespace, self.name, self.data))
