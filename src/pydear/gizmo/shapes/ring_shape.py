from typing import Iterable
import math
import glm
from ..primitive import Quad
from .shape import Shape


class RingShape(Shape):
    def __init__(self, theta, inner, outer, *, sections=20, color=None) -> None:
        super().__init__(glm.mat4(0), True)
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
