from typing import Optional, Iterable
import glm
from ..primitive import Quad
from .shape import Shape


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
        if not position:
            position = glm.vec3(0)
        super().__init__(glm.translate(position), False)
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        self.width = width
        self.height = height
        self.depth = depth
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
