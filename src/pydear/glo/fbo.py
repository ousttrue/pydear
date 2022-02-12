from typing import Optional
from .texture import Texture
from OpenGL import GL
import logging
import ctypes
logger = logging.getLogger(__name__)


class Fbo:
    def __init__(self, width, height) -> None:
        self. texture = Texture(width, height)
        self.fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture.handle, 0)
        GL.glDrawBuffers([GL.GL_COLOR_ATTACHMENT0])
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        logger.debug(f'fbo: {self.fbo}, texture: {self.texture}')

    def __del__(self):
        logger.debug(f'fbo: {self.fbo}')
        GL.glDeleteFramebuffers(1, [self.fbo])

    def bind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)


class FboRenderer:
    def __init__(self) -> None:
        self.fbo: Optional[Fbo] = None

    def clear(self, width, height, color):
        if width == 0 or height == 0:
            return 0

        if self.fbo:
            if self.fbo.texture.width != width or self.fbo.texture.height != height:
                del self.fbo
                self.fbo = None
        if not self.fbo:
            self.fbo = Fbo(width, height)

        self.fbo.bind()
        GL.glViewport(0, 0, width, height)
        GL.glScissor(0, 0, width, height)
        GL.glClearColor(color[0] * color[3],
                        color[1] * color[3],
                        color[2] * color[3],
                        color[3])
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        return ctypes.c_void_p(int(self.fbo.texture.handle))
