from typing import Optional
import gui_app
import logging
import pydear as ImGui
from pydear.utils import dockspace
import ctypes
from OpenGL import GL
logger = logging.getLogger(__name__)


class Fbo:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

        self.texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, width,
                        height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, None)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(
            GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

        self.fbo = GL.glGenFramebuffers(1)
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self.texture, 0)
        GL.glDrawBuffers([GL.GL_COLOR_ATTACHMENT0])
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)

        logger.debug(f'fbo: {self.fbo}, texture: {self.texture}')

    def __del__(self):
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
            if self.fbo.width != width or self.fbo.height != height:
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
        self.fbo.unbind()

        return ctypes.c_void_p(int(self.fbo.texture))


class DockingFboGui(gui_app.Gui):
    def __init__(self, glfw_window) -> None:
        super().__init__(glfw_window)

        io = ImGui.GetIO()
        io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable

        self.clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
        self.fbo_manager = FboRenderer()

        def show_hello(p_open):
            if ImGui.Begin('hello', p_open):
                ImGui.TextUnformatted('hello text')
                ImGui.SliderFloat4('clear color', self.clear_color, 0, 1)
                ImGui.ColorPicker4('color', self.clear_color)
            ImGui.End()

        def show_view(p_open):
            ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
            if ImGui.Begin("render target", p_open,
                           ImGui.ImGuiWindowFlags_.NoScrollbar |
                           ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
                w, h = ImGui.GetContentRegionAvail()
                texture = self.fbo_manager.clear(
                    int(w), int(h), self.clear_color)
                if texture:
                    ImGui.BeginChild("cameraview")
                    ImGui.Image(texture, (w, h))

                    # # update
                    # x, y = ImGui.GetWindowPos()
                    # y += ImGui.GetFrameHeight()
                    # io = ImGui.GetIO()
                    # if ImGui.IsWindowFocused(ImGui.ImGuiFocusedFlags_.RootAndChildWindows):
                    #     # camera.update(io.MouseDelta.x, io.MouseDelta.y, size.x, size.y, io.MouseDown[0], io.MouseDown[1], io.MouseDown[2], io.MouseWheel);}
                    #     pass
                    # if ImGui.IsItemClicked(0) or ImGui.IsItemClicked(1) or ImGui.IsItemClicked(2):
                    #     logger.debug("click")
                    #     ImGui.SetWindowFocus()
                    # # rt.hovered = ImGui.IsItemHovered();
                    ImGui.EndChild()
            ImGui.End()
            ImGui.PopStyleVar()

        self.views = [
            dockspace.DockView('demo', (ctypes.c_bool * 1)
                               (True), ImGui.ShowDemoWindow),
            dockspace.DockView('metrics', (ctypes.c_bool * 1)
                               (True), ImGui.ShowMetricsWindow),
            dockspace.DockView('hello', (ctypes.c_bool * 1)(True), show_hello),
            dockspace.DockView('view', (ctypes.c_bool * 1)(True), show_view),
        ]

    def _widgets(self):
        dockspace.dockspace(self.views)


def main():
    logging.basicConfig(level=logging.DEBUG)

    import glfw_app
    app = glfw_app.GlfwApp('fbo')
    gui = DockingFboGui(app.window)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
