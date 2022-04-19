from typing import Optional
from OpenGL import GL
from pydear.utils.selector import Item
from pydear.scene.camera import Camera
from pydear import glo


class TeaPot(Item):
    def __init__(self) -> None:
        super().__init__('teapot')
        self.drawable: Optional[glo.Drawable] = None
        self.camera = Camera()

    def resize(self, w: int, h: int):
        self.camera.projection.resize(w, h)

    def wheel(self, d: int):
        self.camera.wheel(d)

    def mouse_drag(self, x: int, y: int, dx: int, dy: int, left: bool, right: bool, middle: bool):
        self.camera.mouse_drag(x, y, dx, dy, left, right, middle)

    def mouse_release(self):
        self.camera.mouse_release()

    def render(self):
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
