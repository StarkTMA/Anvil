from anvil.api.core.components import ComponentGroup, _Components
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG


# _Components and ComponentGroup are defined in anvil.api.core.components
# and re-exported here for backward compatibility with existing imports.
__all__ = ["_Components", "ComponentGroup", "_Properties"]


class _Properties:
    def _enforce_count_limit(self):
        if len(self._properties) >= 32:
            raise ValueError(
                "Cannot have more than 32 properties in a component group."
            )

    def __init__(self):
        self._properties = {}

    def enum(
        self, name: str, values: tuple[str], default: str, *, client_sync: bool = False
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "enum",
            "default": default,
            "values": values,
            "client_sync": client_sync,
        }
        return self

    def int(
        self,
        name: str,
        range: tuple[int, int],
        *,
        default: int = 0,
        client_sync: bool = False,
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "int",
            "default": default if isinstance(default, Molang) else int(default),
            "range": range,
            "client_sync": client_sync,
        }
        return self

    def float(
        self,
        name: str,
        range: tuple[float, float],
        *,
        default: float = 0,
        client_sync: bool = False,
    ):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "float",
            "default": float(default),
            "range": [float(f) for f in range],
            "client_sync": client_sync,
        }
        return self

    def bool(self, name: str, *, default: bool = False, client_sync: bool = False):
        self._enforce_count_limit()
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "bool",
            "default": default,
            "client_sync": client_sync,
        }
        return self

    @property
    def _export(self):
        return self._properties
