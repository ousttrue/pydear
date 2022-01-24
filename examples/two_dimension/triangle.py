'''
simple triangle sample
'''
import logging
import ctypes
from pydear import glo

logger = logging.getLogger(__name__)

vs = '''#version 330
in vec2 vPos;
in vec3 vCol;
out vec3 color;
void main()
{
    gl_Position = vec4(vPos, 0.0, 1.0);
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


class Triangle:
    def __init__(self) -> None:
        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return
        vbo = glo.Vbo()
        vbo.set_vertices(vertices)
        self.vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(self.shader.program))

    def render(self):
        if not self.shader:
            return
        with self.shader:
            self.vao.draw(3)
