from typing import Optional, Any, TypeAlias, Dict, Tuple, List, NamedTuple
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes


class Serialized(NamedTuple):
    klass: str
    args: Dict[str, Any]


class InputPin:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.value: Optional[Any] = None

    def to_json(self) -> Serialized:
        return Serialized('InputPin', {'id': self.id, 'name': self.name})

    @staticmethod
    def from_json(klass_map, klass, **kw) -> 'InputPin':
        return klass_map[klass](**kw)

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

    def to_json(self) -> Serialized:
        return Serialized('OutputPin', {'id': self.id, 'name': self.name})

    @staticmethod
    def from_json(klass_map, klass, **kw) -> 'OutputPin':
        return klass_map[klass](**kw)

    def show(self, indent: int):
        ImNodes.BeginOutputAttribute(self.id)
        ImGui.Indent(indent)
        ImGui.Text(self.name)
        ImNodes.EndOutputAttribute()

    def process(self, node: 'Node', in_pin: InputPin):
        pass


InputPinMap: TypeAlias = Dict[int, Tuple['Node', OutputPin]]
OutputPinMap: TypeAlias = Dict[int, Tuple['Node', InputPin]]


class Node:
    def __init__(self, id: int, title: str, inputs: List[InputPin], outputs: List[OutputPin]) -> None:
        self.id = id
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.process_frame = -1

    def to_json(self) -> Serialized:
        return Serialized(
            'Node', {'id': self.id, 'title': self.title,
                     'inputs': [input_pin.to_json() for input_pin in self.inputs],
                     'outputs': [output_pin.to_json() for output_pin in self.outputs]
                     })

    @staticmethod
    def from_json(klass_map, klass: str, **kw):
        if 'inputs' in kw:
            kw['inputs'] = [InputPin.from_json(klass_map, klass, **in_args)
                            for klass, in_args in kw['inputs']]
        if 'outputs' in kw:
            kw['outputs'] = [OutputPin.from_json(klass_map, klass, **out_args)
                             for klass, out_args in kw['outputs']]
        return klass_map[klass](**kw)

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
        if process_frame == self.process_frame:
            return
        self.process_frame = process_frame
        # update upstream
        for in_pin in self.inputs:
            match input_pin_map.get(in_pin.id):
                case (out_node, out_pin):
                    out_node.process(process_frame, input_pin_map)
                    out_pin.process(out_node, in_pin)
                case _:
                    in_pin.value = None
        # self
        self.process_self()

    def show_content(self, graph):
        pass

    def process_self(self):
        pass


KLASS_MAP = {
    'InputPin': InputPin,
    'OutputPin': OutputPin,
    'Node': Node,
}
