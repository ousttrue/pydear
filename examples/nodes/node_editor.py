from typing import Optional
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.setting import SettingInterface


class NodeEditor:
    def __init__(self, name: str, *, state: bytes = b'', setting: Optional[SettingInterface] = None) -> None:
        self.settting = setting
        self.name = name
        self.is_initialized = False

    def __del__(self):
        if self.is_initialized:
            ImNodes.DestroyContext()
            self.is_initialized = False

    def save(self):
        if self.settting:
            self.settting.save(
                ImNodes.SaveCurrentEditorStateToIniString().encode('utf-8'))

    def load(self):
        if self.settting:
            data = self.settting.load()
            if data:
                ImNodes.LoadCurrentEditorStateFromIniString(data, len(data))

    def show(self, p_open):
        if not p_open[0]:
            return
        if ImGui.Begin(self.name):

            if not self.is_initialized:
                ImNodes.CreateContext()
                self.load()
                self.is_initialized = True

            ImNodes.BeginNodeEditor()
            ImNodes.BeginNode(1)

            ImNodes.BeginNodeTitleBar()
            ImGui.TextUnformatted("simple node :)")
            ImNodes.EndNodeTitleBar()

            ImNodes.BeginInputAttribute(2)
            ImGui.Text("input")
            ImNodes.EndInputAttribute()

            ImNodes.BeginOutputAttribute(3)
            ImGui.Indent(40)
            ImGui.Text("output")
            ImNodes.EndOutputAttribute()

            ImNodes.EndNode()
            ImNodes.EndNodeEditor()

        ImGui.End()
