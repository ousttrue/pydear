import pydear.imgui as ImGui

POPUP = {}


def open(name: str):
    POPUP[name] = True


def modal(name: str):
    if POPUP.get(name):
        ImGui.OpenPopup(name)
        del POPUP[name]
    # Always center this window when appearing
    center = ImGui.GetMainViewport().GetCenter()
    ImGui.SetNextWindowPos(center, ImGui.ImGuiCond_.Appearing, (0.5, 0.5))

    if ImGui.BeginPopupModal(name, None):
        if ImGui.Button("OK", (120, 0)):
            ImGui.CloseCurrentPopup()

        ImGui.EndPopup()
