"""VTK implementation of the MeshSerializer port.

Encodes a binary STL fully in memory and returns it as bytes. Nothing is written to
disk, so concurrent requests never share (or overwrite) a file on the server.
"""
import struct

import numpy as np
import vtk
from vtk.util import numpy_support

from src.modeling.mesh_serializer import MeshSerializer


class VtkStlSerializer(MeshSerializer):
    def serialize(self, mesh) -> bytes:
        triangulator = vtk.vtkTriangleFilter()
        triangulator.SetInputData(mesh)
        triangulator.PassLinesOff()
        triangulator.PassVertsOff()
        triangulator.Update()
        triangles = triangulator.GetOutput()

        header = b"\0" * 80  # 80-byte header (unused)

        points_data = triangles.GetPoints()
        triangle_count = triangles.GetNumberOfPolys()
        if points_data is None or triangle_count == 0:
            return header + struct.pack("<I", 0)

        points = numpy_support.vtk_to_numpy(points_data.GetData()).astype("<f4")
        # Triangulated polys are stored as [3, i, j, k, 3, i, j, k, ...]
        connectivity = numpy_support.vtk_to_numpy(triangles.GetPolys().GetData()).reshape(-1, 4)
        indices = connectivity[:, 1:4]

        v0 = points[indices[:, 0]]
        v1 = points[indices[:, 1]]
        v2 = points[indices[:, 2]]

        # Direct vectorized cross-product and normalization
        d1 = v1 - v0
        d2 = v2 - v0
        cx = d1[:, 1] * d2[:, 2] - d1[:, 2] * d2[:, 1]
        cy = d1[:, 2] * d2[:, 0] - d1[:, 0] * d2[:, 2]
        cz = d1[:, 0] * d2[:, 1] - d1[:, 1] * d2[:, 0]
        inv_lengths = 1.0 / np.maximum(np.sqrt(cx * cx + cy * cy + cz * cz), 1e-12)
        normals = np.empty((triangle_count, 3), dtype="<f4")
        normals[:, 0] = cx * inv_lengths
        normals[:, 1] = cy * inv_lengths
        normals[:, 2] = cz * inv_lengths

        # Each STL record is 50 bytes: normal (12B) + 3 vertices (36B) + attribute (2B).
        # Packing via structured dtype allocates contiguous memory directly and avoids slow strided slices.
        stl_dtype = np.dtype([
            ("normal", "<f4", 3),
            ("v0", "<f4", 3),
            ("v1", "<f4", 3),
            ("v2", "<f4", 3),
            ("attr", "<u2"),
        ])
        records = np.empty(triangle_count, dtype=stl_dtype)
        records["normal"] = normals
        records["v0"] = v0
        records["v1"] = v1
        records["v2"] = v2
        records["attr"] = 0

        return header + struct.pack("<I", triangle_count) + records.tobytes()
