from typing import Callable, Optional
import ctypes
import asyncio
import logging
from pydear import imgui as ImGui
from OpenGL import GL
from .setting import SettingInterface
logger = logging.getLogger(__name__)


class Gui:
    def __init__(self, loop: asyncio.AbstractEventLoop, *,
                 widgets: Optional[Callable[[], None]] = None,
                 modal: Optional[Callable[[], None]] = None,
                 setting: Optional[SettingInterface] = None
                 ) -> None:
        self.setting = setting
        self.loop = loop
        ImGui.CreateContext()

        io = ImGui.GetIO()
        if self.setting:
            io.IniFilename = None  # type: ignore
            data = self.setting.load()
            if data:
                ImGui.LoadIniSettingsFromMemory(data, len(data))

        self._setup_font()

        from pydear.backends.impl_opengl3 import Renderer
        self.impl_opengl = Renderer()

        def empty():
            pass
        if not widgets:
            widgets = empty
        self._widgets: Callable[[], None] = widgets
        if not modal:
            modal = empty
        self._modal: Callable[[], None] = modal

    def save(self):
        if self.setting:
            p_size = (ctypes.c_int * 1)()
            data = ImGui.SaveIniSettingsToMemory(p_size)
            if p_size[0]:
                self.setting.save(data.encode('utf-8'))

    def __del__(self):
        logging.debug('ImGui.DestroyContext')
        del self.impl_opengl
        ImGui.DestroyContext()

    def _setup_font(self):
        io = ImGui.GetIO()
        io.Fonts.Build()

    def render(self):
        ImGui.NewFrame()

        self._widgets()
        self._modal()

        ImGui.Render()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.impl_opengl.render(ImGui.GetDrawData())
