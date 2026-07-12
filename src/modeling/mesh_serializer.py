"""Port (abstraction) for turning a finished mesh into serialized bytes."""
from abc import ABC, abstractmethod


class MeshSerializer(ABC):
    @abstractmethod
    def serialize(self, mesh) -> bytes:
        """Serialize a mesh into the bytes of a 3D file (binary STL)."""
