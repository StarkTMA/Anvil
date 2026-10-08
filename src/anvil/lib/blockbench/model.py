"""Converts Blockbench models into geometries, voxel shapes and block culling rules."""

import os
from typing import Any, Dict, List, Optional, Union

from anvil.api.core.enums import BlockFaceValues
from anvil.api.core.types import Vector2D, Vector3D
from anvil.api.logic.molang import Molang
from anvil.api.models.geometry import Geometry, _Bone, _Cube
from anvil.api.models.voxel_shape import VoxelShape, _VoxelGroup
from anvil.lib.blockbench.common import _blockbench_geometry_name, _BlockBenchSource
from anvil.lib.blockbench.mesh import _Mesh
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


class _BlockCulling(AddonObject):
    """Block culling rules for a block's geometry.

    Rules are validated against the bones and cubes of the exported
    :class:`Geometry`, so a collection only accepts its own bones.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "block_culling")

    def __init__(self, name: str, geometry: Geometry) -> None:
        super().__init__(name)
        self._geometry = geometry
        self._rules: List[dict] = []

    def add_rule(
        self,
        direction: BlockFaceValues,
        bone: str,
        face: BlockFaceValues | None = None,
        cube_index: int | None = None,
    ) -> None:
        geometry_bone = self._geometry.find(bone)
        if geometry_bone is None:
            raise ValueError(
                f"Bone '{bone}' not found in geometry '{self._geometry.name}'."
            )
        if cube_index is not None:
            cube_count = len(geometry_bone.compile()["cubes"])
            if cube_index < 0 or cube_index >= cube_count:
                raise ValueError(
                    f"Cube index '{cube_index}' out of range for bone '{bone}' in geometry '{self._geometry.name}' ({cube_count} cubes)."
                )

        if direction == BlockFaceValues.All or direction == BlockFaceValues.Side:
            raise ValueError(
                "Direction cannot be 'all' or 'side'. Please specify a single direction."
            )
        if face == BlockFaceValues.All or face == BlockFaceValues.Side:
            raise ValueError(
                "Face cannot be 'all' or 'side'. Please specify a single face."
            )
        if face is not None and cube_index is None:
            raise ValueError(
                "Face specified without cube_index. Please specify cube_index when using face."
            )

        rule = {
            "direction": direction.value,
            "geometry_part": {
                "bone": bone,
            },
        }
        if face:
            rule["geometry_part"]["face"] = face.value
        if cube_index is not None:
            rule["geometry_part"]["cube"] = cube_index
        # Geometries can be shared by many blocks, each adding the same rule, and
        # Minecraft rejects a rule that matches an earlier one
        if rule not in self._rules:
            self._rules.append(rule)

    def compile(self) -> dict:
        content = JsonSchemes.block_culling_rules(self.identifier)
        content["minecraft:block_culling_rules"]["rules"] = list(self._rules)
        return content

    def __export__(self) -> None:
        self.content(self.compile())
        super().__export__()


# Culling rules of geometries built in code, one per geometry name
_geometry_cullings: Dict[str, _BlockCulling] = {}


def _geometry_block_culling(geometry: Geometry) -> _BlockCulling:
    """The culling rules of a Geometry built in code (Blockbench models use
    `_ModelManager.block_culling`). One rules file per geometry, named after it."""
    culling = _geometry_cullings.get(geometry.name)
    if culling is None:
        culling = _geometry_cullings[geometry.name] = _BlockCulling(
            geometry.name, geometry
        )
        culling.queue()
    elif culling._geometry is not geometry:
        raise ValueError(
            f"Another geometry named '{geometry.name}' already has culling rules. Geometry names must be unique."
        )
    return culling


def _process_uv(data: dict, box_uv: bool) -> Union[List[float], Dict[str, Any]]:
    if box_uv:
        return data.get("uv_offset", [0, 0])

    uvs = {}
    for face, face_data in data.get("faces", {}).items():
        if face_data.get("texture") is None:
            continue

        uv_map = face_data.get("uv", [])
        rotation = face_data.get("rotation", 0)
        material_instance = face_data.get("material_name", {})

        if face in ("up", "down"):
            uv_map = [uv_map[2], uv_map[3], uv_map[0], uv_map[1]]

        uv_size = [
            round(uv_map[2] - uv_map[0], 2),
            round(uv_map[3] - uv_map[1], 2),
        ]

        if uv_size[0] != 0 and uv_size[1] != 0:
            face_uv = {
                "uv": [uv_map[0], uv_map[1]],
                "uv_size": uv_size,
                "material_instance": material_instance,
            }
            if rotation != 0:
                face_uv["uv_rotation"] = rotation
            uvs[face] = face_uv
    return uvs


def _add_bb_cube(bone: _Bone, data: dict) -> None:
    """Converts a Blockbench cube (Java-space) to Bedrock space and adds it to `bone`."""
    rot = [-x for x in data.get("rotation", [0, 0, 0])]
    rot[2] = -rot[2]

    pivot = data.get("origin", [0, 0, 0])
    pivot = [-pivot[0], pivot[1], pivot[2]]

    original_origin = data["from"]
    size = [round(j - i, 2) for i, j in zip(original_origin, data["to"])]

    origin = list(original_origin)
    origin[0] = round(-(origin[0] + size[0]), 2)

    # Built directly rather than through `cube()`: Blockbench cubes can have no
    # visible face (an empty per-face UV), which the public API does not offer.
    bone._add_cube(
        _Cube(
            origin,
            size,
            _process_uv(data, data.get("box_uv", False)),
            pivot=pivot,
            rotation=rot,
            inflate=data.get("inflate", 0),
            mirror=data.get("mirror_uv", False),
        )
    )


def _add_bb_locator(bone: _Bone, data: dict) -> None:
    position = list(data["position"])
    position[0] *= -1
    bone.locator(
        data["name"],
        position,
        rotation=[-x for x in data.get("rotation", [0, 0, 0])],
        ignore_inherited_scale=data.get("ignore_inherited_scale", False),
    )


def _bb_bone_args(data: dict) -> dict:
    """Bedrock-space bone properties from a Blockbench group."""
    pivot = list(data.get("origin", [0, 0, 0]))
    pivot[0] = -pivot[0]

    rot = data.get("rotation", [0, 0, 0])
    rot = [-x if i != 2 else x for i, x in enumerate(rot)]

    return {
        "pivot": pivot,
        "rotation": rot,
        "mirror": data.get("mirror_uv", False),
        "binding": data.get("bedrock_binding", None),
    }


def _add_bb_box(group: _VoxelGroup, data: dict) -> None:
    offset = [-8, 0, -8]
    a = [round(j - i, 2) for i, j in zip(offset, data["from"])]
    b = [round(j - i, 2) for i, j in zip(offset, data["to"])]
    group.box(
        min=[min(i, j) for i, j in zip(a, b)],
        max=[max(i, j) for i, j in zip(a, b)],
    )


class _ModelManager:
    def __init__(self, filename, source: str, bbmodel: dict) -> None:
        """Handles loading and managing Blockbench models.

        Parameters:
            filename (str): The name of the model file (without extension).
            source (str): The source of the model. Defaults to "actors".
            bbmodel (dict): The Blockbench model data.
        """

        self._name = filename
        self._bbmodel = bbmodel
        self._queued = False
        self._source = source
        self._is_wavefront = self._bbmodel["meta"]["model_format"] == "free"
        self.bounding_box: Vector2D | None = None
        self._model_center_offset: Vector3D | None = None
        self._cullings: Dict[str, _BlockCulling] = {}
        self._prepared = False
        self._cubes = {}
        self._groups = {}
        self._outliner_nodes: Dict[str, dict] = {}
        self._outliner_parents: Dict[str, Optional[str]] = {}
        self._geometries: Dict[str, Geometry] = {}
        self._queued_geometries: Dict[str, Geometry] = {}
        self._voxel_shapes: Dict[str, VoxelShape] = {}
        self._queued_voxel_shapes: Dict[str, VoxelShape] = {}
        self._collection_aliases: Dict[str, str] = {}
        self._collections = self._index_collections()

    def _index_collections(self) -> Dict[str, dict]:
        collections: Dict[str, dict] = {}
        export_names: set[str] = set()

        for collection in self._bbmodel.get("collections", []):
            model_identifier = str(collection.get("model_identifier", "")).strip()
            if len(model_identifier) == 0:
                continue

            collection_name = str(collection.get("name", "")).strip()
            if len(collection_name) == 0:
                raise ValueError(
                    f"Blockbench collection in '{self._name}' is missing a name."
                )

            export_suffix = model_identifier.lstrip(".") or collection_name
            if export_suffix.startswith(f"{self._name}."):
                export_suffix = export_suffix[len(self._name) + 1 :]

            export_name = _blockbench_geometry_name(self._name, export_suffix)
            if export_name in export_names:
                raise ValueError(
                    f"Duplicate Blockbench collection export '{export_name}' found in model '{self._name}'."
                )
            if collection_name in collections:
                raise ValueError(
                    f"Duplicate Blockbench collection '{collection_name}' found in model '{self._name}'."
                )

            collections[collection_name] = {
                "name": collection_name,
                "identifier": export_suffix,
                "export_name": export_name,
                "children": collection.get("children", []),
            }
            export_names.add(export_name)

            for alias in {collection_name, export_suffix}:
                if (
                    alias in self._collection_aliases
                    and self._collection_aliases[alias] != collection_name
                ):
                    raise ValueError(
                        f"Collection alias '{alias}' is ambiguous in model '{self._name}'."
                    )
                self._collection_aliases[alias] = collection_name

        return collections

    def _calculate_model_center_offset(self) -> None:
        """Calculate the offset needed to center the entire model around the origin."""
        if not self._is_wavefront:
            return

        all_vertices = []

        # Collect all vertices from all mesh elements
        for element in self._bbmodel["elements"]:
            if element["type"] == "mesh":
                vertices = element.get("vertices", {})
                for vertex in vertices.values():
                    all_vertices.append(vertex)

        if not all_vertices:
            return

        # Calculate overall bounding box
        min_x = min(v[0] for v in all_vertices)
        min_y = min(v[1] for v in all_vertices)
        min_z = min(v[2] for v in all_vertices)

        max_x = max(v[0] for v in all_vertices)
        max_y = max(v[1] for v in all_vertices)
        max_z = max(v[2] for v in all_vertices)

        # Calculate center offset - center X and Z, but put bottom at Y=0
        center_x = (min_x + max_x) / 2
        center_z = (min_z + max_z) / 2

        self._model_center_offset = [center_x, min_y, center_z]

    def _prepare_model(self) -> None:
        if self._prepared:
            return

        if self._is_wavefront:
            self._calculate_model_center_offset()

        self._cubes = {d["uuid"]: d for d in self._bbmodel["elements"]}
        self._groups = {d["uuid"]: d for d in self._bbmodel["groups"]}
        self._outliner_nodes = {}
        self._outliner_parents = {}
        self._index_outliner(self._bbmodel["outliner"])
        self._prepared = True

    def _index_outliner(
        self, nodes: List[Union[str, dict]], parent: Optional[str] = None
    ) -> None:
        """Index the outliner tree so groups can be resolved by UUID with their
        full (nested) children, regardless of where they are referenced from."""
        for node in nodes:
            if isinstance(node, dict):
                uuid = node.get("uuid")
                if uuid is None:
                    continue
                self._outliner_nodes[uuid] = node
                self._outliner_parents[uuid] = parent
                self._index_outliner(node.get("children", []), uuid)
            else:
                self._outliner_parents[node] = parent

    def _collection_roots(
        self, children: List[Union[str, dict]]
    ) -> List[Union[str, dict]]:
        """Collections reference nodes by UUID. Drop any node whose ancestor is
        also in the collection, since it is reached through that ancestor."""
        members = {c if isinstance(c, str) else c.get("uuid") for c in children}
        roots = []
        for child in children:
            uuid = child if isinstance(child, str) else child.get("uuid")
            ancestor = self._outliner_parents.get(uuid)
            nested = False
            while ancestor is not None:
                if ancestor in members:
                    nested = True
                    break
                ancestor = self._outliner_parents.get(ancestor)
            if not nested:
                roots.append(child)
        return roots

    def _resolve_tree_node(self, node: Union[str, dict]) -> Union[str, dict]:
        if isinstance(node, dict):
            return node
        if node in self._groups:
            group = self._groups[node]
            outliner_node = self._outliner_nodes.get(node)
            children = (
                outliner_node.get("children", [])
                if outliner_node is not None
                else group.get("children", [])
            )
            return {"uuid": node, "children": children}
        if node in self._cubes:
            return node
        raise ValueError(
            f"Unknown Blockbench node '{node}' found in model '{self._name}'."
        )

    def _root_bone(self, geometry: Geometry, implicit_root: List[_Bone]) -> _Bone:
        """Bare cubes/locators at the top level go into an implicit 'root' bone."""
        if implicit_root:
            return implicit_root[0]
        root = geometry.find("root") or geometry.bone("root")
        implicit_root.append(root)
        return root

    def _populate_geometry(
        self,
        geometry: Geometry,
        nodes: List[Union[str, dict]],
        parent: Optional[_Bone],
        implicit_root: List[_Bone],
    ) -> None:
        for node in nodes:
            resolved_node = self._resolve_tree_node(node)
            if isinstance(resolved_node, str):
                owner = (
                    parent
                    if parent is not None
                    else self._root_bone(geometry, implicit_root)
                )
                element = self._cubes[resolved_node]
                if element["type"] == "cube":
                    _add_bb_cube(owner, element)
                elif element["type"] == "locator":
                    _add_bb_locator(owner, element)
                elif element["type"] == "mesh" and self._is_wavefront:
                    owner._add_mesh(
                        _Mesh.from_dict(element, owner.name, self._model_center_offset)
                    )
                continue

            bone_group = self._groups.get(resolved_node["uuid"])
            if bone_group is None:
                raise ValueError(
                    f"Blockbench group '{resolved_node['uuid']}' referenced by '{self._name}' was not found."
                )

            args = _bb_bone_args(bone_group)
            name = bone_group["name"]
            if parent is None and implicit_root and implicit_root[0].name == name:
                # A real group named 'root' takes over the implicit one.
                bone = implicit_root[0]
                bone.pivot = args["pivot"]
                bone.rotation = args["rotation"]
                bone.mirror = args["mirror"]
                bone.binding = args["binding"]
                implicit_root.clear()
            elif parent is None:
                bone = geometry.bone(name, **args)
            else:
                bone = parent.bone(name, **args)

            self._populate_geometry(
                geometry, resolved_node.get("children", []), bone, implicit_root
            )

    def _root_group(
        self, shape: VoxelShape, implicit_root: List[_VoxelGroup]
    ) -> _VoxelGroup:
        """Bare bounding boxes at the top level go into an implicit 'root' group."""
        if implicit_root:
            return implicit_root[0]
        root = shape.find("root") or shape.group("root")
        implicit_root.append(root)
        return root

    def _populate_voxel_shape(
        self,
        shape: VoxelShape,
        nodes: List[Union[str, dict]],
        parent: Optional[_VoxelGroup],
        implicit_root: List[_VoxelGroup],
    ) -> None:
        """Mirrors the model's groups into the shape, like `_populate_geometry` does with bones."""
        for node in nodes:
            resolved_node = self._resolve_tree_node(node)

            if isinstance(resolved_node, str):
                element = self._cubes[resolved_node]
                if element["type"] == "bounding_box":
                    owner = (
                        parent
                        if parent is not None
                        else self._root_group(shape, implicit_root)
                    )
                    _add_bb_box(owner, element)
                continue

            bone_group = self._groups.get(resolved_node["uuid"])
            if bone_group is None:
                raise ValueError(
                    f"Blockbench group '{resolved_node['uuid']}' referenced by '{self._name}' was not found."
                )

            name = bone_group["name"]
            if parent is None and implicit_root and implicit_root[0].name == name:
                # A real group named 'root' takes over the implicit one.
                group = implicit_root[0]
                implicit_root.clear()
            elif parent is None:
                group = shape.group(name)
            else:
                group = parent.group(name)

            self._populate_voxel_shape(
                shape, resolved_node.get("children", []), group, implicit_root
            )

    def _resolve_export(
        self, collection: Optional[str], check_identifier: bool = False
    ) -> tuple[str, List[Union[str, dict]]]:
        """Export name and root nodes for the whole model or a collection."""
        if collection is None:
            return self._bbmodel["model_identifier"], self._bbmodel["outliner"]

        collection_data = self._resolve_collection(collection)
        if not collection_data["children"]:
            raise ValueError(
                f"Blockbench collection '{collection_data['name']}' in model '{self._name}' has no exportable children."
            )

        if check_identifier and collection_data["identifier"] != collection:
            raise ValueError(
                f"Blockbench model identifier mismatch: collection identifier expected '{collection}', found '{collection_data['identifier']}'."
            )
        return (
            collection_data["export_name"],
            self._collection_roots(collection_data["children"]),
        )

    def _resolve_collection(self, collection: str) -> dict:
        collection_name = collection.strip()
        canonical_name = self._collection_aliases.get(collection_name)
        if canonical_name is None:
            available = ", ".join(sorted(self._collections.keys())) or "none"
            raise ValueError(
                f"Blockbench collection '{collection}' not found in model '{self._name}'. Available collections: {available}."
            )
        return self._collections[canonical_name]

    def process_block_display(self, geometry: Geometry) -> None:
        unit = [1, 1, 1]
        zero = [0, 0, 0]
        display_data: dict[str, dict[str, list[str | float | Molang]]] = (
            self._bbmodel.get("display", {})
        )
        transforms = geometry.item_display_transforms
        if transforms is None:
            transforms = geometry.item_display_transforms = {}
        if display_data:
            for display, transform in display_data.items():
                if any(
                    [
                        transform.get("rotation") != zero,
                        transform.get("translation") != zero,
                        transform.get("scale") != unit,
                        transform.get("rotation_pivot") != zero,
                        transform.get("scale_pivot") != zero,
                    ]
                ):
                    # Minecraft will not accept fit_to_frame=False from "1.21.130" onwards
                    # transforms[display] = {**transform, "fit_to_frame": {}} Works now I guess
                    transforms[display] = transform

    def _build_geometry(
        self, model_name: str, nodes: List[Union[str, dict]]
    ) -> Geometry:
        width = self._bbmodel["resolution"]["width"]
        height = self._bbmodel["resolution"]["height"]

        size = [
            width * (64 if self._is_wavefront else 1),
            height * (64 if self._is_wavefront else 1),
        ]
        bounding_box = (
            self.bounding_box
            if self.bounding_box
            else (
                self._bbmodel["visible_box"] if not self._is_wavefront else [1024, 1024]
            )
        )
        offset = [0, self._bbmodel["visible_box"][2], 0]

        geometry = Geometry(model_name, size, bounding_box, offset)
        self._populate_geometry(geometry, nodes, None, [])

        if self._source == _BlockBenchSource.BLOCK:
            self.process_block_display(geometry)

        return geometry

    def _get_geometry(self, collection: Optional[str]) -> tuple[str, Geometry]:
        self._prepare_model()
        name, nodes = self._resolve_export(collection, check_identifier=True)
        if name not in self._geometries:
            self._geometries[name] = self._build_geometry(name, nodes)
        return name, self._geometries[name]

    def _get_voxel_shape(self, collection: Optional[str]) -> tuple[str, VoxelShape]:
        self._prepare_model()
        name, nodes = self._resolve_export(collection)
        if name not in self._voxel_shapes:
            # The culling shape is referenced as '<name>_culling_shape'.
            shape = VoxelShape(name, f"{name}_culling_shape")
            self._populate_voxel_shape(shape, nodes, None, [])
            self._voxel_shapes[name] = shape
        return name, self._voxel_shapes[name]

    def geometry(self, collection: Optional[str] = None) -> Geometry:
        """Builds (once) and returns the Geometry for the whole model or a collection.

        The returned object can be modified before the model is exported, e.g.
        to add bones, cubes or locators on top of the imported model. Use
        `queue_model` to export it; do not call `queue()` on it directly.
        """
        return self._get_geometry(collection)[1]

    def queue_model(self, collection: Optional[str] = None) -> Geometry:
        name, geometry = self._get_geometry(collection)
        self._queued_geometries[name] = geometry
        return geometry

    def voxel_shape(self, collection: Optional[str] = None) -> VoxelShape:
        """Builds (once) and returns the VoxelShape for the whole model or a collection.

        The returned object can be modified before the model is exported. Use
        `queue_voxel_shape` to export it.
        """
        return self._get_voxel_shape(collection)[1]

    def queue_voxel_shape(self, collection: Optional[str] = None) -> VoxelShape:
        name, shape = self._get_voxel_shape(collection)
        if not shape.boxes:
            raise ValueError(
                f"Blockbench model '{self._name}'{f' collection {collection!r}' if collection else ''} has no bounding boxes to export as a voxel shape."
            )
        self._queued_voxel_shapes[name] = shape
        return shape

    def override_bounding_box(self, bounding_box: Vector2D) -> None:
        """Overrides the visible bounds of every geometry of this model, built or not."""
        self.bounding_box = bounding_box
        for geometry in self._geometries.values():
            geometry.visible_bounds = list(bounding_box)

    def block_culling(self, collection: Optional[str] = None) -> _BlockCulling:
        """Culling rules of the model's geometry, or of one of its collections.

        Every exported geometry has its own rules file, named after the geometry
        (``<model>`` or ``<model>.<collection>``), and its own rules.
        """
        name, geometry = self._get_geometry(collection)
        if name not in self._cullings:
            self._cullings[name] = _BlockCulling(name, geometry)
        return self._cullings[name]

    def __export__(self) -> None:
        for geometry in self._queued_geometries.values():
            geometry.queue(self._source)

        for shape in self._queued_voxel_shapes.values():
            shape.queue()

        for culling in self._cullings.values():
            culling.queue()
