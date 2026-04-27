__all__ = ["ANVIL", "CONFIG"]


def __getattr__(name: str):
    if name == "CONFIG":
        from .lib.config import CONFIG as _CONFIG

        globals()["CONFIG"] = _CONFIG
        return _CONFIG
    if name == "ANVIL":
        from .api.core.core import ANVIL as _ANVIL

        globals()["ANVIL"] = _ANVIL
        return _ANVIL
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(list(globals().keys()) + ["ANVIL", "CONFIG"])
