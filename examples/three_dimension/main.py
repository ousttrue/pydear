from typing import Optional
import logging
import ctypes
from pydear import imgui as ImGui
LOGGER = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('3D')

    from pydear.utils import dockspace

    from pydear.utils.selector import Selector
    selector = Selector()

    def show_selector(p_open):
        if ImGui.Begin("selector", p_open):
            selector.show()
        ImGui.End()

        if selector.selected:
            selector.selected.show()

    def render(w, h):
        if selector.selected:
            selector.selected.render(w, h)

    from pydear.utils.fbo_view import FboView
    fbo = FboView(render)

    import contents.cube
    selector.add(contents.cube.Cube(fbo.mouse_event))
    import contents.teapot
    selector.add(contents.teapot.TeaPot(fbo.mouse_event))
    import contents.gizmo
    selector.add(contents.gizmo.GizmoScene(fbo.mouse_event))

    views = [
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('samples', show_selector,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('view', fbo.show,
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
