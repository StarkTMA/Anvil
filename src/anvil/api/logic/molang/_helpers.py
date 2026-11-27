def _in_range(name: str, value, low: int, high: int):
    """`value`, after checking that a number is from `low` to `high`. Molang passes as is."""
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and not low <= value <= high
    ):
        raise ValueError(f"'{name}' must be from {low} to {high}, got {value}.")
    return value


def _list_of(query: str, what: str, values: list[str]) -> list[str]:
    """`values`, after checking it is a list rather than a single string."""
    if isinstance(values, str):
        raise TypeError(
            f"{query} takes a list of {what}, got the string {str(values)!r}. "
            f"Use {query}([{str(values)!r}])."
        )
    return list(values)


class _VarMeta(type):
    def __getattr__(cls, name):
        if name.startswith("_"):
            raise AttributeError(name)
        val = cls.__query__(cls, cls.handle, name)
        setattr(cls, name, val)
        return val

