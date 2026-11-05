"""The resource pack's `materials/entity.material`: custom entity materials."""

from typing import Annotated, Any, Literal

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import MATERIALS_VERSION
from anvil.lib.jsonmodel import (
    InRange,
    JsonFile,
    JsonObject,
    Keyed,
    NonNegative,
    Wrapped,
    json_field,
)
from anvil.lib.jsonmodel.enums import (
    MaterialDefinitions,
    MaterialFunc,
    MaterialOperation,
    MaterialStates,
)
from anvil.lib.jsonmodel.types import TextureFilter, TextureWrap


class _StencilFace(JsonObject):
    """The stencil test of the front or back faces of a material. Unset keys are left out."""

    stencilFunc: MaterialFunc | None = None
    stencilFailOp: MaterialOperation | None = None
    stencilDepthFailOp: MaterialOperation | None = None
    stencilPassOp: MaterialOperation | None = None
    stencilPass: MaterialOperation | None = None


class _SamplerState(JsonObject):
    """How a material samples one of its textures. Unset keys are left out."""

    samplerIndex: Annotated[int, NonNegative] = json_field()
    textureFilter: TextureFilter | None = None
    textureWrap: TextureWrap | None = None


class _MaterialSettings(JsonObject, abstract=True):
    """The settings shared by a material and its variants, with their builders. A plain key
    replaces what the base material has, a `+` key adds to it and a `-` key takes from it.
    Unset keys are left out."""

    states: list[MaterialStates] | None = None
    plus_states: list[MaterialStates] | None = json_field(default=None, key="+states")
    minus_states: list[MaterialStates] | None = json_field(default=None, key="-states")
    defines: list[MaterialDefinitions] | None = None
    plus_defines: list[MaterialDefinitions] | None = json_field(
        default=None, key="+defines"
    )
    minus_defines: list[MaterialDefinitions] | None = json_field(
        default=None, key="-defines"
    )
    frontFace: _StencilFace | None = None
    backFace: _StencilFace | None = None
    stencilRef: Annotated[int, InRange(0, 255)] | None = None
    depthFunc: MaterialFunc | None = None
    blendSrc: str | None = None
    blendDst: str | None = None
    vertexShader: str | None = None
    fragmentShader: str | None = None
    geometryShader: str | None = None
    vrGeometryShader: str | None = None
    vertexFields: list[Annotated[str, Wrapped("field")]] | None = None
    msaaSupport: str | None = None
    primitiveMode: str | None = None
    depthBias: float | None = None
    slopeScaledDepthBias: float | None = None
    depthBiasOGL: float | None = None
    slopeScaledDepthBiasOGL: float | None = None
    samplerStates: list[_SamplerState] | None = None
    plus_samplerStates: list[_SamplerState] | None = json_field(
        default=None, key="+samplerStates"
    )

    def set_states(self, *states: MaterialStates) -> "_MaterialSettings":
        """Sets the rendering states, replacing the base material's.

        Rendering states control basic graphics pipeline settings, such as blending, culling
        (rendering backfaces) or writing to the depth buffer.

        Args:
            states (MaterialStates): The states, such as `MaterialStates.DisableCulling`.
        """
        self.states = list(states)
        return self

    def add_states(self, *states: MaterialStates) -> "_MaterialSettings":
        """Adds rendering states to the base material's.

        Args:
            states (MaterialStates): The states to add.
        """
        self.plus_states = (self.plus_states or []) + list(states)
        return self

    def remove_states(self, *states: MaterialStates) -> "_MaterialSettings":
        """Removes rendering states of the base material, such as `DisableCulling` to cull
        backfaces again.

        Args:
            states (MaterialStates): The states to remove.
        """
        self.minus_states = (self.minus_states or []) + list(states)
        return self

    def set_defines(self, *defines: MaterialDefinitions) -> "_MaterialSettings":
        """Sets the shader defines, replacing the base material's.

        Defines toggle shader features, such as alpha testing (`ALPHA_TEST`), the enchantment
        glint (`GLINT`) or color masking (`USE_COLOR_MASK`).

        Args:
            defines (MaterialDefinitions): The defines.
        """
        self.defines = list(defines)
        return self

    def add_defines(self, *defines: MaterialDefinitions) -> "_MaterialSettings":
        """Adds shader defines to the base material's.

        Args:
            defines (MaterialDefinitions): The defines to add.
        """
        self.plus_defines = (self.plus_defines or []) + list(defines)
        return self

    def remove_defines(self, *defines: MaterialDefinitions) -> "_MaterialSettings":
        """Removes shader defines of the base material, such as `USE_OVERLAY` to stop the
        entity flashing red when hurt.

        Args:
            defines (MaterialDefinitions): The defines to remove.
        """
        self.minus_defines = (self.minus_defines or []) + list(defines)
        return self

    def set_frontFace(
        self,
        stencilFunc: MaterialFunc | None = None,
        stencilFailOp: MaterialOperation | None = None,
        stencilDepthFailOp: MaterialOperation | None = None,
        stencilPassOp: MaterialOperation | None = None,
        stencilPass: MaterialOperation | None = None,
    ) -> "_MaterialSettings":
        """Sets the stencil test of front-facing polygons. The stencil buffer masks pixels
        and decides what is drawn by custom rules.

        Args:
            stencilFunc (MaterialFunc, optional): Compares the reference value with the
                buffer to decide if the test passes.
            stencilFailOp (MaterialOperation, optional): What happens to the buffer when the
                stencil test fails.
            stencilDepthFailOp (MaterialOperation, optional): What happens when the stencil
                test passes but the depth test fails.
            stencilPassOp (MaterialOperation, optional): What happens when both tests pass.
            stencilPass (MaterialOperation, optional): The older name of `stencilPassOp`.
        """
        self.frontFace = _StencilFace(
            stencilFunc=stencilFunc,
            stencilFailOp=stencilFailOp,
            stencilDepthFailOp=stencilDepthFailOp,
            stencilPassOp=stencilPassOp,
            stencilPass=stencilPass,
        )
        return self

    def set_backFace(
        self,
        stencilFunc: MaterialFunc | None = None,
        stencilFailOp: MaterialOperation | None = None,
        stencilDepthFailOp: MaterialOperation | None = None,
        stencilPassOp: MaterialOperation | None = None,
        stencilPass: MaterialOperation | None = None,
    ) -> "_MaterialSettings":
        """Sets the stencil test of back-facing polygons, like `set_frontFace`.

        Args:
            stencilFunc (MaterialFunc, optional): The comparison.
            stencilFailOp (MaterialOperation, optional): On stencil fail.
            stencilDepthFailOp (MaterialOperation, optional): On stencil pass and depth fail.
            stencilPassOp (MaterialOperation, optional): When both pass.
            stencilPass (MaterialOperation, optional): The older name of `stencilPassOp`.
        """
        self.backFace = _StencilFace(
            stencilFunc=stencilFunc,
            stencilFailOp=stencilFailOp,
            stencilDepthFailOp=stencilDepthFailOp,
            stencilPassOp=stencilPassOp,
            stencilPass=stencilPass,
        )
        return self

    def set_stencilRef(self, stencilRef: int) -> "_MaterialSettings":
        """Sets the reference value the stencil test compares with the buffer.

        Args:
            stencilRef (int): The value, 0 to 255.
        """
        self.stencilRef = stencilRef
        return self

    def set_depthFunc(self, depthFunc: MaterialFunc) -> "_MaterialSettings":
        """Sets the depth test. The usual test is `LessEqual` (drawn when closer or equal);
        `Always` draws on top of everything.

        Args:
            depthFunc (MaterialFunc): The comparison.
        """
        self.depthFunc = depthFunc
        return self

    def set_blendSrc(self, blendSrc: str) -> "_MaterialSettings":
        """Sets the blend factor of the color being drawn, such as `SourceAlpha`.

        Args:
            blendSrc (str): The factor.
        """
        self.blendSrc = blendSrc
        return self

    def set_blendDst(self, blendDst: str) -> "_MaterialSettings":
        """Sets the blend factor of the color already drawn, such as `OneMinusSrcAlpha`.

        Args:
            blendDst (str): The factor.
        """
        self.blendDst = blendDst
        return self

    def set_vertexShader(self, shader: str) -> "_MaterialSettings":
        """Sets the vertex shader, such as `shaders/entity.vertex`.

        Args:
            shader (str): The shader path.
        """
        self.vertexShader = shader
        return self

    def set_fragmentShader(self, shader: str) -> "_MaterialSettings":
        """Sets the fragment (pixel) shader, such as `shaders/entity.fragment`.

        Args:
            shader (str): The shader path.
        """
        self.fragmentShader = shader
        return self

    def set_geometryShader(self, shader: str) -> "_MaterialSettings":
        """Sets the geometry shader.

        Args:
            shader (str): The shader path.
        """
        self.geometryShader = shader
        return self

    def set_vrGeometryShader(self, shader: str) -> "_MaterialSettings":
        """Sets the geometry shader used in virtual reality, such as
        `shaders/entity.geometry`.

        Args:
            shader (str): The shader path.
        """
        self.vrGeometryShader = shader
        return self

    def set_vertexFields(self, *fields: str) -> "_MaterialSettings":
        """Sets the vertex data passed to the shader, which must match what the shader reads.

        Args:
            fields (str): The fields, such as `"Position"`, `"Normal"`, `"UV0"`.
        """
        self.vertexFields = list(fields)
        return self

    def set_msaaSupport(self, support: str) -> "_MaterialSettings":
        """Sets the multisample anti-aliasing support, such as `"Both"`.

        Args:
            support (str): The support mode.
        """
        self.msaaSupport = support
        return self

    def set_primitiveMode(self, mode: str) -> "_MaterialSettings":
        """Sets how vertices are drawn, such as `"Triangle"` or `"Line"`.

        Args:
            mode (str): The primitive mode.
        """
        self.primitiveMode = mode
        return self

    def set_depthBias(self, bias: float) -> "_MaterialSettings":
        """Sets the depth bias, which draws the geometry closer to the camera than it is, to
        stop two overlapping surfaces flickering.

        Args:
            bias (float): The bias.
        """
        self.depthBias = bias
        return self

    def set_slopeScaledDepthBias(self, bias: float) -> "_MaterialSettings":
        """Sets the depth bias scaled by the polygon's angle to the camera.

        Args:
            bias (float): The slope factor.
        """
        self.slopeScaledDepthBias = bias
        return self

    def set_depthBiasOGL(self, bias: float) -> "_MaterialSettings":
        """Sets the depth bias on OpenGL.

        Args:
            bias (float): The bias.
        """
        self.depthBiasOGL = bias
        return self

    def set_slopeScaledDepthBiasOGL(self, bias: float) -> "_MaterialSettings":
        """Sets the slope-scaled depth bias on OpenGL.

        Args:
            bias (float): The slope factor.
        """
        self.slopeScaledDepthBiasOGL = bias
        return self

    def set_samplerState(
        self,
        samplerIndex: int,
        textureFilter: (
            Literal[
                "Point", "Bilinear", "Trilinear", "MipMapBilinear", "TexelAA", "PCF"
            ]
            | None
        ) = None,
        textureWrap: Literal["Repeat", "Clamp"] | None = None,
    ) -> "_MaterialSettings":
        """Adds how a texture is sampled to `samplerStates`, which replaces the base
        material's sampler states.

        Args:
            samplerIndex (int): The texture's index.
            textureFilter (str, optional): The filter, `"Point"` keeping pixels sharp.
            textureWrap (str, optional): `"Repeat"` or `"Clamp"`.
        """
        state = _SamplerState(
            samplerIndex=samplerIndex,
            textureFilter=textureFilter,
            textureWrap=textureWrap,
        )
        self.samplerStates = (self.samplerStates or []) + [state]
        return self

    def add_samplerState(
        self,
        samplerIndex: int,
        textureFilter: (
            Literal[
                "Point", "Bilinear", "Trilinear", "MipMapBilinear", "TexelAA", "PCF"
            ]
            | None
        ) = None,
        textureWrap: Literal["Repeat", "Clamp"] | None = None,
    ) -> "_MaterialSettings":
        """Adds how a texture is sampled to the base material's sampler states.

        Args:
            samplerIndex (int): The texture's index.
            textureFilter (str, optional): The filter, `"Point"` keeping pixels sharp.
            textureWrap (str, optional): `"Repeat"` or `"Clamp"`.
        """
        state = _SamplerState(
            samplerIndex=samplerIndex,
            textureFilter=textureFilter,
            textureWrap=textureWrap,
        )
        self.plus_samplerStates = (self.plus_samplerStates or []) + [state]
        return self


class _MaterialVariant(_MaterialSettings):
    """A variant of a material, such as `skinning`, written as `{name: settings}`."""

    name: str = json_field(exclude=True, positional=True)

    def __json__(self) -> Any:
        return {self.name: _MaterialSettings.__json__(self)}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": "object",
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": JsonObject.__schema_body__.__func__(
                cls, definitions
            ),
        }


class Material(_MaterialSettings):
    """A custom entity material, written to `materials/entity.material` when queued. Its
    identifier is `<namespace>.<material_name>`, which the entity's client description
    refers to.

    Args:
        material_name (str): The material's name.
        baseMaterial (str, optional): The material it builds on, such as
            `entity_alphatest`.
    """

    material_name: str = json_field(exclude=True, positional=True)
    baseMaterial: str | None = json_field(default=None, exclude=True, positional=True)
    variants: list[_MaterialVariant] | None = None

    @property
    def identifier(self) -> str:
        """The material's identifier, `<namespace>.<material_name>`."""
        return f"{CONFIG.NAMESPACE}.{self.material_name}"

    @property
    def key(self) -> str:
        """The material's key in the file, `<identifier>:<baseMaterial>`."""
        if self.baseMaterial is None:
            return self.identifier
        return f"{self.identifier}:{self.baseMaterial}"

    def add_variant(self, name: str) -> _MaterialVariant:
        """Adds a shader variant, such as `skinning`, and returns it to set it up with the
        same builders as the material.

        Args:
            name (str): The variant's name.
        """
        variant = _MaterialVariant(name)
        self.variants = (self.variants or []) + [variant]
        return variant

    def queue(self) -> "Material":
        """Adds the material to `materials/entity.material`."""
        MaterialsObject()._document.materials.add(self)
        return self

    def __str__(self) -> str:
        return self.identifier


class _Materials(JsonObject):
    """The `materials` object: the version, then each material under its key."""

    version: str = json_field(default=MATERIALS_VERSION)
    definitions: Annotated[list[Material], Keyed("key")] = json_field(
        default_factory=list
    )

    def add(self, material: Material) -> None:
        """Adds a material, replacing one with the same key."""
        self.definitions = [m for m in self.definitions if m.key != material.key] + [
            material
        ]

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        payload.update(payload.pop("definitions", {}))
        return payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, Any]) -> dict[str, Any]:
        material = Material.__schema_body__(definitions)
        return {
            "type": "object",
            "properties": {"version": {"type": "string"}},
            "required": ["version"],
            "additionalProperties": material,
        }


class _MaterialsFile(JsonObject):
    """The content of a `.material` file."""

    materials: _Materials = json_field(default_factory=_Materials)


class MaterialsObject(JsonFile[_MaterialsFile]):
    """The project's custom entity materials, `materials/entity.material`. There is one per
    pack.

    ## [Documentation reference](https://wiki.bedrock.dev/visuals/materials)
    """

    _instance = None
    _extension = ".material"
    _pack = Pack.RP
    _folder = "materials"
    _object_type = "Materials"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MaterialsObject, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("entity")
        self._initialized = True

    def add_material(self, material: Material) -> Material:
        """Adds a material to the file."""
        self._document.materials.add(material)
        return material

    def queue(self) -> "MaterialsObject":
        """Queues the materials for export, when there is any."""
        if self._document.materials.definitions:
            super().queue()
        return self
