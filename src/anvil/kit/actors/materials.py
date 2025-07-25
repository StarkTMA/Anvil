from dataclasses import dataclass

from anvil.api.actors.materials import Material
from anvil.lib.enums import (MaterialDefinitions, MaterialFunc,
                             MaterialOperation, MaterialStates)


def add_entity_outline(xray_mode: bool = False):
    """Adds a material for entity outlines.

    Returns:
        Materials: A dataclass containing the base and outline materials.
    """

    @dataclass
    class Materials:
        base_material: Material
        outline_material: Material

        def queue(self):
            self.base_material.queue()
            self.outline_material.queue()

    entity_outline_base = Material("entity_outline_base", "entity_alphatest")
    entity_outline_base.add_states(MaterialStates.EnableStencilTest, MaterialStates.StencilWrite)
    entity_outline_base.frontFace(
        stencilFunc=MaterialFunc.Always,
        stencilFailOp=MaterialOperation.Replace,
        stencilDepthFailOp=MaterialOperation.Replace,
        stencilPassOp=MaterialOperation.Replace,
    )
    entity_outline_base.backFace(
        stencilFunc=MaterialFunc.Always,
        stencilFailOp=MaterialOperation.Replace,
        stencilDepthFailOp=MaterialOperation.Replace,
        stencilPassOp=MaterialOperation.Replace,
    )
    entity_outline_base.stencilRef(3)

    entity_outline = Material("entity_outline", "entity_alphatest")
    entity_outline.add_states(MaterialStates.EnableStencilTest, MaterialStates.InvertCulling)
    entity_outline.add_defines(MaterialDefinitions.MULTI_COLOR_TINT, MaterialDefinitions.USE_OVERLAY)
    entity_outline.remove_states(MaterialStates.DisableCulling)
    entity_outline.remove_defines(MaterialDefinitions.Fancy)
    entity_outline.frontFace(MaterialFunc.NotEqual)
    entity_outline.stencilRef(3)
    entity_outline.depthFunc(MaterialFunc.Always if xray_mode else MaterialFunc.LessEqual)
    return Materials(entity_outline_base, entity_outline)
