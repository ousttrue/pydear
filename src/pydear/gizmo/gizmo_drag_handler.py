from typing import Optional
from enum import Enum
import glm
from pydear.scene.camera import Camera
from pydear.utils.eventproperty import EventProperty
from .shapes.shape import Shape, ShapeState
from .gizmo import Gizmo, RayHit
from .gizmo_event_handler import GizmoEventHandler


IDENTITY = glm.mat4()


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2


class ScreenLine:
    def __init__(self, start: glm.vec2, dir: glm.vec2) -> None:
        self.start = start
        self.dir = glm.normalize(dir)

    @staticmethod
    def begin_end(self, start: glm.vec2, end: glm.vec2) -> 'ScreenLine':
        '''
        y = ax + b
        b = y - ax
        '''
        return ScreenLine(start, end-self.start)
    #     a = end - start
    #     if a.x:
    #         self.a = a.y/a.x
    #     else:
    #         self.a = float('inf')

    #     self.b = start.y - self.a * start.x

    # def point_from_x(self, x: float) -> glm.vec2:
    #     '''
    #     y = ax + b
    #     '''
    #     return glm.vec2(x, self.a * x + self.b)

    def distance(self, v: glm.vec2):
        return glm.dot(v-self.start, self.dir)


class DragContext:
    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, axis: Axis, target: Shape) -> None:
        self.start_screen_pos = start_screen_pos
        self.manipulator = manipulator
        assert(self.manipulator)
        self.manipulator.add_state(ShapeState.DRAG)
        self.axis = axis
        assert target
        self.target = target
        self.init_matrix = target.matrix.value

    def end(self):
        self.manipulator.remove_state(ShapeState.DRAG)
        self.manipulator = None


class RingDragContext(DragContext):
    '''
    円盤面のドラッグ
    '''

    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, axis: Axis, target: Shape, camera: Camera):
        super().__init__(start_screen_pos, manipulator=manipulator, axis=axis, target=target)

        vp = camera.projection.matrix * camera.view.matrix
        center_pos = vp * manipulator.matrix.value[3]
        cx = center_pos.x / center_pos.w
        cy = center_pos.y / center_pos.w
        center_screen_pos = glm.vec2(
            (cx * 0.5 + 0.5)*camera.projection.width,
            (0.5 - cy * 0.5)*camera.projection.height
        )
        # self.line = ScreenLine(start_screen_pos, self.center_screen_pos)

        # l = ScreenLine(self.start_screen_pos, self.center_screen_pos)
        # self.left = l.point_from_x(0)
        # self.right = l.point_from_x(camera.projection.width)

        view_axis = (camera.view.matrix *
                     manipulator.matrix.value)[axis.value].xyz
        center_start = glm.vec3(self.start_screen_pos, 0) - \
            glm.vec3(center_screen_pos, 0)
        cross = glm.normalize(glm.cross(center_start, view_axis))
        assert cross.x != 0 or cross.y != 0
        # self.edge = False
        cross.z = 0
        cross = glm.normalize(cross)
        self.line = ScreenLine(self.start_screen_pos, cross.xy)

    def drag(self, cursor_pos: glm.vec2):
        d = self.line.distance(cursor_pos)

        angle = d * 0.02
        m = self.init_matrix * glm.rotate(angle, IDENTITY[self.axis.value].xyz)
        self.target.matrix.set(m)
        return m


class RollgDragContext(DragContext):
    '''
    横面のドラッグ
    '''

    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, axis: Axis, target: Shape, camera: Camera):
        super().__init__(start_screen_pos, manipulator=manipulator, axis=axis, target=target)

    def drag(self, cursor_pos: glm.vec2):
        # TODO: axis project to screen
        # TODO: split by start-axis_dir
        m = self.init_matrix
        return m


class GizmoDragHandler(GizmoEventHandler):
    def __init__(self, gizmo: Gizmo, camera, *, inner=0.4, outer=0.6, depth=0.04) -> None:
        super().__init__()
        self.camera = camera
        self.selected = EventProperty[Optional[Shape]](None)

        # draggable
        from pydear.gizmo.shapes.ring_shape import XRingShape, YRingShape, ZRingShape, XRollShape, YRollShape, ZRollShape
        self.x_ring = XRingShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(1, 0.3, 0.3, 1))
        gizmo.add_shape(self.x_ring)
        self.y_ring = YRingShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(0.3, 1, 0.3, 1))
        gizmo.add_shape(self.y_ring)
        self.z_ring = ZRingShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(0.3, 0.3, 1, 1))
        gizmo.add_shape(self.z_ring)

        self.x_roll = XRollShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(1, 0.3, 0.3, 1))
        gizmo.add_shape(self.x_roll)
        self.y_roll = YRollShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(0.3, 1, 0.3, 1))
        gizmo.add_shape(self.y_roll)
        self.z_roll = ZRollShape(inner=inner, outer=outer, depth=depth,
                                 color=glm.vec4(0.3, 0.3, 1, 1))
        gizmo.add_shape(self.z_roll)

        self.context = None

    def drag_begin(self, hit: RayHit):
        match hit.shape:
            case self.x_ring:
                # ring is not selectable
                self.context = RingDragContext(
                    hit.cursor_pos, manipulator=hit.shape, axis=Axis.X,
                    target=self.selected.value, camera=self.camera)
            case self.y_ring:
                # ring is not selectable
                self.context = RingDragContext(
                    hit.cursor_pos, manipulator=hit.shape, axis=Axis.Y,
                    target=self.selected.value, camera=self.camera)
            case self.z_ring:
                # ring is not selectable
                self.context = RingDragContext(
                    hit.cursor_pos, manipulator=hit.shape, axis=Axis.Z,
                    target=self.selected.value, camera=self.camera)
            case _:
                self.select(hit.shape)

    def drag(self, x, y, dx, dy):
        if self.context:
            m = self.context.drag(glm.vec2(x, y))
            self.x_ring.matrix.set(m)
            self.y_ring.matrix.set(m)
            self.z_ring.matrix.set(m)
            self.x_roll.matrix.set(m)
            self.y_roll.matrix.set(m)
            self.z_roll.matrix.set(m)

    def drag_end(self, x, y):
        if self.context:
            self.context.end()
            self.context = None

    def select(self, shape: Optional[Shape]):
        if shape == self.selected.value:
            return
        # clear
        if self.selected.value:
            self.selected.value.remove_state(ShapeState.SELECT)
        # select
        self.selected.set(shape)
        if shape:
            shape.add_state(ShapeState.SELECT)
            self.x_ring.matrix.set(shape.matrix.value)
            self.x_ring.remove_state(ShapeState.HIDE)
            self.y_ring.matrix.set(shape.matrix.value)
            self.y_ring.remove_state(ShapeState.HIDE)
            self.z_ring.matrix.set(shape.matrix.value)
            self.z_ring.remove_state(ShapeState.HIDE)
            self.x_roll.matrix.set(shape.matrix.value)
            self.x_roll.remove_state(ShapeState.HIDE)
            self.y_roll.matrix.set(shape.matrix.value)
            self.y_roll.remove_state(ShapeState.HIDE)
            self.z_roll.matrix.set(shape.matrix.value)
            self.z_roll.remove_state(ShapeState.HIDE)
        else:
            self.x_ring.add_state(ShapeState.HIDE)
            self.y_ring.add_state(ShapeState.HIDE)
            self.z_ring.add_state(ShapeState.HIDE)
            self.x_roll.add_state(ShapeState.HIDE)
            self.y_roll.add_state(ShapeState.HIDE)
            self.z_roll.add_state(ShapeState.HIDE)
