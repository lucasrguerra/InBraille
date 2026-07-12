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

        normals = np.cross(v1 - v0, v2 - v0)
        lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        lengths[lengths == 0] = 1
        normals = normals / lengths

        # Each STL record is 50 bytes: 12 float32 (normal + 3 vertices) + 2 attribute bytes.
        records = np.zeros((triangle_count, 12), dtype="<f4")
        records[:, 0:3] = normals
        records[:, 3:6] = v0
        records[:, 6:9] = v1
        records[:, 9:12] = v2

        padded = np.zeros((triangle_count, 50), dtype="<u1")
        padded[:, 0:48] = records.view("<u1").reshape(triangle_count, 48)

        return header + struct.pack("<I", triangle_count) + padded.tobytes()
