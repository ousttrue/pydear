from typing import Optional
from OpenGL import GL
from pydear.utils.selector import Item
from glglue.camera.mouse_camera import MouseCamera, MouseEvent
from glglue.frame_input import FrameInput
from glglue.drawable import Drawable
from glglue import glo


class TeaPot(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('teapot')
        self.drawable: Optional[Drawable] = None
        self.mouse_camera = MouseCamera(mouse_event = mouse_event)

    def render(self, mouse_input: FrameInput):
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
            from glglue.scene import teapot
            self.drawable = teapot.create(shader, props)

        self.drawable.draw()

    def show(self):
        pass
