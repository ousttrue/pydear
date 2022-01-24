from typing import List
from . import item
from pydear import imgui as ImGui


class Selector:
    def __init__(self) -> None:
        self.items: List[item.Item] = []
        self.selected = None

    @property
    def view_name(self):
        name = self.selected.name if self.selected else ''
        return f'{name}##__selector_view_name__'

    def add(self, item: item.Item):
        self.items.append(item)
        if not self.selected:
            self.selected = item

    def show(self):
        selected = None
        for item in self.items:
            if ImGui.Selectable(item.name, item == self.selected):
                selected = item
        if selected:
            self.selected = selected
