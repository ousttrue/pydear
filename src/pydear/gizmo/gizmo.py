from lib2to3.pgen2.token import OP
from typing import Optional, Dict, List, NamedTuple
import glm
from pydear.scene.camera import Camera, Ray
from .shapes.shape import Shape, ShapeState
from .gizmo_vertex_buffer import GizmoVertexBuffer


class RayHit(NamedTuple):
    cursor_pos: glm.vec2
    ray: Ray
    shape: Optional[Shape]
    distance: float


class Gizmo:
    def __init__(self) -> None:
        self.vertex_buffer = GizmoVertexBuffer()
        self.shapes: List[Shape] = []
        self.hit = RayHit(glm.vec2(), Ray(glm.vec3(), glm.vec3()),
                          None, float('inf'))

    def add_shape(self, shape: Shape) -> int:
        key = len(self.shapes)
        self.shapes.append(shape)
        shape.index = key
        self.vertex_buffer.add_shape(key, shape)
        return key

    def process(self, camera: Camera, x, y):
        # render
        self.vertex_buffer.render(camera)

        # ray intersect
        ray = camera.get_mouse_ray(x, y)
        hit_shape = None
        hit_distance = float('inf')
        for i, shape in enumerate(self.shapes):
            distance = shape.intersect(ray)
            if distance:
                if distance < hit_distance:
                    hit_shape = shape
                    hit_distance = distance

        # update hover
        hover_shape = self.hit.shape if self.hit else None
        if hit_shape != hover_shape:
            if hover_shape:
                hover_shape.remove_state(ShapeState.HOVER)

        self.hit = RayHit(glm.vec2(x, y), ray,
                          hit_shape, hit_distance)
        if self.hit.shape:
            self.hit.shape.add_state(ShapeState.HOVER)
