'''
simple triangle sample
'''
from typing import NamedTuple
import logging
from OpenGL import GL
import glm
from pydear.utils.selector import Item
from pydear.scene.camera import Camera, MouseEvent
from pydear.gizmo.gizmo import Gizmo, AABB

LOGGER = logging.getLogger(__name__)


class Bone(NamedTuple):
    name: str
    head: glm.vec3
    tail: glm.vec3
    up: glm.vec3


BONES = [
    Bone('bone1', glm.vec3(0, 0, 0), glm.vec3(0, 0.2, 0), glm.vec3(0, 0, -1)),
    Bone('bone2', glm.vec3(0, 0.2, 0), glm.vec3(0, 0.4, 0), glm.vec3(0, 0, -1)),
    Bone('bone3', glm.vec3(0, 0.4, 0), glm.vec3(0, 0.6, 0), glm.vec3(0, 0, -1)),
]


class GizmoScene(Item):
    def __init__(self, mouse_event: MouseEvent) -> None:
        super().__init__('gizmo')
        self.camera = Camera()
        self.mouse_event = mouse_event
        self.camera.bind_mouse_event(self.mouse_event)
        self.gizmo = Gizmo()
        self.gizmo.bind_mouse_event(self.mouse_event)
        self.selected = None

    def render(self, w, h):
        self.camera.projection.resize(w, h)
        # GL.glEnable(GL.GL_CULL_FACE)
        # GL.glCullFace(GL.GL_BACK)
        # GL.glFrontFace(GL.GL_CCW)
        GL.glEnable(GL.GL_DEPTH_TEST)

        self.gizmo.begin(self.camera)
        self.gizmo.aabb(AABB(glm.vec3(5, 0, 0), glm.vec3(6, 1, 1)))

        current = None
        for bone in BONES:
            selected = self.gizmo.bone_head_tail(
                bone.name, bone.head, bone.tail, bone.up, is_selected=bone.name == self.selected)
            if selected:
                current = bone.name

        if current:
            self.selected = current
        elif self.mouse_event.last_input.left_down:
            self.selected = None

        self.matrix = glm.mat4()
        self.gizmo.axis(1)

        self.gizmo.end()

    def show(self):
        pass
