import logging
import ctypes
from pydear import imgui as ImGui
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('fbo')

    from pydear.utils import dockspace
    from pydear import glo
    from selector import Selector
    from item import Item
    selector = Selector()
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    from triangle import Triangle
    triangle = Triangle()
    selector.add(Item('triangle', triangle.draw))

    def show_selector(p_open):
        if ImGui.Begin("selector", p_open):
            selector.show()
        ImGui.End()

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin(selector.view_name, p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                if selector.selected:
                    selector.selected.show()

                ImGui.BeginChild("_image_")
                ImGui.Image(texture, (w, h), (0, 1), (1, 0))
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()

    views = [
        dockspace.Dock('demo', (ctypes.c_bool * 1)
                       (True), ImGui.ShowDemoWindow),
        dockspace.Dock('metrics', (ctypes.c_bool * 1)
                       (True), ImGui.ShowMetricsWindow),
        dockspace.Dock('samples', (ctypes.c_bool * 1)(True), show_selector),

        dockspace.Dock('view', (ctypes.c_bool * 1)(True), show_view),
    ]

    gui = dockspace.DockingGui(app.window, views)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
