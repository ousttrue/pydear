'''
simple triangle sample
'''
from typing import List
import logging
import ctypes
from OpenGL import GL
import glm
from pydear import glo
from pydear.utils.item import Item, Input
from .camera import Camera

LOGGER = logging.getLogger(__name__)

vs = '''#version 330
in vec3 aPos;
in vec3 aNormal;
out vec3 vColor;
uniform mediump mat4 uView;
uniform mediump mat4 uProjection;

void main()
{
    //gl_Position = vec4(aPos, 1) * uView * uProjection;
    gl_Position = uProjection * uView * vec4(aPos, 1);

    // lambert
    vec3 L = normalize(vec3(1, 2, 3));
    vec3 N = normalize(aNormal);
    float v = max(dot(N, L), 0.2);    
    vColor = vec3(v, v, v);
}
'''

fs = '''#version 330
in vec3 vColor;
out vec4 FragColor;
void main()
{
    FragColor = vec4(vColor, 1.0);
}
'''


class Float3(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    ]


class Vertex(ctypes.Structure):
    _fields_ = [
        ('position', Float3),
        ('normal', Float3),
    ]


class MeshBuilder:
    def __init__(self) -> None:
        self.vertices: List[Vertex] = []

    def push_triangle(self, p0: glm.vec3, p1: glm.vec3, p2: glm.vec3, n: glm.vec3):
        self.vertices.append(
            Vertex(Float3(p0.x, p0.y, p0.z), Float3(n.x, n.y, n.z)))
        self.vertices.append(
            Vertex(Float3(p1.x, p1.y, p1.z), Float3(n.x, n.y, n.z)))
        self.vertices.append(
            Vertex(Float3(p2.x, p2.y, p2.z), Float3(n.x, n.y, n.z)))

    def push_quad(self, p0, p1, p2, p3):
        n = glm.cross(glm.normalize(p0-p1), glm.normalize(p2-p1))
        self.push_triangle(p0, p1, p2, n)
        self.push_triangle(p2, p3, p0, n)

    def create_vbo(self) -> glo.Vbo:
        vbo = glo.Vbo()
        vertices = (Vertex * len(self.vertices))(*self.vertices)
        vbo.set_vertices(vertices)
        return vbo


'''
OpenGL default is ccw

front back
0+-+3 4+-+7
 | |   | |
1+-+2 5+-+6
'''
SIZE = 0.6
VERTICES = [
    glm.vec3(-SIZE, SIZE, SIZE),
    glm.vec3(-SIZE, -SIZE, SIZE),
    glm.vec3(SIZE, -SIZE, SIZE),
    glm.vec3(SIZE, SIZE, SIZE),
    glm.vec3(-SIZE, SIZE, -SIZE),
    glm.vec3(-SIZE, -SIZE, -SIZE),
    glm.vec3(SIZE, -SIZE, -SIZE),
    glm.vec3(SIZE, SIZE, -SIZE),
]

QUADS = [
    (0, 1, 2, 3),  # front
    (3, 2, 6, 7),  # right
    (7, 6, 5, 4),  # back
    (4, 5, 1, 0),  # left
    (4, 0, 3, 7),  # top
    (2, 1, 5, 6),  # bottom
]


class Cube(Item):
    def __init__(self) -> None:
        super().__init__('cube')
        self.camera = Camera()

    def initialize(self) -> None:
        self.shader = glo.Shader.load(vs, fs)
        if not self.shader:
            return

        view = glo.UniformLocation.create(self.shader.program, "uView")

        projection = glo.UniformLocation.create(
            self.shader.program, "uProjection")
        self.props = [
            glo.ShaderProp(
                lambda x: view.set_mat4(x),
                lambda:glm.value_ptr(self.camera.view.matrix)),
            glo.ShaderProp(
                lambda x: projection.set_mat4(x),
                lambda:glm.value_ptr(self.camera.projection.matrix)),
        ]

        builder = MeshBuilder()
        for i0, i1, i2, i3 in QUADS:
            builder.push_quad(VERTICES[i0], VERTICES[i1],
                              VERTICES[i2], VERTICES[i3])
        vbo = builder.create_vbo()

        self.vao = glo.Vao(
            vbo, glo.VertexLayout.create_list(self.shader.program))

    def input(self, input: Input):
        self.camera.onResize(input.width, input.height)

        if input.left:
            self.camera.onLeftDown(input.x, input.y)
        else:
            self.camera.onLeftUp(input.x, input.y)

        if input.right:
            self.camera.onRightDown(input.x, input.y)
        else:
            self.camera.onRightUp(input.x, input.y)

        if input.middle:
            self.camera.onMiddleDown(input.x, input.y)
        else:
            self.camera.onMiddleUp(input.x, input.y)

        if input.wheel:
            self.camera.onWheel(-input.wheel)
        self.camera.onMotion(input.x, input.y)

    def render(self):
        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        if not self.is_initialized:
            self.initialize()
            self.is_initialized = True

        if not self.shader:
            return
        with self.shader:
            for prop in self.props:
                prop.update()
            self.vao.draw(36)
