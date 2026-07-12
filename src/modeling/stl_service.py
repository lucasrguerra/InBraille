"""Use case: turn a Braille string into the bytes of an STL file."""
from src.modeling.mesh_serializer import MeshSerializer
from src.modeling.model_builder import BrailleModelBuilder
from src.modeling.options import ModelOptions


class StlService:
    def __init__(self, builder: BrailleModelBuilder, serializer: MeshSerializer):
        self._builder = builder
        self._serializer = serializer

    def generate(self, braille: str, options: ModelOptions) -> bytes:
        mesh = self._builder.build(braille, options)
        return self._serializer.serialize(mesh)
