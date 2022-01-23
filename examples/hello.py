import glfw
import logging
from OpenGL import GL
import pydear as ImGui
import ctypes
logger = logging.getLogger(__name__)


class GlfwApp:
    def __init__(self, title: str, width=1024, height=768) -> None:
        def glfw_error_callback(error: int, description: str):
            logger.error(f"{error}: {description}")
        glfw.set_error_callback(glfw_error_callback)

        if not glfw.init():
            raise RuntimeError('glfw.init')
        glfw.swap_interval(1)  # Enable vsync

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            raise RuntimeError('glfw.create_window')

        glfw.make_context_current(self.window)

        logging.debug(GL.glGetString(GL.GL_VERSION))
        self.clear_color = (ctypes.c_float * 4)(0.5, 0.5, 0.8, 1)

    def __del__(self):
        logging.debug('glfw.terminate')
        glfw.terminate()

    def clear(self) -> bool:
        if glfw.window_should_close(self.window):
            return False

        glfw.swap_buffers(self.window)

        glfw.poll_events()

        width, height = glfw.get_framebuffer_size(self.window)
        GL.glViewport(0, 0, width, height)
        GL.glScissor(0, 0, width, height)
        GL.glClearColor(self.clear_color[0] * self.clear_color[3],
                        self.clear_color[1] * self.clear_color[3],
                        self.clear_color[2] * self.clear_color[3],
                        self.clear_color[3])

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        return True


class Gui:
    def __init__(self, glfw_window, clear_color) -> None:
        ImGui.CreateContext()

        io = ImGui.GetIO()

        io.Fonts.Build()

        from pydear.backends.glfw import GlfwRenderer
        self.impl_glfw = GlfwRenderer(glfw_window)
        from pydear.backends.opengl import Renderer
        self.impl_opengl = Renderer()

        self.clear_color = clear_color

    def __del__(self):
        logging.debug('ImGui.DestroyContext')
        del self.impl_opengl
        del self.impl_glfw
        ImGui.DestroyContext()

    def _widgets(self):
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin('hello'):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', self.clear_color, 0, 1)
            ImGui.ColorPicker4('color', self.clear_color)
        ImGui.End()

    def render(self):
        self.impl_glfw.process_inputs()
        ImGui.NewFrame()

        self._widgets()

        ImGui.Render()
        self.impl_opengl.render(ImGui.GetDrawData())


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = GlfwApp('hello')
    gui = Gui(app.window, app.clear_color)

    while app.clear():
        gui.render()

    del gui
    del app


if __name__ == '__main__':
    main()
