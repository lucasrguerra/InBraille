"""Use case: turn a Braille string into the bytes of an STL file."""
from collections import OrderedDict
from src.modeling.mesh_serializer import MeshSerializer
from src.modeling.model_builder import BrailleModelBuilder
from src.modeling.options import ModelOptions


class StlService:
    def __init__(self, builder: BrailleModelBuilder, serializer: MeshSerializer, cache_size: int = 128):
        self._builder = builder
        self._serializer = serializer
        self._cache = OrderedDict()
        self._cache_size = cache_size

    def generate(self, braille: str, options: ModelOptions) -> bytes:
        cache_key = (braille, options)
        if cache_key in self._cache:
            self._cache.move_to_end(cache_key)
            return self._cache[cache_key]

        mesh = self._builder.build(braille, options)
        stl_bytes = self._serializer.serialize(mesh)

        if len(self._cache) >= self._cache_size:
            self._cache.popitem(last=False)
        self._cache[cache_key] = stl_bytes

        return stl_bytes
