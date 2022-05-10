from typing import Optional
import abc
from pydear import imgui as ImGui
from .mouse_event import MouseInput


class Item(abc.ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abc.abstractmethod
    def resize(self, w: int, h: int):
        pass

    @abc.abstractmethod
    def wheel(self, d: int):
        pass

    def on_mouse(self, input: MouseInput, last: Optional[MouseInput]):
        self.resize(input.width, input.height)

        dx = 0
        dy = 0
        if last:
            dx = input.x - last.x
            dy = input.y - last.y

        if input.is_active:
            self.mouse_drag(
                input.x, input.y,
                dx, dy,
                input.left_down, input.right_down, input.middle_down)
        else:
            self.mouse_release(input.x, input.y)

        if input.is_hover:
            self.wheel(input.wheel)

    @abc.abstractmethod
    def mouse_drag(self, x: int, y: int, dx: int, dy: int, left: bool, right: bool, middle: bool):
        '''
        drag
        '''
        pass

    @abc.abstractmethod
    def mouse_release(self, x: int, y: int):
        '''
        hover
        '''
        pass

    @abc.abstractmethod
    def render(self):
        pass

    @abc.abstractmethod
    def show(self):
        pass


class Selector():
    def __init__(self) -> None:
        self.items = []
        self.selected: Optional[Item] = None

    @property
    def view_name(self):
        name = self.selected.name if self.selected else ''
        return f'{name}###__selector_view_name__'

    def add(self, item: Item):
        self.items.append(item)
        if not self.selected:
            self.selected = item

    def show(self):
        ImGui.SetNextItemOpen(True, ImGui.ImGuiCond_.FirstUseEver)
        selected = None
        for item in self.items:
            if ImGui.Selectable(item.name, item == self.selected):
                selected = item

        if selected:
            self.selected = selected
