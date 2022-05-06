from typing import Dict, Optional, Callable, TypeAlias
import asyncio
import pathlib
import ctypes
import pydear.imgui as ImGui

FilterCallback: TypeAlias = Callable[[pathlib.Path], bool]


class Dialog:
    def __init__(self, loop: asyncio.AbstractEventLoop, name: str, path: pathlib.Path, filter: Optional[FilterCallback] = None):
        self.future = loop.create_future()
        self.name = name
        self.path = path
        self.is_open = False
        self.selected = None
        self.p_open = (ctypes.c_bool * 1)(True)
        self.filter = filter

    def __call__(self):
        if not self.is_open:
            ImGui.OpenPopup(self.name)
            self.is_open = True

        # Always center this window when appearing
        center = ImGui.GetMainViewport().GetCenter()
        ImGui.SetNextWindowPos(center, ImGui.ImGuiCond_.Appearing, (0.5, 0.5))
        ImGui.SetNextWindowSize((700, 500), ImGui.ImGuiCond_.FirstUseEver)

        is_closed = False
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

            selected = self._show_files()

            ImGui.EndChild()

            if ImGui.Button("Close", (120, 0)) or selected:
                ImGui.CloseCurrentPopup()
                is_closed = True

            ImGui.EndPopup()

        if is_closed or not self.p_open[0]:
            from .import modal
            modal.remove(self)
            self.future.set_result(selected)
            self.is_open = False

    def _show_files(self) -> Optional[pathlib.Path]:
        selected = None
        # parent
        self._show_file(self.path.parent, '..')

        # files
        for f in self.path.iterdir():
            if self.filter and not self.filter(f):
                continue
            match self._show_file(f):
                case pathlib.Path() as selected:
                    pass

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


FILE_DIALOG = 'ModalFileDialog'


def open_async(loop: asyncio.AbstractEventLoop, path: Optional[pathlib.Path] = None, *, filter: Optional[FilterCallback] = None):
    if not path:
        path = pathlib.Path('.').absolute()
    dialog = Dialog(loop, FILE_DIALOG, path, filter=filter)
    from . import modal
    modal.push(dialog)
    return dialog.future


class Filter:
    def __init__(self, *extensions: str) -> None:
        self.extensions = set(e.lower() for e in extensions)

    def __call__(self, f: pathlib.Path) -> bool:
        if not f.is_file():
            return True
        return f.suffix.lower() in self.extensions
