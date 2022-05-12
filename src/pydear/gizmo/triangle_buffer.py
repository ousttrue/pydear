from typing import Optional, Dict, List
import logging
import ctypes
import glm
from pydear import glo
from pydear.scene.camera import Camera
from .shader_vertex import Vertex, SHADER
from .primitive import Triangle, Quad
from .shapes.shape import Shape
from OpenGL import GL

LOGGER = logging.getLogger(__name__)


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
