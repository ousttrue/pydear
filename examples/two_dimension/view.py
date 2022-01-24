'''
Triangle with Orthogonal Matrix
'''
import logging
import ctypes
from pydear import glo
from pydear.utils.item import Input
from pydear import imgui as ImGui

logger = logging.getLogger(__name__)

vs = '''#version 330
in vec2 vPos;
in vec3 vCol;
out vec3 color;
uniform mat4 Matrix;
void main()
{
    gl_Position = Matrix * vec4(vPos, 0.0, 1.0);
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


vertices = (Vertex * 3)(
    Vertex(-0.6, -0.4, 1., 0., 0.),
    Vertex(0.6, -0.4, 0., 1., 0.),
    Vertex(0.,  0.6, 0., 0., 1.)
)


class View:
    def __init__(self) -> None:
        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return
        vbo = glo.Vbo()
        vbo.set_vertices(vertices)
        self.vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(self.shader.program))

        self.p_open = (ctypes.c_bool * 1)(True)
        self.input = None

    def on_input(self, input: Input):
        self.input = input

    def show(self):
        if not self.p_open[0]:
            return
        if ImGui.Begin('view info', self.p_open):
            if self.input:
                ImGui.TextUnformatted(f"{self.input}")
        ImGui.End()

    def render(self):
        if not self.shader:
            return
        with self.shader:
            self.vao.draw(3)
