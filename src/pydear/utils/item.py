from typing import NamedTuple, Callable, Optional
from pydear import imgui as ImGui


class Input(NamedTuple):
    width: int
    height: int
    x: int
    y: int
    dx: int
    dy: int
    left: bool
    right: bool
    middle: bool
    wheel: int

    @property
    def aspect_ratio(self) -> float:
        return self.width/float(self.height)

    @staticmethod
    def get(hover: bool, w, h) -> Optional['Input']:
        if hover or ImGui.IsMouseDragging(0) or ImGui.IsMouseDragging(1) or ImGui.IsMouseDragging(2):
            x, y = ImGui.GetWindowPos()
            y += ImGui.GetFrameHeight()
            io = ImGui.GetIO()
            return Input(
                int(w), int(h),
                int(io.MousePos.x-x), int(io.MousePos.y-y),
                int(io.MouseDelta.x), int(io.MouseDelta.y),
                io.MouseDown[0], io.MouseDown[1], io.MouseDown[2], int(io.MouseWheel))


def empty(*args):
    pass


class Item:
    def __init__(self, name) -> None:
        self.name = name

    def render(self):
        pass

    def show(self):
        pass

    def input(self, input: Input):
        pass
