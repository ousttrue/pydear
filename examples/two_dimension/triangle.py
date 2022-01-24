'''
simple triangle sample
'''
import logging
import ctypes
from pydear import glo

logger = logging.getLogger(__name__)

vs = '''#version 330
in vec3 vCol;
in vec2 vPos;
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


class Pipeline:
    def __init__(self, shader: glo.Shader) -> None:
        self.shader = shader
        self.MVP = glo.UniformLocation.create(shader.program, "MVP")


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
        self.pipeline = Pipeline(self.shader)
        vbo = glo.Vbo()
        vbo.set_vertices(vertices)

        # glo.AttributeLocation.create_list(self.shader.program)

        self.vao = glo.Vao(vbo, [
            glo.VertexLayout(glo.AttributeLocation.create(
                self.shader.program, 'vPos'), 2, ctypes.sizeof(Vertex), 0),
            glo.VertexLayout(glo.AttributeLocation.create(
                self.shader.program, 'vCol'), 3, ctypes.sizeof(Vertex), 8),
        ])

    def draw(self):
        if not self.shader:
            return
        self.shader.use()
        self.vao.draw(3)
        self.shader.unuse()
