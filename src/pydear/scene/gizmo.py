from typing import NamedTuple, Optional
import logging
import ctypes
import math
from OpenGL import GL
import glm
from pydear import glo
from pydear.scene.camera import Ray

LOGGER = logging.getLogger(__name__)

VS = '''
#version 330
in vec3 aPosition;
in vec4 aColor;
out vec4 vColor;
uniform mediump mat4 vp;

void main() {
  gl_Position = vp * vec4(aPosition, 1);
  vColor = aColor;
}
'''

FS = '''
#version 330
in vec4 vColor;
out vec4 fColor;
void main() { fColor = vColor; }
'''


class AABB(NamedTuple):
    min: glm.vec3
    max: glm.vec3

    def __str__(self) -> str:
        return f'AABB({self.min}, {self.max})'

    def expand(self, rhs: 'AABB') -> 'AABB':
        min = self.min.copy()
        if rhs.min.x < min.x:
            min.x = rhs.min.x
        if rhs.min.y < min.y:
            min.y = rhs.min.y
        if rhs.min.z < min.z:
            min.z = rhs.min.z

        max = self.max.copy()
        if rhs.max.x > max.x:
            max.x = rhs.max.x
        if rhs.max.y > max.y:
            max.y = rhs.max.y
        if rhs.max.z > max.z:
            max.z = rhs.max.z

        return AABB(min, max)

    def transform(self, m: glm.mat4) -> 'AABB':
        p0 = (m * glm.vec4(self.min, 1)).xyz
        p1 = (m * glm.vec4(self.max, 1)).xyz
        min_x, max_x = (p0.x, p1.x) if p0.x < p1.x else (p1.x, p0.x)
        min_y, max_y = (p0.y, p1.y) if p0.y < p1.y else (p1.y, p0.y)
        min_z, max_z = (p0.z, p1.z) if p0.z < p1.z else (p1.z, p0.z)
        return AABB(glm.vec3(min_x, min_y, min_z), glm.vec3(max_x, max_y, max_z))

    @staticmethod
    def new_empty() -> 'AABB':
        return AABB(glm.vec3(float('inf'), float('inf'), float('inf')), -glm.vec3(float('inf'), float('inf'), float('inf')))


class Vertex(ctypes.Structure):

    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('r', ctypes.c_float),
        ('g', ctypes.c_float),
        ('b', ctypes.c_float),
        ('a', ctypes.c_float),
    ]

    @staticmethod
    def pos_color(p: glm.vec3, c: glm.vec4) -> 'Vertex':
        return Vertex(
            p.x,
            p.y,
            p.z,
            c.r,
            c.g,
            c.b,
            c.a,
        )


class Gizmo:
    def __init__(self) -> None:
        # state
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_down = False
        self.mouse_right_down = False
        self.mouse_middle_down = False
        self.camera_view = glm.mat4()
        self.camera_projection = glm.mat4()

        self.ray = Ray(glm.vec3(0, 0, 0), glm.vec3(0, 0, 1))

        self.matrix = glm.mat4()
        self.color = glm.vec4(1, 1, 1, 1)
        # event
        self.click_left = False

        self.line_shader: Optional[glo.Shader] = None
        self.line_props = []
        # lines
        self.lines = (Vertex * 65535)()
        self.line_count = 0
        self.line_drawable: Optional[glo.Vao] = None
        # triangles
        self.triangles = (Vertex * 65535)()
        self.triangle_count = 0
        self.triangle_drawable: Optional[glo.Vao] = None

        # hover selectable
        self.hover = None
        self.hover_last = None

    def begin(self, x: int, y: int, mouse_down: bool,
              view: glm.mat4, projection: glm.mat4, ray: Ray):
        # clear
        self.line_count = 0
        self.triangle_count = 0
        self.matrix = glm.mat4()
        self.color = glm.vec4(1, 1, 1, 1)
        # update
        self.click_left = self.mouse_down and not mouse_down

        self.mouse_x = x
        self.mouse_y = y
        self.mouse_down = mouse_down
        self.camera_view = view
        self.camera_projection = projection
        self.ray = ray

        self.hover_last = self.hover
        self.hover = None

    def end(self):
        if not self.line_shader:
            # shader
            shader_or_error = glo.Shader.load(VS, FS)
            if not isinstance(shader_or_error, glo.Shader):
                LOGGER.error(shader_or_error)
                raise Exception()
            self.line_shader = shader_or_error

            vp = glo.UniformLocation.create(self.line_shader.program, "vp")

            def set_vp():
                m = self.camera_projection * self.camera_view
                vp.set_mat4(glm.value_ptr(m))
            self.line_props.append(set_vp)

            # lines
            line_vbo = glo.Vbo()
            line_vbo.set_vertices(self.lines, is_dynamic=True)

            self.line_drawable = glo.Vao(
                line_vbo, glo.VertexLayout.create_list(self.line_shader.program))

            # vertices
            triangle_vbo = glo.Vbo()
            triangle_vbo.set_vertices(self.lines, is_dynamic=True)

            self.triangle_drawable = glo.Vao(
                triangle_vbo, glo.VertexLayout.create_list(self.line_shader.program))

        else:
            assert self.line_drawable
            self.line_drawable.vbo.update(self.lines)

            assert self.triangle_drawable
            self.triangle_drawable.vbo.update(self.triangles)

        assert self.line_drawable
        assert self.triangle_drawable

        with self.line_shader:
            for prop in self.line_props:
                prop()

            GL.glDisable(GL.GL_DEPTH_TEST)
            GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
            GL.glEnable(GL.GL_BLEND)
            self.triangle_drawable.draw(
                self.triangle_count, topology=GL.GL_TRIANGLES)
            GL.glDisable(GL.GL_BLEND)
            GL.glEnable(GL.GL_DEPTH_TEST)

            self.line_drawable.draw(self.line_count, topology=GL.GL_LINES)

    def line(self, p0: glm.vec3, p1: glm.vec3):
        p0 = (self.matrix * glm.vec4(p0, 1)).xyz
        self.lines[self.line_count] = Vertex.pos_color(p0, self.color)
        self.line_count += 1

        p1 = (self.matrix * glm.vec4(p1, 1)).xyz
        self.lines[self.line_count] = Vertex.pos_color(p1, self.color)
        self.line_count += 1

    def triangle(self, p0: glm.vec3, p1: glm.vec3, p2: glm.vec3, *, intersect=False):
        p0 = (self.matrix * glm.vec4(p0, 1)).xyz
        p1 = (self.matrix * glm.vec4(p1, 1)).xyz
        p2 = (self.matrix * glm.vec4(p2, 1)).xyz

        self.triangles[self.triangle_count] = Vertex.pos_color(p0, self.color)
        self.triangle_count += 1

        self.triangles[self.triangle_count] = Vertex.pos_color(p1, self.color)
        self.triangle_count += 1

        self.triangles[self.triangle_count] = Vertex.pos_color(p2, self.color)
        self.triangle_count += 1

        if intersect:
            return self.ray.intersect_triangle(p0, p1, p2)

    def quad(self, p0: glm.vec3, p1: glm.vec3, p2: glm.vec3, p3: glm.vec3):
        self.triangle(p0, p1, p2)
        self.triangle(p2, p3, p0)

    def axis(self, size: float):
        origin = glm.vec3(0, 0, 0)
        # X
        self.color = glm.vec4(1, 0, 0, 1)
        self.line(origin, glm.vec3(size, 0, 0))
        self.color = glm.vec4(0.5, 0, 0, 1)
        self.line(origin, glm.vec3(-size, 0, 0))
        # Y
        self.color = glm.vec4(0, 1, 0, 1)
        self.line(origin, glm.vec3(0, size, 0))
        self.color = glm.vec4(0, 0.5, 0, 1)
        self.line(origin, glm.vec3(0, -size, 0))
        # Z
        self.color = glm.vec4(0, 0, 1, 1)
        self.line(origin, glm.vec3(0, 0, size))
        self.color = glm.vec4(0, 0, 0.5, 1)
        self.line(origin, glm.vec3(0, 0, -size))

    def aabb(self, aabb: AABB):
        self.color = glm.vec4(1, 1, 1, 1)
        match aabb:
            case AABB(n, p):
                nx = n.x
                ny = n.y
                nz = n.z
                px = p.x
                py = p.y
                pz = p.z
                t0 = glm.vec3(nx, py, nz)
                t1 = glm.vec3(px, py, nz)
                t2 = glm.vec3(px, py, pz)
                t3 = glm.vec3(nx, py, pz)
                b0 = glm.vec3(nx, ny, nz)
                b1 = glm.vec3(px, ny, nz)
                b2 = glm.vec3(px, ny, pz)
                b3 = glm.vec3(nx, ny, pz)
                # top
                self.line(t0, t1)
                self.line(t1, t2)
                self.line(t2, t3)
                self.line(t3, t0)
                # bottom
                self.line(b0, b1)
                self.line(b1, b2)
                self.line(b2, b3)
                self.line(b3, b0)
                # side
                self.line(t0, b0)
                self.line(t1, b1)
                self.line(t2, b2)
                self.line(t3, b3)

    def bone(self, key, length: float, is_selected: bool = False) -> bool:
        '''
        return True if mouse clicked
        '''
        s = length * 0.1
        # head-tail
        #      0, -1(p1)
        # (p2)  |
        # -1, 0 |
        #     --+--->
        #       |    1, 0(p0)
        #       v
        #      0, +1(p3)
        self.color = glm.vec4(1, 0.0, 1, 1)
        h = glm.vec3(0, 0, 0)
        t = glm.vec3(0, length, 0)
        # self.line(h, t, bone.world_matrix)
        p0 = glm.vec3(s, s, 0)
        p1 = glm.vec3(0, s, -s)
        p2 = glm.vec3(-s, s, 0)
        p3 = glm.vec3(0, s, s)

        self.line(p0, p1)
        self.line(p1, p2)
        self.line(p2, p3)
        self.line(p3, p0)

        # self.line(p2, p0, bone.world_matrix)
        self.color = glm.vec4(1, 0, 0, 1)
        self.line(h, p0)
        self.line(p0, t)
        self.color = glm.vec4(0.1, 0, 0, 1)
        if is_selected:
            self.color = glm.vec4(0.1, 1, 0, 1)
        self.line(h, p2)
        self.line(p2, t)

        # self.line(p1, p3, bone.world_matrix)
        self.color = glm.vec4(0, 0, 1, 1)
        self.line(h, p3)
        self.line(p3, t)
        self.color = glm.vec4(0, 0, 0.1, 1)
        if is_selected:
            self.color = glm.vec4(0, 1, 0.1, 1)
        self.line(h, p1)
        self.line(p1, t)

        # triangles
        clicked = False
        self.color = glm.vec4(0.5, 0.5, 0.5, 0.2)
        if is_selected:
            self.color = glm.vec4(0.7, 0.7, 0, 0.7)
        elif self.hover_last == key:
            self.color = glm.vec4(0, 0.7, 0, 0.7)
            if self.click_left:
                clicked = True

        triangles = (
            (p0, h, p1),
            (p1, h, p2),
            (p2, h, p3),
            (p3, h, p0),
            (p0, t, p1),
            (p1, t, p2),
            (p2, t, p3),
            (p3, t, p0),
        )

        any_hit = False
        for t in triangles:
            hit = self.triangle(*t, intersect=(not any_hit))
            if hit:
                self.hover = key
                any_hit = True

        return clicked
