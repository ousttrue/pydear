import glm


class ScreenSlider:
    def __init__(self, start: glm.vec2, dir: glm.vec2, w, h, debug_draw=[]) -> None:
        # v = at + b
        self.start = start
        self.current = start
        self.debug_draw = debug_draw
        self.dir = glm.normalize(dir)
        '''
        y = ax + b
        b = y - ax
        '''
        if self.dir.x == 0:
            self.p0 = glm.vec2(self.start.x, 0)
            self.p1 = glm.vec2(self.start.x, h)
        elif self.dir.y == 0:
            self.p0 = glm.vec2(0, self.start.y)
            self.p1 = glm.vec2(w, self.start.y)
        else:
            # y = ax + b
            a = self.dir.y/self.dir.x
            # b = y - ax
            b = start.y - start.x * a
            # x = 0
            self.p0 = glm.vec2(0, b)
            # x = w
            self.p1 = glm.vec2(w, a * w + b)

    @staticmethod
    def begin_end(start: glm.vec2, end: glm.vec2, w, h) -> 'ScreenSlider':
        return ScreenSlider(start, end-start, w, h)

    def drag(self, v: glm.vec2):
        self.current = v
        return glm.dot(v-self.start, self.dir)

    def nvg_draw(self, vg):
        from pydear import nanovg
        from pydear.utils.nanovg_renderer import nvg_line_from_to
        start = self.start

        nanovg.nvgBeginPath(vg)
        nanovg.nvgCircle(vg, start.x, start.y, 4)
        nanovg.nvgFill(vg)

        current = self.current
        nvg_line_from_to(vg, start.x, start.y, current.x, current.y)

        end = start + self.dir * 100
        nvg_line_from_to(vg, start.x, start.y, end.x, end.y)

        for debug_draw in self.debug_draw:
            debug_draw(vg)
