from typing import Iterable, Tuple
import math
import glm
from ..primitive import Quad
from .shape import Shape, ShapeState


class RingShape(Shape):
    def __init__(self, *, axis: glm.vec3, start: glm.vec3, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(glm.mat4(0))
        self.state.set(ShapeState.HIDE)
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        delta = theta/sections
        angle = 0
        vertices = []
        for i in range(sections):
            vertices.append(glm.angleAxis(angle, axis) * start)
            angle += delta
        self.quads = []

        d = axis * depth * 0.5
        for i, v in enumerate(vertices):
            vv = vertices[(i+1) % sections]
            v0 = d + v * inner
            v1 = d + v * outer
            v2 = d + vv * outer
            v3 = d + vv * inner
            v4 = -d + v * inner
            v5 = -d + v * outer
            v6 = -d + vv * outer
            v7 = -d + vv * inner
            '''
                  v7 v6
            v3 v2 v4 v5
            v0 v1
            '''
            self.quads += [
                Quad.from_points(v0, v1, v2, v3),
                Quad.from_points(v1, v5, v6, v2),
                Quad.from_points(v7, v6, v5, v4),
            ]

    def get_quads(self) -> Iterable[Tuple[Quad, glm.vec4]]:
        for quad in self.quads:
            yield quad, self.color

    def get_lines(self):
        return []


class XRingShape(RingShape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(axis=glm.vec3(1, 0, 0), start=glm.vec3(0, 1, 0),
                         inner=inner, outer=outer,
                         depth=depth, theta=theta, sections=sections, color=color)


class YRingShape(RingShape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(axis=glm.vec3(0, 1, 0), start=glm.vec3(0, 0, 1),
                         inner=inner, outer=outer,
                         depth=depth, theta=theta, sections=sections, color=color)


class ZRingShape(RingShape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(axis=glm.vec3(0, 0, 1), start=glm.vec3(1, 0, 0),
                         inner=inner, outer=outer,
                         depth=depth, theta=theta, sections=sections, color=color)
