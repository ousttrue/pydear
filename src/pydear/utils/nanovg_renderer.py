import pathlib
import contextlib
from pydear import nanovg
from pydear.nanovg_backends import nanovg_impl_opengl3


class NanoVgRenderer:
    def __init__(self, font_path: pathlib.Path, font_name='nanovg_font') -> None:
        self.vg = nanovg.nvgCreate(nanovg.NVGcreateFlags.NVG_ANTIALIAS
                                   | nanovg.NVGcreateFlags.NVG_STENCIL_STROKES
                                   | nanovg.NVGcreateFlags.NVG_DEBUG)
        if not self.vg:
            raise RuntimeError("Could not init nanovg")
        nanovg_impl_opengl3.init(self.vg)

        assert font_path.exists()
        self.font_path = str(font_path.absolute()).replace('\\', '/')
        self.font_initialized = False
        self.font_name = font_name

    def init_font(self):
        '''
        must after nanovg.nvgBeginFrame
        '''
        if self.font_initialized:
            return
        self.fontNormal = nanovg.nvgCreateFont(
            self.vg, self.font_name, self.font_path)
        if self.fontNormal == -1:
            raise RuntimeError("Could not add font italic.")
        self.font_initialized = True

    def __del__(self):
        nanovg_impl_opengl3.delete()

    def begin_frame(self, width, height):
        width = float(width)
        height = float(height)
        if width == 0 or height == 0:
            return
        ratio = width / height
        nanovg.nvgBeginFrame(self.vg, width, height, ratio)
        self.init_font()
        return self.vg

    def end_frame(self):
        nanovg_impl_opengl3.render(nanovg.nvgGetDrawData(self.vg))

    @contextlib.contextmanager
    def render(self, w, h):
        vg = self.begin_frame(w, h)
        try:
            if vg:
                yield vg
        finally:
            self.end_frame()


def nvg_line_from_to(vg, x0, y0, x1, y1):
    nanovg.nvgSave(vg)
    nanovg.nvgStrokeWidth(vg, 1.0)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 192, 255, 255))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, x0, y0)
    nanovg.nvgLineTo(vg, x1, y1)
    nanovg.nvgStroke(vg)
    nanovg.nvgRestore(vg)


def nvg_text(vg, font_name, x, y):
    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, font_name)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 255))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x, y, f'{x}, {y}', None)  # type: ignore
