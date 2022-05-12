from typing import Iterable, Optional
import math
import abc
import glm
from pydear.scene.camera import Ray
from pydear.utils.eventproperty import EventProperty
from ..primitive import Quad


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




