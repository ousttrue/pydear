from typing import Optional
import logging
import dataclasses
import ctypes
from pydear import imgui as ImGui
from pydear import imgui_internal as ImGuiInternal
LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class State:
    active: bool


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('3D')

    from pydear import glo
    from pydear.utils import dockspace
    from pydear.utils.selector import Selector
    selector = Selector()
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    import contents.cube
    selector.add(contents.cube.Cube())

    import contents.teapot
    selector.add(contents.teapot.TeaPot())

    import contents.gizmo
    selector.add(contents.gizmo.GizmoScene())

    def show_selector(p_open):
        if ImGui.Begin("selector", p_open):
            selector.show()
        ImGui.End()

    bg = ImGui.ImVec4(1, 1, 1, 1)
    tint = ImGui.ImVec4(1, 1, 1, 1)

    from pydear.utils.mouseevent import MouseInput, MouseEvent
    mouse_event = MouseEvent()

    def on_mouse(current: MouseInput, last: Optional[MouseInput]):
        selected = selector.selected
        if selected:
            selected.resize(current.width, current.height)

            if current.is_active:
                if last:
                    selected.mouse_drag(
                        current.x, current.y,
                        current.x-last.x,  current.y-last.y,
                        current.left_down, current.right_down, current.middle_down
                    )
            else:
                selected.mouse_release(current.x, current.y)

            if current.is_hover:
                selected.wheel(current.wheel)

            selected.render()

    mouse_event += on_mouse

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin(selector.view_name, p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()

            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:

                ImGui.ImageButton(texture, (w, h), (0, 1), (1, 0), 0, bg, tint)
                ImGuiInternal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,
                                             ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)
                io = ImGui.GetIO()
                x, y = ImGui.GetWindowPos()
                y += ImGui.GetFrameHeight()

                mouse_event.process(MouseInput(int(io.MousePos.x-x), int(io.MousePos.y-y), w, h,
                                    io.MouseDown[0], io.MouseDown[1], io.MouseDown[2],
                                    ImGui.IsItemActive(), ImGui.IsItemHovered(),
                                    int(io.MouseWheel)
                ))

        ImGui.End()
        ImGui.PopStyleVar()

        if selector.selected:
            selector.selected.show()

    views = [
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
