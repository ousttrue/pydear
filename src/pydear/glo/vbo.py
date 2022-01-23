from OpenGL import GL
import logging
import ctypes
logger = logging.getLogger(__name__)


class Vbo:
    def __init__(self):
        self.vbo = GL.glGenBuffers(1)

    def __del__(self):
        logger.debug(f'GL.glDeleteBuffers: {self.vbo}')
        GL.glDeleteBuffers(1, [self.vbo])

    def bind(self):
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)

    def set_vertices(self, vertices):
        self.bind()
        GL.glBufferData(GL.GL_ARRAY_BUFFER, ctypes.sizeof(vertices),
                        vertices, GL.GL_STATIC_DRAW)
