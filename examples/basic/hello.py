import logging
import pathlib
from pydear import imgui as ImGui
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello')

    def hello():
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin('hello'):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', app.clear_color, 0, 1)
            ImGui.ColorPicker4('color', app.clear_color)
        ImGui.End()

    from pydear.utils import gui_app
    gui = gui_app.Gui(app.window, hello)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
