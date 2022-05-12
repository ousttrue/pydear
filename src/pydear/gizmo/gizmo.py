from typing import Optional, Dict, List
import glm
from pydear.scene.camera import Camera
from pydear.utils.mouse_event import MouseEvent
from pydear.utils.eventproperty import EventProperty
from .shapes.shape import Shape, ShapeState
from .shapes.cube_shape import CubeShape
from .shapes.ring_shape import RingShape
from .triangle_buffer import TriangleBuffer


class DragContext:
    def __init__(self, x, y, *, manipulator: Shape, selected: Shape) -> None:
        self.manipulator = manipulator
        self.manipulator.add_state(ShapeState.DRAG)
        assert selected
        self.selected = selected
        self.x = x
        self.y = y
        self.init_matrix = selected.matrix.value

    def drag(self, x, y, dx, dy):
        angle = (y - self.y) * 0.02
        self.selected.matrix.set(
            self.init_matrix * glm.rotate(angle, glm.vec3(0, 0, 1)))

    def end(self):
        self.manipulator.remove_state(ShapeState.DRAG)


class Gizmo:
    '''
    [triangles] の登録
    * 1weight skinning
    * cube
    * ring
    * bone
    * rgba
    * normal diffuse + ambient

    [lines] の登録
    * 1weight skinning
    * axis
    * rgba

    [mouse event]
    cursor ray の[triangles]に対するあたり判定 => hover(highlight)
    hover に対する click(selector)/drag(manipulator) 
    '''

    def __init__(self) -> None:
        self.vertex_buffer = TriangleBuffer()
        self.mouse_event = None
        self.shapes: List[Shape] = []
        self.selected: EventProperty[Optional[Shape]] = EventProperty(None)
        self.hover: Optional[Shape] = None
        self.drag_context = None

    def bind_mouse_event(self, mouse_event: MouseEvent):
        '''
        use left mouse
        '''
        self.mouse_event = mouse_event
        mouse_event.left_pressed.append(self.drag_begin)
        mouse_event.left_drag.append(self.drag)
        mouse_event.left_released.append(self.drag_end)

    def drag_begin(self, x, y):
        if self.hover:
            if self.hover.is_draggable:
                self.drag_context = DragContext(x, y,
                                                manipulator=self.hover,
                                                selected=self.selected.value)
            else:
                if self.hover != self.selected.value:
                    if selected := self.selected.value:
                        selected.remove_state(ShapeState.SELECT)
                    self.selected.set(self.hover)
                    self.hover.add_state(ShapeState.SELECT)
        else:
            if selected := self.selected.value:
                selected.remove_state(ShapeState.SELECT)
                self.selected.set(None)

    def drag(self, x, y, dx, dy):
        if self.drag_context:
            self.drag_context.drag(x, y, dx, dy)

    def drag_end(self, x, y):
        if self.drag_context:
            self.drag_context.end()
            self.drag_context = None

    def add_shape(self, shape: Shape) -> int:
        key = len(self.shapes)
        self.shapes.append(shape)
        shape.index = key
        self.vertex_buffer.add_shape(key, shape)
        return key

    def process(self, camera: Camera, x, y):
        # remder
        self.vertex_buffer.render(camera)

        # ray intersect
        ray = camera.get_mouse_ray(x, y)
        hit_shape = None
        hit_distance = 0
        for i, shape in enumerate(self.shapes):
            distance = shape.intersect(ray)
            if distance:
                if (not hit_shape) or (distance < hit_distance):
                    hit_shape = shape
                    hit_distance = distance

        # update hover
        if hit_shape != self.hover:
            if self.hover:
                self.hover.remove_state(ShapeState.HOVER)
            self.hover = hit_shape
            if self.hover:
                self.hover.add_state(ShapeState.HOVER)
