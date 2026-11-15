"""Builders for the model files of a pack, for content made in code.

- `anvil.api.models.geometry.Geometry`: a geometry file (``*.geo.json``) built from bones, cubes and locators.
- `anvil.api.models.animations.Animations`: an animations file (``*.animations.json``) holding many animations.
- `anvil.api.models.voxel_shape.VoxelShape`: a voxel shape file (``*.shape.json``) built from groups of boxes.

Entities and blocks accept these objects wherever they reference a geometry, an
animation or a culling shape. Models imported from Blockbench produce the same objects.
"""
