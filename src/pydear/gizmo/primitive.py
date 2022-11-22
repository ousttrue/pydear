from typing import NamedTuple, Optional
import glm
from glglue.camera import Ray


class Triangle(NamedTuple):
    v0: glm.vec3
    v1: glm.vec3
    v2: glm.vec3

    def intersect(self, ray: Ray) -> Optional[float]:
        return ray.intersect_triangle(self.v0, self.v1, self.v2)


class Quad(NamedTuple):
    t0: Triangle
    t1: Triangle

    @staticmethod
    def from_points(v0: glm.vec3, v1: glm.vec3, v2: glm.vec3, v3: glm.vec3) -> 'Quad':
        return Quad(
            Triangle(v0, v1, v2),
            Triangle(v2, v3, v0)
        )

    def intersect(self, ray: Ray) -> Optional[float]:
        h0 = self.t0.intersect(ray)
        if h0:
            h1 = self.t1.intersect(ray)
            if h1:
                if h0 < h1:
                    return h0
                else:
                    return h1
            else:
                return h0
        else:
            return self.t1.intersect(ray)
