from typing import Optional, List, Tuple, Dict, TypeAlias, Any
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.setting import BinSetting


class InputPin:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.value: Optional[Any] = None

    def __getstate__(self):
        state = self.__dict__.copy()
        # Don't pickle baz
        if "value" in state:
            del state["value"]
        return state

    def show(self):
        ImNodes.BeginInputAttribute(self.id)
        ImGui.Text(self.name)
        ImNodes.EndInputAttribute()


class OutputPin:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def show(self, indent: int):
        ImNodes.BeginOutputAttribute(self.id)
        ImGui.Indent(indent)
        ImGui.Text(self.name)
        ImNodes.EndOutputAttribute()

    def process(self, node: 'Node', in_pin: InputPin):
        pass


InputPinMap: TypeAlias = Dict[int, Tuple['Node', OutputPin]]
OutputPinMap: TypeAlias = Dict[int, Tuple['Node', InputPin]]


class NodeRuntime:
    def __init__(self) -> None:
        self.process_frame = -1

    def process(self, node: 'Node'):
        pass

    def __getstate__(self):
        # all fields are not pickle
        return {}

    def __setstate__(self, state):
        # call __init__ manually
        self.__init__()


class Node:
    def __init__(self, id: int, title: str, inputs: List[InputPin], outputs: List[OutputPin]) -> None:
        self.id = id
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.runtime = NodeRuntime()

    def get_right_indent(self) -> int:
        return 40

    def contains(self, link: Tuple[int, int]) -> bool:
        for in_pin in self.inputs:
            if in_pin.id in link:
                return True
        for out_pin in self.outputs:
            if out_pin.id in link:
                return True
        return False

    def show(self, graph):
        ImNodes.BeginNode(self.id)

        ImNodes.BeginNodeTitleBar()
        ImGui.TextUnformatted(self.title)
        ImNodes.EndNodeTitleBar()

        self.show_content(graph)

        for in_pin in self.inputs:
            in_pin.show()

        for out_pin in self.outputs:
            out_pin.show(self.get_right_indent())

        ImNodes.EndNode()

    def show_content(self, graph):
        pass

    def has_connected_input(self, input_pin_map: InputPinMap) -> bool:
        for in_pin in self.inputs:
            if in_pin.id in input_pin_map:
                return True
        return False

    def has_connected_output(self, ontput_pin_map: OutputPinMap) -> bool:
        for out_pin in self.outputs:
            if out_pin.id in ontput_pin_map:
                return True
        return False

    def process(self, process_frame: int, input_pin_map: InputPinMap):
        if process_frame == self.runtime.process_frame:
            return
        self.runtime.process_frame = process_frame
        # update upstream
        for in_pin in self.inputs:
            match input_pin_map.get(in_pin.id):
                case (out_node, out_pin):
                    out_node.process(process_frame, input_pin_map)
                    out_pin.process(out_node, in_pin)
                case _:
                    in_pin.value = None
        # self
        self.runtime.process(self)


SETTING_KEY = 'imnodes'
SETTING_GRAPH_KEY = 'imnodes_graph'


class Graph:
    def __init__(self) -> None:
        self.next_id = 1
        self.nodes: List[Node] = []
        self.keep_remove = []
        self.links: List[Tuple[int, int]] = []
        self.input_pin_map: InputPinMap = {}
        self.output_pin_map: OutputPinMap = {}

    def get_next_id(self) -> int:
        value = self.next_id
        self.next_id += 1
        return value

    def find_output(self, output_id: int) -> Tuple[Node, OutputPin]:
        for node in self.nodes:
            for out_pin in node.outputs:
                if out_pin.id == output_id:
                    return node, out_pin
        raise KeyError()

    def find_input(self, input_id: int) -> Tuple[Node, InputPin]:
        for node in self.nodes:
            for in_pin in node.inputs:
                if in_pin.id == input_id:
                    return node, in_pin
        raise KeyError()

    def connect(self, output_id: int, input_id: int):
        self.links.append((output_id, input_id))
        self.input_pin_map[input_id] = self.find_output(output_id)
        self.output_pin_map[output_id] = self.find_input(input_id)

    def disconnect(self, link_index: int):
        output_id, input_id = self.links[link_index]
        del self.links[link_index]
        del self.input_pin_map[input_id]
        del self.output_pin_map[output_id]

    def remove_link(self, node: Node):
        self.links = [link for link in self.links if not node.contains(link)]

    def remove_node(self, node_id: int):
        for node in self.nodes:
            if node.id == node_id:
                self.remove_link(node)
                self.nodes.remove(node)
                # delay __del__
                self.keep_remove.append(node)
                break

        if not self.nodes:
            self.next_id = 1

    def process(self, process_frame: int):
        in_pin_list = set()
        out_pin_list = set()
        for node in self.nodes:
            for in_pin in node.inputs:
                in_pin_list.add(in_pin.id)
            for out_pin in node.outputs:
                out_pin_list.add(out_pin.id)
            if not node.has_connected_output(self.output_pin_map):
                node.process(process_frame, self.input_pin_map)

        def pin_exists(out_pin: int, in_pin: int):
            if out_pin not in out_pin_list:
                return False
            if in_pin not in in_pin_list:
                return False
            return True

        self.links = [link for link in self.links if pin_exists(*link)]

    def show(self):
        if not isinstance(self.keep_remove, list):
            self.keep_remove = []
        self.keep_remove.clear()

        for node in self.nodes:
            node.show(self)

        for i, (begin, end) in enumerate(self.links):
            ImNodes.Link(i, begin, end)

    def update(self, start_attr, end_attr):
        if ImNodes.IsLinkCreated(start_attr, end_attr):
            # add link
            self.connect(start_attr[0], end_attr[0])

        if ImNodes.IsLinkDestroyed(start_attr):
            # remove unlink
            self.disconnect(start_attr[0])

        num_selected = ImNodes.NumSelectedLinks()
        if num_selected and ImGui.IsKeyPressed(ImGui.ImGuiKey_.X):
            # remove selected link
            selected_links = (ctypes.c_int * num_selected)()
            ImNodes.GetSelectedLinks(selected_links)
            for i in reversed(selected_links):
                self.disconnect(i)

        num_selected = ImNodes.NumSelectedNodes()
        if num_selected and ImGui.IsKeyPressed(ImGui.ImGuiKey_.X):
            # remove selected node
            selected_nodes = (ctypes.c_int * num_selected)()
            ImNodes.GetSelectedNodes(selected_nodes)
            for node_id in selected_nodes:
                self.remove_node(node_id)


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
            import pickle
            self.settting[SETTING_GRAPH_KEY] = pickle.dumps(self.graph)

    def load(self):
        if self.settting:
            data = self.settting[SETTING_KEY]
            if data:
                ImNodes.LoadCurrentEditorStateFromIniString(data, len(data))
            graph_data = self.settting[SETTING_GRAPH_KEY]
            if graph_data:
                try:
                    import pickle
                    self.graph = pickle.loads(graph_data)
                except:
                    self.graph = Graph()

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

            if ImGui.MenuItem("output"):
                node = Node(next_id(), 'output', [
                            InputPin(next_id(), 'value')], [])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("sine"):
                node = Node(next_id(), 'sine', [], [
                            OutputPin(next_id(), 'value')])
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            if ImGui.MenuItem("time"):
                node = Node(next_id(), 'time', [], [
                            OutputPin(next_id(), 'value')])
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
