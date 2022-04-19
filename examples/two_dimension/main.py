import logging
import dataclasses
import ctypes
from pydear import imgui as ImGui
from pydear import imgui_internal as ImGuiInternal
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('2D')

    from pydear import glo
    from pydear.utils import dockspace
    from pydear.utils.selector import Selector, Item
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

    bg = ImGui.ImVec4(1, 1, 1, 1)
    tint = ImGui.ImVec4(1, 1, 1, 1)

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin(selector.view_name, p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            selected = selector.selected
            if texture and selected:

                ImGui.ImageButton(texture, (w, h), (0, 1), (1, 0), 0, bg, tint)
                ImGuiInternal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,
                                             ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)
                io = ImGui.GetIO()

                selected.resize(w, h)

                if ImGui.IsItemActive():
                    x, y = ImGui.GetWindowPos()
                    y += ImGui.GetFrameHeight()
                    selected.mouse_drag(
                        int(io.MousePos.x-x), int(io.MousePos.y-y),
                        int(io.MouseDelta.x), int(io.MouseDelta.y),
                        io.MouseDown[0], io.MouseDown[1], io.MouseDown[2])
                else:
                    selected.mouse_release()

                if ImGui.IsItemHovered():
                    selected.wheel(int(io.MouseWheel))

                selected.render()

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
