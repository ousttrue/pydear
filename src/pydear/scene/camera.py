import math
import logging
import glm
LOGGER = logging.getLogger(__name__)


class Perspective:
    def __init__(self, *, near=0.1, far=1000) -> None:
        self.matrix = glm.mat4(1.0)
        self.fov_y = math.pi * 30 / 180
        self.aspect = 1.0
        self.z_near = near
        self.z_far = far
        self.width = 1
        self.height = 1
        self.update_matrix()

    def update_matrix(self) -> None:
        self.matrix = glm.perspectiveRH(self.fov_y, self.aspect, self.z_near,
                                        self.z_far)

    def resize(self, w: int, h: int) -> bool:
        if self.width == w and self.height == h:
            return False
        self.width = w
        self.height = h
        self.aspect = float(w) / h
        self.update_matrix()
        return True


class View:
    def __init__(self) -> None:
        self.matrix = glm.mat4(1)
        self.inverse = glm.mat4(1)


class Orbit:
    def __init__(self, view: View, *, distance=5, y=0) -> None:
        self.view = view
        self.shift = glm.vec3(0, y, -distance)
        self.yaw = 0.0
        self.pitch = 0.0
        self.update_matrix()

    def __str__(self) -> str:
        return f'({self.shift.x:.3f}, {self.shift.y:.3f}, {self.shift.distance:.3f})'

    def update_matrix(self) -> None:
        t = glm.translate(self.shift)
        yaw = glm.rotate(self.yaw, glm.vec3(0, 1, 0))
        pitch = glm.rotate(self.pitch, glm.vec3(1, 0, 0))
        self.view.matrix = t * pitch * yaw
        self.view.inverse = glm.inverse(self.view.matrix)

    def right_drag(self, dx, dy, _) -> bool:
        self.yaw += dx * 0.01
        self.pitch += dy * 0.01
        self.update_matrix()
        return True

    def middle_drag(self, dx, dy, projection) -> bool:
        plane_height = math.tan(
            projection.fov_y * 0.5) * self.shift.z * 2
        self.shift.x -= dx / projection.height * plane_height
        self.shift.y += dy / projection.height * plane_height
        self.update_matrix()
        return True

    def wheel(self, d: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if d < 0:
            self.shift.z *= 1.1
            self.update_matrix()
            return True
        elif d > 0:
            self.shift.z *= 0.9
            self.update_matrix()
            return True
        return False


def get_arcball_vector(x, y, screen_width, screen_height):
    '''
    https://en.wikibooks.org/wiki/OpenGL_Programming/Modern_OpenGL_Tutorial_Arcball
    '''
    P = glm.vec3(x/screen_width*2 - 1.0,
                 y/screen_height*2 - 1.0,
                 0)
    P.y = -P.y
    OP_squared = P.x * P.x + P.y * P.y
    if OP_squared <= 1:
        P.z = math.sqrt(1 - OP_squared)  # Pythagoras
    else:
        P = glm.normalize(P)  # nearest point
    return P


class ArcBall:
    def __init__(self, view: View) -> None:
        self.view = view
        self.shift = glm.vec3(0, 0, -5)
        self.rotation = glm.quat()

    def update_matrix(self) -> None:
        t = glm.translate(self.shift)
        self.view.matrix = t * glm.mat4(self.rotation)
        self.view.inverse = glm.inverse(self.view.matrix)

    def drag(self, x, y, dx, dy, projectin: Perspective) -> bool:
        va = get_arcball_vector(
            x-dx, y-dy, projectin.width, projectin.height)
        vb = get_arcball_vector(x, y, projectin.width, projectin.height)
        angle = math.acos(min(1.0, glm.dot(va, vb)))
        axis_in_camera_coord = glm.cross(va, vb)
        r = glm.angleAxis(angle, axis_in_camera_coord)
        self.rotation = glm.normalize(r * self.rotation)
        self.update_matrix()
        return True


class Camera:
    def __init__(self, *, near=0.01, far=1000, distance=5, y=0):
        self.projection = Perspective(near=near, far=far)
        self.view = View()
        self.orbit = Orbit(self.view, distance=distance, y=y)
        self.arcball = ArcBall(self.view)
        self.left = False
        self.middle = False
        self.right = False

    def drag(self,
             x: int, y: int,
             dx: int, dy: int,
             left: bool, right: bool, middle: bool):
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

        self.onMotion(x, y, dx, dy)

    def onLeftDown(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        if self.left:
            return False
        self.left = True
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
        return False

    def onRightUp(self, x: int, y: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        self.right = False
        return False

    def onMotion(self, x: int, y: int, dx: int, dy: int) -> bool:
        ''' 
        Mouse input. Returns whether redraw is required.
        '''
        redraw_is_required = False
        if self.right:
            if self.arcball.drag(x, y, dx, dy, self.projection):
                redraw_is_required = True

        # if self.middle:
        #     if self.orbit.middle_drag(dx, dy, self.projection):
        #         redraw_is_required = True

        return redraw_is_required

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
