from typing import NamedTuple, Optional, List, Callable, TypeAlias
import abc


class MouseInput(NamedTuple):
    x: int
    y: int
    width: int
    height: int
    left_down: bool
    right_down: bool
    middle_down: bool
    is_active: bool
    is_hover: bool
    wheel: int


Callback: TypeAlias = Callable[[MouseInput, Optional[MouseInput]], None]
BeginEndCallback: TypeAlias = Callable[[MouseInput], None]
DragCallback: TypeAlias = Callable[[MouseInput, int, int], None]


class DragInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def begin(self, mouse_input: MouseInput):
        pass

    @abc.abstractmethod
    def drag(sel, mouse_input: MouseInput, dx: int, dy: int):
        pass

    @abc.abstractmethod
    def end(self, mouse_input: MouseInput):
        pass


class MouseEvent:
    def __init__(self) -> None:
        self.callbacks: List[Callback] = []
        self.last_input: Optional[MouseInput] = None

        # highlevel event
        self.left_active = False
        self.left_pressed: List[BeginEndCallback] = []
        self.left_drag: List[DragCallback] = []
        self.left_released: List[BeginEndCallback] = []
        self.right_active = False
        self.right_pressed: List[BeginEndCallback] = []
        self.right_drag: List[DragCallback] = []
        self.right_released: List[BeginEndCallback] = []
        self.middle_active = False
        self.middle_pressed: List[BeginEndCallback] = []
        self.middle_drag: List[DragCallback] = []
        self.middle_released: List[BeginEndCallback] = []

        self.wheel: List[Callable[[int], None]] = []

    def __iadd__(self, callback: Callback):
        self.callbacks.append(callback)
        return self

    def process(self, current: MouseInput):
        for callback in self.callbacks:
            callback(current, self.last_input)

        #
        # highlevel event
        #
        dx = 0
        dy = 0
        if self.last_input:
            dx = current.x - self.last_input.x
            dy = current.y - self.last_input.y
        # pressed
        if current.is_hover:
            if (not self.last_input or not self.last_input.left_down) and current.left_down:
                self.left_active = True
                for callback in self.left_pressed:
                    callback(current)
            if (not self.last_input or not self.last_input.right_down) and current.right_down:
                self.right_active = True
                for callback in self.right_pressed:
                    callback(current)
            if (not self.last_input or not self.last_input.middle_down) and current.middle_down:
                self.middle_active = True
                for callback in self.middle_pressed:
                    callback(current)
        # drag
        if current.is_active:
            if current.left_down:
                self.left_active = True
                for callback in self.left_drag:
                    callback(current, dx, dy)
            if current.right_down:
                self.right_active = True
                for callback in self.right_drag:
                    callback(current, dx, dy)
            if current.middle_down:
                self.middle_active = True
                for callback in self.middle_drag:
                    callback(current, dx, dy)
        # released
        if self.left_active and not current.left_down:
            for callback in self.left_released:
                callback(current)
            self.left_active = False
        if self.right_active and not current.right_down:
            for callback in self.right_released:
                callback(current)
            self.right_active = False
        if self.middle_active and not current.middle_down:
            for callback in self.middle_released:
                callback(current)
            self.middle_active = False

        if current.is_active or current.is_hover:
            if current.wheel:
                for callback in self.wheel:
                    callback(current.wheel)

        self.last_input = current

    def bind_left_drag(self, drag_handler: DragInterface):
        self.left_pressed.append(drag_handler.begin)
        self.left_drag.append(drag_handler.drag)
        self.left_released.append(drag_handler.end)

    def bind_right_drag(self, drag_handler: DragInterface):
        self.right_pressed.append(drag_handler.begin)
        self.right_drag.append(drag_handler.drag)
        self.right_released.append(drag_handler.end)

    def bind_middle_drag(self, drag_handler: DragInterface):
        self.middle_pressed.append(drag_handler.begin)
        self.middle_drag.append(drag_handler.drag)
        self.middle_released.append(drag_handler.end)
