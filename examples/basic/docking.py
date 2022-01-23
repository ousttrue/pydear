import gui_app
import logging
import pydear as ImGui
from pydear.utils import dockspace
import ctypes
logger = logging.getLogger(__name__)


class DockingGui(gui_app.Gui):
    def __init__(self, glfw_window, clear_color) -> None:
        super().__init__(glfw_window)
        self.clear_color = clear_color

        io = ImGui.GetIO()
        io.ConfigFlags |= ImGui.ImGuiConfigFlags_.DockingEnable

        def show_hello(p_open):
            if ImGui.Begin('hello', p_open):
                ImGui.TextUnformatted('hello text')
                ImGui.SliderFloat4('clear color', self.clear_color, 0, 1)
                ImGui.ColorPicker4('color', self.clear_color)
            ImGui.End()
        self.views = [
            dockspace.DockView('demo', (ctypes.c_bool * 1)
                               (True), ImGui.ShowDemoWindow),
            dockspace.DockView('metrics', (ctypes.c_bool * 1)
                               (True), ImGui.ShowMetricsWindow),
            dockspace.DockView('hello', (ctypes.c_bool * 1)(True), show_hello),
        ]

    def _widgets(self):
        dockspace.dockspace(self.views)


def main():
    logging.basicConfig(level=logging.DEBUG)

    import glfw_app
    app = glfw_app.GlfwApp('hello_docking')
    gui = DockingGui(app.window, app.clear_color)
    while app.clear():
        gui.render()
    del gui

if __name__ == '__main__':
    main()
