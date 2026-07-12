from io import BytesIO
import struct
import numpy as np
import vtk
from vtk.util import numpy_support



def createScene():
    return vtk.vtkAppendPolyData()



def makeTranslation(object, x, y, z, rotate_x=0.0, rotate_y=0.0, rotate_z=0.0):
    transform = vtk.vtkTransform()
    transform.Translate(x, y, z)
    transform.RotateX(rotate_x)
    transform.RotateY(rotate_y)
    transform.RotateZ(rotate_z)
    transform_filter = vtk.vtkTransformPolyDataFilter()
    transform_filter.SetTransform(transform)
    transform_filter.SetInputData(object)
    transform_filter.Update()
    return transform_filter.GetOutput()


def createSphere(radius=1, resolution=20):
    sphere = vtk.vtkSphereSource()
    sphere.SetRadius(radius)
    sphere.SetThetaResolution(resolution)
    sphere.SetPhiResolution(resolution)
    sphere.SetCenter(0, 0, 0)
    sphere.Update()
    return sphere.GetOutput()



def createBrailleCap(radius=1, apparent_thickness=0.65, resolution=20):
    sphere = createSphere(radius, resolution)

    cut_z = radius - apparent_thickness
    plane = vtk.vtkPlane()
    plane.SetOrigin(0, 0, cut_z)
    plane.SetNormal(0, 0, 1)

    planes = vtk.vtkPlaneCollection()
    planes.AddItem(plane)

    clipper = vtk.vtkClipClosedSurface()
    clipper.SetInputData(sphere)
    clipper.SetClippingPlanes(planes)
    clipper.Update()

    return makeTranslation(clipper.GetOutput(), 0, 0, -cut_z)



def createPlate(width=1, height=1, depth=1):
    plate = vtk.vtkCubeSource()
    plate.SetXLength(width)
    plate.SetYLength(height)
    plate.SetZLength(depth)
    plate.SetCenter(0, 0, 0)
    plate.Update()
    return plate.GetOutput()



def createCylinder(radius=1, width=1, resolution=20):
    cylinder = vtk.vtkCylinderSource()
    cylinder.SetRadius(radius)
    cylinder.SetHeight(width)
    cylinder.SetResolution(resolution)
    cylinder.SetCenter(0, 0, 0)
    cylinder.Update()
    return makeTranslation(cylinder.GetOutput(), -radius, 0, 0, 90)



def createBraillePoints(
        points_code,
        radius = 1,
        spacing = 2.7,
        resolution = 20,
        points_only = False,
        apparent_thickness = 0.65,
    ):
    character = createScene()

    def createDot():
        if points_only:
            return createBrailleCap(radius, apparent_thickness, resolution)
        return createSphere(radius, resolution)

    if points_code[0] == "1":
        character.AddInputData(makeTranslation(createDot(), 0, (2 * spacing), 0))
    if points_code[1] == "1":
        character.AddInputData(makeTranslation(createDot(), 0, spacing, 0))
    if points_code[2] == "1":
        character.AddInputData(makeTranslation(createDot(), 0, 0, 0))
    if points_code[3] == "1":
        character.AddInputData(makeTranslation(createDot(), spacing, (2 * spacing), 0))
    if points_code[4] == "1":
        character.AddInputData(makeTranslation(createDot(), spacing, spacing, 0))
    if points_code[5] == "1":
        character.AddInputData(makeTranslation(createDot(), spacing, 0, 0))

    character.Update()
    return character.GetOutput()



def sceneToSTL(scene):
    # Encode a binary STL fully in memory and return it as a buffer. Nothing is written
    # to disk, so concurrent requests never share (or overwrite) a file on the server.
    triangulator = vtk.vtkTriangleFilter()
    triangulator.SetInputData(scene)
    triangulator.PassLinesOff()
    triangulator.PassVertsOff()
    triangulator.Update()
    mesh = triangulator.GetOutput()

    output = BytesIO()
    output.write(b"\0" * 80)  # 80-byte header (unused)

    points_data = mesh.GetPoints()
    triangle_count = mesh.GetNumberOfPolys()
    if points_data is None or triangle_count == 0:
        output.write(struct.pack("<I", 0))
        output.seek(0)
        return output

    points = numpy_support.vtk_to_numpy(points_data.GetData()).astype("<f4")
    # Triangulated polys are stored as [3, i, j, k, 3, i, j, k, ...]
    connectivity = numpy_support.vtk_to_numpy(mesh.GetPolys().GetData()).reshape(-1, 4)
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

    output.write(struct.pack("<I", triangle_count))
    output.write(padded.tobytes())
    output.seek(0)
    return output
