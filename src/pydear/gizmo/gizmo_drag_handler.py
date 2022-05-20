from typing import Optional, Dict, Type, Tuple
import abc
from enum import Enum
import glm
from pydear.scene.camera import Camera, DragInterface
from pydear.utils.eventproperty import EventProperty
from pydear.utils.mouse_event import MouseInput
from .shapes.shape import Shape, ShapeState
from .gizmo import Gizmo, RayHit


IDENTITY = glm.mat4()


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2


class DragContext(metaclass=abc.ABCMeta):
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

    @abc.abstractmethod
    def drag(self, cursor_pos: glm.vec2) -> glm.mat4:
        pass

    @abc.abstractmethod
    def nvg_draw(self, vg):
        pass


class RingDragContext(DragContext):
    '''
    円盤面のドラッグ
    '''

    def __init__(self, start_screen_pos: glm.vec2, *, manipulator: Shape, axis: Axis, target: Shape, camera: Camera):
        super().__init__(start_screen_pos, manipulator=manipulator, target=target)
        self.axis = axis

        vp = camera.projection.matrix * camera.view.matrix
        center_pos = vp * target.matrix.value * glm.vec4(0, 0, 0, 1)
        cx = center_pos.x / center_pos.w
        cy = center_pos.y / center_pos.w
        center_screen_pos = glm.vec2(
            (cx * 0.5 + 0.5)*camera.projection.width,
            -(cy - 1)*0.5*camera.projection.height
        )

        def draw_center_start(vg):
            from pydear.utils.nanovg_renderer import nvg_line_from_to
            nvg_line_from_to(vg, center_screen_pos.x, center_screen_pos.y,
                             self.start_screen_pos.x, self.start_screen_pos.y)
        # self.line = ScreenLine(start_screen_pos, self.center_screen_pos)

        # l = ScreenLine(self.start_screen_pos, self.center_screen_pos)
        # self.left = l.point_from_x(0)
        # self.right = l.point_from_x(camera.projection.width)

        view_axis = (camera.view.matrix *
                     manipulator.matrix.value)[axis.value].xyz
        center_start = glm.vec3(self.start_screen_pos, 0) - \
            glm.vec3(center_screen_pos, 0)
        cross = glm.normalize(glm.cross(center_start, view_axis))
        # assert cross.x != 0 or cross.y != 0
        # self.edge = False
        n = glm.normalize(cross.xy)
        from .screen_slider import ScreenSlider
        self.line = ScreenSlider(self.start_screen_pos, n,
                                 camera.projection.width, camera.projection.height,
                                 debug_draw=[draw_center_start])

    def drag(self, cursor_pos: glm.vec2):
        d = self.line.drag(cursor_pos)

        angle = d * 0.02
        m = self.init_matrix * glm.rotate(angle, IDENTITY[self.axis.value].xyz)
        self.target.matrix.set(m)
        return m

    def nvg_draw(self, vg):
        self.line.nvg_draw(vg)


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
        from .screen_slider import ScreenSlider
        self.line = ScreenSlider(
            start_screen_pos, glm.vec2(view_axis.y, view_axis.x), camera.projection.width, camera.projection.height)

    def drag(self, cursor_pos: glm.vec2):
        d = self.line.drag(cursor_pos)

        angle = d * 0.02
        m = self.init_matrix * glm.rotate(angle, IDENTITY[self.axis.value].xyz)
        self.target.matrix.set(m)
        return m

    def nvg_draw(self, vg):
        self.line.nvg_draw(vg)


class GizmoDragHandler(DragInterface):
    def __init__(self, gizmo: Gizmo, camera, *, inner=0.4, outer=0.6, depth=0.04) -> None:
        super().__init__()
        self.gizmo = gizmo
        self.camera = camera
        self.selected = EventProperty[Optional[Shape]](None)

        # draggable
        self.drag_shapes = self.create_rotation_shapes(inner, outer, depth)
        for drag_shape in self.drag_shapes.keys():
            gizmo.add_shape(drag_shape)

        self.context: Optional[DragContext] = None

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

    def begin(self, mouse_input: MouseInput):
        hit = self.gizmo.hit
        match self.drag_shapes.get(hit.shape):  # type: ignore
            case (t, kw):
                # ring is not selectable
                self.context = t(
                    hit.cursor_pos, manipulator=hit.shape,
                    target=self.selected.value, camera=self.camera, **kw)
            case _:
                self.select(hit.shape)

    def drag(self, mouse_input: MouseInput, dx, dy):
        if self.context:
            m = self.context.drag(glm.vec2(mouse_input.x, mouse_input.y))
            for drag_shape in self.drag_shapes.keys():
                drag_shape.matrix.set(m)

    def end(self, mouse_input: MouseInput):
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
        if shape:
            shape.add_state(ShapeState.SELECT)
            for drag_shape in self.drag_shapes.keys():
                drag_shape.matrix.set(shape.matrix.value)
                drag_shape.remove_state(ShapeState.HIDE)
        else:
            for drag_shape in self.drag_shapes.keys():
                drag_shape.add_state(ShapeState.HIDE)
        self.selected.set(shape)
