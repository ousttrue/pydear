from typing import Optional
import pathlib
import argparse
import logging
import ctypes
from pydear import imgui as ImGui
from pydear.utils.fbo_view import FboView
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', type=pathlib.Path)
    args = parser.parse_args()

    setting = None
    if args.ini:
        from pydear.utils.setting import BinSetting
        setting = BinSetting(args.ini)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('2D', setting=setting)

    from pydear.utils import dockspace
    from pydear.utils.selector import Selector, Item
    selector = Selector()

    def show_selector(p_open):
        if not p_open or p_open[0]:
            if ImGui.Begin("selector", p_open):
                selector.show()
            ImGui.End()

        if selector.selected:
            selector.selected.show()

    def render(w: int, h: int):
        if selector.selected:
            selector.selected.render(w, h)

    fbo = FboView(render)

    import contents.triangle
    selector.add(contents.triangle.Triangle())
    import contents.view
    selector.add(contents.view.View(fbo.mouse_event))
    import contents.text
    selector.add(contents.text.TextRenderer(fbo.mouse_event))

    views = [
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('samples', show_selector,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('view', fbo.show,
                       (ctypes.c_bool * 1)(True)),
    ]

    gui = dockspace.DockingGui(app.loop, docks=views, setting=setting)

    # main loop
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()

    # save ini
    if setting:
        gui.save()
        app.save()
        setting.save()


if __name__ == '__main__':
    main()
