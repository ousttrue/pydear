from typing import Optional, Any, TypeAlias, Dict, Tuple, List
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes


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
