from typing import Optional
import ctypes
import pathlib
import cydeer as ImGui


NAME = b"fileopendialog"

dont_ask_me_next_time = (ctypes.c_bool * 1)(False)


def fileopendialog(dir: pathlib.Path = None) -> Optional[pathlib.Path]:
    # Always center this window when appearing
    center = ImGui.GetMainViewport().GetCenter()
    ImGui.SetNextWindowPos(
        center, ImGui.ImGuiCond_.Appearing, (0.5, 0.5))

    result = None
    if ImGui.BeginPopupModal(NAME, None, ImGui.ImGuiWindowFlags_.AlwaysAutoResize):
        ImGui.Text(
            "All those beautiful files will be deleted.\nThis operation cannot be undone!\n\n")
        ImGui.Separator()

        # static int unused_i = 0
        # ImGui.Combo("Combo", &unused_i, "Delete\0Delete harder\0")

        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.FramePadding, (0, 0))
        ImGui.Checkbox("Don't ask me next time", dont_ask_me_next_time)
        ImGui.PopStyleVar()

        if ImGui.Button("OK", (120, 0)):
            ImGui.CloseCurrentPopup()
            result = pathlib.Path(__file__)
        ImGui.SetItemDefaultFocus()
        ImGui.SameLine()
        if ImGui.Button("Cancel", (120, 0)):
            ImGui.CloseCurrentPopup()
        ImGui.EndPopup()
    return result
