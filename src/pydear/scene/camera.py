from typing import NamedTuple, Optional
import math
import logging
import glm
import abc
LOGGER = logging.getLogger(__name__)


kEpsilon = 1e-5


class Ray(NamedTuple):
    origin: glm.vec3
    dir: glm.vec3

    def intersect_triangle(self, v0: glm.vec3, v1: glm.vec3, v2: glm.vec3) -> Optional[float]:
        '''
        https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/ray-triangle-intersection-geometric-solution
        '''
        # compute plane's normal
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        # no need to normalize
        N = glm.cross(v0v1, v0v2)  # N
        # area2 = N.get_length()

        # Step 1: finding P

        # check if ray and plane are parallel ?
        NdotRayDirection = glm.dot(N, self.dir)
        if math.fabs(NdotRayDirection) < kEpsilon:  # almost 0
            return  # they are parallel so they don't intersect !

        # compute d parameter using equation 2
        d = -glm.dot(N, v0)

        # compute t (equation 3)
        t = -(glm.dot(N, self.origin) + d) / NdotRayDirection
        # check if the triangle is in behind the ray
        if t < 0:
            return  # the triangle is behind

        # compute the intersection point using equation 1
        P = self.origin + self.dir * t

        # Step 2: inside-outside test
        # Vec3f C  # vector perpendicular to triangle's plane

        # edge 0
        edge0 = v1 - v0
        vp0 = P - v0
        C = glm.cross(edge0, vp0)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        # edge 1
        edge1 = v2 - v1
        vp1 = P - v1
        C = glm.cross(edge1, vp1)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        # edge 2
        edge2 = v0 - v2
        vp2 = P - v2
        C = glm.cross(edge2, vp2)
        if glm.dot(N, C) < 0:
            return  # P is on the right side

        return t  # this ray hits the triangle


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
        self.rotation = glm.quat()
        self.shift = glm.vec3(0, 0, -5)
        self.update_matrix()

    def update_matrix(self):
        t = glm.translate(self.shift)
        r = glm.mat4(self.rotation)
        self.matrix = t * r
        self.inverse = glm.inverse(self.matrix)


class DragInterface(abc.ABC):
    @abc.abstractmethod
    def begin(self, x, y):
        pass

    @abc.abstractmethod
    def drag(self, x, y, dx, dy):
        pass

    @abc.abstractmethod
    def end(self):
        pass


class ScreenShift(DragInterface):
    def __init__(self, view: View, projection: Perspective, *, distance=5, y=0) -> None:
        self.view = view
        self.projection = projection
        self.shift = glm.vec3(0, y, -distance)
        self.update()

    def update(self) -> None:
        self.view.shift = self.shift
        self.view.update_matrix()

    def begin(self, x, y):
        pass

    def drag(self, x, y, dx: int, dy: int) -> bool:
        plane_height = math.tan(
            self.projection.fov_y * 0.5) * self.shift.z * 2
        self.shift.x -= dx / self.projection.height * plane_height
        self.shift.y += dy / self.projection.height * plane_height
        self.update()
        return True

    def end(self):
        pass

    def wheel(self, d: int) -> bool:
        if d < 0:
            self.shift.z *= 1.1
            self.update()
            return True
        elif d > 0:
            self.shift.z *= 0.9
            self.update()
            return True
        return False


class TurnTable(DragInterface):
    def __init__(self, view: View) -> None:
        self.view = view
        self.yaw = 0.0
        self.pitch = 0.0
        self.update()

    def update(self) -> None:
        yaw = glm.angleAxis(self.yaw, glm.vec3(0, 1, 0))
        pitch = glm.angleAxis(self.pitch, glm.vec3(1, 0, 0))
        self.view.rotation = pitch * yaw
        self.view.update_matrix()

    def begin(self, x, y):
        pass

    def drag(self, x, y, dx: int, dy: int) -> bool:
        self.yaw += dx * 0.01
        self.pitch += dy * 0.01
        self.update()
        return True

    def end(self):
        pass


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


class ArcBall(DragInterface):
    def __init__(self, view: View, projection: Perspective) -> None:
        self.view = view
        self.projection = projection
        self.rotation = glm.quat()
        self.tmp_rotation = glm.quat()
        self.x = None
        self.y = None
        self.va = None

    def update(self) -> None:
        self.view.rotation = glm.normalize(self.tmp_rotation * self.rotation)
        self.view.update_matrix()

    def begin(self, x, y):
        self.rotation = self.view.rotation
        self.x = x
        self.y = y
        self.va = get_arcball_vector(
            x, y, self.projection.width, self.projection.height)

    def drag(self, x, y, dx, dy) -> bool:
        if x == self.x and y == self.y:
            return False
        self.x = x
        self.y = y
        vb = get_arcball_vector(
            x, y, self.projection.width, self.projection.height)
        angle = math.acos(min(1.0, glm.dot(self.va, vb))) * 2
        axis = glm.cross(self.va, vb)
        self.tmp_rotation = glm.angleAxis(angle, axis)
        self.update()
        return True

    def end(self):
        self.rotation = glm.normalize(self.tmp_rotation * self.rotation)
        self.tmp_rotation = glm.quat()
        self.update()


class Camera:
    def __init__(self, *, near=0.01, far=1000, distance=5, y=0):
        self.projection = Perspective(near=near, far=far)
        self.view = View()
        # self.right_drag = TurnTable(self.view)
        self.right_drag = ArcBall(self.view, self.projection)
        self.middle_drag = ScreenShift(
            self.view, self.projection, distance=distance, y=y)
        self.on_wheel = self.middle_drag

        # mouse state
        self.x = 0
        self.y = 0
        self.left = False
        self.right = False
        self.middle = False

    def mouse_drag(self,
                   x: int, y: int,
                   dx: int, dy: int,
                   left: bool, right: bool, middle: bool):
        self.x = x
        self.y = y
        self.left = left
        if right:
            if not self.right:
                self.right = True
                self.right_drag.begin(x, y)
            self.right_drag.drag(x, y, dx, dy)
        else:
            if self.right:
                self.right = False
                self.right_drag.end()

        if middle:
            if not self.middle:
                self.middle = True
                self.middle_drag.begin(x, y)
            self.middle_drag.drag(x, y, dx, dy)
        else:
            if self.middle:
                self.middle = False
                self.middle_drag.end()

    def mouse_release(self, x: int, y: int):
        self.x = x
        self.y = y
        self.left = False

        if self.right:
            self.right = False
            self.right_drag.end()

        if self.middle:
            self.middle = False
            self.middle_drag.end()

    def wheel(self, d):
        self.on_wheel.wheel(d)

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

    def get_mouse_ray(self, x: int, y: int) -> Ray:
        origin = self.view.inverse[3].xyz
        half_fov = self.projection.fov_y/2
        dir = self.view.inverse * glm.vec4(
            (x/self.projection.width * 2 - 1) *
            math.tan(half_fov) * (self.projection.aspect),
            -(y/self.projection.height * 2 - 1) * math.tan(half_fov),
            -1,
            0)
        return Ray(origin, glm.normalize(dir.xyz))
