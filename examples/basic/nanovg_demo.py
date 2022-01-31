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
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(32, 32, 32, 255))
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
    _text = "This is longer chunk of text.\n  \n  Would have used lorem ipsum but she    was busy jumping over the lazy dog with the fox and all the men who came to the aid of the party.🎉"
    # text = ctypes.create_string_buffer(_text, len(_text))
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
    # nanovg.NVG_NOTUSED(height);

    nanovg.nvgSave(vg)

    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_TOP)
    nanovg.nvgTextMetrics(vg, None, None, lineh)

    # The text break API can be used to fill a large buffer of rows,
    # or to iterate over the text just few lines (or just one) at a time.
    # The "next" variable of the last returned item tells where to continue.
    start = _text
    end = _text[:len(_text)]
    while True:
        nrows = nanovg.nvgTextBreakLines(vg, start, end, width, rows, 3)
        if not nrows:
            break
        # for (i=0
        #      i < nrows
        #      i++) {
        #     NVGtextRow * row = &rows[i]
        #     int hit = mx > x & & mx < (x+width) & & my >= y & & my < (y+lineh)

        #     nanovg.nvgBeginPath(vg)
        #     nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, hit?64: 16))
        #     nanovg.nvgRect(vg, x + row -> minx, y, row -> maxx - row -> minx, lineh)
        #     nanovg.nvgFill(vg)

        #     nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 255))
        #     nanovg.nvgText(vg, x, y, row -> start, row -> end)

        #     if (hit) {
        #         caretx = (mx < x+row -> width/2) ? x: x+row -> width
        #         px = x
        #         nglyphs = nanovg.nvgTextGlyphPositions(vg, x, y, row -> start, row -> end, glyphs, 100)
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
        #         nanovg.nvgBeginPath(vg)
        #         nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 192, 0, 255))
        #         nanovg.nvgRect(vg, caretx, y, 1, lineh)
        #         nanovg.nvgFill(vg)

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
    # 	nanovg.nvgFontSize(vg, 12.0f);
    # 	nanovg.nvgTextAlign(vg, NVG_ALIGN_RIGHT|NVG_ALIGN_MIDDLE);

    # 	nanovg.nvgTextBounds(vg, gx,gy, txt, NULL, bounds);

    # 	nanovg.nvgBeginPath(vg);
    # 	nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255,192,0,255));
    # 	nanovg.nvgRoundedRect(vg, (int)bounds[0]-4,(int)bounds[1]-2, (int)(bounds[2]-bounds[0])+8, (int)(bounds[3]-bounds[1])+4, ((int)(bounds[3]-bounds[1])+4)/2-1);
    # 	nanovg.nvgFill(vg);

    # 	nanovg.nvgFillColor(vg, nanovg.nvgRGBA(32,32,32,255));
    # 	nanovg.nvgText(vg, gx,gy, txt, NULL);
    # }

    # y += 20.0f;

    # nanovg.nvgFontSize(vg, 11.0f);
    # nanovg.nvgTextAlign(vg, NVG_ALIGN_LEFT|NVG_ALIGN_TOP);
    # nanovg.nvgTextLineHeight(vg, 1.2f);

    # nanovg.nvgTextBoxBounds(vg, x,y, 150, hoverText, NULL, bounds);

    # // Fade the tooltip out when close to it.
    # gx = clampf(mx, bounds[0], bounds[2]) - mx;
    # gy = clampf(my, bounds[1], bounds[3]) - my;
    # a = sqrtf(gx*gx + gy*gy) / 30.0f;
    # a = clampf(a, 0, 1);
    # nanovg.nvgGlobalAlpha(vg, a);

    # nanovg.nvgBeginPath(vg);
    # nanovg.nvgFillColor(vg, nanovg.nvgRGBA(220,220,220,255));
    # nanovg.nvgRoundedRect(vg, bounds[0]-2,bounds[1]-2, (int)(bounds[2]-bounds[0])+4, (int)(bounds[3]-bounds[1])+4, 3);
    # px = (int)((bounds[2]+bounds[0])/2);
    # nanovg.nvgMoveTo(vg, px,bounds[1] - 10);
    # nanovg.nvgLineTo(vg, px+7,bounds[1]+1);
    # nanovg.nvgLineTo(vg, px-7,bounds[1]+1);
    # nanovg.nvgFill(vg);

    # nanovg.nvgFillColor(vg, nanovg.nvgRGBA(0,0,0,220));
    # nanovg.nvgTextBox(vg, x,y, 150, hoverText, NULL);

    nanovg.nvgRestore(vg)


def drawGraph(vg, x, y, w, h, t):

    samples = []
    sx = (ctypes.c_float * 6)()
    sy = (ctypes.c_float * 6)()
    dx = w/5.0

    samples.append((1+math.sin(t*1.2345+math.cos(t*0.33457)*0.44))*0.5)
    samples.append((1+math.sin(t*0.68363+math.cos(t*1.3)*1.55))*0.5)
    samples.append((1+math.sin(t*1.1642+math.cos(t*0.33457)*1.24))*0.5)
    samples.append((1+math.sin(t*0.56345+math.cos(t*1.63)*0.14))*0.5)
    samples.append((1+math.sin(t*1.6245+math.cos(t*0.254)*0.3))*0.5)
    samples.append((1+math.sin(t*0.345+math.cos(t*0.03)*0.6))*0.5)

    for i in range(6):
        sx[i] = x+i*dx
        sy[i] = y+h*samples[i]*0.8

    # Graph background
    bg = nanovg.nvgLinearGradient(
        vg, x, y, x, y+h, nanovg.nvgRGBA(0, 160, 192, 0), nanovg.nvgRGBA(0, 160, 192, 64))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, sx[0], sy[0])
    for i in range(1, 6):
        nanovg.nvgBezierTo(vg, sx[i-1]+dx*0.5, sy[i-1],
                           sx[i]-dx*0.5, sy[i], sx[i], sy[i])
    nanovg.nvgLineTo(vg, x+w, y+h)
    nanovg.nvgLineTo(vg, x, y+h)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    # Graph line
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, sx[0], sy[0]+2)
    for i in range(1, 6):
        nanovg.nvgBezierTo(vg, sx[i-1]+dx*0.5, sy[i-1]+2,
                           sx[i]-dx*0.5, sy[i]+2, sx[i], sy[i]+2)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 32))
    nanovg.nvgStrokeWidth(vg, 3.0)
    nanovg.nvgStroke(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, sx[0], sy[0])
    for i in range(1, 6):
        nanovg.nvgBezierTo(vg, sx[i-1]+dx*0.5, sy[i-1],
                           sx[i]-dx*0.5, sy[i], sx[i], sy[i])
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 160, 192, 255))
    nanovg.nvgStrokeWidth(vg, 3.0)
    nanovg.nvgStroke(vg)

    # Graph sample pos
    for i in range(6):
        bg = nanovg.nvgRadialGradient(
            vg, sx[i], sy[i]+2, 3.0, 8.0, nanovg.nvgRGBA(0, 0, 0, 32), nanovg.nvgRGBA(0, 0, 0, 0))
        nanovg.nvgBeginPath(vg)
        nanovg.nvgRect(vg, sx[i]-10, sy[i]-10+2, 20, 20)
        nanovg.nvgFillPaint(vg, bg)
        nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    for i in range(6):
        nanovg.nvgCircle(vg, sx[i], sy[i], 4.0)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(0, 160, 192, 255))
    nanovg.nvgFill(vg)
    nanovg.nvgBeginPath(vg)
    for i in range(6):
        nanovg.nvgCircle(vg, sx[i], sy[i], 2.0)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(220, 220, 220, 255))
    nanovg.nvgFill(vg)

    nanovg.nvgStrokeWidth(vg, 1.01)


def drawColorwheel(vg, x, y, w, h, t):
    hue = math.sin(t * 0.12)

    nanovg.nvgSave(vg)

    cx = x + w*0.5
    cy = y + h*0.5
    r1 = (w if w < h else h) * 0.5 - 5.0
    r0 = r1 - 20.0
    aeps = 0.5 / r1  # half a pixel arc length in radians (2pi cancels out).

    for i in range(6):
        a0 = float(i / 6.0 * math.pi * 2.0 - aeps)
        a1 = float((i+1.0) / 6.0 * math.pi * 2.0 + aeps)
        nanovg.nvgBeginPath(vg)
        nanovg.nvgArc(vg, cx, cy, r0, a0, a1, nanovg.NVGwinding.NVG_CW)
        nanovg.nvgArc(vg, cx, cy, r1, a1, a0, nanovg.NVGwinding.NVG_CCW)
        nanovg.nvgClosePath(vg)
        ax = cx + math.cos(a0) * (r0+r1)*0.5
        ay = cy + math.sin(a0) * (r0+r1)*0.5
        bx = cx + math.cos(a1) * (r0+r1)*0.5
        by = cy + math.sin(a1) * (r0+r1)*0.5
        paint = nanovg.nvgLinearGradient(vg, ax, ay, bx, by, nanovg.nvgHSLA(
            a0/(math.pi*2), 1.0, 0.55, 255), nanovg.nvgHSLA(a1/(math.pi*2), 1.0, 0.55, 255))
        nanovg.nvgFillPaint(vg, paint)
        nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgCircle(vg, cx, cy, r0-0.5)
    nanovg.nvgCircle(vg, cx, cy, r1+0.5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 64))
    nanovg.nvgStrokeWidth(vg, 1.0)
    nanovg.nvgStroke(vg)

    # Selector
    nanovg.nvgSave(vg)
    nanovg.nvgTranslate(vg, cx, cy)
    nanovg.nvgRotate(vg, hue*math.pi*2)

    # Marker on
    nanovg.nvgStrokeWidth(vg, 2.0)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, r0-1, -3, r1-r0+2, 6)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(255, 255, 255, 192))
    nanovg.nvgStroke(vg)

    paint = nanovg.nvgBoxGradient(
        vg, r0-3, -5, r1-r0+6, 10, 2, 4, nanovg.nvgRGBA(0, 0, 0, 128), nanovg.nvgRGBA(0, 0, 0, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, r0-2-10, -4-10, r1-r0+4+20, 8+20)
    nanovg.nvgRect(vg, r0-2, -4, r1-r0+4, 8)
    nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
    nanovg.nvgFillPaint(vg, paint)
    nanovg.nvgFill(vg)

    # Center triangle
    r = r0 - 6
    ax = math.cos(120.0/180.0*math.pi) * r
    ay = math.sin(120.0/180.0*math.pi) * r
    bx = math.cos(-120.0/180.0*math.pi) * r
    by = math.sin(-120.0/180.0*math.pi) * r
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, r, 0)
    nanovg.nvgLineTo(vg, ax, ay)
    nanovg.nvgLineTo(vg, bx, by)
    nanovg.nvgClosePath(vg)
    paint = nanovg.nvgLinearGradient(vg, r, 0, ax, ay, nanovg.nvgHSLA(
        hue, 1.0, 0.5, 255), nanovg.nvgRGBA(255, 255, 255, 255))
    nanovg.nvgFillPaint(vg, paint)
    nanovg.nvgFill(vg)
    paint = nanovg.nvgLinearGradient(
        vg, (r+ax)*0.5, (0+ay)*0.5, bx, by, nanovg.nvgRGBA(0, 0, 0, 0), nanovg.nvgRGBA(0, 0, 0, 255))
    nanovg.nvgFillPaint(vg, paint)
    nanovg.nvgFill(vg)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 64))
    nanovg.nvgStroke(vg)

    # Select circle on triangle
    ax = math.cos(120.0/180.0*math.pi) * r*0.3
    ay = math.sin(120.0/180.0*math.pi) * r*0.4
    nanovg.nvgStrokeWidth(vg, 2.0)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgCircle(vg, ax, ay, 5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(255, 255, 255, 192))
    nanovg.nvgStroke(vg)

    paint = nanovg.nvgRadialGradient(vg, ax, ay, 7, 9, nanovg.nvgRGBA(
        0, 0, 0, 64), nanovg.nvgRGBA(0, 0, 0, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, ax-20, ay-20, 40, 40)
    nanovg.nvgCircle(vg, ax, ay, 7)
    nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
    nanovg.nvgFillPaint(vg, paint)
    nanovg.nvgFill(vg)

    nanovg.nvgRestore(vg)

    nanovg.nvgRestore(vg)


def drawLines(vg, x, y, w, h, t):

    # int i, j;
    pad = 5.0
    s = w/9.0 - pad*2
    # float pts[4*2], fx, fy;
    joins = [nanovg.NVGlineCap.NVG_MITER,
             nanovg.NVGlineCap.NVG_ROUND, nanovg.NVGlineCap.NVG_BEVEL]
    caps = [nanovg.NVGlineCap.NVG_BUTT,
            nanovg.NVGlineCap.NVG_ROUND, nanovg.NVGlineCap.NVG_SQUARE]

    nanovg.nvgSave(vg)
    pts = []
    pts.append(-s*0.25 + math.cos(t*0.3) * s*0.5)
    pts.append(math.sin(t*0.3) * s*0.5)
    pts.append(-s*0.25)
    pts.append(0)
    pts.append(s*0.25)
    pts.append(0)
    pts.append(s*0.25 + math.cos(-t*0.3) * s*0.5)
    pts.append(math.sin(-t*0.3) * s*0.5)

    for i in range(3):
        for j in range(3):
            fx = x + s*0.5 + (i*3+j)/9.0*w + pad
            fy = y - s*0.5 + pad

            nanovg.nvgLineCap(vg, caps[i])
            nanovg.nvgLineJoin(vg, joins[j])

            nanovg.nvgStrokeWidth(vg, s*0.3)
            nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 160))
            nanovg.nvgBeginPath(vg)
            nanovg.nvgMoveTo(vg, fx+pts[0], fy+pts[1])
            nanovg.nvgLineTo(vg, fx+pts[2], fy+pts[3])
            nanovg.nvgLineTo(vg, fx+pts[4], fy+pts[5])
            nanovg.nvgLineTo(vg, fx+pts[6], fy+pts[7])
            nanovg.nvgStroke(vg)

            nanovg.nvgLineCap(vg, nanovg.NVGlineCap.NVG_BUTT)
            nanovg.nvgLineJoin(vg, nanovg.NVGlineCap.NVG_BEVEL)

            nanovg.nvgStrokeWidth(vg, 1.0)
            nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 192, 255, 255))
            nanovg.nvgBeginPath(vg)
            nanovg.nvgMoveTo(vg, fx+pts[0], fy+pts[1])
            nanovg.nvgLineTo(vg, fx+pts[2], fy+pts[3])
            nanovg.nvgLineTo(vg, fx+pts[4], fy+pts[5])
            nanovg.nvgLineTo(vg, fx+pts[6], fy+pts[7])
            nanovg.nvgStroke(vg)

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
        nanovg.nvgBeginFrame(self.vg, width, height, ratio)

        drawEyes(self.vg, width - 250, 50, 150, 100, mx, my, t)
        drawParagraph(self.vg, width - 450, 50, 150, 100, mx, my)
        drawGraph(self.vg, 0, height/2, width, height/2, t)
        drawColorwheel(self.vg, width - 300, height - 300, 250.0, 250.0, t)

        # Line joints
        drawLines(self.vg, 120, height-50, 600, 50, t)

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
