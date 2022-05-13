from typing import Iterable
import math
import glm
from ..primitive import Quad
from .shape import Shape, ShapeState


class XRingShape(Shape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(glm.mat4(0), True)
        self.state.set(ShapeState.HIDE)
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        delta = theta/sections
        angle = 0
        angles = []
        for i in range(sections):
            angles.append(angle)
            angle += delta
        sin_cos = [(math.sin(angle), math.cos(angle)) for angle in angles]
        self.quads = []

        d = depth * 0.5
        for i, (s0, c0) in enumerate(sin_cos):
            s1, c1 = sin_cos[(i+1) % sections]
            v0 = glm.vec3(d, c0 * inner, s0 * inner)
            v1 = glm.vec3(d, c0 * outer, s0 * outer)
            v2 = glm.vec3(d, c1 * outer, s1 * outer)
            v3 = glm.vec3(d, c1 * inner, s1 * inner)
            v4 = glm.vec3(-d, c0 * inner, s0 * inner)
            v5 = glm.vec3(-d, c0 * outer, s0 * outer)
            v6 = glm.vec3(-d, c1 * outer, s1 * outer)
            v7 = glm.vec3(-d, c1 * inner, s1 * inner)
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

    def get_color(self) -> glm.vec4:
        return self.color

    def get_quads(self) -> Iterable[Quad]:
        return self.quads


class YRingShape(Shape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(glm.mat4(0), True)
        self.state.set(ShapeState.HIDE)
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        delta = theta/sections
        angle = 0
        angles = []
        for i in range(sections):
            angles.append(angle)
            angle += delta
        sin_cos = [(math.sin(angle), math.cos(angle)) for angle in angles]
        self.quads = []

        d = depth * 0.5
        for i, (s0, c0) in enumerate(sin_cos):
            s1, c1 = sin_cos[(i+1) % sections]
            v0 = glm.vec3(s0 * inner, d, c0 * inner)
            v1 = glm.vec3(s0 * outer, d, c0 * outer)
            v2 = glm.vec3(s1 * outer, d, c1 * outer)
            v3 = glm.vec3(s1 * inner, d, c1 * inner)
            v4 = glm.vec3(s0 * inner, -d, c0 * inner)
            v5 = glm.vec3(s0 * outer, -d, c0 * outer)
            v6 = glm.vec3(s1 * outer, -d, c1 * outer)
            v7 = glm.vec3(s1 * inner, -d, c1 * inner)
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

    def get_color(self) -> glm.vec4:
        return self.color

    def get_quads(self) -> Iterable[Quad]:
        return self.quads


class ZRingShape(Shape):
    def __init__(self, *, inner: float, outer: float, depth: float, theta: float = math.pi * 2, sections=20, color=None) -> None:
        super().__init__(glm.mat4(0), True)
        self.state.set(ShapeState.HIDE)
        self.color = color if color else glm.vec4(1, 1, 1, 1)
        delta = theta/sections
        angle = 0
        angles = []
        for i in range(sections):
            angles.append(angle)
            angle += delta
        sin_cos = [(math.sin(angle), math.cos(angle)) for angle in angles]
        self.quads = []

        d = depth * 0.5
        for i, (s0, c0) in enumerate(sin_cos):
            s1, c1 = sin_cos[(i+1) % sections]
            v0 = glm.vec3(c0 * inner, s0 * inner, d)
            v1 = glm.vec3(c0 * outer, s0 * outer, d)
            v2 = glm.vec3(c1 * outer, s1 * outer, d)
            v3 = glm.vec3(c1 * inner, s1 * inner, d)
            v4 = glm.vec3(c0 * inner, s0 * inner, -d)
            v5 = glm.vec3(c0 * outer, s0 * outer, -d)
            v6 = glm.vec3(c1 * outer, s1 * outer, -d)
            v7 = glm.vec3(c1 * inner, s1 * inner, -d)
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

    def get_color(self) -> glm.vec4:
        return self.color

    def get_quads(self) -> Iterable[Quad]:
        return self.quads
