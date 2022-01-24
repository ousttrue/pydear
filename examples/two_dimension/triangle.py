import logging
import ctypes
from OpenGL import GL
from pydear import glo

logger = logging.getLogger(__name__)

vs = '''
#version 110
uniform mat4 MVP;
attribute vec3 vCol;
attribute vec2 vPos;
varying vec3 color;
void main()
{
    gl_Position = MVP * vec4(vPos, 0.0, 1.0);
    color = vCol;
}
'''

fs = '''
#version 110
varying vec3 color;
void main()
{
    gl_FragColor = vec4(color, 1.0);
}
'''


class Pipeline:
    def __init__(self, shader: glo.Shader) -> None:
        self.shader = shader
        self.MVP = glo.UniformVariable(shader.program, "MVP")
        self.vPos = glo.VertexAttribute(shader.program, "vPos")
        self.vCol = glo.VertexAttribute(shader.program, "vCol")


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
        self.pipeline = Pipeline(self.shader)
        self.vbo = glo.Vbo()
        self.vbo.set_vertices(vertices)

    def draw(self):
        self.vbo.bind()
        GL.glEnableVertexAttribArray(self.pipeline.vPos.locatin)
        GL.glVertexAttribPointer(self.pipeline.vPos.locatin, 2, GL.GL_FLOAT, GL.GL_FALSE,
                                 ctypes.sizeof(Vertex), ctypes.c_void_p(12))

        GL.glEnableVertexAttribArray(self.pipeline.vCol.locatin)
        GL.glVertexAttribPointer(self.pipeline.vCol.locatin, 3, GL.GL_FLOAT, GL.GL_FALSE,
                                 ctypes.sizeof(Vertex), ctypes.c_void_p(0))

        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
