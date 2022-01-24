from typing import NamedTuple, Callable
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


def empty(*args):
    pass


class Item:
    def __init__(self, name) -> None:
        self.name = name
        self.is_initialized = False

    def render(self):
        pass

    def show(self):
        pass

    def input(self, input: Input):
        pass
