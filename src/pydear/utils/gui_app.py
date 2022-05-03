from typing import Callable, Optional
import ctypes
import asyncio
import logging
from pydear import imgui as ImGui
from OpenGL import GL
from .setting import BinSetting
logger = logging.getLogger(__name__)

SETTING_KEY = 'imgui'


class Gui:
    def __init__(self, loop: asyncio.AbstractEventLoop, *,
                 widgets: Optional[Callable[[], None]] = None,
                 setting: Optional[BinSetting] = None
                 ) -> None:
        self.setting = setting
        self.loop = loop
        ImGui.CreateContext()

        io = ImGui.GetIO()
        if self.setting:
            io.IniFilename = None  # type: ignore
            data = self.setting[SETTING_KEY]
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

    def save(self):
        if self.setting:
            p_size = (ctypes.c_int * 1)()
            data = ImGui.SaveIniSettingsToMemory(p_size)
            if p_size[0]:
                self.setting[SETTING_KEY] = data.encode('utf-8')

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
        from .import modal
        modal.show()

        ImGui.Render()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        self.impl_opengl.render(ImGui.GetDrawData())
