'''
simple triangle sample
'''
from typing import Optional
import logging
from OpenGL import GL
import glm
from pydear.utils.selector import Item
from pydear.scene.camera import Camera
from pydear.scene.gizmo import Gizmo, AABB

LOGGER = logging.getLogger(__name__)


class GizmoScene(Item):
    def __init__(self) -> None:
        super().__init__('gizmo')
        self.camera = Camera()
        self.gizmo = Gizmo()

        self.left_down = False
        self.x = 0
        self.y = 0
        self.selected = None

    def resize(self, w: int, h: int):
        self.camera.projection.resize(w, h)

    def wheel(self, d: int):
        self.camera.wheel(d)

    def mouse_drag(self, x: int, y: int, dx: int, dy: int, left: bool, right: bool, middle: bool):
        self.camera.mouse_drag(x, y, dx, dy, left, right, middle)
        self.left_down = left
        self.x = x
        self.y = y

    def mouse_release(self, x: int, y: int):
        self.camera.mouse_release()
        self.left_down = False
        self.x = x
        self.y = y

    def render(self):
        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.gizmo.begin(self.x, self.y, self.left_down,
                         self.camera.view.matrix, self.camera.projection.matrix,
                         self.camera.get_mouse_ray(self.x, self.y))
        self.gizmo.aabb(AABB(glm.vec3(5, 0, 0), glm.vec3(6, 1, 1)))

        self.gizmo.axis(1)
        key = "bone1"
        selected = self.gizmo.bone(key, 1, key == self.selected)
        if selected:
            self.selected = key
        elif self.left_down:
            self.selected = None

        self.gizmo.end()

    def show(self):
        pass
