from typing import NamedTuple, List, Any
from OpenGL import GL
from .shader import Shader, ShaderProp
from .vao import Vao


class Submesh(NamedTuple):
    shader: Shader
    draw_count: int
    properties: List[ShaderProp]
    topology: Any


class Drawable:
    def __init__(self, vao: Vao) -> None:
        self.vao = vao
        self.submeshes: List[Submesh] = []

    def push_submesh(self, shader: Shader, draw_count: int, properties: List[ShaderProp], *, topology=GL.GL_TRIANGLES):
        self.submeshes.append(Submesh(shader, draw_count, properties, topology))

    def draw(self):
        self.vao.bind()
        for submesh in self.submeshes:
            with submesh.shader:
                for prop in submesh.properties:
                    prop.update()
                self.vao.draw(submesh.draw_count, topology=submesh.topology)
        self.vao.unbind()
