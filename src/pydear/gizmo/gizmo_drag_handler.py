from typing import Optional, Dict, Type, Tuple
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
    def __init__(self, start: glm.vec2, dir: glm.vec2, w, h) -> None:
        # v = at + b
        self.start = start
        self.dir = glm.normalize(dir)
        '''
        y = ax + b
        b = y - ax
        '''
        if self.dir.x == 0:
            self.p0 = glm.vec2(self.start.x, 0)
            self.p1 = glm.vec2(self.start.x, h)
        elif self.dir.y == 0:
            self.p0 = glm.vec2(0, self.start.y)
            self.p1 = glm.vec2(w, self.start.y)
        else:
            # y = ax + b
            a = self.dir.y/self.dir.x
            # b = y - ax
            b = start.y - start.x * a
            # x = 0
            self.p0 = glm.vec2(0, b)
            # x = w
            self.p1 = glm.vec2(w, a * w + b)

    @staticmethod
    def begin_end(start: glm.vec2, end: glm.vec2, w, h) -> 'ScreenLine':
        return ScreenLine(start, end-start, w, h)
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

    def get_t(self, t: float) -> glm.vec2:
        return self.start + self.dir * t


class DragContext:
    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, target: Shape) -> None:
        self.start_screen_pos = start_screen_pos
        self.manipulator = manipulator
        assert(isinstance(self.manipulator, Shape))
        self.manipulator.add_state(ShapeState.DRAG)
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
        super().__init__(start_screen_pos, manipulator=manipulator, target=target)
        self.axis = axis

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
        n = glm.normalize(cross.xy)
        self.line = ScreenLine(
            self.start_screen_pos, glm.vec2(n.y, n.x), camera.projection.width, camera.projection.height)

    def drag(self, cursor_pos: glm.vec2):
        d = self.line.distance(cursor_pos)

        angle = d * 0.02
        m = self.init_matrix * glm.rotate(angle, IDENTITY[self.axis.value].xyz)
        self.target.matrix.set(m)
        return m


class RollDragContext(DragContext):
    '''
    横面のドラッグ
    '''

    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, axis: Axis, target: Shape, camera: Camera):
        super().__init__(start_screen_pos, manipulator=manipulator, target=target)
        self.axis = axis

        view_axis = (camera.view.matrix *
                     manipulator.matrix.value)[axis.value].xy
        view_axis = glm.normalize(view_axis)
        self.line = ScreenLine(
            start_screen_pos, glm.vec2(view_axis.y, view_axis.x), camera.projection.width, camera.projection.height)

    def drag(self, cursor_pos: glm.vec2):
        d = self.line.distance(cursor_pos)

        angle = d * 0.02
        m = self.init_matrix * glm.rotate(angle, IDENTITY[self.axis.value].xyz)
        self.target.matrix.set(m)
        return m


class GizmoDragHandler(GizmoEventHandler):
    def __init__(self, gizmo: Gizmo, camera, *, inner=0.4, outer=0.6, depth=0.04) -> None:
        super().__init__()
        self.camera = camera
        self.selected = EventProperty[Optional[Shape]](None)

        # draggable
        self.drag_shapes = self.create_rotation_shapes(inner, outer, depth)
        for drag_shape in self.drag_shapes.keys():
            gizmo.add_shape(drag_shape)

        self.context = None

    def create_rotation_shapes(self, inner: float, outer: float, depth: float) -> Dict[Shape, Tuple[Type, dict]]:
        from pydear.gizmo.shapes.ring_shape import XRingShape, YRingShape, ZRingShape, XRollShape, YRollShape, ZRollShape
        return {
            XRingShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(1, 0.3, 0.3, 1)): (RingDragContext, {'axis': Axis.X}),
            YRingShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(0.3, 1, 0.3, 1)): (RingDragContext, {'axis': Axis.Y}),
            ZRingShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(0.3, 0.3, 1, 1)): (RingDragContext, {'axis': Axis.Z}),
            XRollShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(1, 0.3, 0.3, 1)): (RollDragContext, {'axis': Axis.X}),
            YRollShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(0.3, 1, 0.3, 1)): (RollDragContext, {'axis': Axis.Y}),
            ZRollShape(inner=inner, outer=outer, depth=depth, color=glm.vec4(0.3, 0.3, 1, 1)): (RollDragContext, {'axis': Axis.Z}),
        }

    def drag_begin(self, hit: RayHit):
        match self.drag_shapes.get(hit.shape):  # type: ignore
            case (t, kw):
                # ring is not selectable
                self.context = t(
                    hit.cursor_pos, manipulator=hit.shape,
                    target=self.selected.value, camera=self.camera, **kw)
            case _:
                self.select(hit.shape)

    def drag(self, x, y, dx, dy):
        if self.context:
            m = self.context.drag(glm.vec2(x, y))
            for drag_shape in self.drag_shapes.keys():
                drag_shape.matrix.set(m)

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
            for drag_shape in self.drag_shapes.keys():
                drag_shape.matrix.set(shape.matrix.value)
                drag_shape.remove_state(ShapeState.HIDE)
        else:
            for drag_shape in self.drag_shapes.keys():
                drag_shape.add_state(ShapeState.HIDE)
