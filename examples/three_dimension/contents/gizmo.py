'''
simple triangle sample
'''
from typing import Optional, Iterable, Tuple, List
import pathlib
import logging
import glm
from pydear.utils.selector import Item
from glglue.camera.mouse_camera import MouseCamera, MouseEvent
from glglue.frame_input import FrameInput
from pydear.gizmo.gizmo import Gizmo
from pydear.gizmo.shapes.shape import Shape, Quad
from pydear.gizmo.gizmo_drag_handler import GizmoDragHandler
from pydear.utils.nanovg_renderer import NanoVgRenderer
LOGGER = logging.getLogger(__name__)


class XYSquare(Shape):
    def __init__(self, size: float) -> None:
        super().__init__(glm.mat4())
        v0 = glm.vec3(-size, -size, 0)
        v1 = glm.vec3(size, -size, 0)
        v2 = glm.vec3(size, size, 0)
        v3 = glm.vec3(-size, size, 0)
        self.lines = [
            (v0, v1, glm.vec4(1, 1, 1, 1)),
            (v1, v2, glm.vec4(1, 1, 1, 1)),
            (v2, v3, glm.vec4(1, 1, 1, 1)),
            (v3, v0, glm.vec4(1, 1, 1, 1)),
        ]

    def get_quads(self) -> Iterable[Tuple[Quad, glm.vec4]]:
        return []

    def get_lines(self) -> Iterable[Tuple[glm.vec3, glm.vec3, glm.vec4]]:
        return self.lines


class GizmoScene(Item):
    def __init__(self, mouse_event: MouseEvent, *, font: pathlib.Path) -> None:
        super().__init__('gizmo')
        self.mouse_camera = MouseCamera(mouse_event=mouse_event)
        self.nvg = NanoVgRenderer(font)

        # gizmo shapes
        self.gizmo = Gizmo()
        from pydear.gizmo.shapes.cube_shape import CubeShape
        self.selected: Optional[Shape] = None
        self.cubes: List[Shape] = []
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                cube = CubeShape(0.5, 0.5, 0.5,
                                 position=glm.vec3(i, j, 0))
                self.gizmo.add_shape(cube)
                self.cubes.append(cube)

        line_shape = XYSquare(2)
        self.gizmo.add_shape(line_shape)

        # mouse event handling
        self.handler = GizmoDragHandler(self.gizmo, self.mouse_camera.camera)
        mouse_event.bind_left_drag(self.handler)

        # camera gaze when selection
        def on_selected(selected: Optional[Shape]):
            if selected:
                position = selected.matrix.value[3].xyz
                self.mouse_camera.camera.view.set_gaze(position)

            self.selected = selected
        self.handler.selected += on_selected

    def render(self, mouse_input: FrameInput):
        camera = self.mouse_camera.camera
        camera.projection.resize(mouse_input.width, mouse_input.height)
        self.gizmo.process(camera, mouse_input.x, mouse_input.y)

        context = self.handler.context
        if context:
            with self.nvg.render(mouse_input.width, mouse_input.height) as vg:
                context.nvg_draw(vg)

    def show(self):
        from pydear import imgui as ImGui
        if ImGui.Begin('gizmo cubes'):
            selected = None
            for i, cube in enumerate(self.cubes):
                if ImGui.Selectable(f'cube#{i}', cube == self.selected):
                    selected = cube

            if selected:
                # select from ImGui list
                self.handler.select(selected)
                self.mouse_camera.middle_drag.reset(glm.vec3(0, 0, -5))

        ImGui.End()
