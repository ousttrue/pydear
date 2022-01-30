import pathlib
import math
from pydear import nanovg
from pydear import nanovg_gl
from pydear import glew

HERE = pathlib.Path(__file__).absolute().parent
NVG_DIR = HERE.parent.parent / '_external/nanovg'


def drawEyes(vg, x, y, w, h, mx, my, t):

    ex = w * 0.23
    ey = h * 0.5
    lx = x + ex
    ly = y + ey
    rx = x + w - ex
    ry = y + ey
    br = (ex if ex < ey else ey) * 0.5
    blink = 1 - pow(math.sin(t*0.5), 200)*0.8

    bg = nanovg.nvgLinearGradient(
        vg, x, y+h*0.5, x+w*0.1, y+h, nanovg.nvgRGBA(0, 0, 0, 32), nanovg.nvgRGBA(0, 0, 0, 16))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, lx+3.0, ly+16.0, ex, ey)
    nanovg.nvgEllipse(vg, rx+3.0, ry+16.0, ex, ey)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    bg = nanovg.nvgLinearGradient(vg, x, y+h*0.25, x+w*0.1, y+h, nanovg.nvgRGBA(
        220, 220, 220, 255), nanovg.nvgRGBA(128, 128, 128, 255))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, lx, ly, ex, ey)
    nanovg.nvgEllipse(vg, rx, ry, ex, ey)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    dx = (mx - rx) / (ex * 10)
    dy = (my - ry) / (ey * 10)
    d = math.sqrt(dx*dx+dy*dy)
    if d > 1.0:
        dx /= d
        dy /= d
    dx *= ex*0.4
    dy *= ey*0.5
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, lx+dx, ly+dy+ey*0.25*(1-blink), br, br*blink)
    nanovg.nvgFillColor(vg, nanovg. nvgRGBA(32, 32, 32, 255))
    nanovg.nvgFill(vg)

    dx = (mx - rx) / (ex * 10)
    dy = (my - ry) / (ey * 10)
    d = math.sqrt(dx*dx+dy*dy)
    if d > 1.0:
        dx /= d
        dy /= d
    dx *= ex*0.4
    dy *= ey*0.5
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, rx+dx, ry+dy+ey*0.25*(1-blink), br, br*blink)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(32, 32, 32, 255))
    nanovg.nvgFill(vg)

    gloss = nanovg.nvgRadialGradient(vg, lx-ex*0.25, ly-ey*0.5, ex*0.1, ex*0.75,
                                     nanovg.nvgRGBA(255, 255, 255, 128), nanovg.nvgRGBA(255, 255, 255, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, lx, ly, ex, ey)
    nanovg.nvgFillPaint(vg, gloss)
    nanovg.nvgFill(vg)

    gloss = nanovg.nvgRadialGradient(vg, rx-ex*0.25, ry-ey*0.5, ex*0.1, ex*0.75,
                                     nanovg.nvgRGBA(255, 255, 255, 128), nanovg.nvgRGBA(255, 255, 255, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgEllipse(vg, rx, ry, ex, ey)
    nanovg.nvgFillPaint(vg, gloss)
    nanovg.nvgFill(vg)


class Demo:
    def __init__(self) -> None:
        glew.glewInit()
        self.vg = nanovg_gl.nvgCreateGL3(
            nanovg_gl.NVGcreateFlags.NVG_ANTIALIAS
            | nanovg_gl.NVGcreateFlags.NVG_STENCIL_STROKES
            | nanovg_gl.NVGcreateFlags.NVG_DEBUG)
        if not self.vg:
            raise RuntimeError("Could not init nanovg")

        # data
        self.images = []
        self.load_data()

    def __del__(self):
        nanovg_gl.nvgDeleteGL3_2(self.vg)

    def load_data(self):
        for i in range(12):
            file = NVG_DIR / f"example/images/image{i+1}.jpg"
            assert(file.exists())
            self.images.append(nanovg.nvgCreateImage(self.vg, str(file), 0))
            if not self.images[-1]:
                raise RuntimeError("Could not load %s.\n", file)

        self.fontIcons = nanovg.nvgCreateFont(
            self.vg, "icons", str(NVG_DIR / "example/entypo.ttf"))
        if self.fontIcons == -1:
            raise RuntimeError("Could not add font icons.")

        self.fontNormal = nanovg.nvgCreateFont(
            self.vg, "sans", str(NVG_DIR / "example/Roboto-Regular.ttf"))
        if self.fontNormal == -1:
            raise RuntimeError("Could not add font italic.")

        self.fontBold = nanovg.nvgCreateFont(
            self.vg, "sans-bold", str(NVG_DIR / "example/Roboto-Bold.ttf"))
        if self.fontBold == -1:
            raise RuntimeError("Could not add font bold.")

        self.fontEmoji = nanovg.nvgCreateFont(
            self.vg, "emoji", str(NVG_DIR/"example/NotoEmoji-Regular.ttf"))
        if self.fontEmoji == -1:
            raise RuntimeError("Could not add font emoji.")

        nanovg.nvgAddFallbackFontId(self.vg, self.fontNormal, self.fontEmoji)
        nanovg.nvgAddFallbackFontId(self.vg, self.fontBold, self.fontEmoji)

    def render(self, mx, my, width, height, t):
        width = float(width)
        height = float(height)
        ratio = width / height

        drawEyes(self.vg, width - 250, 50, 150, 100, mx, my, t)

        nanovg.nvgBeginFrame(self.vg, width, height, ratio)
        # data.render(vg, mx.value, my.value, fb_width.value,
        #             fb_height.value, t, False)
        # fps.render(vg, 5, 5)

        # render(vg, x, y, w, h)

        nanovg.nvgEndFrame(self.vg)


def render(vg, x, y, w, h):
    w = float(w)
    h = float(h)
    cornerRadius = 4.0
    s = nanovg.nvgRGBA(255, 255, 255, 16)
    e = nanovg.nvgRGBA(0, 0, 0, 16)
    bg = nanovg.nvgLinearGradient(vg, x, y, x, y+h, s, e)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+1, w-2, h-2, cornerRadius-1)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)
