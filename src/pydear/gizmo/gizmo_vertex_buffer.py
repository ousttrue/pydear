from typing import Optional, Dict, List
import logging
import ctypes
import glm
from glglue import glo
from pydear.scene.camera import Camera
from .shader_vertex import Vertex, SHADER
from .primitive import Triangle, Quad
from .shapes.shape import Shape
from OpenGL import GL

LOGGER = logging.getLogger(__name__)


class GizmoVertexBuffer:
    def __init__(self) -> None:
        self.shader: Optional[glo.Shader] = None
        self.props = []
        self.view_projection = glm.mat4()

        self.vertices = (Vertex * 65535)()
        self.vertex_count = 0
        self.bone_vertex_map: Dict[int, List[int]] = {}
        self.indices = (ctypes.c_uint16 * 65535)()
        self.index_count = 0
        self.triangle_vao: Optional[glo.Vao] = None

        self.line_vertices = (Vertex * 65535)()
        self.line_count = 0
        self.bone_line_map: Dict[int, List[int]] = {}
        self.line_vao: Optional[glo.Vao] = None

        self.skin = glm.array.zeros(200, glm.mat4)

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

    def add_line_vertex(self, bone: int, v: glm.vec3, c: glm.vec4) -> int:
        i = self.line_count
        self.line_vertices[i] = Vertex(
            v.x, v.y, v.z, bone, c.r, c.g, c.b, c.a, 1, 1, 1)
        self.line_count += 1
        line_vertices = self.bone_line_map.get(bone)

        if not line_vertices:
            line_vertices = []
            self.bone_line_map[bone] = line_vertices
        line_vertices.append(i)
        return i

    def add_line(self, bone: int, v0: glm.vec3, v1: glm.vec3, color: glm.vec4):
        i0 = self.add_line_vertex(bone, v0, color)
        i1 = self.add_line_vertex(bone, v1, color)

    def add_shape(self, bone: int, shape: Shape):
        for quad, color in shape.get_quads():
            self.add_quad(bone, quad, color)

        for v0, v1, color in shape.get_lines():
            self.add_line(bone, v0, v1, color)

        # bind matrix

        def on_matrix(m):
            self.skin[bone] = m
        shape.matrix += on_matrix
        self.skin[bone] = shape.matrix.value

        # bind state

        def on_state(state):
            indices = self.bone_vertex_map[shape.index]
            for i in indices:
                v = self.vertices[i]
                v.state = state.value
        shape.state += on_state

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
            vertex_layout = glo.VertexLayout.create_list(self.shader.program)
            vbo = glo.Vbo()
            vbo.set_vertices(self.vertices, is_dynamic=True)
            ibo = glo.Ibo()
            ibo.set_indices(self.indices, is_dynamic=True)
            self.triangle_vao = glo.Vao(
                vbo, vertex_layout, ibo)

            line_vbo = glo.Vbo()
            line_vbo.set_vertices(self.line_vertices, is_dynamic=True)
            self.line_vao = glo.Vao(
                line_vbo, vertex_layout)
        else:
            assert self.triangle_vao
            self.triangle_vao.vbo.update(self.vertices)
            assert self.triangle_vao.ibo
            self.triangle_vao.ibo.update(self.indices)
            assert self.line_vao
            self.line_vao.vbo.update(self.line_vertices)

        self.view_projection = camera.projection.matrix * camera.view.matrix

        assert self.triangle_vao

        with self.shader:
            for prop in self.props:
                prop()
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glEnable(GL.GL_CULL_FACE)
            self.triangle_vao.draw(
                self.index_count, topology=GL.GL_TRIANGLES)
            self.line_vao.draw(
                self.line_count, topology=GL.GL_LINES)
