from typing import Optional, List, Tuple, TypedDict
import ctypes
import json
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.setting import SettingInterface


class IdGenerator:
    def __init__(self) -> None:
        self.next_id = 1

    def __call__(self) -> int:
        value = self.next_id
        self.next_id += 1
        return value


NEXT_ID = IdGenerator()


class InputPinData(TypedDict):
    id: int
    name: str


class OutputPinData(TypedDict):
    id: int
    name: str


class NodeData(TypedDict):
    id: int
    title: str
    inputs: List[InputPinData]
    outputs: List[OutputPinData]


class InputPin:
    def __init__(self, name: str, *, id=None) -> None:
        self.id = id if isinstance(id, int) else NEXT_ID()
        self.name = name

    @staticmethod
    def load(value: InputPinData) -> 'InputPin':
        return InputPin(value['name'], id=value['id'])

    def show(self):
        ImNodes.BeginInputAttribute(self.id)
        ImGui.Text(self.name)
        ImNodes.EndInputAttribute()


class OutputPin:
    def __init__(self, name: str, *, id=None) -> None:
        self.id = id if isinstance(id, int) else NEXT_ID()
        self.name = name

    @staticmethod
    def load(value: OutputPinData) -> 'OutputPin':
        return OutputPin(value['name'], id=value['id'])

    def show(self):
        ImNodes.BeginOutputAttribute(self.id)
        ImGui.Indent(40)
        ImGui.Text(self.name)
        ImNodes.EndOutputAttribute()


class Node:
    def __init__(self, title: str, *, id=None, inputs=None, outputs=None) -> None:
        self.id = id if isinstance(id, int) else NEXT_ID()
        self.title = title
        self.inputs: List[InputPin] = inputs if inputs else [InputPin('input')]
        self.outputs: List[OutputPin] = outputs if outputs else [
            OutputPin('output')]

    @staticmethod
    def load(value: NodeData) -> 'Node':
        return Node(
            value['title'],
            id=value['id'],
            inputs=[InputPin.load(x) for x in value['inputs']],
            outputs=[OutputPin.load(x) for x in value['outputs']],
        )

    def dump(self) -> NodeData:
        return NodeData(
            id=self.id,
            title=self.title,
            inputs=[InputPinData(id=x.id, name=x.name) for x in self.inputs],
            outputs=[OutputPinData(id=x.id, name=x.name) for x in self.outputs]
        )

    def contains(self, link: Tuple[int, int]) -> bool:
        for input in self.inputs:
            if input.id in link:
                return True
        for output in self.outputs:
            if output.id in link:
                return True
        return False

    def show(self):
        ImNodes.BeginNode(self.id)

        ImNodes.BeginNodeTitleBar()
        ImGui.TextUnformatted(self.title)
        ImNodes.EndNodeTitleBar()

        for input in self.inputs:
            input.show()

        for output in self.outputs:
            output.show()

        ImNodes.EndNode()


SETTING_KEY = 'imnodes'
SETTING_GRAPH_KEY = 'imnodes_graph'


class NodeEditor:
    def __init__(self, name: str, *, state: bytes = b'', setting: Optional[SettingInterface] = None) -> None:
        self.settting = setting
        self.name = name
        self.is_initialized = False
        self.nodes: List[Node] = []
        self.links: List[Tuple[int, int]] = []
        self.start_attr = (ctypes.c_int * 1)()
        self.end_attr = (ctypes.c_int * 1)()

    def __del__(self):
        if self.is_initialized:
            ImNodes.DestroyContext()
            self.is_initialized = False

    def remove_link(self, node: Node):
        self.links = [link for link in self.links if not node.contains(link)]

    def remove_node(self, node_id: int):
        for node in self.nodes:
            if node.id == node_id:
                self.remove_link(node)
                self.nodes.remove(node)
                break

        if not self.nodes:
            NEXT_ID.next_id = 1

    def save(self):
        if self.settting:
            self.settting.save(SETTING_KEY,
                               ImNodes.SaveCurrentEditorStateToIniString().encode('utf-8'))
            self.settting.save(SETTING_GRAPH_KEY,
                               json.dumps(self.dump_graph()).encode('utf-8'))

    def load(self):
        if self.settting:
            data = self.settting.load(SETTING_KEY)
            if data:
                ImNodes.LoadCurrentEditorStateFromIniString(data, len(data))
            graph_data = self.settting.load(SETTING_GRAPH_KEY)
            if graph_data:
                graph = json.loads(graph_data)
                for node in graph.get('nodes', []):
                    self.nodes.append(Node.load(node))
                for link in graph.get('links', []):
                    self.links.append(link)
                NEXT_ID.next_id = graph.get('next_id', 1)

    def dump_graph(self):
        return {
            'nodes': [node.dump() for node in self.nodes],
            'links': self.links,
            'next_id': NEXT_ID.next_id,
        }

    def popup_menu(self):
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
            if ImGui.MenuItem("add"):
                node = Node('add')
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("multiply"):
                node = Node('multiply')
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("output"):
                node = Node('output')
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("sine"):
                node = Node('sine')
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("time"):
                node = Node('time')
                self.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.EndPopup()
        ImGui.PopStyleVar()

    def show(self, p_open):
        if not p_open[0]:
            return
        if ImGui.Begin(self.name):

            if not self.is_initialized:
                ImNodes.CreateContext()
                ImNodes.PushAttributeFlag(
                    ImNodes.ImNodesAttributeFlags_.EnableLinkDetachWithDragClick)

                self.load()
                self.is_initialized = True

            ImNodes.BeginNodeEditor()
            self.popup_menu()

            for node in self.nodes:
                node.show()

            for i, (begin, end) in enumerate(self.links):
                ImNodes.Link(i, begin, end)

            ImNodes.EndNodeEditor()

            if ImNodes.IsLinkCreated(self.start_attr, self.end_attr):
                self.links.append((self.start_attr[0], self.end_attr[0]))

            if ImNodes.IsLinkDestroyed(self.start_attr):
                del self.links[self.start_attr[0]]

            num_selected = ImNodes.NumSelectedNodes()
            if num_selected and ImGui.IsKeyDown(ImGui.ImGuiKey_.X):
                selected_nodes = (ctypes.c_int * num_selected)()
                ImNodes.GetSelectedNodes(selected_nodes)
                for node_id in selected_nodes:
                    self.remove_node(node_id)

        ImGui.End()
