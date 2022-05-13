from typing import Optional
import abc
import glm
from pydear.utils.eventproperty import EventProperty
from pydear.utils.mouse_event import MouseEvent
from .shapes.shape import Shape, ShapeState
from .gizmo import Gizmo, RayHit


class GizmoEventHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def drag_begin(self, hit: RayHit):
        pass

    @abc.abstractmethod
    def drag(self, x, y, dx, dy):
        pass

    @abc.abstractmethod
    def drag_end(self, x, y):
        pass

    def bind_mouse_event_with_gizmo(self, mouse_event: MouseEvent, gizmo: Gizmo):
        def drag_begin(x, y):
            self.drag_begin(gizmo.hit)
        mouse_event.left_pressed.append(drag_begin)
        mouse_event.left_drag.append(self.drag)
        mouse_event.left_released.append(self.drag_end)


class GizmoSelectHandler(GizmoEventHandler):
    def __init__(self) -> None:
        self.selected = EventProperty[Optional[Shape]](None)

    def drag_begin(self, hit: RayHit):
        self.select(hit)

    def drag(self, x, y, dx, dy):
        pass

    def drag_end(self, x, y):
        pass

    def select(self, hit: RayHit):
        shape = hit.shape
        if shape != self.selected.value:
            # clear
            if self.selected.value:
                self.selected.value.remove_state(ShapeState.SELECT)
            # select
            self.selected.set(shape)
            if shape:
                shape.add_state(ShapeState.SELECT)


class DragContext:
    def __init__(self, x, y, manipulator, target: Shape):
        self.y = y
        assert(manipulator)
        self.manipulator = manipulator
        self.manipulator.add_state(ShapeState.DRAG)
        assert target
        self.target = target
        self.init_matrix = target.matrix.value

    def drag(self, x: int, y: int):
        angle = (y - self.y) * 0.02
        if self.target:
            self.target.matrix.set(
                self.init_matrix * glm.rotate(angle, glm.vec3(0, 0, 1)))

    def end(self):
        self.manipulator.remove_state(ShapeState.DRAG)
        self.manipulator = None


class DragEventHandler(GizmoEventHandler):
    def __init__(self, gizmo: Gizmo) -> None:
        super().__init__()
        self.selected = EventProperty[Optional[Shape]](None)

        # draggable
        from pydear.gizmo.shapes.ring_shape import RingShape
        self.ring = RingShape(inner=0.4, outer=0.6, depth=0.02,
                              color=glm.vec4(0.3, 0.3, 1, 1))
        gizmo.add_shape(self.ring)

        self.context = None

    def drag_begin(self, hit: RayHit):
        if hit.shape == self.ring:
            # ring is not selectable
            self.context = DragContext(
                hit.x, hit.y, hit.shape, self.selected.value)
        else:
            self.select(hit)

    def drag(self, x, y, dx, dy):
        if self.context:
            self.context.drag(x, y)

    def drag_end(self, x, y):
        if self.context:
            self.context.end()
            self.context = None

    def select(self, hit: RayHit):
        shape = hit.shape
        if shape != self.selected.value:
            # clear
            if self.selected.value:
                self.selected.value.remove_state(ShapeState.SELECT)
            # select
            self.selected.set(shape)
            if shape:
                shape.add_state(ShapeState.SELECT)
                self.ring.matrix.set(shape.matrix.value)
                self.ring.remove_state(ShapeState.HIDE)
            else:
                self.ring.add_state(ShapeState.HIDE)
