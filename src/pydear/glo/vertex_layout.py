from typing import NamedTuple, Iterable
from OpenGL import GL
import logging
logger = logging.getLogger(__name__)


class AttributeLocation(NamedTuple):
    name: str
    location: int

    @staticmethod
    def create(program,  name: str) -> 'AttributeLocation':
        return AttributeLocation(name, GL.glGetAttribLocation(program, name))

    @staticmethod
    def create_list(program) -> Iterable['AttributeLocation']:
        count = GL.glGetProgramiv(program, GL.GL_ACTIVE_ATTRIBUTES)
        logger.debug(f"Active Attributes: {count}")

        for i in range(count):
            name, size, type_ = GL.glGetActiveAttrib(program, i)
            yield AttributeLocation.create(program, name)


class VertexLayout(NamedTuple):
    attribute: AttributeLocation
    item_count: int  # maybe float1, 2, 3, 4 and 16
    stride: int
    byte_offset: int
