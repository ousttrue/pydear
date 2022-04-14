from typing import NamedTuple, List, Any, Optional, Callable
from OpenGL import GL
from .shader import Shader
from .vao import Vao


class Submesh:
    def __init__(self, topology, *, draw_count=0, shader: Optional[Shader] = None, props: List[Callable[[], None]] = None) -> None:
        self.topology = topology
        self.draw_count = draw_count
        assert (not shader) or isinstance(shader, Shader)
        self.shader = shader
        self.properties = props


class Drawable:
    def __init__(self, vao: Vao) -> None:
        self.vao = vao
        self.submeshes: List[Submesh] = []

    def push_submesh(self, shader: Shader, draw_count: int, properties: list, *, topology=GL.GL_TRIANGLES):
        assert isinstance(shader, Shader)
        self.submeshes.append(
            Submesh(topology, shader=shader, draw_count=draw_count, props=properties))

    def draw(self):
        self.vao.bind()
        for submesh in self.submeshes:
            with submesh.shader:
                for prop in submesh.properties:
                    prop()
                self.vao.draw(submesh.draw_count, topology=submesh.topology)
        self.vao.unbind()
