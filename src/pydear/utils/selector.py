from typing import List, Callable, TypeVar, Generic
from .item import Item
from pydear import imgui as ImGui
from pydear.scene.camera import Camera


class Selector():
    def __init__(self) -> None:
        self.items = []
        self.selected = None

        self.camera = Camera()
        self.view_types = ['turntable', 'trackball']
        self.selected_view_type = self.view_types[0]

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
        if ImGui.CollapsingHeader("samples"):
            selected = None
            for item in self.items:
                if ImGui.Selectable(item.name, item == self.selected):
                    selected = item

            if selected:
                self.selected = selected

        ImGui.SetNextItemOpen(True, ImGui.ImGuiCond_.FirstUseEver)
        if ImGui.CollapsingHeader("cameras"):
            selected_camera = None
            for view_type in ('turn table', 'track bacll'):
                if ImGui.Selectable(view_type, view_type == self.selected_view_type):
                    selected_camera = view_type

            if selected_camera:
                self.selected_view_type = selected_camera

        ImGui.SetNextItemOpen(True, ImGui.ImGuiCond_.FirstUseEver)
        if ImGui.CollapsingHeader("gizmos"):
            pass
