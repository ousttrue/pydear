from typing import Optional
import pathlib
from pydear import nanovg
from pydear.utils.mouse_event import MouseEvent
from pydear.utils.selector import Item
from pydear.utils.nanovg_renderer import NanoVgRenderer


def line_from_to(vg, x0, y0, x1, y1):
    nanovg.nvgSave(vg)
    nanovg.nvgStrokeWidth(vg, 1.0)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 192, 255, 255))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, x0, y0)
    nanovg.nvgLineTo(vg, x1, y1)
    nanovg.nvgStroke(vg)
    nanovg.nvgRestore(vg)


def text(vg, font_name, x, y):
    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, font_name)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 255))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x, y, f'{x}, {y}', None)  # type: ignore


class NanoVgSample(Item):
    def __init__(self, font_path: pathlib.Path, mouse_event: MouseEvent) -> None:
        super().__init__('nanovg')

        self.nvg = NanoVgRenderer(font_path)

        # mouse
        self.begin = None
        self.mouse_event = mouse_event

        def on_left_begin(x, y):
            self.begin = (x, y)
        self.mouse_event.left_pressed += [on_left_begin]

        def on_left_end(x, y):
            self.begin = None
        self.mouse_event.left_released += [on_left_end]

    def render(self, w: int, h: int):
        input = self.mouse_event.last_input
        assert(input)

        vg = self.nvg.begin_frame(w, h)
        if not vg:
            return

        nanovg.nvgBeginPath(vg)
        nanovg.nvgRoundedRect(vg, 0, 0, 0, 0, 0)
        nanovg.nvgFill(vg)

        text(vg, self.nvg.font_name, input.x, input.y)
        if self.begin:
            text(vg, self.nvg.font_name, self.begin[0], self.begin[1])
            line_from_to(vg, self.begin[0],
                         self.begin[1], input.x, input.y)

        self.nvg.end_frame()

    def show(self):
        pass
