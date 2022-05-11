from typing import NamedTuple, Optional, Dict, List, Iterable
import abc
import logging
import ctypes
import math
from OpenGL import GL
import glm
from pydear import glo
from pydear.scene.camera import Ray, Camera
from pydear.utils.mouse_event import MouseEvent
from .shader_vertex import Vertex, SHADER, LineVertex
from .aabb import AABB

LOGGER = logging.getLogger(__name__)
UP_RED = glm.vec3(0.9, 0.2, 0.2) * 0.5


class GizmoMesh:
    def __init__(self) -> None:
        self.matrix = glm.mat4()
        self.triangles = []
        self.lines = []


EPSILON = 1e-5


class Triangle(NamedTuple):
    v0: glm.vec3
    v1: glm.vec3
    v2: glm.vec3

    def intersect(self, ray: Ray) -> Optional[float]:
        return ray.intersect_triangle(self.v0, self.v1, self.v2)


class Quad(NamedTuple):
    t0: Triangle
    t1: Triangle

    @staticmethod
    def from_points(v0: glm.vec3, v1: glm.vec3, v2: glm.vec3, v3: glm.vec3) -> 'Quad':
        return Quad(
            Triangle(v0, v1, v2),
            Triangle(v2, v3, v0)
        )

    def intersect(self, ray: Ray) -> Optional[float]:
        h0 = self.t0.intersect(ray)
        if h0:
            h1 = self.t1.intersect(ray)
            if h1:
                if h0 < h1:
                    return h0
                else:
                    return h1
            else:
                return h0
        else:
            return self.t1.intersect(ray)


class Shape(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_color(self) -> glm.vec4:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_matrix(self) -> glm.mat4:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_quads(self) -> Iterable[Quad]:
        raise NotImplementedError()

    def intersect(self, ray: Ray) -> Optional[float]:
        to_local = glm.inverse(self.get_matrix())
        local_ray = Ray((to_local * glm.vec4(ray.origin, 1)).xyz,
                        (to_local * glm.vec4(ray.dir, 0)).xyz)
        hits = [quad.intersect(local_ray) for quad in self.get_quads()]
        hits = [hit for hit in hits if hit]
        if not hits:
            return None
        hits.sort()
        return hits[0]


class CubeShape(Shape):
    '''
        4 7
    0 3+-+
    +-+| |
    | |+-+
    +-+5 6
    1 2
    '''

    def __init__(self, width: float, height: float, depth: float, *, position: Optional[glm.vec3] = None, color=None) -> None:
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position
        x = self.width/2
        y = self.height/2
        z = self.depth/2
        v0 = glm.vec3(-x, y, z)
        v1 = glm.vec3(-x, -y, z)
        v2 = glm.vec3(x, -y, z)
        v3 = glm.vec3(x, y, z)
        v4 = glm.vec3(-x, y, -z)
        v5 = glm.vec3(-x, -y, -z)
        v6 = glm.vec3(x, -y, -z)
        v7 = glm.vec3(x, y, -z)
        self.quads = [
            Quad.from_points(v0, v1, v2, v3),
            Quad.from_points(v3, v2, v6, v7),
            Quad.from_points(v7, v6, v5, v4),
            Quad.from_points(v4, v5, v1, v0),
            Quad.from_points(v4, v0, v3, v7),
            Quad.from_points(v1, v5, v6, v2),
        ]

    def get_color(self) -> glm.vec4:
        return self.color

    def get_quads(self) -> Iterable[Quad]:
        return self.quads

    def get_matrix(self) -> glm.mat4:
        return glm.translate(self.position)


class RingShape(Shape):
    def __init__(self, theta, inner, outer, *, sections=20, color=None) -> None:
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        delta = theta/sections
        angle = 0
        angles = []
        for i in range(sections):
            angles.append(angle)
            angle += delta
        sin_cos = [(math.sin(angle), math.cos(angle)) for angle in angles]
        self.quads = []
        for i, (s0, c0) in enumerate(sin_cos):
            v0 = glm.vec3(c0, s0, 0)
            s1, c1 = sin_cos[(i+1) % sections]
            v1 = glm.vec3(c1, s1, 0)
            self.quads.append(Quad.from_points(
                v0*inner, v0*outer, v1*outer, v1*inner))

    def get_color(self) -> glm.vec4:
        return self.color

    def get_matrix(self) -> glm.mat4:
        return glm.mat4()

    def get_quads(self) -> Iterable[Quad]:
        return self.quads


class TriangleBuffer:
    def __init__(self) -> None:
        self.shader: Optional[glo.Shader] = None
        self.props = []
        self.view_projection = glm.mat4()
        self.vertices = (Vertex * 65535)()
        self.vertex_count = 0
        self.bone_vertex_map: Dict[int, List[int]] = {}
        self.indices = (ctypes.c_uint16 * 65535)()
        self.index_count = 0
        self.vao: Optional[glo.Vao] = None
        self.skin = glm.array.zeros(200, glm.mat4)
        self.skin[0] = glm.mat4()
        self.hover_index = -1
        self.select_index = -1

    def add_vertex(self, bone: int, v: glm.vec3, n: glm.vec3, c: glm.vec4) -> int:
        i = self.vertex_count
        self.vertices[i] = Vertex(
            v.x, v.y, v.z, bone, c.r, c.g, c.b, c.a, n.x, n.y, n.z)
        self.vertex_count += 1
        vertices = self.bone_vertex_map.get(bone)

        if not vertices:
            vertices = []
            self.bone_vertex_map[bone] = vertices
        vertices.append(i)

        return i

    def add_triangle(self, bone: int, t: Triangle, color: glm.vec4):
        '''
        ccw
        '''
        v10 = t.v0-t.v1
        v12 = t.v2-t.v1
        n = glm.normalize(glm.cross(v10, v12))
        i0 = self.add_vertex(bone, t.v0, n, color)
        i1 = self.add_vertex(bone, t.v1, n, color)
        i2 = self.add_vertex(bone, t.v2, n, color)
        self.indices[self.index_count] = i0
        self.index_count += 1
        self.indices[self.index_count] = i1
        self.index_count += 1
        self.indices[self.index_count] = i2
        self.index_count += 1

    def add_quad(self, bone: int, quad: Quad, color: glm.vec4):
        self.add_triangle(bone, quad.t0, color)
        self.add_triangle(bone, quad.t1, color)

    def add_shape(self, bone: int, shape: Shape):
        color = shape.get_color()
        for quad in shape.get_quads():
            self.add_quad(bone, quad, color)
        self.skin[bone] = shape.get_matrix()

    def set_color(self, bone, r, g, b):
        if bone < 0:
            return
        indices = self.bone_vertex_map[bone]
        for i in indices:
            v = self.vertices[i]
            v.r = r
            v.g = g
            v.b = b

    def select_hover(self, select_index: int,  hover_index: int):
        self.set_color(hover_index, 0.5, 1, 0.5)
        self.set_color(select_index, 1, 0.5, 0.5)
        if self.hover_index != select_index and self.hover_index != hover_index:
            self.set_color(self.hover_index, 1, 1, 1)
        if self.select_index != select_index and self.select_index != hover_index:
            self.set_color(self.select_index, 1, 1, 1)
        self.hover_index = hover_index
        self.select_index = select_index

    def render(self, camera: Camera):
        if not self.shader:
            # shader
            shader_or_error = glo.Shader.load_from_pkg("pydear", SHADER)
            if not isinstance(shader_or_error, glo.Shader):
                LOGGER.error(shader_or_error)
                raise Exception()
            self.shader = shader_or_error

            # uVP
            vp = glo.UniformLocation.create(self.shader.program, "uVP")

            def set_vp():
                vp.set_mat4(glm.value_ptr(self.view_projection))
            self.props.append(set_vp)

            # uBoneMatrices
            skin = glo.UniformLocation.create(
                self.shader.program, "uBoneMatrices")

            def set_skin():
                skin.set_mat4(self.skin.ptr, count=len(self.skin))
            self.props.append(set_skin)

            # vao
            vbo = glo.Vbo()
            vbo.set_vertices(self.vertices, is_dynamic=True)
            ibo = glo.Ibo()
            ibo.set_indices(self.indices, is_dynamic=True)
            self.vao = glo.Vao(
                vbo, glo.VertexLayout.create_list(self.shader.program), ibo)

        else:
            assert self.vao
            self.vao.vbo.update(self.vertices)
            assert self.vao.ibo
            self.vao.ibo.update(self.indices)

        self.view_projection = camera.projection.matrix * camera.view.matrix

        assert self.vao

        with self.shader:
            for prop in self.props:
                prop()
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_CULL_FACE)
            self.vao.draw(
                self.index_count, topology=GL.GL_TRIANGLES)


class Gizmo:
    '''
    [triangles] の登録
    * 1weight skinning
    * cube
    * ring
    * bone
    * rgba
    * normal diffuse + ambient

    [lines] の登録
    * 1weight skinning
    * axis
    * rgba

    [mouse event]
    cursor ray の[triangles]に対するあたり判定 => hover(highlight)
    hover に対する click(selector)/drag(manipulator) 
    '''

    def __init__(self) -> None:
        self.vertex_buffer = TriangleBuffer()
        self.mouse_event = None
        self.shapes: List[Shape] = []
        self.selected = -1

    def bind_mouse_event(self, mouse_event: MouseEvent):
        '''
        use left mouse
        '''
        self.mouse_event = mouse_event
        mouse_event.left_pressed.append(self.drag_begin)
        mouse_event.left_drag.append(self.drag)
        mouse_event.left_released.append(self.drag_end)

    def drag_begin(self, x, y):
        if self.vertex_buffer.hover_index >= 0:
            self.selected = self.vertex_buffer.hover_index
        else:
            self.selected = -1

    def drag(self, x, y, dx, dy):
        pass

    def drag_end(self, x, y):
        self.mouse_clicked = True

    def add_shape(self, shape: Shape, *, draggable=False) -> int:
        key = len(self.shapes)
        self.shapes.append(shape)

        self.vertex_buffer.add_shape(key, shape)

        return key

    def process(self, camera: Camera, x, y):
        self.vertex_buffer.render(camera)

        # update hover
        ray = camera.get_mouse_ray(x, y)
        hit_shape_index = -1
        hit_distance = 0
        for i, shape in enumerate(self.shapes):
            distance = shape.intersect(ray)
            if distance:
                if (hit_shape_index == -1) or (distance < hit_distance):
                    hit_shape_index = i
                    hit_distance = distance

        self.vertex_buffer.select_hover(self.selected, hit_shape_index)

    # def line(self, p0: glm.vec3, p1: glm.vec3):
    #     p0 = (self.matrix * glm.vec4(p0, 1)).xyz
    #     self.lines[self.line_count] = Vertex.pos_color(p0, self.color)
    #     self.line_count += 1

    #     p1 = (self.matrix * glm.vec4(p1, 1)).xyz
    #     self.lines[self.line_count] = Vertex.pos_color(p1, self.color)
    #     self.line_count += 1

    # def triangle(self, p0: glm.vec3, p1: glm.vec3, p2: glm.vec3, *, intersect=False) -> Optional[float]:
    #     p0 = (self.matrix * glm.vec4(p0, 1)).xyz
    #     p1 = (self.matrix * glm.vec4(p1, 1)).xyz
    #     p2 = (self.matrix * glm.vec4(p2, 1)).xyz

    #     self.triangles[self.triangle_count] = Vertex.pos_color(p0, self.color)
    #     self.triangle_count += 1

    #     self.triangles[self.triangle_count] = Vertex.pos_color(p1, self.color)
    #     self.triangle_count += 1

    #     self.triangles[self.triangle_count] = Vertex.pos_color(p2, self.color)
    #     self.triangle_count += 1

    #     if intersect:
    #         return self.ray.intersect_triangle(p0, p1, p2)

    # def quad(self, p0: glm.vec3, p1: glm.vec3, p2: glm.vec3, p3: glm.vec3, *, intersect=False) -> Optional[float]:
    #     i0 = self.triangle(p0, p1, p2, intersect=intersect)
    #     i1 = self.triangle(p2, p3, p0, intersect=intersect)

    #     if intersect:
    #         if i0 and i1:
    #             if i0 < i1:
    #                 return i0
    #             else:
    #                 return i1
    #         elif i0:
    #             return i0
    #         elif i1:
    #             return i1

    # def axis(self, size: float):
    #     origin = glm.vec3(0, 0, 0)
    #     # X
    #     self.color = glm.vec4(1, 0, 0, 1)
    #     self.line(origin, glm.vec3(size, 0, 0))
    #     self.color = glm.vec4(0.5, 0, 0, 1)
    #     self.line(origin, glm.vec3(-size, 0, 0))
    #     # Y
    #     self.color = glm.vec4(0, 1, 0, 1)
    #     self.line(origin, glm.vec3(0, size, 0))
    #     self.color = glm.vec4(0, 0.5, 0, 1)
    #     self.line(origin, glm.vec3(0, -size, 0))
    #     # Z
    #     self.color = glm.vec4(0, 0, 1, 1)
    #     self.line(origin, glm.vec3(0, 0, size))
    #     self.color = glm.vec4(0, 0, 0.5, 1)
    #     self.line(origin, glm.vec3(0, 0, -size))

    # def ground_mark(self):
    #     # 足元の軸表示
    #     WHITE = glm.vec4(1, 1, 1, 0.8)
    #     S = 0.5
    #     LINE_VERTICES = [
    #         # X
    #         LineVertex(glm.vec3(0, 0, 0), glm.vec4(1, 0, 0, 1)),
    #         LineVertex(glm.vec3(S, 0, 0), glm.vec4(1, 0, 0, 1)),
    #         LineVertex(glm.vec3(0, 0, 0), glm.vec4(0.5, 0, 0, 1)),
    #         LineVertex(glm.vec3(-S, 0, 0), glm.vec4(0.5, 0, 0, 1)),
    #         # Z
    #         LineVertex(glm.vec3(0, 0, 0), glm.vec4(0, 0, 1, 1)),
    #         LineVertex(glm.vec3(0, 0, S), glm.vec4(0, 0, 1, 1)),
    #         LineVertex(glm.vec3(0, 0, 0), glm.vec4(0, 0, 0.5, 1)),
    #         LineVertex(glm.vec3(0, 0, -S), glm.vec4(0, 0, 0.5, 1)),
    #         # box
    #         LineVertex(glm.vec3(-S, 0, -S), WHITE),
    #         LineVertex(glm.vec3(S, 0, -S), WHITE),
    #         LineVertex(glm.vec3(S, 0, -S), WHITE),
    #         LineVertex(glm.vec3(S, 0, S), WHITE),
    #         LineVertex(glm.vec3(S, 0, S), WHITE),
    #         LineVertex(glm.vec3(-S, 0, S), WHITE),
    #         LineVertex(glm.vec3(-S, 0, S), WHITE),
    #         LineVertex(glm.vec3(-S, 0, -S), WHITE),
    #         # front
    #         LineVertex(glm.vec3(S, 0, S+0.1),
    #                    WHITE), LineVertex(glm.vec3(0, 0, S+0.1+S), WHITE),
    #         LineVertex(glm.vec3(0, 0, S+0.1+S),
    #                    WHITE), LineVertex(glm.vec3(-S, 0, S+0.1), WHITE),
    #         LineVertex(glm.vec3(-S, 0, S+0.1),
    #                    WHITE), LineVertex(glm.vec3(S, 0, S+0.1), WHITE),
    #     ]
    #     for i in range(0, len(LINE_VERTICES), 2):
    #         head, tail = LINE_VERTICES[i:i+2]
    #         self.color = head.color
    #         self.line(head.position, tail.position)

    # def aabb(self, aabb: AABB):
    #     self.color = glm.vec4(1, 1, 1, 1)
    #     match aabb:
    #         case AABB(n, p):
    #             nx = n.x
    #             ny = n.y
    #             nz = n.z
    #             px = p.x
    #             py = p.y
    #             pz = p.z
    #             t0 = glm.vec3(nx, py, nz)
    #             t1 = glm.vec3(px, py, nz)
    #             t2 = glm.vec3(px, py, pz)
    #             t3 = glm.vec3(nx, py, pz)
    #             b0 = glm.vec3(nx, ny, nz)
    #             b1 = glm.vec3(px, ny, nz)
    #             b2 = glm.vec3(px, ny, pz)
    #             b3 = glm.vec3(nx, ny, pz)
    #             # top
    #             self.line(t0, t1)
    #             self.line(t1, t2)
    #             self.line(t2, t3)
    #             self.line(t3, t0)
    #             # bottom
    #             self.line(b0, b1)
    #             self.line(b1, b2)
    #             self.line(b2, b3)
    #             self.line(b3, b0)
    #             # side
    #             self.line(t0, b0)
    #             self.line(t1, b1)
    #             self.line(t2, b2)
    #             self.line(t3, b3)

    # def bone_octahedron(self, key, length: float, is_selected: bool = False) -> bool:
    #     '''
    #     return True if mouse clicked
    #     '''
    #     s = length * 0.1
    #     # head-tail
    #     #      0, -1(p1)
    #     # (p2)  |
    #     # -1, 0 |
    #     #     --+--->
    #     #       |    1, 0(p0)
    #     #       v
    #     #      0, +1(p3)
    #     self.color = glm.vec4(1, 0.0, 1, 1)
    #     h = glm.vec3(0, 0, 0)
    #     t = glm.vec3(0, length, 0)
    #     # self.line(h, t, bone.world_matrix)
    #     p0 = glm.vec3(s, s, 0)
    #     p1 = glm.vec3(0, s, -s)
    #     p2 = glm.vec3(-s, s, 0)
    #     p3 = glm.vec3(0, s, s)

    #     self.line(p0, p1)
    #     self.line(p1, p2)
    #     self.line(p2, p3)
    #     self.line(p3, p0)

    #     # self.line(p2, p0, bone.world_matrix)
    #     self.color = glm.vec4(1, 0, 0, 1)
    #     self.line(h, p0)
    #     self.line(p0, t)
    #     self.color = glm.vec4(0.1, 0, 0, 1)
    #     if is_selected:
    #         self.color = glm.vec4(0.1, 1, 0, 1)
    #     self.line(h, p2)
    #     self.line(p2, t)

    #     # self.line(p1, p3, bone.world_matrix)
    #     self.color = glm.vec4(0, 0, 1, 1)
    #     self.line(h, p3)
    #     self.line(p3, t)
    #     self.color = glm.vec4(0, 0, 0.1, 1)
    #     if is_selected:
    #         self.color = glm.vec4(0, 1, 0.1, 1)
    #     self.line(h, p1)
    #     self.line(p1, t)

    #     # triangles
    #     clicked = False
    #     self.color = glm.vec4(0.5, 0.5, 0.5, 0.2)
    #     if is_selected:
    #         self.color = glm.vec4(0.7, 0.7, 0, 0.7)
    #     elif self.hover_last == key:
    #         self.color = glm.vec4(0, 0.7, 0, 0.7)
    #         if self.mouse_clicked:
    #             clicked = True
    #             self.mouse_clicked = False

    #     triangles = (
    #         (p0, h, p1),
    #         (p1, h, p2),
    #         (p2, h, p3),
    #         (p3, h, p0),
    #         (p0, t, p1),
    #         (p1, t, p2),
    #         (p2, t, p3),
    #         (p3, t, p0),
    #     )

    #     any_hit = False
    #     for t in triangles:
    #         hit = self.triangle(*t, intersect=(not any_hit))
    #         if hit:
    #             self.hover = key
    #             any_hit = True

    #     return clicked

    # def bone_cube(self, key, w: float, h: float, length: float, *, is_selected: bool = False) -> bool:
    #     '''
    #     _X_
    #     w   A height _Y_
    #     i   |
    #     d   +------>
    #     t  /      /
    #     h +------> length _Z_
    #      /      /
    #     +------>
    #     '''
    #     clicked = False
    #     self.color = glm.vec4(0.5, 0.5, 0.5, 0.2)
    #     if is_selected:
    #         self.color = glm.vec4(0.7, 0.7, 0, 0.7)
    #     elif self.hover_last == key:
    #         self.color = glm.vec4(0, 0.7, 0, 0.7)
    #         if self.mouse_clicked:
    #             clicked = True
    #             self.mouse_clicked = False
    #     any_hit = False

    #     x = glm.vec3(1, 0, 0)
    #     y = glm.vec3(0, 0, 1)
    #     p0 = glm.vec3(0)
    #     p1 = glm.vec3(0, length, 0)
    #     p0_0 = p0-x*w-y*h
    #     p0_1 = p0+x*w-y*h
    #     p0_2 = p0+x*w+y*h
    #     p0_3 = p0-x*w+y*h
    #     p1_0 = p1-x*w-y*h
    #     p1_1 = p1+x*w-y*h
    #     p1_2 = p1+x*w+y*h
    #     p1_3 = p1-x*w+y*h
    #     # cap
    #     hit = self.quad(p1_0,
    #                     p1_3,
    #                     p1_2,
    #                     p1_1, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     hit = self.quad(p0_0,
    #                     p0_1,
    #                     p0_2,
    #                     p0_3, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     # left
    #     hit = self.quad(p0_0,
    #                     p0_3,
    #                     p1_3,
    #                     p1_0, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     # right
    #     hit = self.quad(p0_2,
    #                     p0_1,
    #                     p1_1,
    #                     p1_2, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     # bottom
    #     hit = self.quad(p0_1,
    #                     p0_0,
    #                     p1_0,
    #                     p1_1, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     # top
    #     self.color = UP_RED
    #     hit = self.quad(p0_3,
    #                     p0_2,
    #                     p1_2,
    #                     p1_3, intersect=True)
    #     if hit:
    #         self.hover = key
    #         any_hit = True

    #     return clicked

    # def bone_head_tail(self, key: str, head: glm.vec3, tail: glm.vec3, up: glm.vec3, *,
    #                    is_selected=False) -> bool:

    #     head_tail = tail - head
    #     y = glm.normalize(head_tail)
    #     x = glm.normalize(glm.cross(y, up))
    #     z = glm.normalize(glm.cross(x, y))

    #     self.matrix = glm.mat4(
    #         glm.vec4(x, 0),
    #         glm.vec4(y, 0),
    #         glm.vec4(z, 0),
    #         glm.vec4(head, 1))

    #     return self.bone_octahedron(key, glm.length(head_tail), is_selected)

    # def ring_yaw(self, m: glm.mat4, inner: float, outer: float, *, section=20):
    #     to_pi = math.pi / 180
    #     step = 360//section
    #     values = [degree * to_pi for degree in range(0, 360, step)]

    #     def theta_to_xy(theta):
    #         s = math.sin(theta)
    #         c = math.cos(theta)
    #         return (s, c)
    #     points = [theta_to_xy(theta) for theta in values]
    #     for i, (ix, iy) in enumerate(points):
    #         j = (i+1) % len(points)
    #         (jx, jy) = points[j]

    #         self.quad(
    #             glm.vec3(ix, iy, 0)*inner,
    #             glm.vec3(jx, jy, 0)*inner,
    #             glm.vec3(jx, jy, 0)*outer,
    #             glm.vec3(ix, iy, 0)*outer)

    # def ring_pitch(self, m: glm.mat4, inner: float, outer: float, *, section=20):
    #     to_pi = math.pi / 180
    #     step = 360//section
    #     values = [degree * to_pi for degree in range(0, 360, step)]

    #     def theta_to_xy(theta):
    #         s = math.sin(theta)
    #         c = math.cos(theta)
    #         return (s, c)
    #     points = [theta_to_xy(theta) for theta in values]
    #     for i, (ix, iy) in enumerate(points):
    #         j = (i+1) % len(points)
    #         (jx, jy) = points[j]

    #         self.quad(
    #             glm.vec3(0, ix, iy)*inner,
    #             glm.vec3(0, jx, jy)*inner,
    #             glm.vec3(0, jx, jy)*outer,
    #             glm.vec3(0, ix, iy)*outer)

    # def ring_roll(self, m: glm.mat4, inner: float, outer: float, *, section=20):
    #     to_pi = math.pi / 180
    #     step = 360//section
    #     values = [degree * to_pi for degree in range(0, 360, step)]

    #     def theta_to_xy(theta):
    #         s = math.sin(theta)
    #         c = math.cos(theta)
    #         return (s, c)
    #     points = [theta_to_xy(theta) for theta in values]
    #     for i, (ix, iy) in enumerate(points):
    #         j = (i+1) % len(points)
    #         (jx, jy) = points[j]

    #         self.quad(
    #             glm.vec3(ix, 0, iy)*inner,
    #             glm.vec3(jx, 0, jy)*inner,
    #             glm.vec3(jx, 0, jy)*outer,
    #             glm.vec3(ix, 0, iy)*outer)
