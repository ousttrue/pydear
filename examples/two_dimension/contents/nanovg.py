from typing import Optional
import pathlib
from pydear import nanovg
from pydear.utils.mouse_event import MouseEvent, MouseInput
from pydear.utils.selector import Item
from pydear.utils.nanovg_renderer import NanoVgRenderer, nvg_text, nvg_line_from_to


class NanoVgSample(Item):
    def __init__(self, font_path: pathlib.Path, mouse_event: MouseEvent) -> None:
        super().__init__('nanovg')

        self.nvg = NanoVgRenderer(font_path)

        # mouse
        self.begin: Optional[MouseInput] = None
        self.mouse_event = mouse_event

        def on_left_begin(mouse_input: MouseInput):
            self.begin = mouse_input
        self.mouse_event.left_pressed += [on_left_begin]

        def on_left_end(mouse_input: MouseInput):
            self.begin = None
        self.mouse_event.left_released += [on_left_end]

    def render(self, mouse_input: MouseInput):
        input = self.mouse_event.last_input
        assert(input)

        with self.nvg.render(mouse_input.width, mouse_input.height) as vg:
            nanovg.nvgBeginPath(vg)
            nanovg.nvgRoundedRect(vg, 0, 0, 0, 0, 0)
            nanovg.nvgFill(vg)

            nvg_text(vg, self.nvg.font_name, input.x, input.y)
            if self.begin:
                nvg_text(vg, self.nvg.font_name, self.begin[0], self.begin[1])
                nvg_line_from_to(vg, self.begin[0],
                                 self.begin[1], input.x, input.y)

    def show(self):
        pass
