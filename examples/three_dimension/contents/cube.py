'''
simple triangle sample
'''
from typing import Optional
import logging
from OpenGL import GL
from pydear.utils.item import Item
from pydear import glo
from pydear.scene.camera import Camera

LOGGER = logging.getLogger(__name__)


class Cube(Item):
    def __init__(self) -> None:
        super().__init__('cube')
        self.drawable: Optional[glo.Drawable] = None

    def render(self, camera: Camera):
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
