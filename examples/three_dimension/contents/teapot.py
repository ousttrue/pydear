from typing import Optional
from OpenGL import GL
from pydear.utils.selector import Item
from pydear.scene.camera import Camera, MouseEvent, ArcBall, ScreenShift
from pydear import glo


class TeaPot(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('teapot')
        self.drawable: Optional[glo.Drawable] = None
        self.camera = Camera()
        mouse_event.bind_right_drag(ArcBall(self.camera.view, self.camera.projection))
        middle_drag = ScreenShift(self.camera.view, self.camera.projection)
        mouse_event.bind_middle_drag(middle_drag)
        mouse_event.wheel += [middle_drag.wheel]

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
            from pydear.scene import teapot
            self.drawable = teapot.create(shader, props)

        self.drawable.draw()

    def show(self):
        pass
