
import os
from enum import StrEnum

from anvil import CONFIG
from anvil.api.enums import (MaterialDefinitions, MaterialFunc,
                             MaterialOperation, MaterialStates)
from anvil.lib.schemas import AddonObject, JsonSchemes


class Material():
    """A class representing a material with customizable states and definitions.

    Attributes:
        Material_name (str): The name of the material.
        Material (dict): The attributes and states of the material.
    """

    def __init__(self, material_name, baseMaterial) -> None:
        """
        Initializes a Material instance.

        Args:
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
        Sets the states for the material.

        Args:
            states (MaterialStates): The material states to be set.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["states"] = states
        return self

    def remove_states(self, *states: MaterialStates):
        """
        Removes the states for the material.

        Args:
            states (MaterialStates): The material states to be removed.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-states"] = states
        return self

    def add_states(self, *states: MaterialStates):
        """
        Adds states to the material.

        Args:
            states (MaterialStates): The material states to be added.

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
        Sets the front face stencil properties of the material.

        Args:
            stencilFunc (MaterialFunc, optional): The function for the stencil.
            stencilFailOp (MaterialOperation, optional): The operation on fail for the stencil.
            stencilDepthFailOp (MaterialOperation, optional): The operation on depth fail for the stencil.
            stencilPassOp (MaterialOperation, optional): The operation on pass for the stencil.
            stencilPass (MaterialOperation, optional): The pass for the stencil.

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
        self._material[self._material_name]["frontFace"] = {key: value.value for key, value in a.items() if value != None}
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
        Sets the back face stencil properties of the material.

        Args:
            stencilFunc (MaterialFunc, optional): The function for the stencil.
            stencilFailOp (MaterialOperation, optional): The operation on fail for the stencil.
            stencilDepthFailOp (MaterialOperation, optional): The operation on depth fail for the stencil.
            stencilPassOp (MaterialOperation, optional): The operation on pass for the stencil.
            stencilPass (MaterialOperation, optional): The pass for the stencil.

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
        Sets the stencil reference value of the material.

        Args:
            stencilRef (int): The reference value for the stencil.

        Returns:
            Material: The instance of the class to enable method chaining.
        """

        self._material[self._material_name]["stencilRef"] = stencilRef
        return self

    def depthFunc(self, depthFunc: MaterialFunc):
        """
        Sets the depth function of the material.

        Args:
            depthFunc (MaterialFunc): The function for the depth.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthFunc"] = depthFunc
        return self

    def defines(self, *defines: MaterialDefinitions):
        """
        Sets the defines for the material.

        Args:
            defines (MaterialDefinitions): The defines for the material.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["defines"] = defines
        return self

    def remove_defines(self, *defines: MaterialDefinitions):
        """
        Removes the defines for the material.

        Args:
            defines (MaterialDefinitions): The defines to be removed.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-defines"] = defines
        return self

    def add_defines(self, *defines: MaterialDefinitions):
        """
        Adds defines to the material.

        Args:
            defines (MaterialDefinitions): The defines to be added.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+defines"] = defines
        return self

    @property
    def _queue(self):
        """
        Provides the dictionary representing the material's states and properties.

        Returns:
            dict: The material dictionary.
        """
        return self._material

    def __str__(self) -> str:
        return self.identifier

class MaterialsObject(AddonObject):
    """Handles materials.

    Attributes:
        Materials (list[Material], optional): A list of materials. Defaults to empty list.
    """
    
    _extension = ".material"
    _path = os.path.join(CONFIG.RP_PATH, "materials")

    def __init__(self) -> None:
        """Initializes a Materials instance."""
        super().__init__("entity")
        self._materials: list[Material] = []
        self._content = JsonSchemes.materials()

    def add_material(self, material_name, base_material):
        """Adds a material to the Materials instance.

        Args:
            material_name (str): The name of the material.
            base_material (str): The base material.

        Returns:
            Material: The created material instance.
        """
        material = Material(material_name, base_material)
        self._materials.append(material)
        return material

    @property
    def queue(self):
        """Returns the queue for the materials.

        Returns:
            queue: The queue for the materials.
        """
        for m in self._materials:
            self._content["materials"].update(m._queue)
        super().queue()
