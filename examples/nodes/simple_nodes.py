from typing import Tuple, Dict, Type, Optional
import ctypes
from pydear.utils.node_editor.node import Serialized, Node, OutputPin, InputPin, color_int, PinStyle
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes


class FloatOutputPin(OutputPin[float]):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.value = 0.0

    def get_value(self, node: 'Node') -> float:
        return self.value


class FloatValueNode(Node):
    def __init__(self, id: int, out_id: int, value=0) -> None:
        self.out = FloatOutputPin(out_id, 'value')
        super().__init__(id, 'value', [], [self.out])
        self._array = (ctypes.c_float*1)(value)

    @classmethod
    def imgui_menu(cls, graph, click_pos):
        if ImGui.MenuItem("input"):
            node = FloatValueNode(graph.get_next_id(), graph.get_next_id())
            graph.nodes.append(node)
            ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {
            'id': self.id,
            'out_id': self.out.id,
            'value': self._array[0]
        })

    def get_right_indent(self) -> int:
        return 100

    def show_content(self, graph):
        ImGui.SetNextItemWidth(100)
        ImGui.SliderFloat(f'value##{id}', self._array, 0, 1)
        self.out.value = self._array[0]


class FloatInputPin(InputPin[float]):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.value = 0

    def set_value(self, value: float):
        if isinstance(value, (int, float)):
            self.value = value


class RgbMuxerPin(OutputPin[Optional[Tuple[float, float, float]]]):
    def __init__(self, id: int):
        super().__init__(id, 'muxer')
        self.value = None

    def get_value(self, node: 'RgbMuxerNode') -> Tuple[float, float, float]:
        return node.get_mux()


class RgbMuxerNode(Node):
    def __init__(self, id: int, r_id, g_id, b_id, out_id):
        self.r_input = FloatInputPin(r_id, 'r')
        self.g_input = FloatInputPin(g_id, 'g')
        self.b_input = FloatInputPin(b_id, 'b')
        self.out = RgbMuxerPin(out_id)
        super().__init__(id, 'muxer',
                         [self.r_input, self.g_input, self.b_input],
                         [self.out])

    @classmethod
    def imgui_menu(cls, graph, click_pos):
        if ImGui.MenuItem("muxer"):
            node = RgbMuxerNode(
                graph.get_next_id(),
                graph.get_next_id(), graph.get_next_id(), graph.get_next_id(),
                graph.get_next_id())
            graph.nodes.append(node)
            ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {
            'id': self.id,
            'r_id': self.r_input.id,
            'g_id': self.g_input.id,
            'b_id': self.b_input.id,
            'out_id': self.out.id,
        })

    def get_mux(self) -> Tuple[float, float, float]:
        return (self.r_input.value, self.g_input.value, self.b_input.value)


class Float3InputPin(InputPin[Tuple[float, float, float]]):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.value: Tuple[float, float, float] = (0, 0, 0)

    def set_value(self, value: Tuple[float, float, float]):
        if value:
            self.value = value


class ColorOutNode(Node):
    def __init__(self, id: int, color_id) -> None:
        self.in_color = Float3InputPin(color_id, 'color')
        self._array = (ctypes.c_float * 3)()
        super().__init__(id, 'color', [self.in_color], [])

    @classmethod
    def imgui_menu(cls, graph, click_pos):
        if ImGui.MenuItem("output"):
            node = ColorOutNode(graph.get_next_id(), graph.get_next_id())
            graph.nodes.append(node)
            ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {
            'id': self.id,
            'color_id': self.in_color.id,
        })

    def show_content(self, graph):
        if self.in_color.value:
            if self.in_color.value:
                self._array[0] = self.in_color.value[0]
                self._array[1] = self.in_color.value[1]
                self._array[2] = self.in_color.value[2]
        ImGui.SetNextItemWidth(200)
        ImGui.ColorPicker3(f'color##{id}', self._array)


TYPES = [
    FloatOutputPin, FloatValueNode,
    FloatInputPin, RgbMuxerPin, RgbMuxerNode,
    Float3InputPin, ColorOutNode
]

PIN_STYLE_MAP: Dict[Type, PinStyle] = {
    Tuple[float, float, float]: PinStyle(
        ImNodes.ImNodesPinShape_.QuadFilled, color_int(255, 128, 128))
}
