from typing import Optional
from .gizmo import RayHit
from .shapes.shape import Shape, ShapeState
from .gizmo_event_handler import GizmoEventHandler
from pydear.utils.eventproperty import EventProperty


class GizmoSelectHandler(GizmoEventHandler):
    def __init__(self) -> None:
        self.selected = EventProperty[Optional[Shape]](None)

    def drag_begin(self, hit: RayHit):
        '''
        select when mouse down
        '''
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

    def drag(self, x, y, dx, dy):
        pass

    def drag_end(self, x, y):
        pass
