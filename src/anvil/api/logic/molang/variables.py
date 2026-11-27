from anvil.api.logic.molang._helpers import _VarMeta
from anvil.api.logic.molang.core import Molang
from anvil.api.logic.molang.query import Context

__all__ = ["Variable", "TempVar"]


class Variable(Molang):
    handle = "v"

    @classmethod
    def _set_var(cls, name) -> None:
        setattr(cls, name, cls.__query__(cls, "v", name))
        Context._set_var(name)

    @classmethod
    def IsFirstPerson(cls) -> Molang:
        return cls.__query__(cls, "v", "is_first_person")

    @classmethod
    def IsPaperdoll(cls) -> Molang:
        return cls.__query__(cls, "v", "is_paperdoll")

    @classmethod
    def AttackTime(cls) -> Molang:
        return cls.__query__(cls, "v", "attack_time")


class TempVar(Molang, metaclass=_VarMeta):
    handle = "t"
