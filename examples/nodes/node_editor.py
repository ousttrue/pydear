from pydear import imgui as ImGui
from pydear import imnodes as ImNodes


class NodeEditor:
    def __init__(self, name: str, *, state: bytes = b'') -> None:
        self.name = name
        self.is_initialized = False
        self.state = state

    def __del__(self):
        if self.is_initialized:
            self.save()
            ImNodes.DestroyContext()
            self.is_initialized = False

    def save(self):
        self.state = ImNodes.SaveCurrentEditorStateToIniString().encode('utf-8')

    def load(self):
        if self.state:
            ImNodes.LoadCurrentEditorStateFromIniString(
                self.state, len(self.state))

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
