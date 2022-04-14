from typing import Optional
'''
Triangle with Orthogonal Matrix
'''
import logging
import ctypes
from pydear import glo
from pydear.utils.item import Input, Item
from pydear import imgui as ImGui
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

vertices = (Vertex * 3)(
    Vertex(-SIZE, -SIZE, 1., 0., 0.),
    Vertex(SIZE, -SIZE, 0., 1., 0.),
    Vertex(0.,  SIZE, 0., 0., 1.)
)


class View(Item):
    def __init__(self) -> None:
        super().__init__('view')
        self._input = None

    def initialize(self):
        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return

        vbo = glo.Vbo()
        vbo.set_vertices(vertices)
        self.vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(self.shader.program))

        self.p_open = (ctypes.c_bool * 1)(True)
        self._input = None

        self.zoom = 1
        self.x = 0
        self.y = 0

        self.model = glm.mat4()
        model = glo.UniformLocation.create(self.shader.program, "M")
        self.view = glm.mat4()
        view = glo.UniformLocation.create(self.shader.program, "V")
        self.props = [
            glo.ShaderProp(lambda x: model.set_mat4(
                x), lambda:glm.value_ptr(self.model)),
            glo.ShaderProp(lambda x: view.set_mat4(
                x), lambda:glm.value_ptr(self.view)),
        ]

    def drag(self, input: Input):
        self._input = input

        if input.wheel < 0:
            self.zoom *= 1.1
        elif input.wheel > 0:
            self.zoom *= 0.9

        if input.middle:
            self.x -= input.dx * self.zoom
            self.y += input.dy * self.zoom

        w = input.width/2 * self.zoom
        h = input.height/2 * self.zoom

        self.view = glm.ortho(
            self.x-w, self.x+w,
            self.y-h, self.y+h,
            0, 1)

    def show(self):
        if not self.p_open[0]:
            return
        if ImGui.Begin('view info', self.p_open):
            input = self._input
            if input:
                ImGui.TextUnformatted(f"{self._input}")
                w = input.width/2
                h = input.height/2
                ImGui.TextUnformatted(f"{w}: {h}")

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
