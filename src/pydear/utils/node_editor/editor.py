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
        from .node import KLASS_MAP
        self.type_map = {k: v for k, v in KLASS_MAP.items()}

    def __del__(self):
        if self.is_initialized:
            ImNodes.DestroyContext()
            self.is_initialized = False

    def save(self):
        if self.settting:
            self.settting[SETTING_KEY] = ImNodes.SaveCurrentEditorStateToIniString().encode(
                'utf-8')
            self.settting[SETTING_GRAPH_KEY] = self.graph.to_bytes()

    def register_type(self, t: Type):
        k = t.__name__
        self.type_map[k] = t

    def load(self):
        if self.settting:
            data = self.settting[SETTING_KEY]
            if data:
                ImNodes.LoadCurrentEditorStateFromIniString(data, len(data))
            graph_data = self.settting[SETTING_GRAPH_KEY]
            if graph_data:
                self.graph.from_bytes(self.type_map, graph_data)

    def before_node_editor(self):
        '''
        this is sample
        '''
        ImGui.TextUnformatted("Right click -- add node")
        ImGui.TextUnformatted("X -- delete selected node")

    def on_node_editor(self):
        '''
        this is sample
        '''
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
            next_id = self.graph.get_next_id
            from .node import Node, InputPin, OutputPin

            if ImGui.MenuItem("input"):
                node = Node(next_id(), 'input', [], [
                            OutputPin(next_id(), 'value')])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.MenuItem("----")

            if ImGui.MenuItem("output"):
                node = Node(next_id(), 'output', [
                            InputPin(next_id(), 'value')], [])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.MenuItem("----")

            if ImGui.MenuItem("add"):
                node = Node(next_id(), 'add',
                            [InputPin(next_id(), 'a'),
                             InputPin(next_id(), 'b')],
                            [OutputPin(next_id(), 'value')])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("multiply"):
                node = Node(next_id(), 'mult',
                            [InputPin(next_id(), 'a'),
                             InputPin(next_id(), 'b')],
                            [OutputPin(next_id(), 'value')])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.EndPopup()
        ImGui.PopStyleVar()

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
