from typing import Callable, Optional
import logging
import pydear as ImGui
from OpenGL import GL
logger = logging.getLogger(__name__)


class Gui:
    def __init__(self, glfw_window, widgets: Optional[Callable[[], None]] = None) -> None:
        ImGui.CreateContext()

        io = ImGui.GetIO()

        io.Fonts.Build()

        from pydear.backends.glfw import GlfwRenderer
        self.impl_glfw = GlfwRenderer(glfw_window)
        from pydear.backends.opengl import Renderer
        self.impl_opengl = Renderer()

        if not widgets:
            def empty():
                pass
            widgets = empty
        self._widgets: Callable[[], None] = widgets

    def __del__(self):
        logging.debug('ImGui.DestroyContext')
        del self.impl_opengl
        del self.impl_glfw
        ImGui.DestroyContext()

    def render(self):
        self.impl_glfw.process_inputs()
        ImGui.NewFrame()

        self._widgets()

        ImGui.Render()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.impl_opengl.render(ImGui.GetDrawData())
