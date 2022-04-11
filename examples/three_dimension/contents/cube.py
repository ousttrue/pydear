'''
simple triangle sample
'''
from typing import Optional
import logging
from OpenGL import GL
from pydear.utils.item import Item, Input
from pydear.scene.camera import Camera
from pydear import glo


LOGGER = logging.getLogger(__name__)


class Cube(Item):
    def __init__(self) -> None:
        super().__init__('cube')
        self.camera = Camera()
        self.drawable: Optional[glo.Drawable] = None

    def input(self, input: Input):
        self.camera.update(input.width, input.height,
                           input.x, input.y,
                           input.left, input.right, input.middle,
                           input.wheel)

    def render(self):
        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        if not self.drawable:
            # shader
            import pydear.scene.mesh_shader
            shader, props = pydear.scene.mesh_shader.get(self.camera)

            # mesh
            from pydear.scene import cube
            self.drawable = cube.create(shader, props)

        self.drawable.draw()
