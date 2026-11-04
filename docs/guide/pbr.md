# Assets & Textures

This guide explains how to manage **Textures**, **Animations**, and **PBR (Physically Based Rendering)** in Anvil.

---

## Block & Entity Assets

For **Blocks** and **Entities**, textures and animations are **not** stored as separate image files in your resource pack. Instead, they must be **embedded inside the Blockbench model file** (`.bbmodel`).

### Workflow

1.  **Create your model** in Blockbench.
2.  **Import your textures** (Color, Normal, MER) into the Blockbench project.
3.  **Save the model** as a `.bbmodel` file.
4.  **Place the file** in `assets/bbmodels/` (e.g., `assets/bbmodels/my_model.bbmodel`).

Anvil will automatically extract the textures, processing PBR maps like Normal and MER (Metalness/Emissive/Roughness) during the build.

### PBR Blocks Example

Here is a production-ready example demonstrating a **Mystic Crystal** block. It uses:

- **PBR Textures**: Color, MER, and Height maps.
- **Render Method**: Blending for transparency/translucency.

```python title="blocks/mystic_crystal.py"
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockGeometry,
    BlockMaterialInstance,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.lib.jsonmodel.enums import BlockFaceValues, BlockMaterial

block = Block("mystic_crystal")
block.server.components.add(
    BlockGeometry(blockbench="mystic_crystal"),
    BlockMaterialInstance().add_instance(
        spec=InstanceSpec(
            blockbench="mystic_crystal",
            face=BlockFaceValues.All,
            variations=[
                InstanceVariant(
                    # These texture names must match what is inside 'mystic_crystal.bbmodel'
                    color="mystic_crystal_texture",
                    mer="mystic_crystal_mer",
                    height="mystic_crystal_height",
                )
            ],
            params=MaterialParams(render_method=BlockMaterial.Blend),
        )
    ),
)
block.queue()
```

A flipbook animates the texture: give `InstanceSpec` several `InstanceVariant`s (one per frame, all in the same Blockbench file) and `flipbooks=[FlipbookParams(frames=[0, 1, 2, 3], ticks_per_frame=20)]`.

!!! warning "Do not use loose PNGs"
    Do not place block or entity textures in `assets/textures/`. They will be ignored. Usage of the Blockbench file is mandatory for these assets.

### PBR Entities Example

This example shows a **Mystic Wisp** entity using PBR textures defined in its client description.

```python title="entities/mystic_wisp.py"
from anvil.api.actors.entity import Entity
from anvil.api.pbr.texture_set import TextureComponents

def mystic_wisp():
    entity = Entity("mystic_wisp")

    # Define the geometry and textures (must be in 'mystic_wisp.bbmodel')
    entity.client.description.add_geometry("mystic_wisp")
    entity.client.description.add_texture(
        blockbench="mystic_wisp",
        component=TextureComponents(
            color="mystic_wisp",
            mer="mystic_wisp_mer",
            height="mystic_wisp_height"
        ),
    )

    # Render Controller
    rc = entity.client.description.render_controller("default")
    rc.set_geometry("mystic_wisp")
    rc.add_texture("mystic_wisp")

    return entity.queue()
```

---

## PBR Textures

Anvil supports Minecraft's PBR system. If you include PBR maps in your Blockbench model, they are automatically handled.

| Map Type   | Conventional Key | Description                                                      |
| :--------- | :--------------- | :--------------------------------------------------------------- |
| **Color**  | `name`           | Base color texture.                                              |
| **Normal** | `name_normal`    | Surface bumpiness/depth.                                         |
| **MER**    | `name_mer`       | **M**etalness (Red), **E**missive (Green), **R**oughness (Blue). |
| **Height** | `name_height`    | Displacement (exclusive with Normal).                            |

---

## Item Assets

Unlike Blocks and Entities, **Items** typically use standalone texture files.

- **Location**: Place your `.png` files in `assets/textures/items/`.
- **Naming**: The filename (without extension) is referenced in your code.

```python
from anvil.api.items.components import ItemIcon
from anvil.api.pbr.texture_set import TextureComponents

# References 'assets/textures/items/my_item.png'
ItemIcon(textures=TextureComponents(color="my_item"))
```

---

## World Settings

Vibrant Visuals also has world-level files: `LightingSettings`, `AtmosphericSettings`, `FogSettings`, `WaterSettings`, `ColorGradingSettings`, `ShadowSettings` and `LocalLighting` in `anvil.api.pbr`. [Creating a biome](custom_biome.md) builds a full set and attaches it to a biome.
