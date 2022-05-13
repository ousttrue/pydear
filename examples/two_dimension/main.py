from typing import Optional
import pathlib
import argparse
import logging
import ctypes
from pydear import imgui as ImGui
from pydear.utils.fbo_view import FboView
logger = logging.getLogger(__name__)


class SelectorView:
    def __init__(self, fbo: FboView, font: pathlib.Path) -> None:
        from pydear.utils.selector import Selector, Item
        self.selector = Selector()

        from contents.triangle import Triangle
        self.selector.add(Triangle())
        from contents.view import View
        self.selector.add(View(fbo.mouse_event))
        from contents.text import TextRenderer
        self.selector.add(TextRenderer(fbo.mouse_event))
        from contents.nanovg import NanoVgSample
        self.selector.add(NanoVgSample(font, fbo.mouse_event))

    def show(self, p_open):
        if not p_open or p_open[0]:
            if ImGui.Begin("selector", p_open):
                self.selector.show()
            ImGui.End()

        if self.selector.selected:
            self.selector.selected.show()

    def render(self, w: int, h: int):
        if self.selector.selected:
            self.selector.selected.render(w, h)


def main():
    logging.basicConfig(
        format='[%(levelname)s]%(name)s:%(funcName)s: %(message)s', level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', type=pathlib.Path)
    parser.add_argument('--font', type=pathlib.Path)
    args = parser.parse_args()

    setting = None
    if args.ini:
        from pydear.utils.setting import BinSetting
        setting = BinSetting(args.ini)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('2D', setting=setting)

    # selector
    fbo = FboView()
    selector = SelectorView(fbo, args.font)
    fbo.render = selector.render

    # docking
    from pydear.utils import dockspace
    views = [
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('samples', selector.show,
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
