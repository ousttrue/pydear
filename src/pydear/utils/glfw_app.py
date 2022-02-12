from typing import Tuple
import logging
import glfw
from OpenGL import GL
import ctypes
logger = logging.getLogger(__name__)


class GlfwApp:
    def __init__(self, title: str, width=1024, height=768, gl_major=3, gl_minor=3, use_core_profile=True, use_vsync=True) -> None:
        def glfw_error_callback(error: int, description: str):
            logger.error(f"{error}: {description}")
        glfw.set_error_callback(glfw_error_callback)

        if not glfw.init():
            raise RuntimeError('glfw.init')

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, gl_major)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, gl_minor)
        if use_core_profile:
            # Context profiles are only defined for OpenGL version 3.2 and above
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            raise RuntimeError('glfw.create_window')

        glfw.make_context_current(self.window)
        if use_vsync:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

        glfw.set_time(0)
        logging.debug(GL.glGetString(GL.GL_VERSION))
        self.clear_color = (ctypes.c_float * 4)(0.5, 0.5, 0.8, 1)

    def __del__(self):
        logging.debug('exit...')
        glfw.destroy_window(self.window)
        glfw.terminate()

    def clear(self) -> bool:

        glfw.swap_buffers(self.window)

        glfw.poll_events()
        if glfw.window_should_close(self.window):
            return False

        width, height = glfw.get_framebuffer_size(self.window)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glViewport(0, 0, width, height)
        GL.glScissor(0, 0, width, height)
        GL.glClearColor(self.clear_color[0] * self.clear_color[3],
                        self.clear_color[1] * self.clear_color[3],
                        self.clear_color[2] * self.clear_color[3],
                        self.clear_color[3])

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        return True

    def get_rect(self) -> Tuple[float, float, float, float]:
        x, y = glfw.get_cursor_pos(self.window)
        w, h = glfw.get_framebuffer_size(self.window)
        return x, y, w, h
