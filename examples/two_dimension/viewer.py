from typing import Optional
import logging
import ctypes
from OpenGL import GL
logger = logging.getLogger(__name__)





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
