'''
simple triangle sample
'''
from typing import Optional
import logging
import glm
from pydear.utils.selector import Item
from pydear.scene.camera import Camera, MouseEvent
from pydear.gizmo.gizmo import Gizmo
from pydear.gizmo.gizmo_event_handler import DragEventHandler

LOGGER = logging.getLogger(__name__)


class GizmoScene(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('gizmo')
        self.camera = Camera()
        self.mouse_event = mouse_event
        self.camera.bind_mouse_event(self.mouse_event)

        # gizmo shapes
        self.gizmo = Gizmo()
        from pydear.gizmo.shapes.cube_shape import CubeShape
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                cube = CubeShape(0.5, 0.5, 0.5,
                                 position=glm.vec3(i, j, 0))
                self.gizmo.add_shape(cube)

        # mouse event handling
        self.handler = DragEventHandler(self.gizmo)
        self.handler.bind_mouse_event_with_gizmo(
            self.mouse_event, self.gizmo)

    def render(self, w, h):
        self.camera.projection.resize(w, h)
        input = self.mouse_event.last_input
        assert(input)
        self.gizmo.process(self.camera, input.x, input.y)

    def show(self):
        pass
