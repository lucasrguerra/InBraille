"""Port (abstraction) for the 3D primitives the model builder needs.

The builder depends only on this interface, never on a concrete 3D library, so the
rendering backend (VTK today) can be swapped without touching the modeling logic.
Meshes are opaque handles from the builder's point of view.
"""
from abc import ABC, abstractmethod


class MeshEngine(ABC):
    @abstractmethod
    def create_scene(self):
        """Create an empty scene that meshes can be added to."""

    @abstractmethod
    def add(self, scene, mesh):
        """Add a mesh to a scene."""

    @abstractmethod
    def finalize(self, scene):
        """Combine everything added to a scene into a single mesh and return it."""

    @abstractmethod
    def translate(self, mesh, x, y, z, rotate_x=0.0):
        """Return a copy of mesh translated by (x, y, z) then rotated around X."""

    @abstractmethod
    def create_sphere(self, radius, resolution):
        """Create a full sphere centered at the origin."""

    @abstractmethod
    def create_cap(self, radius, apparent_thickness, resolution):
        """Create a spherical cap of the given apparent thickness, base at z=0."""

    @abstractmethod
    def create_plate(self, width, height, depth):
        """Create a rectangular box centered at the origin."""

    @abstractmethod
    def create_cylinder(self, radius, height, resolution):
        """Create a cylinder used for rounded plate borders."""

    @abstractmethod
    def bounds(self, mesh):
        """Return the axis-aligned bounds (xmin, xmax, ymin, ymax, zmin, zmax)."""

    @abstractmethod
    def copy(self, mesh):
        """Return an independent copy of a mesh (for reusing a template)."""
