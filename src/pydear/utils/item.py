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


class Item(NamedTuple):
    name: str
    render: Callable[[], None]
    show: Callable[[], None] = empty
    input: Callable[[Input], None] = empty
