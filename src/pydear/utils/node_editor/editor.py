from typing import Optional, Dict, Type, Tuple
import ctypes
from pydear import imgui as ImGui
from pydear import imnodes as ImNodes
from pydear.utils.setting import BinSetting
from .graph import Graph
from .node import Node, InputPin, OutputPin, Serialized, SHAPE_MAP, color_int


SETTING_KEY = 'imnodes'
SETTING_GRAPH_KEY = 'imnodes_graph'


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

    def to_json(self) -> Serialized:
        return Serialized(self.__class__.__name__, {
            'id': self.id,
            'out_id': self.out.id,
            'value': self._array[0]
        })

    def show_content(self, graph):
        ImGui.SetNextItemWidth(200)
        ImGui.SliderFloat(f'value##{id}', self._array, 0, 1)
        self.out.value = self._array[0]


class FloatInputPin(InputPin[float]):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.value = 0

    def set_value(self, value: float):
        if isinstance(value, (int, float)):
            self.value = value


class RgbMuxerPin(OutputPin[Tuple[float, float, float]]):
    def __init__(self, id: int):
        super().__init__(id, 'muxer')
        self.value = (0.0, 0.0, 0.0)

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

                # register befor load
                SHAPE_MAP[Tuple[float, float, float]
                          ] = (ImNodes.ImNodesPinShape_.QuadFilled, color_int(255, 128, 128))
                self.register_type(FloatInputPin)
                self.register_type(FloatValueNode)
                self.register_type(FloatInputPin)
                self.register_type(RgbMuxerPin)
                self.register_type(RgbMuxerNode)
                self.register_type(Float3InputPin)
                self.register_type(ColorOutNode)
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

            if ImGui.MenuItem("input"):
                node = FloatValueNode(next_id(), next_id())
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.MenuItem("----")

            if ImGui.MenuItem("output"):
                node = ColorOutNode(next_id(), next_id())
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.MenuItem("----")

            if ImGui.MenuItem("muxer"):
                node = RgbMuxerNode(
                    next_id(),
                    next_id(), next_id(), next_id(),
                    next_id())
                self.graph.nodes.append(node)
                ImNodes.SetNodeScreenSpacePos(node.id, click_pos)

            ImGui.EndPopup()
        ImGui.PopStyleVar()
