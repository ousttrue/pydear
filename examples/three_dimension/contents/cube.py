'''
simple triangle sample
'''
import logging
from OpenGL import GL
import glm
from pydear import glo
from pydear.utils.item import Item, Input
from pydear.scene.camera import Camera

LOGGER = logging.getLogger(__name__)


class Cube(Item):
    def __init__(self) -> None:
        super().__init__('cube')
        self.camera = Camera()
        self.drawable = None

    def initialize(self) -> None:
        # shader
        shader = glo.Shader.get('assets/mesh')
        if not shader:
            return
        view = glo.UniformLocation.create(shader.program, "uView")
        projection = glo.UniformLocation.create(
            shader.program, "uProjection")
        props = [
            glo.ShaderProp(
                lambda x: view.set_mat4(x),
                lambda:glm.value_ptr(self.camera.view.matrix)),
            glo.ShaderProp(
                lambda x: projection.set_mat4(x),
                lambda:glm.value_ptr(self.camera.projection.matrix)),
        ]

        # mesh
        from pydear.scene import cube
        self.drawable = cube.create(shader, props)

    def input(self, input: Input):
        self.camera.onResize(input.width, input.height)

        if input.left:
            self.camera.onLeftDown(input.x, input.y)
        else:
            self.camera.onLeftUp(input.x, input.y)

        if input.right:
            self.camera.onRightDown(input.x, input.y)
        else:
            self.camera.onRightUp(input.x, input.y)

        if input.middle:
            self.camera.onMiddleDown(input.x, input.y)
        else:
            self.camera.onMiddleUp(input.x, input.y)

        if input.wheel:
            self.camera.onWheel(-input.wheel)
        self.camera.onMotion(input.x, input.y)

    def render(self):
        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        if not self.is_initialized:
            self.initialize()
            self.is_initialized = True

        if self.drawable:
            self.drawable.draw()
