from typing import List, Tuple, Dict, Type, Optional, NamedTuple
import pathlib
import logging
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from .node import Node, InputPin, OutputPin, OutputFromInput, InputFromOutput, PinStyle, Link, DEFAULT_STYLE

LOGGER = logging.getLogger(__name__)


class Graph:
    def __init__(self) -> None:
        self.next_id = 1
        self.nodes: List[Node] = []
        self.keep_remove = []
        self.links: List[Link] = []
        self.output_from_input: OutputFromInput = {}
        self.input_from_output: InputFromOutput = {}
        self.current_dir: Optional[pathlib.Path] = None
        self.type_map: Dict[str, Type] = {}
        self.shape_map: Dict[Type, PinStyle] = {}

    def register_type(self, t: Type):
        k = t.__name__
        self.type_map[k] = t

    def add_pin_style(self, t: Type, style: PinStyle):
        self.shape_map[t] = style

    def to_bytes(self) -> bytes:
        graph = {
            'nodes': [node.to_json() for node in self.nodes],
            'links': [(link.out_pin_id, link.in_pin_id) for link in self.links],
            'next_id': self.next_id,
        }
        import json
        return json.dumps(graph).encode('utf-8')

    def from_bytes(self, data: bytes):
        # clear
        self.nodes.clear()
        self.links.clear()
        self.next_id = 1

        # load
        try:
            import json
            parsed = json.loads(data)
            self.next_id = parsed['next_id']
            for klass, args in parsed['nodes']:
                node = self.type_map[klass](**args)
                self.nodes.append(node)
            for begin, end in parsed['links']:
                self.connect(begin, end)
        except Exception as ex:
            LOGGER.error(ex)

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

    def connect(self, out_pin_id: int, in_pin_id: int):
        out_node, out_pin = self.find_output(out_pin_id)
        in_node, in_pin = self.find_input(in_pin_id)

        t = in_pin.get_acceptale_type(out_pin)
        if not t:
            return

        # remove link that has same input_id or output_id
        self.links = [link for link in self.links if link.out_pin_id != out_pin_id
                      and link.in_pin_id != in_pin_id]

        pin_style = self.shape_map.get(t, DEFAULT_STYLE)
        self.links.append(Link(out_pin_id, in_pin_id, pin_style.color))
        self.output_from_input[in_pin_id] = (out_node, out_pin)
        self.input_from_output[out_pin_id] = (in_node, in_pin)

    def disconnect(self, link_index: int):
        # TODO: multi output
        output_id, input_id, color = self.links[link_index]
        del self.links[link_index]
        del self.output_from_input[input_id]
        del self.input_from_output[output_id]

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
            if not node.has_connected_output(self.input_from_output):
                node.process(process_frame, self.output_from_input)

        def pin_exists(link: Link):
            if link.out_pin_id not in out_pin_list:
                return False
            if link.in_pin_id not in in_pin_list:
                return False
            return True

        self.links = [link for link in self.links if pin_exists(link)]

    def show(self):
        if not isinstance(self.keep_remove, list):
            self.keep_remove = []
        self.keep_remove.clear()

        for node in self.nodes:
            node.show(self)

        for i, link in enumerate(self.links):
            ImNodes.PushColorStyle(ImNodes.ImNodesCol_.Link, link.color)
            ImNodes.Link(i, link.out_pin_id, link.in_pin_id)
            ImNodes.PopColorStyle()

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
