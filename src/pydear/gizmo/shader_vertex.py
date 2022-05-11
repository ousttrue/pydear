from typing import NamedTuple
import ctypes
import glm


SHADER = 'assets/gizmo'


class Vertex(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('bone', ctypes.c_float),
        ('r', ctypes.c_float),
        ('g', ctypes.c_float),
        ('b', ctypes.c_float),
        ('a', ctypes.c_float),
        ('nx', ctypes.c_float),
        ('ny', ctypes.c_float),
        ('nz', ctypes.c_float),
    ]

    @staticmethod
    def pos_color(p: glm.vec3, c: glm.vec4, *, bone: int = 0, normal: glm.vec3 = None) -> 'Vertex':
        if not normal:
            normal = glm.vec3(0, 1, 0)

        if isinstance(c, glm.vec3):
            return Vertex(
                p.x,
                p.y,
                p.z,
                bone,
                c.r,
                c.g,
                c.b,
                1,
                normal.x,
                normal.y,
                normal.z,
            )
        elif isinstance(c, glm.vec4):
            return Vertex(
                p.x,
                p.y,
                p.z,
                bone,
                c.r,
                c.g,
                c.b,
                c.a,
                normal.x,
                normal.y,
                normal.z,
            )
        else:
            raise NotImplementedError()


def LineVertex(p, c):
    return Vertex.pos_color(p, c)
