
import logging
import dataclasses
import ctypes
from pydear.utils.item import Item, Input
from pydear import glo
from pydear import imgui as ImGui
import xyztile
import glm

logger = logging.getLogger(__name__)

vs = '''#version 330
in vec2 vPos;
in vec3 vCol;
out vec3 color;
uniform mat4 V;
uniform mat4 M;
void main()
{
    gl_Position = V * M * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
'''

fs = '''#version 330
in vec3 color;
out vec4 FragColor;
void main()
{
    FragColor = vec4(color, 1.0);
}
'''


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('r', ctypes.c_float),
        ('g', ctypes.c_float),
        ('b', ctypes.c_float),
    ]


SIZE = 100

vertices = (Vertex * 65536)()
indices = (ctypes.c_ushort * 65536)()


class XYZTile(Item):
    def __init__(self) -> None:
        super().__init__('xyztile')
        self._input = None
        self.map = xyztile.Map(3)
        self.p_open = (ctypes.c_bool * 1)(True)
        self.draw_count = 0
        self.tiles = []

    def add_tile(self, i: int, tile: xyztile.Tile):
        self.tiles.append(tile)

    def initialize(self):
        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return

        vbo = glo.Vbo()
        vbo.set_vertices(vertices, True)
        ibo = glo.Ibo()
        ibo.set_indices(indices)
        self.vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(self.shader.program), ibo)

        self.view = glm.mat4()
        view = glo.UniformLocation.create(self.shader.program, "V")
        self.props = [
            glo.ShaderProp(lambda x: view.set_mat4(
                x), lambda:glm.value_ptr(self.view)),
        ]

    def input(self, input: Input):
        if not self.is_initialized:
            return

        self._input = input

        if input.wheel:
            self.map.view.wheel(input.wheel)
        if input.middle:
            self.map.view.drag(input.height, input.dx, input.dy)

        self.tiles.clear()
        for i, tile in enumerate(self.map.iter_visible()):
            # setup vertices
            self.add_tile(i, tile)

        self.view = self.map.view.get_matrix()

    def show(self):
        if not self.p_open[0]:
            return

        if ImGui.Begin('view info', self.p_open):
            input = self._input
            if input:
                ImGui.TextUnformatted(f"{self.map}")

            # table
            flags = (
                ImGui.ImGuiTableFlags_.BordersV
                | ImGui.ImGuiTableFlags_.BordersOuterH
                | ImGui.ImGuiTableFlags_.Resizable
                | ImGui.ImGuiTableFlags_.RowBg
                | ImGui.ImGuiTableFlags_.NoBordersInBody
            )
            if ImGui.BeginTable("tiles", 4, flags):
                # header
                # ImGui.TableSetupScrollFreeze(0, 1); // Make top row always visible
                ImGui.TableSetupColumn('index')
                ImGui.TableSetupColumn('z')
                ImGui.TableSetupColumn('x')
                ImGui.TableSetupColumn('y')
                ImGui.TableHeadersRow()

                # body
                for i, tile in enumerate(self.tiles):
                    ImGui.TableNextRow()
                    # index
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{i:03}')
                    #
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{tile.z}')
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{tile.x}')
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{tile.y}')

                ImGui.EndTable()

        ImGui.End()

    def render(self):
        if not self.is_initialized:
            self.initialize()
            self.is_initialized = True

        if not self.shader:
            return
        with self.shader:
            for prop in self.props:
                prop.update()
            self.vao.draw(3)


@dataclasses.dataclass
class State:
    hover: bool


def main():
    logging.basicConfig(level=logging.DEBUG)

    from pydear.utils import glfw_app
    app = glfw_app.GlfwApp('tile')

    from pydear import imgui as ImGui
    from pydear.utils import dockspace
    clear_color = (ctypes.c_float * 4)(0.1, 0.2, 0.3, 1)
    fbo_manager = glo.FboRenderer()

    def show_hello(p_open):
        if ImGui.Begin('hello', p_open):
            ImGui.TextUnformatted('hello text')
            ImGui.SliderFloat4('clear color', clear_color, 0, 1)
            ImGui.ColorPicker4('color', clear_color)
        ImGui.End()

    view = XYZTile()
    state = State(False)

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:
                # input handling
                input = Input.get(state.hover, w, h)
                if input:
                    view.input(input)

                # rendering
                view.render()

                ImGui.BeginChild("_image_")
                ImGui.Image(texture, (w, h), (0, 1), (1, 0))
                state.hover = ImGui.IsItemHovered()
                ImGui.EndChild()
        ImGui.End()
        ImGui.PopStyleVar()

        view.show()

    views = [
        dockspace.Dock('demo', (ctypes.c_bool * 1)
                       (True), ImGui.ShowDemoWindow),
        dockspace.Dock('metrics', (ctypes.c_bool * 1)
                       (True), ImGui.ShowMetricsWindow),
        dockspace.Dock('hello', (ctypes.c_bool * 1)(True), show_hello),
        dockspace.Dock('view', (ctypes.c_bool * 1)(True), show_view),
    ]

    gui = dockspace.DockingGui(app.window, views)
    while app.clear():
        gui.render()
    del gui


if __name__ == '__main__':
    main()
