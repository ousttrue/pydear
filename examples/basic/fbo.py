from typing import Optional
import logging
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


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('fbo')

    from pydear import imgui as ImGui
    from pydear.utils import dockspace
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = FboRenderer()

    def show_hello(p_open):
        if ImGui.Begin('hello', p_open):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', clear_color, 0, 1)
            ImGui.ColorPicker4('color', clear_color)
        ImGui.End()

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                ImGui.BeginChild("_image_")
                ImGui.Image(texture, (w, h))
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()

    views = [
        dockspace.Dock('demo', (ctypes.c_bool * 1)
                       (True), ImGui.ShowDemoWindow),
        dockspace.Dock('metrics', (ctypes.c_bool * 1)
                       (True), ImGui.ShowMetricsWindow),
        dockspace.Dock('hello', (ctypes.c_bool * 1)(True), show_hello),
        dockspace.Dock('view', (ctypes.c_bool * 1)(True), show_view),
    ]

    gui = dockspace.DockingGui(app.window, views)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
