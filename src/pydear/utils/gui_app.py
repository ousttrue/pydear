from typing import Callable, Optional
import asyncio
import logging
from pydear import imgui as ImGui
from OpenGL import GL
logger = logging.getLogger(__name__)


class Gui:
    def __init__(self, loop: asyncio.AbstractEventLoop, widgets: Optional[Callable[[], None]] = None) -> None:
        self.loop = loop
        ImGui.CreateContext()

        io = ImGui.GetIO()

        io.Fonts.Build()

        from pydear.backends.impl_opengl3 import Renderer
        self.impl_opengl = Renderer()

        if not widgets:
            def empty():
                pass
            widgets = empty
        self._widgets: Callable[[], None] = widgets

    def __del__(self):
        logging.debug('ImGui.DestroyContext')
        del self.impl_opengl
        ImGui.DestroyContext()

    def render(self):
        ImGui.NewFrame()

        self._widgets()

        ImGui.Render()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.impl_opengl.render(ImGui.GetDrawData())
