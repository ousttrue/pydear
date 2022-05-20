'''
simple triangle sample
'''
from typing import Optional
import logging
from OpenGL import GL
from pydear.utils.selector import Item
from pydear import glo
from pydear.scene.camera import Camera, ArcBall, ScreenShift
from pydear.utils.mouse_event import MouseEvent

LOGGER = logging.getLogger(__name__)


class Cube(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('cube')
        self.camera = Camera()
        mouse_event.bind_right_drag(ArcBall(self.camera.view, self.camera.projection))
        middle_drag = ScreenShift(self.camera.view, self.camera.projection)
        mouse_event.bind_middle_drag(middle_drag)
        mouse_event.wheel += [middle_drag.wheel]
        self.drawable: Optional[glo.Drawable] = None

    def render(self, w, h):
        self.camera.projection.resize(w, h)

        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        if not self.drawable:
            # shader
            shader = glo.Shader.load_from_pkg('pydear', 'assets/mesh')
            assert isinstance(shader, glo.Shader)
            props = shader.create_props(self.camera)

            # mesh
            from pydear.scene import cube
            self.drawable = cube.create(shader, props)

        self.drawable.draw()

    def show(self):
        pass
