from typing import Optional
import pathlib
from pydear.utils.selector import Item
from pydear import nanovg
from pydear.nanovg_backends import nanovg_impl_opengl3
from pydear.utils.mouse_event import MouseEvent

FONT = 'font_name'


def line_from_to(vg, x0, y0, x1, y1):
    nanovg.nvgSave(vg)
    nanovg.nvgStrokeWidth(vg, 1.0)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 192, 255, 255))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, x0, y0)
    nanovg.nvgLineTo(vg, x1, y1)
    nanovg.nvgStroke(vg)
    nanovg.nvgRestore(vg)


def text(vg, x, y):
    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, FONT)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 255))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x, y, f'{x}, {y}', None)  # type: ignore


class NanoVg(Item):
    def __init__(self, mouse_event: MouseEvent, font_path: pathlib.Path) -> None:
        super().__init__('nanovg')
        self.vg = nanovg.nvgCreate(nanovg.NVGcreateFlags.NVG_ANTIALIAS
                                   | nanovg.NVGcreateFlags.NVG_STENCIL_STROKES
                                   | nanovg.NVGcreateFlags.NVG_DEBUG)
        if not self.vg:
            raise RuntimeError("Could not init nanovg")
        nanovg_impl_opengl3.init(self.vg)
        assert font_path.exists()
        self.font_path = str(font_path.absolute()).replace('\\', '/')
        self.font_initialized = False

        # mouse
        self.begin = None
        self.mouse_event = mouse_event

        def on_middle_begin(x, y):
            self.begin = (x, y)
        self.mouse_event.middle_pressed += [on_middle_begin]

        def on_middle_end(x, y):
            self.begin = None
        self.mouse_event.middle_released += [on_middle_end]

    def init_font(self):
        '''
        must after nanovg.nvgBeginFrame
        '''
        if self.font_initialized:
            return
        self.fontNormal = nanovg.nvgCreateFont(
            self.vg, FONT, self.font_path)
        if self.fontNormal == -1:
            raise RuntimeError("Could not add font italic.")
        self.font_initialized = True

    def __del__(self):
        nanovg_impl_opengl3.delete()

    def render(self, width, height):

        width = float(width)
        height = float(height)
        if width == 0 or height == 0:
            return
        ratio = width / height
        nanovg.nvgBeginFrame(self.vg, width, height, ratio)
        self.init_font()

        input = self.mouse_event.last_input
        assert(input)

        nanovg.nvgBeginPath(self.vg)
        nanovg.nvgRoundedRect(self.vg, 0, 0, 0, 0,0)
        nanovg.nvgFill(self.vg)

        text(self.vg, input.x, input.y)
        if self.begin:
            text(self.vg, self.begin[0], self.begin[1])
            line_from_to(self.vg, self.begin[0],
                         self.begin[1], input.x, input.y)

        nanovg_impl_opengl3.render(nanovg.nvgGetDrawData(self.vg))

    def show(self):
        pass
