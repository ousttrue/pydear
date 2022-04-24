from typing import List
import asyncio
import logging
import ctypes
from pydear.utils.selector import Item
from pydear.utils import glfw_app
from pydear import glo
from pydear import imgui as ImGui
from pydear import imgui_internal as ImGuiInternal
import xyztile
import glm
from tile_texture_manager import TileTextureManager
import pathlib
HERE = pathlib.Path(__file__).absolute().parent

LOGGER = logging.getLogger(__name__)

vs = '''#version 330
in vec2 aPos;
in vec2 aUv;
out vec2 fUv;
uniform mat4 V;
void main()
{
    gl_Position = V * vec4(aPos, 0.0, 1.0);
    fUv = aUv;
}
'''

fs = '''#version 330
in vec2 fUv;
out vec4 FragColor;
uniform sampler2D ColorTexture;
void main()
{
    FragColor = texture(ColorTexture, fUv);    
}
'''


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('u', ctypes.c_float),
        ('v', ctypes.c_float),
    ]


SIZE = 100
VERTICES = (Vertex * 65536)()
INDICES = (ctypes.c_ushort * 65536)()
vpos = 0
for i in range(0, 65530, 6):
    INDICES[i] = vpos
    INDICES[i+1] = vpos+1
    INDICES[i+2] = vpos+2
    INDICES[i+3] = vpos+2
    INDICES[i+4] = vpos+3
    INDICES[i+5] = vpos
    vpos += 4


class XYZTile(Item):
    def __init__(self, loop: asyncio.AbstractEventLoop, base_url) -> None:
        super().__init__('xyztile')
        self._input = None
        self.map = xyztile.Map(1)
        self.p_open = (ctypes.c_bool * 1)(True)
        self.tiles: List[xyztile.Tile] = []
        self.texture_manager = TileTextureManager(
            loop,
            base_url,
            HERE.parent.parent / 'tile_cache'
        )

        self.shader = None
        self.vao = None

    def add_tile(self, i: int, tile: xyztile.Tile):
        self.tiles.append(tile)
        rect = tile.rect
        l = rect.left
        t = rect.top
        r = rect.right
        b = rect.bottom
        vpos = i*4
        VERTICES[vpos] = Vertex(l, b, 0, 1)
        VERTICES[vpos+1] = Vertex(r, b, 1, 1)
        VERTICES[vpos+2] = Vertex(r, t, 1, 0)
        VERTICES[vpos+3] = Vertex(l, t, 0, 0)

    def resize(self, w: int, h: int):
        self.map.view.aspect_ratio = w/h

    def wheel(self, d: int):
        self.map.view.wheel(d)

    def mouse_drag(self, x: int, y: int, dx: int, dy: int, left: bool, right: bool, middle: bool):
        if middle:
            self.map.view.drag(input.height, input.dx, input.dy)

    def mouse_release(self):
        pass

    def show(self):
        if not self.p_open[0]:
            return

        if ImGui.Begin('view info', self.p_open):

            ImGui.InputInt('zoom level', self.map.zoom_level)

            p = ctypes.cast(glm.value_ptr(self.view), ctypes.c_void_p).value
            ImGui.InputFloat4("view1", ctypes.c_void_p(p))  # type: ignore
            ImGui.InputFloat4("view2", ctypes.c_void_p(p+16))  # type: ignore
            ImGui.InputFloat4("view3", ctypes.c_void_p(p+32))  # type: ignore
            ImGui.InputFloat4("view4", ctypes.c_void_p(p+48))  # type: ignore

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
            if ImGui.BeginTable("tiles", 5, flags):
                # header
                # ImGui.TableSetupScrollFreeze(0, 1); // Make top row always visible
                ImGui.TableSetupColumn('index')
                ImGui.TableSetupColumn('left')
                ImGui.TableSetupColumn('top')
                ImGui.TableSetupColumn('right')
                ImGui.TableSetupColumn('bottom')
                ImGui.TableHeadersRow()

                # body
                for i, tile in enumerate(self.tiles):
                    ImGui.TableNextRow()
                    # index
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{i:03}:{tile.z}:{tile.x}:{tile.y}')
                    #
                    rect = tile.rect
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{rect.left}')
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{rect.top}')
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{rect.right}')
                    ImGui.TableNextColumn()
                    ImGui.TextUnformatted(f'{rect.bottom}')

                ImGui.EndTable()

        ImGui.End()

    def render(self):
        if not self.shader:
            shader_or_error = glo.Shader.load(vs, fs)
            if not isinstance(shader_or_error, glo.Shader):
                LOGGER.error(shader_or_error)
                return
            self.shader = shader_or_error

            vbo = glo.Vbo()
            vbo.set_vertices(VERTICES, True)
            ibo = glo.Ibo()
            ibo.set_indices(INDICES)
            self.vao = glo.Vao(
                vbo, glo.VertexLayout.create_list(self.shader.program), ibo)

            self.view = glm.mat4()
            view = glo.UniformLocation.create(self.shader.program, "V")

            def set_V():
                view.set_mat4(glm.value_ptr(self.view))
            self.props = [
                set_V
            ]

        assert self.vao
        self.tiles.clear()
        for i, tile in enumerate(self.map.iter_visible()):
            # setup vertices
            self.add_tile(i, tile)
        self.vao.vbo.update(VERTICES)
        self.view = self.map.view.get_matrix()

        with self.shader:
            for prop in self.props:
                prop()

            offset = 0
            for tile in self.tiles:
                texture = self.texture_manager.get_or_enqueue(tile)
                if texture:
                    texture.bind()
                self.vao.draw(6, offset)
                offset += 6 * 2


def main():
    logging.basicConfig(level=logging.DEBUG)
    from pydear.utils.loghandler import ImGuiLogHandler
    log_handler = ImGuiLogHandler()
    log_handler.setFormatter(logging.Formatter(
        '%(name)s:%(lineno)s[%(levelname)s]%(message)s'))
    log_handler.register_root()

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

    url = 'http://tile.openstreetmap.org'
    # url = None
    view = XYZTile(app.loop, url)

    bg = ImGui.ImVec4(1, 1, 1, 1)
    tint = ImGui.ImVec4(1, 1, 1, 1)

    def show_view(p_open):
        ImGui.PushStyleVar_2(ImGui.ImGuiStyleVar_.WindowPadding, (0, 0))
        if ImGui.Begin("render target", p_open,
                       ImGui.ImGuiWindowFlags_.NoScrollbar |
                       ImGui.ImGuiWindowFlags_.NoScrollWithMouse):
            w, h = ImGui.GetContentRegionAvail()
            texture = fbo_manager.clear(
                int(w), int(h), clear_color)
            if texture:

                ImGui.ImageButton(texture, (w, h), (0, 1), (1, 0), 0, bg, tint)
                ImGuiInternal.ButtonBehavior(ImGui.Custom_GetLastItemRect(), ImGui.Custom_GetLastItemId(), None, None,
                                             ImGui.ImGuiButtonFlags_.MouseButtonMiddle | ImGui.ImGuiButtonFlags_.MouseButtonRight)
                io = ImGui.GetIO()
                if ImGui.IsItemActive():
                    x, y = ImGui.GetWindowPos()
                    y += ImGui.GetFrameHeight()
                    view.mouse_drag(
                        int(io.MousePos.x-x), int(io.MousePos.y-y),
                        int(io.MouseDelta.x), int(io.MouseDelta.y),
                        io.MouseDown[0], io.MouseDown[1], io.MouseDown[2])
                else:
                    view.mouse_release()

                if ImGui.IsItemHovered():
                    view.wheel(int(io.MouseWheel))

                # rendering
                view.render()

        ImGui.End()
        ImGui.PopStyleVar()

        view.show()

    views = [
        dockspace.Dock('demo', ImGui.ShowDemoWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('metrics', ImGui.ShowMetricsWindow,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('hello', show_hello,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('view', show_view,
                       (ctypes.c_bool * 1)(True)),
        dockspace.Dock('log', log_handler.show,
                       (ctypes.c_bool * 1)(True)),
    ]

    gui = dockspace.DockingGui(app.loop, docks=views)
    from pydear.backends.impl_glfw import ImplGlfwInput
    impl_glfw = ImplGlfwInput(app.window)
    while app.clear():
        impl_glfw.process_inputs()
        gui.render()
    del gui


if __name__ == '__main__':
    main()
