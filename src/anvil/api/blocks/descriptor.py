"""`BlockDescriptor`: a block matched by name, states, tags, or a mix of them."""

from anvil.lib.jsonmodel import Identifier, JsonObject, json_field

__all__ = ["BlockDescriptor"]


class BlockDescriptor(JsonObject):
    """A block matched by its name, its states, a Molang expression over its tags, or a mix
    of them. A block with only a name is written as the name itself, so use an `Identifier`
    or a `Block` for that.

    Args:
        name (Identifier, optional): The block.
        states (dict[str, str | int | float | bool], optional): The states to match. Needs a
            name.
        tags (str, optional): A Molang expression over block tags, such as
            `Query.AllTags(["stone"])`.
    """

    name: Identifier | None = None
    states: dict[str, str | int | float | bool] = json_field(
        default_factory=dict, omit_default=True
    )
    tags: str | None = None

    def __validate__(self) -> None:
        if self.name is None and self.tags is None:
            raise ValueError("A block descriptor needs a name or tags.")
        if self.states and self.name is None:
            raise ValueError(
                f"States need a block name. Block descriptor [tags={self.tags}]"
            )
        if self.states and self.tags is not None:
            raise ValueError(
                f"A block descriptor with tags cannot have states. Block descriptor "
                f"[name={self.name}, tags={self.tags}]"
            )
