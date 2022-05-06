from typing import List, Tuple, Dict, Type, Optional
import pathlib
import logging
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from .node import Node, InputPin, OutputPin, InputPinMap, OutputPinMap

LOGGER = logging.getLogger(__name__)


class Graph:
    def __init__(self) -> None:
        self.next_id = 1
        self.nodes: List[Node] = []
        self.keep_remove = []
        self.links: List[Tuple[int, int]] = []
        self.input_pin_map: InputPinMap = {}
        self.output_pin_map: OutputPinMap = {}
        self.current_dir: Optional[pathlib.Path] = None

    def to_bytes(self) -> bytes:
        graph = {
            'nodes': [node.to_json() for node in self.nodes],
            'links': self.links,
            'next_id': self.next_id,
        }
        import json
        return json.dumps(graph).encode('utf-8')

    def from_bytes(self, class_map: Dict[str, Type], data: bytes):
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
                self.nodes.append(Node.from_json(class_map, klass, **args))
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

    def connect(self, output_id: int, input_id: int):
        # TODO: remove multi input
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
