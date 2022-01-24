from OpenGL import GL
import logging
logger = logging.getLogger(__name__)


class Texture:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.handle = GL.glGenTextures(1)

        self.bind()
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width,
                        height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        self.unbind()

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.handle)

    def unbind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
