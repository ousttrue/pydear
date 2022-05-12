'''
simple triangle sample
'''
from typing import Optional
import logging
import glm
from pydear.utils.selector import Item
from pydear.utils.eventproperty import EventProperty
from pydear.scene.camera import Camera, MouseEvent
from pydear.gizmo.gizmo import Gizmo, RayHit
from pydear.gizmo.shapes.shape import Shape, ShapeState

LOGGER = logging.getLogger(__name__)


def gizmo_mouse_select(mouse_event: MouseEvent, gizmo: Gizmo) -> EventProperty[Optional[Shape]]:
    selected = EventProperty[Optional[Shape]](None)

    # select
    def select(hit: RayHit):
        shape = hit.shape
        if shape != selected.value:
            # clear
            if selected.value:
                selected.value.remove_state(ShapeState.SELECT)
            # select
            selected.set(shape)
            if shape:
                shape.add_state(ShapeState.SELECT)

    def drag_begin(x, y):
        select(gizmo.hit)

    mouse_event.left_pressed.append(drag_begin)
    return selected


class Drag:
    def __init__(self) -> None:
        self.manipulator = None
        self.target = None

    def begin(self, x: int, y: int, manipulator: Shape, target: Shape):
        self.x = x
        self.y = y
        self.manipulator = manipulator
        self.manipulator.add_state(ShapeState.DRAG)
        assert target
        self.target = target
        self.init_matrix = target.matrix.value

    def drag(self, x: int, y: int, dx: int, dy: int):
        if self.manipulator:
            angle = (y - self.y) * 0.02
            if self.target:
                self.target.matrix.set(
                    self.init_matrix * glm.rotate(angle, glm.vec3(0, 0, 1)))

    def drag_end(self, x: int, y: int):
        if self.manipulator:
            self.manipulator.remove_state(ShapeState.DRAG)
            self.manipulator = None


def gizmo_mouse_select_and_drag(mouse_event: MouseEvent, gizmo: Gizmo) -> EventProperty[Optional[Shape]]:
    selected = EventProperty[Optional[Shape]](None)

    # select
    def select(hit: RayHit):
        shape = hit.shape
        if shape != selected.value:
            # clear
            if selected.value:
                selected.value.remove_state(ShapeState.SELECT)
            # select
            selected.set(shape)
            if shape:
                shape.add_state(ShapeState.SELECT)

    # draggable
    from pydear.gizmo.shapes.ring_shape import RingShape
    ring = RingShape(inner=0.4, outer=0.6, depth=0.02,
                     color=glm.vec4(0.3, 0.3, 1, 1))
    gizmo.add_shape(ring)

    def on_selected(shape: Optional[Shape]):
        if shape:
            ring.matrix.set(shape.matrix.value)
            ring.remove_state(ShapeState.HIDE)
        else:
            ring.add_state(ShapeState.HIDE)
    selected += on_selected

    drag = Drag()

    def drag_begin(x, y):
        if gizmo.hit.shape == ring:
            # ring is not selectable
            drag.begin(x, y, ring, selected.value)
        else:
            select(gizmo.hit)

    mouse_event.left_pressed.append(drag_begin)
    mouse_event.left_drag.append(drag.drag)
    mouse_event.left_released.append(drag.drag_end)

    return selected


class GizmoScene(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('gizmo')
        self.camera = Camera()
        self.mouse_event = mouse_event
        self.camera.bind_mouse_event(self.mouse_event)
        self.gizmo = Gizmo()

        # gizmo shapes
        from pydear.gizmo.shapes.cube_shape import CubeShape
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                cube = CubeShape(0.5, 0.5, 0.5,
                                 position=glm.vec3(i, j, 0))
                self.gizmo.add_shape(cube)

        # mouse event handling
        if False:
            gizmo_mouse_select(self.mouse_event, self.gizmo)
        else:
            gizmo_mouse_select_and_drag(self.mouse_event, self.gizmo)

    def render(self, w, h):
        self.camera.projection.resize(w, h)
        input = self.mouse_event.last_input
        assert(input)
        self.gizmo.process(self.camera, input.x, input.y)

    def show(self):
        pass
