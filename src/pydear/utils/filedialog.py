from typing import Dict, Optional
import pathlib
import ctypes
import pydear.imgui as ImGui


class Dialog:
    def __init__(self, name: str, path: pathlib.Path):
        self.name = name
        self.path = path
        self.is_open = False
        self.selected = None
        self.p_open = (ctypes.c_bool * 1)(True)

    def show(self):
        if not self.is_open:
            ImGui.OpenPopup(self.name)
            self.is_open = True

        # Always center this window when appearing
        center = ImGui.GetMainViewport().GetCenter()
        ImGui.SetNextWindowPos(center, ImGui.ImGuiCond_.Appearing, (0.5, 0.5))

        selected = None
        if ImGui.BeginPopupModal(self.name, self.p_open):

            ImGui.Text(f"{self.path}")

            w, h = ImGui.GetWindowSize()
            ImGui.BeginChild("Files##1", (w-50, h-100), True,
                             ImGui.ImGuiWindowFlags_.HorizontalScrollbar)
            ImGui.Columns(3)
            if ImGui.Selectable("File"):
                pass
            ImGui.NextColumn()
            if ImGui.Selectable("Type"):
                pass
            ImGui.NextColumn()
            if ImGui.Selectable("Size"):
                pass
            ImGui.NextColumn()
            ImGui.Separator()

            selected = self.show_files()

            ImGui.EndChild()

            if ImGui.Button("Close", (120, 0)) or selected:
                ImGui.CloseCurrentPopup()

            ImGui.EndPopup()

        return selected

    def _show_file(self, f: pathlib.Path, override: Optional[str] = None) -> Optional[pathlib.Path]:
        selected = None
        if ImGui.Selectable(override if override else f.stem, f == self.selected, ImGui.ImGuiSelectableFlags_.AllowDoubleClick, (ImGui.GetWindowContentRegionWidth(), 0)):
            if ImGui.IsMouseDoubleClicked(0):
                if f.is_file():
                    selected = f
                elif f.is_dir():
                    self.path = f
            else:
                self.selected = f
        ImGui.NextColumn()
        ImGui.TextUnformatted(f.suffix)
        ImGui.NextColumn()
        if f.is_file():
            ImGui.TextUnformatted(f'{f.stat().st_size}')
        else:
            ImGui.TextUnformatted('---')
        ImGui.NextColumn()
        return selected

    def show_files(self) -> Optional[pathlib.Path]:
        selected = None
        # parent
        self._show_file(self.path.parent, '..')

        # files
        for f in self.path.iterdir():
            match self._show_file(f):
                case pathlib.Path() as selected:
                    pass

        return selected


POPUP: Dict[str, Dialog] = {}


def open(name: str, path: pathlib.Path = pathlib.Path('.').absolute()):
    POPUP[name] = Dialog(name, path)


def modal(name: str) -> Optional[pathlib.Path]:
    state = POPUP.get(name)
    if state:
        return state.show()
