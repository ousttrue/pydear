import ctypes
import pathlib
import math
from pydear import nanovg


HERE = pathlib.Path(__file__).absolute().parent
NVG_DIR = HERE.parent.parent / '_external/nanovg'
# ICON_SEARCH = '\u1F50D'
ICON_CIRCLED_CROSS = '\u2716'
ICON_CHEVRON_RIGHT = '\uE75E'
ICON_CHECK = '\u2713'
ICON_LOGIN = '\uE740'
ICON_TRASH = '\uE729'


def clamp(my_value, min_value, max_value):
    return max(min(my_value, max_value), min_value)


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
    glyphs = (nanovg.NVGglyphPosition * 100)()
    _text = "This is longer chunk of text.\n  \n  Would have used lorem ipsum but she    was busy jumping over the lazy dog with the fox and all the men who came to the aid of the party.🎉".encode(
        'utf-8')
    text = ctypes.create_string_buffer(_text, len(_text))
    # const char* start;
    # const char* end;
    # int nrows, i, nglyphs, j
    lnum = 0
    lineh = (ctypes.c_float * 1)()
    # float caretx, px;
    bounds = (ctypes.c_float * 4)()
    # float a;
    hoverText = "Hover your mouse over the text to see calculated caret position."
    # float gx,gy;
    gutter = 0
    # const char* boxText = "Testing\nsome multiline\ntext.";
    # nanovg.NVG_NOTUSED(height);

    nanovg.nvgSave(vg)

    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_TOP)
    nanovg.nvgTextMetrics(vg, None, None, lineh)  # type: ignore

    # The text break API can be used to fill a large buffer of rows,
    # or to iterate over the text just few lines (or just one) at a time.
    # The "next" variable of the last returned item tells where to continue.
    start = text
    end = ctypes.c_void_p(
        ctypes.cast(start, ctypes.c_void_p).value + len(text))  # type: ignore
    while True:
        nrows = nanovg.nvgTextBreakLines(
            vg, start, end, width, rows, 3)  # type: ignore
        if not nrows:
            break
        for i in range(nrows):
            row = rows[i]
            hit = mx > x and mx < (x+width) and my >= y and my < (y+lineh[0])

            nanovg.nvgBeginPath(vg)
            nanovg.nvgFillColor(vg, nanovg.nvgRGBA(
                255, 255, 255, 64 if hit else 16))
            nanovg.nvgRect(vg, x + row.minx, y, row.maxx - row.minx, lineh[0])
            nanovg.nvgFill(vg)

            nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 255))
            row_str = ctypes.string_at(row.start, row.end-row.start)
            nanovg.nvgText(vg, x, y, row_str, None)  # type: ignore

            if hit:
                caretx = x if(mx < x+row.width/2) else x+row.width
                px = x
                nglyphs = nanovg.nvgTextGlyphPositions(
                    vg, x, y, row_str, None, glyphs, 100)  # type: ignore
                for j in range(nglyphs):
                    x0 = glyphs[j].x
                    x1 = glyphs[j+1].x if (j+1 < nglyphs) else x+row.width
                    gx = x0 * 0.3 + x1 * 0.7
                    if mx >= px and mx < gx:
                        caretx = glyphs[j].x
                        px = gx
                nanovg.nvgBeginPath(vg)
                nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 192, 0, 255))
                nanovg.nvgRect(vg, caretx, y, 1, lineh[0])
                nanovg.nvgFill(vg)

                gutter = lnum+1
                gx = x - 10
                gy = y + lineh[0]/2
            lnum += 1
            y += lineh[0]

        # Keep going...
        start = ctypes.c_void_p(rows[nrows-1].next)

    if gutter:
        txt = f'{gutter}'
        nanovg.nvgFontSize(vg, 12.0)
        nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_RIGHT |
                            nanovg.NVGalign. NVG_ALIGN_MIDDLE)

        nanovg.nvgTextBounds(vg, gx, gy, txt, None, bounds)  # type: ignore

        nanovg.nvgBeginPath(vg)
        nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 192, 0, 255))
        nanovg.nvgRoundedRect(
            vg,
            int(bounds[0]-4),
            int(bounds[1]-2),
            int((bounds[2]-bounds[0])+8),
            int((bounds[3]-bounds[1])+4),
            (int(bounds[3]-bounds[1])+4)/2-1)
        nanovg.nvgFill(vg)

        nanovg.nvgFillColor(vg, nanovg.nvgRGBA(32, 32, 32, 255))
        nanovg.nvgText(vg, gx, gy, txt, None)  # type: ignore

    y += 20.0

    nanovg.nvgFontSize(vg, 11.0)
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_TOP)
    nanovg.nvgTextLineHeight(vg, 1.2)

    nanovg.nvgTextBoxBounds(vg, x, y, 150, hoverText,
                            None, bounds)  # type: ignore

    # Fade the tooltip out when close to it.
    gx = clamp(mx, bounds[0], bounds[2]) - mx
    gy = clamp(my, bounds[1], bounds[3]) - my
    a = math.sqrt(gx*gx + gy*gy) / 30.0
    a = clamp(a, 0, 1)
    nanovg.nvgGlobalAlpha(vg, a)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(220, 220, 220, 255))
    nanovg.nvgRoundedRect(
        vg, bounds[0]-2, bounds[1]-2, int(bounds[2]-bounds[0])+4, int(bounds[3]-bounds[1])+4, 3)
    px = int((bounds[2]+bounds[0])/2)
    nanovg.nvgMoveTo(vg, px, bounds[1] - 10)
    nanovg.nvgLineTo(vg, px+7, bounds[1]+1)
    nanovg.nvgLineTo(vg, px-7, bounds[1]+1)
    nanovg.nvgFill(vg)

    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(0, 0, 0, 220))
    nanovg.nvgTextBox(vg, x, y, 150, hoverText, None)  # type: ignore

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


def drawWidths(vg, x, y, width):
    nanovg.nvgSave(vg)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 255))
    for i in range(20):
        w = (i+0.5)*0.1
        nanovg.nvgStrokeWidth(vg, w)
        nanovg.nvgBeginPath(vg)
        nanovg.nvgMoveTo(vg, x, y)
        nanovg.nvgLineTo(vg, x+width, y+width*0.3)
        nanovg.nvgStroke(vg)
        y += 10
    nanovg.nvgRestore(vg)


def drawCaps(vg, x, y, width):

    caps = [nanovg.NVGlineCap.NVG_BUTT,
            nanovg.NVGlineCap.NVG_ROUND, nanovg.NVGlineCap.NVG_SQUARE]
    lineWidth = 8.0

    nanovg.nvgSave(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x-lineWidth/2, y, width+lineWidth, 40)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 32))
    nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x, y, width, 40)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 32))
    nanovg.nvgFill(vg)

    nanovg.nvgStrokeWidth(vg, lineWidth)
    for i in range(3):
        nanovg.nvgLineCap(vg, caps[i])
        nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 255))
        nanovg.nvgBeginPath(vg)
        nanovg.nvgMoveTo(vg, x, y + i*10 + 5)
        nanovg.nvgLineTo(vg, x+width, y + i*10 + 5)
        nanovg.nvgStroke(vg)

    nanovg.nvgRestore(vg)


def drawScissor(vg, x, y, t):

    nanovg.nvgSave(vg)

    # Draw first rect and set scissor to it's area.
    nanovg.nvgTranslate(vg, x, y)
    nanovg.nvgRotate(vg, nanovg.nvgDegToRad(5))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, -20, -20, 60, 40)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 0, 0, 255))
    nanovg.nvgFill(vg)
    nanovg.nvgScissor(vg, -20, -20, 60, 40)

    # Draw second rectangle with offset and rotation.
    nanovg.nvgTranslate(vg, 40, 0)
    nanovg.nvgRotate(vg, t)

    # Draw the intended second rectangle without any scissoring.
    nanovg.nvgSave(vg)
    nanovg.nvgResetScissor(vg)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, -20, -10, 60, 30)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 128, 0, 64))
    nanovg.nvgFill(vg)
    nanovg.nvgRestore(vg)

    # Draw second rectangle with combined scissoring.
    nanovg.nvgIntersectScissor(vg, -20, -10, 60, 30)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, -20, -10, 60, 30)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 128, 0, 255))
    nanovg.nvgFill(vg)

    nanovg.nvgRestore(vg)


def drawWindow(vg, title, x, y, w, h):

    cornerRadius = 3.0

    nanovg.nvgSave(vg)

    # Window
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x, y, w, h, cornerRadius)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(28, 30, 34, 192))
    nanovg.nvgFill(vg)

    # Drop shadow
    shadowPaint = nanovg.nvgBoxGradient(
        vg, x, y+2, w, h, cornerRadius*2, 10, nanovg.nvgRGBA(0, 0, 0, 128), nanovg.nvgRGBA(0, 0, 0, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x-10, y-10, w+20, h+30)
    nanovg.nvgRoundedRect(vg, x, y, w, h, cornerRadius)
    nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
    nanovg.nvgFillPaint(vg, shadowPaint)
    nanovg.nvgFill(vg)

    # Header
    headerPaint = nanovg.nvgLinearGradient(
        vg, x, y, x, y+15, nanovg.nvgRGBA(255, 255, 255, 8), nanovg.nvgRGBA(0, 0, 0, 16))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+1, w-2, 30, cornerRadius-1)
    nanovg.nvgFillPaint(vg, headerPaint)
    nanovg.nvgFill(vg)
    nanovg.nvgBeginPath(vg)
    nanovg.nvgMoveTo(vg, x+0.5, y+0.5+30)
    nanovg.nvgLineTo(vg, x+0.5+w-1, y+0.5+30)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 32))
    nanovg.nvgStroke(vg)

    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans-bold")
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_CENTER |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)

    nanovg.nvgFontBlur(vg, 2)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(0, 0, 0, 128))
    nanovg.nvgText(vg, x+w/2, y+16+1, title, None)  # type: ignore

    nanovg.nvgFontBlur(vg, 0)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(220, 220, 220, 160))
    nanovg.nvgText(vg, x+w/2, y+16, title, None)  # type: ignore

    nanovg.nvgRestore(vg)


def drawSearchBox(vg, text, x, y, w, h):

    cornerRadius = h/2-1

    # Edit
    bg = nanovg.nvgBoxGradient(
        vg, x, y+1.5, w, h, h/2, 5, nanovg.nvgRGBA(0, 0, 0, 16), nanovg.nvgRGBA(0, 0, 0, 92))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x, y, w, h, cornerRadius)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    nanovg.nvgFontSize(vg, h*1.3)
    nanovg.nvgFontFace(vg, "icons")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 64))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_CENTER |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    # nanovg.nvgText(vg, x+h*0.55, y+h*0.55, cpToUTF8(ICON_SEARCH,icon), NULL);

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 32))

    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x+h*1.05, y+h*0.5, text, None)  # type: ignore

    nanovg.nvgFontSize(vg, h*1.3)
    nanovg.nvgFontFace(vg, "icons")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 32))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_CENTER |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    # nanovg.nvgText(vg, x+w-h*0.55f, y+h*0.55f, cpToUTF8(ICON_CIRCLED_CROSS,icon), NULL);


def drawDropDown(vg, text, x, y, w, h):
    # NVGpaint bg;
    # char icon[8];
    cornerRadius = 4.0

    bg = nanovg.nvgLinearGradient(
        vg, x, y, x, y+h, nanovg.nvgRGBA(255, 255, 255, 16), nanovg.nvgRGBA(0, 0, 0, 16))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+1, w-2, h-2, cornerRadius-1)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+0.5, y+0.5, w-1, h-1, cornerRadius-0.5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 48))
    nanovg.nvgStroke(vg)

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 160))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x+h*0.3, y+h*0.5, text, None)  # type: ignore

    nanovg.nvgFontSize(vg, h*1.3)
    nanovg.nvgFontFace(vg, "icons")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 64))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_CENTER |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    # nanovg.nvgText(vg, x+w-h*0.5f, y+h*0.5f, cpToUTF8(ICON_CHEVRON_RIGHT,icon), NULL);


def drawEditBoxBase(vg, x, y, w,  h):
    # Edit
    bg = nanovg.nvgBoxGradient(vg, x+1, y+1+1.5, w-2, h-2, 3, 4,
                               nanovg.nvgRGBA(255, 255, 255, 32), nanovg.nvgRGBA(32, 32, 32, 32))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+1, w-2, h-2, 4-1)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+0.5, y+0.5, w-1, h-1, 4-0.5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 48))
    nanovg.nvgStroke(vg)


def drawEditBox(vg, text, x, y, w, h):
    drawEditBoxBase(vg, x, y, w, h)

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 64))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x+h*0.3, y+h*0.5, text, None)  # type: ignore


def drawCheckBox(vg, text, x, y, w, h):
    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 160))

    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x+28, y+h*0.5, text, None)  # type: ignore

    bg = nanovg.nvgBoxGradient(vg, x+1, y+(int)(h*0.5)-9+1, 18, 18,
                               3, 3, nanovg.nvgRGBA(0, 0, 0, 32), nanovg.nvgRGBA(0, 0, 0, 92))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x+1, y+(int)(h*0.5)-9, 18, 18, 3)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    nanovg.nvgFontSize(vg, 33)
    nanovg.nvgFontFace(vg, "icons")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 128))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_CENTER |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    # nanovg.nvgText(vg, x+9+2, y+h*0.5f, cpToUTF8(ICON_CHECK,icon), NULL);


def drawLabel(vg, text, x, y, w, h):
    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 128))

    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x, y+h*0.5, text, None)  # type: ignore


def isBlack(col):
    # Returns 1 if col.rgba is 0.0f,0.0f,0.0f,0.0f, 0 otherwise
    if (col.r == 0.0 and col.g == 0.0 and col.b == 0.0 and col.a == 0.0):
        return 1

    return 0


def drawButton(vg, preicon, text, x, y, w, h, col):
    cornerRadius = 4.0
    bg = nanovg.nvgLinearGradient(vg, x, y, x, y + h,
                                  nanovg.nvgRGBA(
                                      255, 255, 255, 16 if isBlack(col) else 32),
                                  nanovg.nvgRGBA(
                                      0, 0, 0, 16 if isBlack(col) else 32))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x + 1, y + 1, w - 2, h - 2, cornerRadius - 1)
    if not isBlack(col):
        nanovg.nvgFillColor(vg, col)
        nanovg.nvgFill(vg)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x + 0.5, y + 0.5, w - 1,
                          h - 1, cornerRadius - 0.5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 48))
    nanovg.nvgStroke(vg)

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans-bold")
    iw = 0
    tw = nanovg.nvgTextBounds(vg, 0, 0, text, None, None)  # type: ignore
    if preicon:
        nanovg.nvgFontSize(vg, h * 1.3)
        nanovg.nvgFontFace(vg, "icons")
        iw = nanovg.nvgTextBounds(
            vg, 0, 0, preicon, None, None)  # type: ignore
        iw += h * 0.15

    if preicon:
        nanovg.nvgFontSize(vg, h * 1.3)
        nanovg.nvgFontFace(vg, "icons")
        nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 96))
        nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                            nanovg.NVGalign.NVG_ALIGN_MIDDLE)
        nanovg.nvgText(vg, x + w * 0.5 - tw * 0.5 - iw *
                       0.75, y + h * 0.5, preicon, None)  # type: ignore

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans-bold")
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_LEFT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(0, 0, 0, 160))
    nanovg.nvgText(vg, x + w * 0.5 - tw * 0.5 + iw *
                   0.25, y + h * 0.5 - 1, text, None)  # type: ignore
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 160))
    nanovg.nvgText(vg, x + w * 0.5 - tw * 0.5 +
                   iw * 0.25, y + h * 0.5, text, None)  # type: ignore


def drawEditBoxNum(vg, text, units, x, y, w, h):
    #   float uw;

    drawEditBoxBase(vg, x, y, w, h)

    uw = nanovg.nvgTextBounds(vg, 0, 0, units, None, None)  # type: ignore

    nanovg.nvgFontSize(vg, 15.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 64))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_RIGHT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x + w - h * 0.3, y + h *
                   0.5, units, None)  # type: ignore

    nanovg.nvgFontSize(vg, 17.0)
    nanovg.nvgFontFace(vg, "sans")
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(255, 255, 255, 128))
    nanovg.nvgTextAlign(vg, nanovg.NVGalign.NVG_ALIGN_RIGHT |
                        nanovg.NVGalign.NVG_ALIGN_MIDDLE)
    nanovg.nvgText(vg, x + w - uw - h * 0.5, y + h *
                   0.5, text, None)  # type: ignore


def drawSlider(vg, pos, x, y, w, h):
    #   NVGpaint bg, knob;
    cy = y + int(h * 0.5)
    kr = int(h * 0.25)

    nanovg.nvgSave(vg)

    # Slot
    bg = nanovg.nvgBoxGradient(vg, x, cy - 2 + 1, w, 4, 2, 2, nanovg.nvgRGBA(0, 0, 0, 32),
                               nanovg.nvgRGBA(0, 0, 0, 128))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x, cy - 2, w, 4, 2)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    # Knob Shadow
    bg = nanovg.nvgRadialGradient(vg, x + (int)(pos * w), cy + 1, kr - 3, kr + 3,
                                  nanovg.nvgRGBA(0, 0, 0, 64), nanovg.nvgRGBA(0, 0, 0, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x + (int)(pos * w) - kr - 5, cy - kr - 5, kr * 2 + 5 + 5,
                   kr * 2 + 5 + 5 + 3)
    nanovg.nvgCircle(vg, x + (int)(pos * w), cy, kr)
    nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
    nanovg.nvgFillPaint(vg, bg)
    nanovg.nvgFill(vg)

    # Knob
    knob = nanovg.nvgLinearGradient(vg, x, cy - kr, x, cy + kr,
                                    nanovg.nvgRGBA(255, 255, 255, 16), nanovg.nvgRGBA(0, 0, 0, 16))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgCircle(vg, x + int(pos * w), cy, kr - 1)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(40, 43, 48, 255))
    nanovg.nvgFill(vg)
    nanovg.nvgFillPaint(vg, knob)
    nanovg.nvgFill(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgCircle(vg, x + int(pos * w), cy, kr - 0.5)
    nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(0, 0, 0, 92))
    nanovg.nvgStroke(vg)

    nanovg.nvgRestore(vg)


def drawSpinner(vg, cx, cy, r, t):
    a0 = 0.0 + t * 6
    a1 = math.pi + t * 6
    r0 = r
    r1 = r * 0.75

    nanovg.nvgSave(vg)

    nanovg.nvgBeginPath(vg)
    nanovg.nvgArc(vg, cx, cy, r0, a0, a1, nanovg.NVGwinding.NVG_CW)
    nanovg.nvgArc(vg, cx, cy, r1, a1, a0, nanovg.NVGwinding.NVG_CCW)
    nanovg.nvgClosePath(vg)
    ax = cx + math.cos(a0) * (r0 + r1) * 0.5
    ay = cy + math.sin(a0) * (r0 + r1) * 0.5
    bx = cx + math.cos(a1) * (r0 + r1) * 0.5
    by = cy + math.sin(a1) * (r0 + r1) * 0.5
    paint = nanovg.nvgLinearGradient(vg, ax, ay, bx, by, nanovg.nvgRGBA(0, 0, 0, 0),
                                     nanovg.nvgRGBA(0, 0, 0, 128))
    nanovg.nvgFillPaint(vg, paint)
    nanovg.nvgFill(vg)

    nanovg.nvgRestore(vg)


def drawThumbnails(vg, x, y, w, h, images, nimages, t):
    cornerRadius = 3.0
#   NVGpaint shadowPaint, imgPaint, fadePaint;
#   float ix, iy, iw, ih;
    thumb = 60.0
    arry = 30.5
    imgw = (ctypes.c_int * 1)()
    imgh = (ctypes.c_int * 1)()
    stackh = (nimages / 2) * (thumb + 10) + 10
#   int i;
    u = (1 + math.cos(t * 0.5)) * 0.5
    u2 = (1 - math.cos(t * 0.2)) * 0.5
#   float scrollh, dv;

    nanovg.nvgSave(vg)

    # Drop shadow
    shadowPaint = nanovg.nvgBoxGradient(vg, x, y + 4, w, h, cornerRadius * 2, 20,
                                        nanovg.nvgRGBA(0, 0, 0, 128), nanovg.nvgRGBA(0, 0, 0, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x - 10, y - 10, w + 20, h + 30)
    nanovg.nvgRoundedRect(vg, x, y, w, h, cornerRadius)
    nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
    nanovg.nvgFillPaint(vg, shadowPaint)
    nanovg.nvgFill(vg)

    # Window
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x, y, w, h, cornerRadius)
    nanovg.nvgMoveTo(vg, x - 10, y + arry)
    nanovg.nvgLineTo(vg, x + 1, y + arry - 11)
    nanovg.nvgLineTo(vg, x + 1, y + arry + 11)
    nanovg.nvgFillColor(vg, nanovg.nvgRGBA(200, 200, 200, 255))
    nanovg.nvgFill(vg)

    nanovg.nvgSave(vg)
    nanovg.nvgScissor(vg, x, y, w, h)
    nanovg.nvgTranslate(vg, 0, -(stackh - h) * u)

    dv = 1.0 / float(nimages - 1)

    for i in range(nimages):
        tx = x + 10
        ty = y + 10
        tx += int(i % 2) * (thumb + 10)
        ty += int(i / 2) * (thumb + 10)
        nanovg.nvgImageSize(vg, images[i], imgw, imgh)
        if imgw[0] < imgh[0]:
            iw = thumb
            ih = int(iw * float(imgh[0]) / float(imgw[0]))
            ix = 0
            iy = int(-(ih - thumb) * 0.5)
        else:
            ih = thumb
            iw = int(ih * float(imgw[0]) / float(imgh[0]))
            ix = int(-(iw - thumb) * 0.5)
            iy = 0

        v = int(i * dv)
        a = clamp((u2 - v) / dv, 0, 1)

        if a < 1.0:
            drawSpinner(vg, tx + thumb / 2, ty + thumb / 2, thumb * 0.25, t)

        imgPaint = nanovg.nvgImagePattern(vg, tx + ix, ty + iy, iw, ih,
                                          0.0 / 180.0 * math.pi, images[i], a)
        nanovg.nvgBeginPath(vg)
        nanovg.nvgRoundedRect(vg, tx, ty, thumb, thumb, 5)
        nanovg.nvgFillPaint(vg, imgPaint)
        nanovg.nvgFill(vg)

        shadowPaint = nanovg.nvgBoxGradient(vg, tx - 1, ty, thumb + 2, thumb + 2, 5, 3,
                                            nanovg.nvgRGBA(0, 0, 0, 128), nanovg.nvgRGBA(0, 0, 0, 0))
        nanovg.nvgBeginPath(vg)
        nanovg.nvgRect(vg, tx - 5, ty - 5, thumb + 10, thumb + 10)
        nanovg.nvgRoundedRect(vg, tx, ty, thumb, thumb, 6)
        nanovg.nvgPathWinding(vg, nanovg.NVGsolidity.NVG_HOLE)
        nanovg.nvgFillPaint(vg, shadowPaint)
        nanovg.nvgFill(vg)

        nanovg.nvgBeginPath(vg)
        nanovg.nvgRoundedRect(vg, tx + 0.5, ty + 0.5,
                              thumb - 1, thumb - 1, 4 - 0.5)
        nanovg.nvgStrokeWidth(vg, 1.0)
        nanovg.nvgStrokeColor(vg, nanovg.nvgRGBA(255, 255, 255, 192))
        nanovg.nvgStroke(vg)

    nanovg.nvgRestore(vg)

    # Hide fades
    fadePaint = nanovg.nvgLinearGradient(vg, x, y, x, y + 6, nanovg.nvgRGBA(200, 200, 200, 255),
                                         nanovg.nvgRGBA(200, 200, 200, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x + 4, y, w - 8, 6)
    nanovg.nvgFillPaint(vg, fadePaint)
    nanovg.nvgFill(vg)

    fadePaint = nanovg.nvgLinearGradient(vg, x, y + h, x, y + h - 6, nanovg.nvgRGBA(200, 200, 200, 255),
                                         nanovg.nvgRGBA(200, 200, 200, 0))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRect(vg, x + 4, y + h - 6, w - 8, 6)
    nanovg.nvgFillPaint(vg, fadePaint)
    nanovg.nvgFill(vg)

    # Scroll bar
    shadowPaint = nanovg.nvgBoxGradient(vg, x + w - 12 + 1, y + 4 + 1, 8, h - 8, 3, 4,
                                        nanovg.nvgRGBA(0, 0, 0, 32), nanovg.nvgRGBA(0, 0, 0, 92))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x + w - 12, y + 4, 8, h - 8, 3)
    nanovg.nvgFillPaint(vg, shadowPaint)
    nanovg.nvgFill(vg)

    scrollh = (h / stackh) * (h - 8)
    shadowPaint = nanovg.nvgBoxGradient(
        vg, x + w - 12 - 1, y + 4 +
        (h - 8 - scrollh) * u - 1, 8, scrollh, 3, 4,
        nanovg.nvgRGBA(220, 220, 220, 255), nanovg.nvgRGBA(128, 128, 128, 255))
    nanovg.nvgBeginPath(vg)
    nanovg.nvgRoundedRect(vg, x + w - 12 + 1, y + 4 + 1 + (h - 8 - scrollh) * u, 8 - 2,
                          scrollh - 2, 2)
    nanovg.nvgFillPaint(vg, shadowPaint)
    nanovg.nvgFill(vg)

    nanovg.nvgRestore(vg)


class Demo:
    def __init__(self, vg) -> None:
        self.vg = vg
        self.images = []
        self.load_data()
        self.blowup = False

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
        if width == 0 or height == 0:
            return
        ratio = width / height
        nanovg.nvgBeginFrame(self.vg, width, height, ratio)

        drawEyes(self.vg, width - 250, 50, 150, 100, mx, my, t)
        drawParagraph(self.vg, width - 450, 50, 150, 100, mx, my)
        drawGraph(self.vg, 0, height/2, width, height/2, t)
        drawColorwheel(self.vg, width - 300, height - 300, 250.0, 250.0, t)

        # Line joints
        drawLines(self.vg, 120, height-50, 600, 50, t)

        # Line caps
        drawWidths(self.vg, 10, 50, 30)

        # Line caps
        drawCaps(self.vg, 10, 300, 30)

        drawScissor(self.vg, 50, height-80, t)

        nanovg.nvgSave(self.vg)
        if self.blowup:
            nanovg.nvgRotate(self.vg, math.sin(t*0.3)*5.0/180.0*math.pi)
            nanovg.nvgScale(self.vg, 2.0, 2.0)

        # Widgets
        drawWindow(self.vg, "Widgets `n Stuff", 50, 50, 300, 400)
        x = 60
        y = 95
        drawSearchBox(self.vg, "Search", x, y, 280, 25)
        y += 40
        drawDropDown(self.vg, "Effects", x, y, 280, 28)

        # Form
        popy = y + 14
        y += 45
        drawLabel(self.vg, "Login", x, y, 280, 20)
        y += 25
        drawEditBox(self.vg, "Email",  x, y, 280, 28)
        y += 35
        drawEditBox(self.vg, "Password", x, y, 280, 28)
        y += 38
        drawCheckBox(self.vg, "Remember me", x, y, 140, 28)
        drawButton(self.vg, ICON_LOGIN, "Sign in", x+138, y,
                   140, 28, nanovg.nvgRGBA(0, 96, 128, 255))
        y += 45

        # Slider
        drawLabel(self.vg, "Diameter", x, y, 280, 20)
        y += 25
        drawEditBoxNum(self.vg, "123.00", "px", x+180, y, 100, 28)
        drawSlider(self.vg, 0.4, x, y, 170, 28)
        y += 55

        drawButton(self.vg, ICON_TRASH, "Delete", x, y,
                   160, 28, nanovg.nvgRGBA(128, 16, 8, 255))
        drawButton(self.vg, 0, "Cancel", x+170, y,
                   110, 28, nanovg.nvgRGBA(0, 0, 0, 0))

        # Thumbnails box
        drawThumbnails(self.vg, 365, popy-30, 160, 300, self.images, 12, t)


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
