from typing import Optional

from pydear.utils.mouse_event import MouseInput
from .gizmo import RayHit
from .shapes.shape import Shape, ShapeState
from pydear.utils.eventproperty import EventProperty
from pydear.scene.camera import DragInterface
from .gizmo import Gizmo


class GizmoSelectHandler(DragInterface):
    def __init__(self, gizmo: Gizmo) -> None:
        self.gizmo = gizmo
        self.selected = EventProperty[Optional[Shape]](None)

    def begin(self, mouse_input: MouseInput):
        '''
        select when mouse down
        '''
        hit = self.gizmo.hit
        shape = hit.shape
        if shape == self.selected.value:
            return
        # clear
        if self.selected.value:
            self.selected.value.remove_state(ShapeState.SELECT)
        # select
        self.selected.set(shape)
        if shape:
            shape.add_state(ShapeState.SELECT)

    def drag(self, mouse_input, dx, dy):
        pass

    def end(self, mouse_input):
        pass
