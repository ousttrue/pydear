import math
import logging
import glm
LOGGER = logging.getLogger(__name__)


class Perspective:
    def __init__(self) -> None:
        self.matrix = glm.mat4(1.0)
        self.fov_y = math.pi * 30 / 180
        self.aspect = 1.0
        self.z_near = 0.1
        self.z_far = 1000
        self.update_matrix()

    def update_matrix(self) -> None:
        self.matrix = glm.perspectiveRH(self.fov_y, self.aspect, self.z_near,
                                        self.z_far)


class Orbit:
    def __init__(self, *, distance=5, y=0) -> None:
        self.matrix = glm.mat4(1)
        self.inverse = glm.mat4(1)
        self.x = 0.0
        self.y = y
        self.distance = distance
        self.yaw = 0.0
        self.pitch = 0.0
        self.update_matrix()

    def __str__(self) -> str:
        return f'({self.x:.3f}, {self.y:.3f}, {self.distance:.3f})'

    def update_matrix(self) -> None:
        t = glm.translate(glm.vec3(self.x, self.y, -self.distance))
        yaw = glm.rotate(self.yaw, glm.vec3(0, 1, 0))
        pitch = glm.rotate(self.pitch, glm.vec3(1, 0, 0))
        # self.matrix = yaw * pitch * t
        self.matrix = t * pitch * yaw
        self.inverse = glm.inverse(self.matrix)


class Camera:
    def __init__(self, *, distance=5, y=0):
        self.projection = Perspective()
        self.view = Orbit(distance=distance, y=y)
        self.width = 1
        self.height = 1
        self.x = 0
        self.y = 0
        self.left = False
        self.middle = False
        self.right = False

    def update(self, width: int, height: int,
               x: int, y: int,
               left: bool, right: bool, middle: bool,
               wheel: int
               ):
        self.onResize(width, height)

        if left:
            self.onLeftDown(x, y)
        else:
            self.onLeftUp(x, y)

        if right:
            self.onRightDown(x, y)
        else:
            self.onRightUp(x, y)

        if middle:
            self.onMiddleDown(x, y)
        else:
            self.onMiddleUp(x, y)

        if wheel:
            self.onWheel(-wheel)
        self.onMotion(x, y)

    def onResize(self, w: int, h: int) -> bool:
        if self.width == w and self.height == h:
            return False
        self.width = w
        self.height = h
        self.projection.aspect = float(w) / h
        self.projection.update_matrix()
        return True

    def onLeftDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.left:
            return False
        self.left = True
        self.x = x
        self.y = y
        return False

    def onLeftUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.left = False
        return False

    def onMiddleDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.middle:
            return False
        self.middle = True
        self.x = x
        self.y = y
        return False

    def onMiddleUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.middle = False
        return False

    def onRightDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.right:
            return False
        self.right = True
        self.x = x
        self.y = y
        return False

    def onRightUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.right = False
        return False

    def onMotion(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        dx = x - self.x
        self.x = x
        dy = y - self.y
        self.y = y

        redraw_is_required = False
        if self.right:
            self.view.yaw += dx * 0.01
            self.view.pitch += dy * 0.01
            self.view.update_matrix()
            redraw_is_required = True

        if self.middle:
            plane_height = math.tan(
                self.projection.fov_y * 0.5) * self.view.distance * 2
            self.view.x += dx / self.height * plane_height
            self.view.y -= dy / self.height * plane_height
            self.view.update_matrix()
            redraw_is_required = True

        return redraw_is_required

    def onWheel(self, d: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if d > 0:
            self.view.distance *= 1.1
            self.view.update_matrix()
            return True
        elif d < 0:
            self.view.distance *= 0.9
            self.view.update_matrix()
            return True
        return False

    # def fit(self, p0: Float3, p1: Float3):
    #     if math.isnan(p0.x) or math.isnan(p0.y) or math.isnan(p0.z) or math.isnan(p1.x) or math.isnan(p1.y) or math.isnan(p1.z):
    #         return
    #     if math.isinf(p0.x) or math.isinf(p0.y) or math.isinf(p0.z) or math.isinf(p1.x) or math.isinf(p1.y) or math.isinf(p1.z):
    #         return

    #     self.view.x = 0
    #     self.view.y = -(p1.y+p0.y)/2
    #     self.view.distance = (p1.y-p0.y) / \
    #         math.tan(self.projection.fov_y / 2)
    #     self.view.yaw = 0
    #     self.view.pitch = 0
    #     self.view.update_matrix()
    #     logger.info(self.view)

    #     if self.view.distance*2 > self.projection.z_far:
    #         self.projection.z_far = self.view.distance*2
    #         self.projection.update_matrix()

    # def get_mouse_ray(self):
    #     origin = Float3(
    #         self.view.inverse._41,
    #         self.view.inverse._42,
    #         self.view.inverse._43)
    #     half_fov = self.projection.fov_y/2
    #     dir = Float3(
    #         (self.x/self.width * 2 - 1) *
    #         math.tan(half_fov) * (self.projection.aspect),
    #         -(self.y/self.height * 2 - 1) * math.tan(half_fov),
    #         -1)
    #     dir = self.view.inverse.apply(*dir, translate=False)

    #     return Ray(origin, dir.normalized())

    # def get_state(self, light: Float4) -> FrameState:
    #     ray = self.get_mouse_ray()
    #     return FrameState(
    #         Float4(0, 0, self.width, self.height),
    #         self.x, self.y,
    #         self.left, self.right, self.middle,
    #         self.view.matrix, self.projection.matrix,
    #         ray, light
    #     )
