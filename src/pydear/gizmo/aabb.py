from typing import NamedTuple
import glm


class AABB(NamedTuple):
    min: glm.vec3
    max: glm.vec3

    def __str__(self) -> str:
        return f'AABB({self.min}, {self.max})'

    def expand(self, rhs: 'AABB') -> 'AABB':
        min = self.min.copy()
        if rhs.min.x < min.x:
            min.x = rhs.min.x
        if rhs.min.y < min.y:
            min.y = rhs.min.y
        if rhs.min.z < min.z:
            min.z = rhs.min.z

        max = self.max.copy()
        if rhs.max.x > max.x:
            max.x = rhs.max.x
        if rhs.max.y > max.y:
            max.y = rhs.max.y
        if rhs.max.z > max.z:
            max.z = rhs.max.z

        return AABB(min, max)

    def transform(self, m: glm.mat4) -> 'AABB':
        p0 = (m * glm.vec4(self.min, 1)).xyz
        p1 = (m * glm.vec4(self.max, 1)).xyz
        min_x, max_x = (p0.x, p1.x) if p0.x < p1.x else (p1.x, p0.x)
        min_y, max_y = (p0.y, p1.y) if p0.y < p1.y else (p1.y, p0.y)
        min_z, max_z = (p0.z, p1.z) if p0.z < p1.z else (p1.z, p0.z)
        return AABB(glm.vec3(min_x, min_y, min_z), glm.vec3(max_x, max_y, max_z))

    @staticmethod
    def new_empty() -> 'AABB':
        return AABB(glm.vec3(float('inf'), float('inf'), float('inf')), -glm.vec3(float('inf'), float('inf'), float('inf')))
