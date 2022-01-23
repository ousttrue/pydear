import gui_app
import logging
import pydear as ImGui
logger = logging.getLogger(__name__)


class Hello(gui_app.Gui):
    def __init__(self, glfw_window, clear_color) -> None:
        super().__init__(glfw_window)
        self.clear_color = clear_color

    def _widgets(self):
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin('hello'):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', self.clear_color, 0, 1)
            ImGui.ColorPicker4('color', self.clear_color)
        ImGui.End()


def main():
    logging.basicConfig(level=logging.DEBUG)

    import glfw_app
    app = glfw_app.GlfwApp('hello')
    gui = Hello(app.window, app.clear_color)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
