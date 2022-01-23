import logging
import glfw
from OpenGL import GL
import ctypes
logger = logging.getLogger(__name__)

class GlfwApp:
    def __init__(self, title: str, width=1024, height=768) -> None:
        def glfw_error_callback(error: int, description: str):
            logger.error(f"{error}: {description}")
        glfw.set_error_callback(glfw_error_callback)

        if not glfw.init():
            raise RuntimeError('glfw.init')

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            raise RuntimeError('glfw.create_window')

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # Enable vsync

        logging.debug(GL.glGetString(GL.GL_VERSION))
        self.clear_color = (ctypes.c_float * 4)(0.5, 0.5, 0.8, 1)

    def __del__(self):
        logging.debug('exit...')

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
