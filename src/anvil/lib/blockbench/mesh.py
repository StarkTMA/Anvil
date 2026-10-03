from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class _Mesh:
    name: str
    vertices: Dict[str, List[float]]
    faces: Dict[str, Any]
    model_center_offset: List[float] = field(default_factory=lambda: [0, 0, 0])
    parent: str = "root"

    mesh_texture_multiplier: int = 64

    @classmethod
    def from_dict(
        cls, data: dict, parent: str = "root", model_center_offset: List[float] = None
    ) -> "_Mesh":
        return cls(
            name=data.get("name", "mesh"),
            vertices=data.get("vertices", {}),
            faces=data.get("faces", {}),
            model_center_offset=model_center_offset or [0, 0, 0],
            parent=parent,
        )

    def extract_cuboids(self):
        # Re-implementation of extract_cuboids using internal data
        face_verts = {fid: set(face["vertices"]) for fid, face in self.faces.items()}

        vertex_to_faces = defaultdict(list)
        for fid, face in self.faces.items():
            for vid in face["vertices"]:
                vertex_to_faces[vid].append(fid)

        shared_counts = defaultdict(int)
        for face_list in vertex_to_faces.values():
            for i in range(len(face_list)):
                for j in range(i + 1, len(face_list)):
                    f1, f2 = face_list[i], face_list[j]
                    if f1 > f2:
                        f1, f2 = f2, f1
                    shared_counts[(f1, f2)] += 1

        face_neighbors = {fid: set() for fid in self.faces}
        for (f1, f2), count in shared_counts.items():
            if count >= 2:
                face_neighbors[f1].add(f2)
                face_neighbors[f2].add(f1)

        all_visited = set()
        cuboids = []
        cuboid_id = 0

        for fid in self.faces:
            if fid in all_visited:
                continue

            # Extract a connected component of faces
            original_component = set()
            stack = [fid]
            while stack:
                current = stack.pop()
                if current not in original_component:
                    original_component.add(current)
                    stack.extend(face_neighbors[current] - original_component)

            unvisited = original_component - all_visited
            while unvisited:
                seed = next(iter(unvisited))
                working_faces = set()
                working_verts = set()
                working_stack = [seed]

                while working_stack:
                    current = working_stack.pop()
                    if current in working_faces:
                        continue

                    current_verts = face_verts[current]
                    new_verts = working_verts.union(current_verts)
                    if len(new_verts) > 8:
                        continue

                    coords = [self.vertices[vid] for vid in new_verts]
                    xs, ys, zs = zip(*coords)
                    if (
                        max(xs) - min(xs) > 24
                        or max(ys) - min(ys) > 24
                        or max(zs) - min(zs) > 24
                    ):
                        continue

                    working_faces.add(current)
                    working_verts = new_verts
                    neighbors = face_neighbors[current] & unvisited
                    working_stack.extend(neighbors - working_faces)

                if working_faces:
                    cuboid = {
                        "name": f"{self.name}_{cuboid_id}",
                        "type": "mesh",
                        "faces": {cfid: self.faces[cfid] for cfid in working_faces},
                        "vertices": {vid: self.vertices[vid] for vid in working_verts},
                    }
                    cuboids.append(cuboid)
                    cuboid_id += 1
                    all_visited.update(working_faces)
                    unvisited.difference_update(working_faces)
                else:
                    all_visited.add(seed)
                    unvisited.discard(seed)

        return cuboids

    def map_vertices(self, cube_origin: List[float], vertices: List[float]) -> str:
        x_min = min(v[0] for v in vertices)
        y_min = min(v[1] for v in vertices)
        z_min = min(v[2] for v in vertices)

        x_max = max(v[0] for v in vertices)
        y_max = max(v[1] for v in vertices)
        z_max = max(v[2] for v in vertices)

        vertices_size = [
            round(x_max - x_min, 4),
            round(y_max - y_min, 4),
            round(z_max - z_min, 4),
        ]

        if vertices_size[0] == 0:
            return "west" if x_max > cube_origin[0] else "east"
        elif vertices_size[1] == 0:
            return "up" if y_max > cube_origin[1] else "down"
        elif vertices_size[2] == 0:
            return "south" if z_max > cube_origin[2] else "north"
        else:
            return "east"

    def process_cubes(self):
        vertices_values = list(self.vertices.values())

        origin = [
            min(x[0] for x in vertices_values),
            min(x[1] for x in vertices_values),
            min(x[2] for x in vertices_values),
        ]
        size = [
            max(x[0] for x in vertices_values) - origin[0],
            max(x[1] for x in vertices_values) - origin[1],
            max(x[2] for x in vertices_values) - origin[2],
        ]

        if self.model_center_offset != [0, 0, 0]:
            origin[0] -= self.model_center_offset[0]
            origin[1] -= self.model_center_offset[1]
            origin[2] -= self.model_center_offset[2]

        uv = {}
        for face_id, face_data in self.faces.items():
            uv_values = list(face_data["uv"].values())
            x_min = min(i[0] for i in uv_values) * self.mesh_texture_multiplier
            y_min = min(i[1] for i in uv_values) * self.mesh_texture_multiplier

            x_max = max(i[0] for i in uv_values) * self.mesh_texture_multiplier
            y_max = max(i[1] for i in uv_values) * self.mesh_texture_multiplier

            face_vertices = face_data["vertices"]
            vertices = []

            for v in face_vertices:
                vertices.append(self.vertices[v])

            original_origin = [
                origin[0] + self.model_center_offset[0],
                origin[1] + self.model_center_offset[1],
                origin[2] + self.model_center_offset[2],
            ]

            # Note: map_vertices expects specific args.
            direction = self.map_vertices(original_origin, vertices)

            uv[direction] = {
                "uv": [x_min, y_min],
                "uv_size": [round(x_max - x_min, 4), round(y_max - y_min, 4)],
            }

        return [{"origin": origin, "size": size, "uv": uv}]

    def compile(self):
        vertices_count = len(self.vertices.keys())
        if vertices_count > 0 and vertices_count <= 8:
            return self.process_cubes()
        else:
            meshes = []
            cuboids = self.extract_cuboids()

            for cube_data in cuboids:
                # Recursively create Mesh objects for sub-cuboids and compile them
                m = _Mesh.from_dict(cube_data, self.parent, self.model_center_offset)
                meshes.extend(m.compile())
            return meshes
