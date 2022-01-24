from typing import NamedTuple
from OpenGL import GL


class AttributeLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program,  name: str) -> 'AttributeLocation':
        return AttributeLocation(name, GL.glGetAttribLocation(program, name))


class VertexLayout(NamedTuple):
    attribute: AttributeLocation
    item_count: int  # maybe float1, 2, 3, 4 and 16
    stride: int
    byte_offset: int
