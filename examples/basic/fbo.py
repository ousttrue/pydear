from typing import Optional
import asyncio
import logging
import ctypes
from pydear import imgui as ImGui
from pydear.utils.mouse_event import MouseInput
from pydear.utils import dockspace
LOGGER = logging.getLogger(__name__)


class GUI(dockspace.DockingGui):
    def __init__(self, loop: asyncio.events.AbstractEventLoop) -> None:
        from pydear.utils.fbo_view import FboView
        self.texture_view = FboView()

        def on_event(current: MouseInput, last: Optional[MouseInput]):

            if current.is_active:
                # any pressed
                self.texture_view.clear_color[0] = current.x / current.width
                self.texture_view.clear_color[1] = current.y / current.height
                self.texture_view.tint.x = 1.0
            else:
                if current.is_hover:
                    self.texture_view.tint.z = 1.0
                else:
                    self.texture_view.tint.z = 0.5

        self.texture_view.mouse_event += on_event

        from pydear.utils.loghandler import ImGuiLogHandler
        log_handler = ImGuiLogHandler()
        log_handler.register_root(append=True)

        self.docks = [
            dockspace.Dock('demo', ImGui.ShowDemoWindow,
                           (ctypes.c_bool * 1)(True)),
            dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                           (ctypes.c_bool * 1)(True)),
            dockspace.Dock('view', self.texture_view.show,
                           (ctypes.c_bool * 1)(True)),
            dockspace.Dock('logger', log_handler.show,
                           (ctypes.c_bool * 1)(True)),
        ]

        super().__init__(loop, docks=self.docks)


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('fbo')
    gui = GUI(app.loop)

    from pydear.backends import impl_glfw
    impl_glfw = impl_glfw.ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    del gui


if __name__ == '__main__':
    main()
