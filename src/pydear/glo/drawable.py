from typing import NamedTuple, List
from .shader import Shader, ShaderProp
from .vao import Vao


class Submesh(NamedTuple):
    shader: Shader
    draw_count: int
    properties: List[ShaderProp]


class Drawable:
    def __init__(self, vao: Vao) -> None:
        self.vao = vao
        self.submeshes: List[Submesh] = []

    def push_submesh(self, shader: Shader, draw_count: int, properties: List[ShaderProp]):
        self.submeshes.append(Submesh(shader, draw_count, properties))

    def draw(self):
        self.vao.bind()
        for submesh in self.submeshes:
            with submesh.shader:
                for prop in submesh.properties:
                    prop.update()
                self.vao.draw(submesh.draw_count)
        self.vao.unbind()
