import os
from enum import StrEnum

from anvil import CONFIG
from anvil.lib.enums import (MaterialDefinitions, MaterialFunc,
                             MaterialOperation, MaterialStates)
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Identifier


class _MaterialsObject(AddonObject):
    """Handles materials.

    Attributes:
        Materials (list[Material], optional): A list of materials. Defaults to empty list.
    """

    _extension = ".material"
    _path = os.path.join(CONFIG.RP_PATH, "materials")
    _object_type = "Materials"

    def __init__(self) -> None:
        """Initializes a Materials instance."""
        super().__init__("entity")
        self._materials: list[Material] = []
        self._content = JsonSchemes.materials()

    def add_material(self, material: 'Material'):
        self._materials.append(material)
        return material

    @property
    def size(self) -> int:
        """Returns the size of the materials.

        Returns:
            int: The size of the materials.
        """
        return len(self._materials)

    def queue(self):
        """Returns the queue for the materials.

        Returns:
            queue: The queue for the materials.
        """
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
        Sets the states for the material.

        Parameters:
            states (MaterialStates): The material states to be set.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["states"] = states
        return self

    def remove_states(self, *states: MaterialStates):
        """
        Removes the states for the material.

        Parameters:
            states (MaterialStates): The material states to be removed.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-states"] = states
        return self

    def add_states(self, *states: MaterialStates):
        """
        Adds states to the material.

        Parameters:
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

        Parameters:
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

        Parameters:
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

        Parameters:
            stencilRef (int): The reference value for the stencil.

        Returns:
            Material: The instance of the class to enable method chaining.
        """

        self._material[self._material_name]["stencilRef"] = stencilRef
        return self

    def depthFunc(self, depthFunc: MaterialFunc):
        """
        Sets the depth function of the material.

        Parameters:
            depthFunc (MaterialFunc): The function for the depth.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["depthFunc"] = depthFunc
        return self

    def defines(self, *defines: MaterialDefinitions):
        """
        Sets the defines for the material.

        Parameters:
            defines (MaterialDefinitions): The defines for the material.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["defines"] = defines
        return self

    def remove_defines(self, *defines: MaterialDefinitions):
        """
        Removes the defines for the material.

        Parameters:
            defines (MaterialDefinitions): The defines to be removed.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["-defines"] = defines
        return self

    def add_defines(self, *defines: MaterialDefinitions):
        """
        Adds defines to the material.

        Parameters:
            defines (MaterialDefinitions): The defines to be added.

        Returns:
            Material: The instance of the class to enable method chaining.
        """
        self._material[self._material_name]["+defines"] = defines
        return self

    def queue(self):
        from anvil import ANVIL

        ANVIL.definitions._materials_object.add_material(self)

    def _export(self) -> dict:
        """Exports the material as a dictionary.

        Returns:
            dict: The material as a dictionary.
        """
        return self._material

    def __str__(self) -> Identifier:
        return self.identifier
