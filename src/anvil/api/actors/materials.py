import os

from anvil.api.core.enums import MaterialDefinitions, MaterialFunc, MaterialOperation, MaterialStates
from anvil.api.core.types import Identifier
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


class MaterialsObject(AddonObject):
    """Handles materials as a singleton.

    Attributes:
        Materials (list[Material], optional): A list of materials. Defaults to empty list.
    """

    _instance = None
    _extension = ".material"
    _path = os.path.join(CONFIG.RP_PATH, "materials")
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
        self._materials: list[Material] = []
        self._content = JsonSchemes.materials()
        self._initialized = True

    def add_material(self, material: "Material"):
        self._materials.append(material)
        return material

    def queue(self):
        """Returns the queue for the materials.

        Returns:
            queue: The queue for the materials.
        """
        if (len(self._materials)) > 0:
            for m in self._materials:
                self._content["materials"].update(m._export())
            super().queue()


class Material:
    """A class representing a material with customizable states and definitions.

    Attributes:
        Material_name (str): The name of the material.
        Material (dict): The attributes and states of the material.
    """

    def __init__(self, material_name, baseMaterial) -> None:
        """
        Initializes a Material instance.

        Parameters:
            material_name (str): The name of the material.
            baseMaterial (str): The base material's name, if any.
        """
        self._identifier = f"{CONFIG.NAMESPACE}.{material_name}"
        self._material_name = f"{self._identifier}" if baseMaterial == None else f"{self._identifier}:{baseMaterial}"
        self._material = {self._material_name: {}}

    @property
    def identifier(self):
        return self._identifier

    def states(self, *states: MaterialStates):
        """
        Sets the rendering states for the material.

        Rendering states control basic graphics pipeline settings, such as whether to enable blending,
        disable culling (rendering backfaces), or write to the depth buffer.

        Parameters:
            states (MaterialStates): One or more `MaterialStates` enum values (e.g., `MaterialStates.DisableCulling`, `MaterialStates.Blending`).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["states"] = states
        return self

    def remove_states(self, *states: MaterialStates):
        """
        Removes specific rendering states from the material configuration.

        Use this to disable default behaviors inherited from a base material.
        For example, removing `DisableCulling` to restore backface culling.

        Parameters:
            states (MaterialStates): The material states to remove.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-states"] = states
        return self

    def add_states(self, *states: MaterialStates):
        """
        Adds rendering states to the existing material configuration.

        This appends to the states inherited from the base material instead of replacing them.

        Parameters:
            states (MaterialStates): The material states to add.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+states"] = states
        return self

    def frontFace(
        self,
        stencilFunc: MaterialFunc = None,
        stencilFailOp: MaterialOperation = None,
        stencilDepthFailOp: MaterialOperation = None,
        stencilPassOp: MaterialOperation = None,
        stencilPass: MaterialOperation = None,
    ):
        """
        Configures stencil testing for front-facing polygons.

        The stencil buffer is used to mask pixels and control drawing based on custom rules.
        This method defines how the stencil test behaves for the front side of the geometry.

        Parameters:
            stencilFunc (MaterialFunc, optional): The comparison function (e.g. Equal, Always) used to determine if the stencil test passes.
            stencilFailOp (MaterialOperation, optional): The operation to perform on the stencil buffer value if the stencil test fails.
            stencilDepthFailOp (MaterialOperation, optional): The operation to perform if the stencil test passes but the depth test fails.
            stencilPassOp (MaterialOperation, optional): The operation to perform if both stencil and depth tests pass.
            stencilPass (MaterialOperation, optional): (Legacy/Alternative name for stencilPassOp).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        a = {
            "stencilFunc": stencilFunc,
            "stencilFailOp": stencilFailOp,
            "stencilDepthFailOp": stencilDepthFailOp,
            "stencilPassOp": stencilPassOp,
            "stencilPass": stencilPass,
        }
        self._material[self._material_name]["frontFace"] = {
            key: value.value for key, value in a.items() if value != None
        }
        return self

    def backFace(
        self,
        stencilFunc: MaterialFunc = None,
        stencilFailOp: MaterialOperation = None,
        stencilDepthFailOp: MaterialOperation = None,
        stencilPassOp: MaterialOperation = None,
        stencilPass: MaterialOperation = None,
    ):
        """
        Configures stencil testing for back-facing polygons.

        Functionally identical to `frontFace`, but applied to the back side of geometry.
        This allows for double-sided stencil effects (e.g. treating the inside of a volume differently).

        Parameters:
            stencilFunc (MaterialFunc, optional): The comparison function.
            stencilFailOp (MaterialOperation, optional): Operation on stencil fail.
            stencilDepthFailOp (MaterialOperation, optional): Operation on stencil pass but depth fail.
            stencilPassOp (MaterialOperation, optional): Operation on both pass.
            stencilPass (MaterialOperation, optional): (Legacy/Alternative name).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        a = {
            "stencilFunc": stencilFunc,
            "stencilFailOp": stencilFailOp,
            "stencilDepthFailOp": stencilDepthFailOp,
            "stencilPassOp": stencilPassOp,
            "stencilPass": stencilPass,
        }
        self._material[self._material_name]["backFace"] = {key: value for key, value in a.items() if value != None}
        return self

    def stencilRef(self, stencilRef: int):
        """
        Sets the reference value for the stencil test.

        This value is compared against the value in the stencil buffer using the `stencilFunc`.
        For example, if `stencilFunc` is `Equal` and `stencilRef` is 1, pixels are only drawn where the stencil buffer is 1.

        Parameters:
            stencilRef (int): The integer reference value (0-255).

        Returns:
            Material: The instance of the class to enable method chaining.
        """

        self._material[self._material_name]["stencilRef"] = stencilRef
        return self

    def depthFunc(self, depthFunc: MaterialFunc):
        """
        Sets the function used for the depth test.

        The depth test determines if a pixel is obscured by other objects.
        Standard depth testing uses `LessEqual` (draw if closer or equal).
        Changing this allows valid rendering of objects behind others (e.g. `Greater`) or always drawing on top (`Always`).

        Parameters:
            depthFunc (MaterialFunc): The comparison function to use (e.g. `MaterialFunc.LessEqual`, `MaterialFunc.Always`).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthFunc"] = depthFunc
        return self

    def blendSrc(self, blendSrc: str):
        """
        Sets the blending factor for the source color (the pixel being drawn).

        Blending combines the source color with the destination color (the pixel already in the buffer).
        Example: `SourceAlpha` uses the texture's alpha channel for transparency.

        Parameters:
            blendSrc (str): The source blend factor string (e.g., "SourceAlpha", "One").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["blendSrc"] = blendSrc
        return self

    def blendDst(self, blendDst: str):
        """
        Sets the blending factor for the destination color (the background).

        Together with `blendSrc`, this determines the final pixel color.
        Example: `OneMinusSrcAlpha` is commonly used for standard transparency (inverted alpha).

        Parameters:
            blendDst (str): The destination blend factor (e.g., "OneMinusSrcAlpha", "Zero").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["blendDst"] = blendDst
        return self

    def vertexShader(self, shader: str):
        """
        Sets the path to the vertex shader file.

        The vertex shader processes each vertex's position and attributes (UVs, normals).
        It transforms 3D model coordinates into screen space.

        Parameters:
            shader (str): The relative path to the vertex shader (e.g., "shaders/entity.vertex").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["vertexShader"] = shader
        return self

    def fragmentShader(self, shader: str):
        """
        Sets the path to the fragment (pixel) shader file.

        The fragment shader calculates the color of each pixel, applying textures, lighting, and effects.

        Parameters:
            shader (str): The relative path to the fragment shader (e.g., "shaders/entity.fragment").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["fragmentShader"] = shader
        return self

    def geometryShader(self, shader: str):
        """
        Sets the path to the geometry shader file.

        Geometry shaders can generate new geometry (vertices/primitives) on the fly.
        (Less commonly used in standard Bedrock entity materials).

        Parameters:
            shader (str): The relative path to the geometry shader file.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["geometryShader"] = shader
        return self

    def vrGeometryShader(self, shader: str):
        """
        Sets the path to the VR-specific geometry shader.

        Used when playing in Virtual Reality mode to handle stereo rendering adjustments.

        Parameters:
            shader (str): The relative path to the shader (e.g., "shaders/entity.geometry").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["vrGeometryShader"] = shader
        return self

    def vertexFields(self, fields: list[dict]):
        """
        Defines the data layout for vertices passed to the shader.

        Specifies what information (Position, Normal, UVs, Color/BoneWeights) is available
        in the shader input attributes. Must match the shader's expectation.

        Parameters:
            fields (list[dict]): List of field objects (e.g., `[{"field": "Position"}, {"field": "UV0"}]`).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["vertexFields"] = fields
        return self

    def variants(self, variants: list[dict]):
        """
        Defines shader variants.

        Variants allow switching between different shader setups (defines, vertex fields)
        based on conditions, such as skinning support or specific defines being active.

        Parameters:
            variants (list[dict]): A list of variant configuration dictionaries.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["variants"] = variants
        return self

    def msaaSupport(self, support: str):
        """
        Configures Multisample Anti-Aliasing (MSAA) support.

        Controls whether the material benefits from MSAA to smooth jagged edges.

        Parameters:
            support (str): The support mode (e.g., "Both", "None", "MSAA").

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["msaaSupport"] = support
        return self

    def primitiveMode(self, mode: str):
        """
        Sets the geometric primitive drawing mode.

        Determines how vertices are interpreted.
        - "Triangle": Standard mesh rendering.
        - "Line": Draws wireframe lines.
        - "Quad": Draws quads.

        Parameters:
            mode (str): The primitive mode string.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["primitiveMode"] = mode
        return self

    def depthBias(self, bias: float):
        """
        Sets the depth bias.

        Offsets the depth value of the rendered geometry. Positive values pull the geometry "closer" to the camera
        without changing its actual position. Used to prevent z-fighting (flickering) when two surfaces overlap.

        Parameters:
            bias (float): The bias value (typically small, e.g., 100.0).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthBias"] = bias
        return self

    def slopeScaledDepthBias(self, bias: float):
        """
        Sets the slope-scaled depth bias.

        Offsets depth based on the polygon's angle to the camera. Surfaces viewed at a steep angle need more bias
        to prevent z-fighting. Works in conjunction with `depthBias`.

        Parameters:
            bias (float): The slope-scale factor (e.g., 0.1).

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["slopeScaledDepthBias"] = bias
        return self

    def depthBiasOGL(self, bias: float):
        """
        Sets the OpenGL-specific depth bias.

        Similar to `depthBias`, but specifically for the OpenGL backend (some platforms).
        Usually kept consistent with `depthBias`.

        Parameters:
            bias (float): The OpenGL depth bias value.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthBiasOGL"] = bias
        return self

    def slopeScaledDepthBiasOGL(self, bias: float):
        """
        Sets the OpenGL-specific slope-scaled depth bias.

        Similar to `slopeScaledDepthBias`, but for the OpenGL backend.

        Parameters:
            bias (float): The OpenGL slope-scale factor.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["slopeScaledDepthBiasOGL"] = bias
        return self

    def samplerStates(self, states: list[dict]):
        """
        Configures texture sampling.

        Defines how textures are filtered (Nearest/Linear) and wrapped (Repeat/Clamp).
        Example: Setting filter to 'Point' creates a pixelated look (Minecraft default).

        Parameters:
            states (list[dict]): A list of sampler state objects.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["samplerStates"] = states
        return self

    def add_samplerStates(self, states: list[dict]):
        """
        Adds additional sampler states.

        Appends to existing sampler states inherited from the base material.

        Parameters:
            states (list[dict]): A list of sampler state objects to add.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+samplerStates"] = states
        return self

    def defines(self, *defines: MaterialDefinitions):
        """
        Sets the shader preprocessor defines.

        Defines toggle features in the shader code, such as enabling alpha testing (`ALPHA_TEST`),
        glint effects (`GLINT`), or color masking (`USE_COLOR_MASK`).
        **Overwrites** all existing defines.

        Parameters:
            defines (MaterialDefinitions): Variable arguments of `MaterialDefinitions`.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["defines"] = defines
        return self

    def remove_defines(self, *defines: MaterialDefinitions):
        """
        Removes specific defines from the material.

        Use this to disable features inherited from a base material.
        Example: Removing `USE_OVERLAY` to stop an entity from flashing red when hit.

        Parameters:
            defines (MaterialDefinitions): The defines to remove.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-defines"] = defines
        return self

    def add_defines(self, *defines: MaterialDefinitions):
        """
        Adds defines to the material.

        Enables additional features like emulation or multi-texturing on top of the base material's configuration.

        Parameters:
            defines (MaterialDefinitions): The defines to add.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+defines"] = defines
        return self

    def queue(self):
        MaterialsObject().add_material(self)

    def _export(self) -> dict:
        """Exports the material as a dictionary.

        Returns:
            dict: The material as a dictionary.
        """
        return self._material

    def __str__(self) -> Identifier:
        return self.identifier
