import logging
import ctypes
LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('fbo')

    from pydear import imgui as ImGui
    from pydear.utils import dockspace
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    from pydear import glo
    fbo_manager = glo.FboRenderer()

    bg = ImGui.ImVec4(1, 1, 1, 1)
    tint = ImGui.ImVec4(1, 1, 1, 1)

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                ImGui.ImageButton(texture, (w, h), (0, 1), (1, 0), 0, bg, tint)
                from pydear import imgui_internal
                imgui_internal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,
                                              ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)
                io = ImGui.GetIO()
                if ImGui.IsItemActive():
                    x, y = ImGui.GetWindowPos()
                    y += ImGui.GetFrameHeight()

                    clear_color[0] = (io.MousePos.x-x) / w
                    clear_color[1] = (io.MousePos.y-y) / h
                    # selected.mouse_drag(
                    #     int(io.MousePos.x-x), int(io.MousePos.y-y),
                    #     int(io.MouseDelta.x), int(io.MouseDelta.y),
                    #     io.MouseDown[0], io.MouseDown[1], io.MouseDown[2])
                    tint.x = 1.0
                else:
                    tint.x = 0.5
                    # selected.mouse_release()

                if ImGui.IsItemHovered():
                    tint.z = 1.0
                else:
                    tint.z = 0.5

                # selected.render()

        ImGui.End()
        ImGui.PopStyleVar()

    views = [
        dockspace.Dock('demo', ImGui.ShowDemoWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('view', show_view,
                       (ctypes.c_bool * 1)(True)),
    ]

    gui = dockspace.DockingGui(app.loop, docks=views)
    from pydear.backends import impl_glfw
    impl_glfw = impl_glfw.ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    del gui


if __name__ == '__main__':
    main()
