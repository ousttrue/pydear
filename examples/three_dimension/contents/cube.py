'''
simple triangle sample
'''
from typing import Optional
import logging
from OpenGL import GL
from pydear.utils.selector import Item
from glglue import glo
from pydear.utils.mouse_camera import MouseCamera, MouseEvent
from pydear.utils.mouse_event import MouseInput

LOGGER = logging.getLogger(__name__)


class Cube(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('cube')
        self.mouse_camera = MouseCamera(mouse_event)
        self.drawable: Optional[glo.Drawable] = None

    def render(self, mouse_input: MouseInput):
        camera = self.mouse_camera.camera
        camera.projection.resize(mouse_input.width, mouse_input.height)

        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        if not self.drawable:
            # shader
            shader = glo.Shader.load_from_pkg('pydear', 'assets/mesh')
            assert isinstance(shader, glo.Shader)
            props = shader.create_props(camera)

            # mesh
            from pydear.scene import cube
            self.drawable = cube.create(shader, props)

        self.drawable.draw()

    def show(self):
        pass
