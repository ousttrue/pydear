import ctypes
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


def drawParagraph(vg, x, y, width, height, mx, my):

    rows = (nanovg.NVGtextRow * 3)()
    # NVGglyphPosition glyphs[100];
    _text = "This is longer chunk of text.\n  \n  Would have used lorem ipsum but she    was busy jumping over the lazy dog with the fox and all the men who came to the aid of the party.🎉".encode(
        'utf-8')
    text = ctypes.create_string_buffer(_text, len(_text))
    # const char* start;
    # const char* end;
    # int nrows, i, nglyphs, j, lnum = 0;
    lineh = (ctypes.c_float * 1)()
    # float caretx, px;
    # float bounds[4];
    # float a;
    # const char* hoverText = "Hover your mouse over the text to see calculated caret position.";
    # float gx,gy;
    # int gutter = 0;
    # const char* boxText = "Testing\nsome multiline\ntext.";
    # NVG_NOTUSED(height);

    nanovg.nvgSave(vg)

    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_TOP)
    nanovg.nvgTextMetrics(vg, None, None, lineh)

    # The text break API can be used to fill a large buffer of rows,
    # or to iterate over the text just few lines (or just one) at a time.
    # The "next" variable of the last returned item tells where to continue.
    start = ctypes.cast(text, ctypes.c_void_p)
    end = ctypes.c_void_p(start.value + len(_text))
    while True:
        nrows = nanovg.nvgTextBreakLines(vg, start, end, width, rows, 3)
        if not nrows:
            break
        # for (i=0
        #      i < nrows
        #      i++) {
        #     NVGtextRow * row = &rows[i]
        #     int hit = mx > x & & mx < (x+width) & & my >= y & & my < (y+lineh)

        #     nvgBeginPath(vg)
        #     nvgFillColor(vg, nvgRGBA(255, 255, 255, hit?64: 16))
        #     nvgRect(vg, x + row -> minx, y, row -> maxx - row -> minx, lineh)
        #     nvgFill(vg)

        #     nvgFillColor(vg, nvgRGBA(255, 255, 255, 255))
        #     nvgText(vg, x, y, row -> start, row -> end)

        #     if (hit) {
        #         caretx = (mx < x+row -> width/2) ? x: x+row -> width
        #         px = x
        #         nglyphs = nvgTextGlyphPositions(vg, x, y, row -> start, row -> end, glyphs, 100)
        #         for (j=0
        #              j < nglyphs
        #              j++) {
        #             float x0 = glyphs[j].x
        #             float x1 = (j+1 < nglyphs) ? glyphs[j+1].x: x+row -> width
        #             float gx = x0 * 0.3f + x1 * 0.7f
        #             if (mx >= px & & mx < gx)
        #             caretx = glyphs[j].x
        #             px = gx
        #         }
        #         nvgBeginPath(vg)
        #         nvgFillColor(vg, nvgRGBA(255, 192, 0, 255))
        #         nvgRect(vg, caretx, y, 1, lineh)
        #         nvgFill(vg)

        #         gutter = lnum+1
        #         gx = x - 10
        #         gy = y + lineh/2
        #     }
        #     lnum++
        #     y += lineh
        # }
        # Keep going...
        start = rows[nrows-1].next

    # if (gutter) {
    # 	char txt[16];
    # 	snprintf(txt, sizeof(txt), "%d", gutter);
    # 	nvgFontSize(vg, 12.0f);
    # 	nvgTextAlign(vg, NVG_ALIGN_RIGHT|NVG_ALIGN_MIDDLE);

    # 	nvgTextBounds(vg, gx,gy, txt, NULL, bounds);

    # 	nvgBeginPath(vg);
    # 	nvgFillColor(vg, nvgRGBA(255,192,0,255));
    # 	nvgRoundedRect(vg, (int)bounds[0]-4,(int)bounds[1]-2, (int)(bounds[2]-bounds[0])+8, (int)(bounds[3]-bounds[1])+4, ((int)(bounds[3]-bounds[1])+4)/2-1);
    # 	nvgFill(vg);

    # 	nvgFillColor(vg, nvgRGBA(32,32,32,255));
    # 	nvgText(vg, gx,gy, txt, NULL);
    # }

    # y += 20.0f;

    # nvgFontSize(vg, 11.0f);
    # nvgTextAlign(vg, NVG_ALIGN_LEFT|NVG_ALIGN_TOP);
    # nvgTextLineHeight(vg, 1.2f);

    # nvgTextBoxBounds(vg, x,y, 150, hoverText, NULL, bounds);

    # // Fade the tooltip out when close to it.
    # gx = clampf(mx, bounds[0], bounds[2]) - mx;
    # gy = clampf(my, bounds[1], bounds[3]) - my;
    # a = sqrtf(gx*gx + gy*gy) / 30.0f;
    # a = clampf(a, 0, 1);
    # nvgGlobalAlpha(vg, a);

    # nvgBeginPath(vg);
    # nvgFillColor(vg, nvgRGBA(220,220,220,255));
    # nvgRoundedRect(vg, bounds[0]-2,bounds[1]-2, (int)(bounds[2]-bounds[0])+4, (int)(bounds[3]-bounds[1])+4, 3);
    # px = (int)((bounds[2]+bounds[0])/2);
    # nvgMoveTo(vg, px,bounds[1] - 10);
    # nvgLineTo(vg, px+7,bounds[1]+1);
    # nvgLineTo(vg, px-7,bounds[1]+1);
    # nvgFill(vg);

    # nvgFillColor(vg, nvgRGBA(0,0,0,220));
    # nvgTextBox(vg, x,y, 150, hoverText, NULL);

    nanovg.nvgRestore(vg)


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
        drawParagraph(self.vg, width - 450, 50, 150, 100, mx, my)

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
