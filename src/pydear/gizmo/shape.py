from typing import Iterable, Optional
import math
import abc
import glm
from pydear.scene.camera import Ray
from pydear.utils.eventproperty import EventProperty
from .primitive import Quad


class Shape(metaclass=abc.ABCMeta):
    def __init__(self, matrix: glm.mat4, is_draggable: bool) -> None:
        self.matrix = EventProperty[glm.mat4](matrix)
        self.is_draggable = is_draggable
        self.index = -1

    @abc.abstractmethod
    def get_color(self) -> glm.vec4:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_quads(self) -> Iterable[Quad]:
        raise NotImplementedError()

    def intersect(self, ray: Ray) -> Optional[float]:
        to_local = glm.inverse(self.matrix.value)
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
