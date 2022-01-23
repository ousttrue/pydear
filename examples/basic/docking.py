import logging
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello_docking')

    from pydear.utils import dockspace
    from pydear import imgui as ImGui
    import ctypes

    def show_hello(p_open):
        if ImGui.Begin('hello', p_open):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', app.clear_color, 0, 1)
            ImGui.ColorPicker4('color', app.clear_color)
        ImGui.End()
    views = [
        dockspace.Dock('demo', (ctypes.c_bool * 1)
                           (True), ImGui.ShowDemoWindow),
        dockspace.Dock('metrics', (ctypes.c_bool * 1)
                           (True), ImGui.ShowMetricsWindow),
        dockspace.Dock('hello', (ctypes.c_bool * 1)(True), show_hello),
    ]

    gui = dockspace.DockingGui(app.window, views)

    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
