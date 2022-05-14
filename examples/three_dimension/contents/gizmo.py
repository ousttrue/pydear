'''
simple triangle sample
'''
from typing import Optional
import pathlib
import logging
import glm
from pydear.utils.selector import Item
from pydear.scene.camera import Camera, MouseEvent
from pydear.gizmo.gizmo import Gizmo
from pydear.gizmo.gizmo_drag_handler import GizmoDragHandler
from pydear.utils.nanovg_renderer import NanoVgRenderer, nvg_line_from_to
LOGGER = logging.getLogger(__name__)


class GizmoScene(Item):
    def __init__(self, mouse_event: MouseEvent, *, font: pathlib.Path) -> None:
        super().__init__('gizmo')
        self.camera = Camera()
        self.mouse_event = mouse_event
        self.camera.bind_mouse_event(self.mouse_event)

        self.nvg = NanoVgRenderer(font)

        # gizmo shapes
        self.gizmo = Gizmo()
        from pydear.gizmo.shapes.cube_shape import CubeShape
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                cube = CubeShape(0.5, 0.5, 0.5,
                                 position=glm.vec3(i, j, 0))
                self.gizmo.add_shape(cube)

        # mouse event handling
        self.handler = GizmoDragHandler(self.gizmo, self.camera)
        self.handler.bind_mouse_event_with_gizmo(
            self.mouse_event, self.gizmo)

    def render(self, w, h):
        self.camera.projection.resize(w, h)
        input = self.mouse_event.last_input
        assert(input)
        self.gizmo.process(self.camera, input.x, input.y)

        context = self.handler.context
        if context:
            start = context.start_screen_pos
            with self.nvg.render(w, h) as vg:
                nvg_line_from_to(vg, start.x, start.y, input.x, input.y)
                if not context.edge:
                    a = context.left
                    b = context.right
                    nvg_line_from_to(vg, a.x, a.y, b.x, b.y)

    def show(self):
        pass
