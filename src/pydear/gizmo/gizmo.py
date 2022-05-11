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
from pydear.utils.eventproperty import EventProperty
from .shader_vertex import Vertex, SHADER, LineVertex
from .aabb import AABB


LOGGER = logging.getLogger(__name__)
UP_RED = glm.vec3(0.9, 0.2, 0.2) * 0.5
HOVER = 0x01
SELECTED = 0x02


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
    def __init__(self, is_draggable: bool) -> None:
        self.is_draggable = is_draggable
        self.matrix = glm.mat4()

    @abc.abstractmethod
    def get_color(self) -> glm.vec4:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_quads(self) -> Iterable[Quad]:
        raise NotImplementedError()

    def intersect(self, ray: Ray) -> Optional[float]:
        to_local = glm.inverse(self.matrix)
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
        super().__init__(False)
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
        self.matrix = glm.translate(self.position)

    def get_color(self) -> glm.vec4:
        return self.color

    def get_quads(self) -> Iterable[Quad]:
        return self.quads


class RingShape(Shape):
    def __init__(self, theta, inner, outer, *, sections=20, color=None) -> None:
        super().__init__(True)
        self.matrix = glm.mat4(0)
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
        self.skin[bone] = shape.matrix

    def set_state(self, bone, state):
        if bone < 0:
            return
        indices = self.bone_vertex_map[bone]
        for i in indices:
            v = self.vertices[i]
            v.state = state

    def select_hover(self, select_index: int,  hover_index: int):
        self.set_state(self.hover_index, 0)
        self.set_state(self.select_index, 0)
        if select_index == hover_index:
            self.set_state(hover_index, HOVER | SELECTED)
        else:
            self.set_state(hover_index, HOVER)
            self.set_state(select_index, SELECTED)
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


class DragContext:
    def __init__(self, x, y, *, manipulator: Shape, selected: Shape, set_matrix) -> None:
        self.manipulator = manipulator
        self.selected = selected
        self.x = x
        self.y = y
        self.init_matrix = selected.matrix
        self.set_matrix = set_matrix

    def drag(self, x, y, dx, dy):
        angle = (y - self.y) * 0.02
        self.selected.matrix = self.init_matrix * \
            glm.rotate(angle, glm.vec3(0, 0, 1))
        self.set_matrix(self.selected.matrix)


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
        self.selected = EventProperty[int](-1)
        self.drag_context = None

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
            shape = self.shapes[self.vertex_buffer.hover_index]
            if shape.is_draggable:
                def set_matrix(m):
                    self.vertex_buffer.skin[self.selected.value] = m
                self.drag_context = DragContext(x, y,
                                                manipulator=shape,
                                                selected=self.shapes[self.selected.value],
                                                set_matrix=set_matrix)
            else:
                self.selected.set(self.vertex_buffer.hover_index)
        else:
            self.selected.set(-1)

    def drag(self, x, y, dx, dy):
        if self.drag_context:
            self.drag_context.drag(x, y, dx, dy)

    def drag_end(self, x, y):
        self.drag_context = None

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

        self.vertex_buffer.select_hover(self.selected.value, hit_shape_index)
