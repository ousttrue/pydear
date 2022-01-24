import logging
import dataclasses
import ctypes
from pydear import imgui as ImGui
logger = logging.getLogger(__name__)


@dataclasses.dataclass
class State:
    hover: bool


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('samples')

    from pydear import glo
    from pydear.utils import dockspace
    from pydear.utils.selector import Selector
    from pydear.utils.item import Item, Input
    selector = Selector()
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    from triangle import Triangle
    triangle = Triangle()
    selector.add(Item('triangle', triangle.render))
    from view import View
    view = View()
    selector.add(Item('view', view.render,
                 input=view.on_input,
                 show=view.show)
                 )

    def show_selector(p_open):
        if ImGui.Begin("selector", p_open):
            selector.show()
        ImGui.End()

    state = State(False)

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin(selector.view_name, p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                selected = selector.selected
                if selected:
                    # input handling
                    if state.hover or ImGui.IsMouseDragging(0) or ImGui.IsMouseDragging(1) or ImGui.IsMouseDragging(2):
                        x, y = ImGui.GetWindowPos()
                        y += ImGui.GetFrameHeight()
                        io = ImGui.GetIO()

                        input = Input(
                            int(w), int(h),
                            int(io.MousePos.x-x), int(io.MousePos.y-y),
                            int(io.MouseDelta.x), int(io.MouseDelta.y),
                            io.MouseDown[0], io.MouseDown[1], io.MouseDown[2], int(io.MouseWheel))
                        selected.input(input)

                    # rendering
                    selected.render()

                ImGui.BeginChild("_image_")
                ImGui.Image(texture, (w, h), (0, 1), (1, 0))
                state.hover = ImGui.IsItemHovered()
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()

        if selector.selected:
            selector.selected.show()

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
