from typing import Optional, Dict, Type
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.setting import BinSetting
from .graph import Graph


SETTING_KEY = 'imnodes'
SETTING_GRAPH_KEY = 'imnodes_graph'


class NodeEditor:
    '''
    TODO: undo, redo
    '''

    def __init__(self, name: str, *, setting: Optional[BinSetting] = None) -> None:
        self.settting = setting
        self.name = name
        self.is_initialized = False
        self.start_attr = (ctypes.c_int * 1)()
        self.end_attr = (ctypes.c_int * 1)()
        self.graph = Graph()
        self.process_frame = 0

    def __del__(self):
        if self.is_initialized:
            ImNodes.DestroyContext()
            self.is_initialized = False

    def save(self):
        if self.settting:
            self.settting[SETTING_KEY] = ImNodes.SaveCurrentEditorStateToIniString().encode(
                'utf-8')
            self.settting[SETTING_GRAPH_KEY] = self.graph.to_bytes()

    def load(self):
        if self.settting:
            data = self.settting[SETTING_KEY]
            if data:
                ImNodes.LoadCurrentEditorStateFromIniString(data, len(data))
            graph_data = self.settting[SETTING_GRAPH_KEY]
            if graph_data:
                self.graph.from_bytes(graph_data)

    def show(self, p_open):
        process_frame = self.process_frame
        self.process_frame += 1
        self.graph.process(process_frame)

        if not p_open[0]:
            return

        if ImGui.Begin(self.name):

            if not self.is_initialized:
                # init
                ImNodes.CreateContext()
                ImNodes.PushAttributeFlag(
                    ImNodes.ImNodesAttributeFlags_.EnableLinkDetachWithDragClick)

                self.load()

                self.is_initialized = True

            # show
            self.before_node_editor()
            ImNodes.BeginNodeEditor()
            self.on_node_editor()
            self.graph.show()
            ImNodes.EndNodeEditor()

            # update
            self.graph.update(self.start_attr, self.end_attr)

        ImGui.End()

    def before_node_editor(self):
        ImGui.TextUnformatted("Right click -- add node")
        ImGui.TextUnformatted("X -- delete selected node")

    def on_node_editor(self):
        open_popup = False
        if (ImGui.IsWindowFocused(ImGui.ImGuiFocusedFlags_.RootAndChildWindows) and
                ImNodes.IsEditorHovered()):
            if ImGui.IsMouseClicked(1):
                open_popup = True

        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (8, 8))
        if not ImGui.IsAnyItemHovered() and open_popup:
            ImGui.OpenPopup("add node")

        if ImGui.BeginPopup("add node"):
            click_pos = ImGui.GetMousePosOnOpeningCurrentPopup()

            from.node import Node
            for k, t in self.graph.type_map.items():
                if issubclass(t, Node):
                    t.imgui_menu(self.graph, click_pos)

            ImGui.EndPopup()
        ImGui.PopStyleVar()
