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
    app = glfw_app.GlfwApp('2D')

    from pydear import glo
    from pydear.utils import dockspace
    from pydear.utils.selector import Selector
    from pydear.utils.item import Item, Input
    selector = Selector()
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    import contents.triangle
    selector.add(contents.triangle.Triangle())
    import contents.view
    selector.add(contents.view.View())
    import contents.text
    selector.add(contents.text.TextRenderer())

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
                    input = Input.get(state.hover, w, h)
                    if input:
                        selected.drag(input)

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
        dockspace.Dock('demo', ImGui.ShowDemoWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('samples', show_selector,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('view', show_view,
                       (ctypes.c_bool * 1)(True)),
    ]

    gui = dockspace.DockingGui(app.loop, docks=views)
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    del gui


if __name__ == '__main__':
    main()
