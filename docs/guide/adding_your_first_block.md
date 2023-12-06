[//]: <> (https://squidfunk.github.io/mkdocs-material/reference/)

## Introduction

Adding blocks follows the same process as adding entities. In this tutorial, we will be creating a new block called `vertical_slab` in the `my_project` project.

## First steps

Open the `my_project.py` file in your project folder. 

Firstly we import the `Block` class from the `api.blocks` module.

```py  title="my_project.py" 
from anvil.api.blocks import Block
```

## Creating the block

Now that we have imported the `Entity` class, we can create our entity.

```py  title="my_project.py"
vertical_slab = Block("vertical_slab")
```

!!! success 
    This will create a new block called `vertical_slab` in the `my_project` project.

## Adding visuals

Each block must have a geometry and a material instance added to its components. 
We must first import the relevant components from the `api.blocks` module.

```py title="my_project.py"
from anvil.api.blocks import BlockMaterialInstance, BlockGeometry
```
Then we process adding the geometry and material instance to the block.

```py  title="my_project.py"
vertical_slab.Server.components.add(
    BlockGeometry("vertical_slab"),
    BlockMaterialInstance().add_instance(
        "vertical_cube", 
        BlockFaces.All, 
        BlockMaterial.AlphaTest, 
        ambient_occlusion=True, 
        face_dimming=True
    ),
)
```

!!!tip
    Most of the redundant parameters are optional, and can be omitted. The only required parameters are the name of the geometry and the name of the material instance.
!!!failure
    Exporting a block without a geometry and a material instance in its components will raise an error.


## Adding more components

To make it a real vertical slab, we must change the collision and selection boxes, I also fancy making it emit light. As it is the pattern, we first import the necessary components from the `api.blocks` module.

```py title="my_project.py"
from anvil.api.blocks import BlockCollisionBox, BlockSelectionBox, BlockLightEmission
```
Then we add the components to the block.

```py  title="my_project.py"
vertical_slab.Server.components.add(
    BlockCollisionBox((8, 16, 16), (0, 0, -8)),
    BlockSelectionBox((8, 16, 16), (0, 0, -8)),
    BlockLightEmission(15),
)
```
!!! success 
    The block now has a vertical slab collision box and emits light.

## Exporting the block

Similar to entities, blocks must be queued for exporting. This is done by calling the `queue` method on the block.

```python
vertical_slab.queue("slabs")
```

!!! success 
    The block will be exported to the `slabs` folder.

## Compiling the project

Now that we have created our entity, we can compile the project. this is the complete code for the `my_project.py` file.

```py title="my_project.py" linenums="1"
from anvil import *
from anvil.api.blocks import (Block, BlockCollisionBox, BlockGeometry,
                              BlockLightEmission, BlockMaterialInstance,
                              BlockSelectionBox)

def create_block():
    vertical_slab = Block("vertical_slab")
    vertical_slab.Server.components.add(
        BlockGeometry("vertical_slab"),
        BlockMaterialInstance().add_instance("vertical_cube", BlockFaces.All, BlockMaterial.AlphaTest, ambient_occlusion=True, face_dimming=True),
        BlockCollisionBox((8, 16, 16), (0, 0, -8)),
        BlockSelectionBox((8, 16, 16), (0, 0, -8)),
        BlockLightEmission(15)
    )
    vertical_slab.queue("slabs")

if __name__ == "__main__":
    create_block()

    ANVIL.compile()
```
!!! note
    Note the use of ANVIL.compile() at the end of the file. This is required to compile the project, anything added after this line will not be compiled.
