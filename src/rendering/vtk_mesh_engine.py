"""VTK implementation of the MeshEngine port."""
import copy

import vtk

from src.modeling.mesh_engine import MeshEngine


class VtkMeshEngine(MeshEngine):
    def create_scene(self):
        return vtk.vtkAppendPolyData()

    def add(self, scene, mesh):
        scene.AddInputData(mesh)

    def finalize(self, scene):
        scene.Update()
        return scene.GetOutput()

    def translate(self, mesh, x, y, z, rotate_x=0.0):
        transform = vtk.vtkTransform()
        transform.Translate(x, y, z)
        transform.RotateX(rotate_x)
        transform_filter = vtk.vtkTransformPolyDataFilter()
        transform_filter.SetTransform(transform)
        transform_filter.SetInputData(mesh)
        transform_filter.Update()
        return transform_filter.GetOutput()

    def create_sphere(self, radius, resolution):
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(radius)
        sphere.SetThetaResolution(resolution)
        sphere.SetPhiResolution(resolution)
        sphere.SetCenter(0, 0, 0)
        sphere.Update()
        return sphere.GetOutput()

    def create_cap(self, radius, apparent_thickness, resolution):
        sphere = self.create_sphere(radius, resolution)

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

        return self.translate(clipper.GetOutput(), 0, 0, -cut_z)

    def create_plate(self, width, height, depth):
        plate = vtk.vtkCubeSource()
        plate.SetXLength(width)
        plate.SetYLength(height)
        plate.SetZLength(depth)
        plate.SetCenter(0, 0, 0)
        plate.Update()
        return plate.GetOutput()

    def create_cylinder(self, radius, height, resolution):
        cylinder = vtk.vtkCylinderSource()
        cylinder.SetRadius(radius)
        cylinder.SetHeight(height)
        cylinder.SetResolution(resolution)
        cylinder.SetCenter(0, 0, 0)
        cylinder.Update()
        return self.translate(cylinder.GetOutput(), -radius, 0, 0, 90)

    def bounds(self, mesh):
        return mesh.GetBounds()

    def copy(self, mesh):
        return copy.deepcopy(mesh)
