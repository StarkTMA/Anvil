from anvil.api.logic.molang.core import Molang

__all__ = ["_Vec3Struct", "_AabbStruct", "_ColorStruct", "_UVStruct", "_TRSStruct"]


class _Vec3Struct(Molang):
    """Molang struct with x, y, z component access."""

    def __new__(cls, molang: "Molang | str") -> "_Vec3Struct":
        return super().__new__(cls, str(molang))

    @property
    def x(self) -> "Molang":
        return Molang(self.__struct__("x"))

    @property
    def y(self) -> "Molang":
        return Molang(self.__struct__("y"))

    @property
    def z(self) -> "Molang":
        return Molang(self.__struct__("z"))


class _AabbStruct(Molang):
    """Molang struct for axis-aligned bounding boxes, with .min and .max each returning a Vec3Struct."""

    def __new__(cls, molang: "Molang | str") -> "_AabbStruct":
        return super().__new__(cls, str(molang))

    @property
    def min(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("min"))

    @property
    def max(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("max"))


class _ColorStruct(Molang):
    """Molang struct with r, g, b, a color component access, each 0.0 to 1.0."""

    def __new__(cls, molang: "Molang | str") -> "_ColorStruct":
        return super().__new__(cls, str(molang))

    @property
    def r(self) -> "Molang":
        return Molang(self.__struct__("r"))

    @property
    def g(self) -> "Molang":
        return Molang(self.__struct__("g"))

    @property
    def b(self) -> "Molang":
        return Molang(self.__struct__("b"))

    @property
    def a(self) -> "Molang":
        return Molang(self.__struct__("a"))


class _UVStruct(Molang):
    """Molang struct with u, v texture coordinate/size component access."""

    def __new__(cls, molang: "Molang | str") -> "_UVStruct":
        return super().__new__(cls, str(molang))

    @property
    def u(self) -> "Molang":
        return Molang(self.__struct__("u"))

    @property
    def v(self) -> "Molang":
        return Molang(self.__struct__("v"))


class _TRSStruct(Molang):
    """Molang struct with translation, rotation, and scale component access, each returning a Vec3Struct."""

    def __new__(cls, molang: "Molang | str") -> "_TRSStruct":
        return super().__new__(cls, str(molang))

    @property
    def translation(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("t"))

    @property
    def rotation(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("r"))

    @property
    def scale(self) -> "_Vec3Struct":
        return _Vec3Struct(self.__struct__("s"))
