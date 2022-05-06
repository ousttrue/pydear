
from typing import Optional
import pathlib
import argparse
import ctypes
import logging
import asyncio
from pydear.utils import gui_app
from pydear import imgui as ImGui
LOGGER = logging.getLogger(__name__)
HERE = pathlib.Path('__file__').absolute().parent


class FontLoad(gui_app.Gui):
    def __init__(self, loop: asyncio.AbstractEventLoop, nerdfont_path: Optional[pathlib.Path]) -> None:
        self.nerdfont_path = nerdfont_path
        super().__init__(loop, widgets=self.hello)

    def _setup_font(self):
        io = ImGui.GetIO()
        io.Fonts.AddFontDefault()

        if self.nerdfont_path and self.nerdfont_path.exists():

            from pydear.utils import nerdfont
            self.nerdfont_range = nerdfont.create_font_range()

            from pydear.utils import fontloader
            fontloader.load(self.nerdfont_path, 13,
                            self.nerdfont_range, merge=True, monospace=True)

        io.Fonts.Build()

    def hello(self):
        '''
        imgui widgets
        '''
        ImGui.ShowDemoWindow()

        ImGui.ShowMetricsWindow()

        if ImGui.Begin('hello'):
            ImGui.TextUnformatted('hello nerdfont')
            text = ''
            for i, cp in enumerate(range(0xe300, 0xe3eb+1)):
                if i and i % 10 == 0:
                    ImGui.TextUnformatted(text)
                    text = ''
                else:
                    text += chr(cp)
            ImGui.TextUnformatted(text)
        ImGui.End()


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('--nerdfont', type=pathlib.Path)
    args = parser.parse_args()

    #
    # glfw app
    #
    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('hello')

    #
    # imgui
    #
    gui = FontLoad(app.loop, args.nerdfont)

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
