
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

            # font load
            # https://github.com/ryanoasis/nerd-fonts/wiki/Glyph-Sets-and-Code-Points
            range = []

            def push_range(*values):
                match values:
                    case (value,):
                        range.append(value)
                        range.append(value)
                    case (v0, v1):
                        range.append(v0)
                        range.append(v1)
                    case _:
                        raise NotImplementedError()
            push_range(0x23fb, 0x23fe)  # IEC Power Symbols
            push_range(0x2665)  # Octicons
            push_range(0x26a1)  # Octicons
            push_range(0x2b58)  # IEC Power Symbols
            push_range(0xe000, 0xe00a)  # Pomicons
            push_range(0xe0a0, 0xe0a2)  # Powerline
            push_range(0xe0a3)  # Powerline Extra
            push_range(0xe0b0, 0xe0b3)  # Powerline
            push_range(0xe0b4, 0xe0c8)  # Powerline Extra
            push_range(0xe0b4, 0xe0c8)  # Powerline Extrax
            push_range(0xe0cc, 0xe0d4)  # Powerline Extra
            push_range(0xe200, 0xe2a9)  # Font Awesome Extension
            push_range(0xe300, 0xe3eb)  # Weather Icons
            push_range(0xe5fa, 0xe631)  # Seti-UI + Custom
            push_range(0xe700, 0xe7c5)  # Devicons
            push_range(0xea60, 0xebeb)  # Codicons
            push_range(0xf000, 0xf2e0)  # Font Awesome
            push_range(0xf300, 0xf32d)  # Font Logos
            push_range(0xf400, 0xf4a8)  # Octicons
            push_range(0xf4a9)  # Octicons
            push_range(0xf500, 0xfd46)  # Material Design

            from pydear.utils import fontloader
            font_range = (ctypes.c_ushort * (len(range)+1))(*range, 0)
            fontloader.load(self.nerdfont_path, 13,
                            font_range, merge=True, monospace=True)

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
