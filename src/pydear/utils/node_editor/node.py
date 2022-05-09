from typing import Optional, Any, TypeAlias, Dict, Tuple, List, NamedTuple, TypeVar, Generic, get_args, get_origin, Union, Type
import types
import abc
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes


T = TypeVar('T')


def get_generic_type(cls) -> Type:
    # https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    t = get_args(cls.__orig_bases__[0])[0]
    o = get_origin(t)
    if o is Union:  # Optional[T] => Union[T, None]
        args = get_args(t)
        match args:
            case (tt, types.NoneType):
                # resolve Optional[T]
                t = tt
    return t


def color_int(r, g, b):
    return (255 << 24) + (b << 16) + (g << 8) + (r << 0)


class PinStyle(NamedTuple):
    shape: ImNodes.ImNodesPinShape_
    color: int


PIN_COLOR = color_int(255, 255, 128)
DEFAULT_STYLE = PinStyle(ImNodes.ImNodesPinShape_.CircleFilled, PIN_COLOR)


class Serialized(NamedTuple):
    klass: str
    args: Dict[str, Any]


class Link(NamedTuple):
    out_pin_id: int
    in_pin_id: int
    color: int


class InputPin(Generic[T], metaclass=abc.ABCMeta):
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.generic_type = get_generic_type(self)

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {'id': self.id, 'name': self.name})

    def get_acceptale_type(self, out: 'OutputPin') -> Optional[Type]:
        if self.generic_type == out.generic_type:
            return self.generic_type

    @staticmethod
    def from_json(klass_map, klass, **kw) -> 'InputPin':
        return klass_map[klass](**kw)

    @abc.abstractmethod
    def set_value(self, value: T):
        raise NotImplementedError()

    def show(self, shape_map):
        shape, color = shape_map.get(
            self.generic_type, DEFAULT_STYLE)
        ImNodes.PushColorStyle(ImNodes.ImNodesCol_.Pin, color)
        ImNodes.BeginInputAttribute(self.id, shape)
        ImGui.Text(self.name)
        ImNodes.EndInputAttribute()
        ImNodes.PopColorStyle()


class OutputPin(Generic[T], metaclass=abc.ABCMeta):
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.generic_type = get_generic_type(self)

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {'id': self.id, 'name': self.name})

    @staticmethod
    def from_json(klass_map, klass, **kw) -> 'OutputPin':
        return klass_map[klass](**kw)

    @abc.abstractmethod
    def get_value(self, node: 'Node') -> T:
        raise NotImplementedError()

    def show(self, shape_map, indent: int):
        t = get_generic_type(self)
        shape, color = shape_map.get(
            t, DEFAULT_STYLE)
        ImNodes.PushColorStyle(ImNodes.ImNodesCol_.Pin, color)
        ImNodes.BeginOutputAttribute(self.id, shape)
        ImGui.Indent(indent)
        ImGui.Text(self.name)
        ImNodes.EndOutputAttribute()
        ImNodes.PopColorStyle()


OutputFromInput: TypeAlias = Dict[int, Tuple['Node', OutputPin]]
InputFromOutput: TypeAlias = Dict[int, Tuple['Node', InputPin]]


class Node(metaclass=abc.ABCMeta):
    def __init__(self, id: int, title: str, inputs: List[InputPin], outputs: List[OutputPin]) -> None:
        self.id = id
        self.title = title
        self.inputs = inputs
        self.outputs = outputs
        self.process_frame = -1

    @classmethod
    @abc.abstractmethod
    def imgui_menu(cls, graph, click_pos):
        raise NotImplementedError()

    def to_json(self) -> Serialized:
        return Serialized(
            'Node', {'id': self.id, 'title': self.title,
                     'inputs': [input_pin.to_json() for input_pin in self.inputs],
                     'outputs': [output_pin.to_json() for output_pin in self.outputs]
                     })

    def get_right_indent(self) -> int:
        return 40

    def contains(self, link: Link) -> bool:
        for in_pin in self.inputs:
            if in_pin.id == link.in_pin_id:
                return True
        for out_pin in self.outputs:
            if out_pin.id == link.out_pin_id:
                return True
        return False

    def show(self, graph):
        ImNodes.BeginNode(self.id)

        ImNodes.BeginNodeTitleBar()
        ImGui.TextUnformatted(self.title)
        ImNodes.EndNodeTitleBar()

        self.show_content(graph)

        for in_pin in self.inputs:
            in_pin.show(graph.shape_map)

        for out_pin in self.outputs:
            out_pin.show(graph.shape_map, self.get_right_indent())

        ImNodes.EndNode()

    def has_connected_input(self, input_pin_map: OutputFromInput) -> bool:
        for in_pin in self.inputs:
            if in_pin.id in input_pin_map:
                return True
        return False

    def has_connected_output(self, ontput_pin_map: InputFromOutput) -> bool:
        for out_pin in self.outputs:
            if out_pin.id in ontput_pin_map:
                return True
        return False

    def process(self, process_frame: int, input_pin_map: OutputFromInput):
        if process_frame == self.process_frame:
            return
        self.process_frame = process_frame
        # update upstream
        for in_pin in self.inputs:
            match input_pin_map.get(in_pin.id):
                case (out_node, out_pin):
                    out_node.process(process_frame, input_pin_map)
                    in_pin.set_value(out_pin.get_value(out_node))
                case _:
                    in_pin.set_value(None)  # or default value ?
        # self
        self.process_self()

    def show_content(self, graph):
        pass

    def process_self(self):
        pass
