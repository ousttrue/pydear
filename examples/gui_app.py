import logging
import pydear as ImGui
logger = logging.getLogger(__name__)


class Gui:
    def __init__(self, glfw_window) -> None:
        ImGui.CreateContext()

        io = ImGui.GetIO()

        io.Fonts.Build()

        from pydear.backends.glfw import GlfwRenderer
        self.impl_glfw = GlfwRenderer(glfw_window)
        from pydear.backends.opengl import Renderer
        self.impl_opengl = Renderer()

    def __del__(self):
        logging.debug('ImGui.DestroyContext')
        del self.impl_opengl
        del self.impl_glfw
        ImGui.DestroyContext()

    def _widgets(self):
        pass

    def render(self):
        self.impl_glfw.process_inputs()
        ImGui.NewFrame()

        self._widgets()

        ImGui.Render()
        self.impl_opengl.render(ImGui.GetDrawData())
