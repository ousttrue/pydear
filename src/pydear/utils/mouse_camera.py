from ..scene.camera import Camera, ArcBall, ScreenShift
from .mouse_event import MouseEvent


class MouseCamera:
    def __init__(self, mouse_event: MouseEvent) -> None:
        self.camera = Camera()
        mouse_event.bind_right_drag(
            ArcBall(self.camera.view, self.camera.projection))
        self.middle_drag = ScreenShift(self.camera.view, self.camera.projection)
        mouse_event.bind_middle_drag(self.middle_drag)
        mouse_event.wheel += [self.middle_drag.wheel]
