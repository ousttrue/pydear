import logging
from pydear import imgui as ImGui
LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    #
    # glfw app
    #
    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello')

    def hello():
        '''
        imgui widgets
        '''
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin('hello'):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', app.clear_color, 0, 1)
            ImGui.ColorPicker4('color', app.clear_color)
        ImGui.End()

    #
    # imgui
    #
    from pydear.utils import gui_app
    gui = gui_app.Gui(app.loop, widgets=hello)

    #
    # glfw_app => ImplGlfwInput => imgui
    #
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)

    #
    # main loop
    #
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()


if __name__ == '__main__':
    main()
