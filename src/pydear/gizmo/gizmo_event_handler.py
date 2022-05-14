from typing import Optional
import abc
from pydear.utils.mouse_event import MouseEvent
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
