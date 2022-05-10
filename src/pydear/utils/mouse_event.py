from typing import NamedTuple, Optional, List, Callable, TypeAlias


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
XYCallback: TypeAlias = Callable[[int, int], None]
DragCallback: TypeAlias = Callable[[int, int, int, int], None]


class MouseEvent:
    def __init__(self) -> None:
        self.callbacks: List[Callback] = []
        self.last_input: Optional[MouseInput] = None

        # highlevel event
        self.left_active = False
        self.left_pressed: List[XYCallback] = []
        self.left_drag: List[DragCallback] = []
        self.left_released: List[XYCallback] = []
        self.right_active = False
        self.right_pressed: List[XYCallback] = []
        self.right_drag: List[DragCallback] = []
        self.right_released: List[XYCallback] = []
        self.middle_active = False
        self.middle_pressed: List[XYCallback] = []
        self.middle_drag: List[DragCallback] = []
        self.middle_released: List[XYCallback] = []

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
                    callback(current.x, current.y)
            if (not self.last_input or not self.last_input.right_down) and current.right_down:
                self.right_active = True
                for callback in self.right_pressed:
                    callback(current.x, current.y)
            if (not self.last_input or not self.last_input.middle_down) and current.middle_down:
                self.middle_active = True
                for callback in self.middle_pressed:
                    callback(current.x, current.y)
        # drag
        if current.is_active:
            if current.left_down:
                self.left_active = True
                for callback in self.left_drag:
                    callback(current.x, current.y, dx, dy)
            if current.right_down:
                self.right_active = True
                for callback in self.right_drag:
                    callback(current.x, current.y, dx, dy)
            if current.middle_down:
                self.middle_active = True
                for callback in self.middle_drag:
                    callback(current.x, current.y, dx, dy)
        # released
        if self.left_active and not current.left_down:
            for callback in self.left_released:
                callback(current.x, current.y)
            self.left_active = False
        if self.right_active and not current.right_down:
            for callback in self.right_released:
                callback(current.x, current.y)
            self.right_active = False
        if self.middle_active and not current.middle_down:
            for callback in self.middle_released:
                callback(current.x, current.y)
            self.middle_active = False

        if current.wheel:
            for callback in self.wheel:
                callback(current.wheel)

        self.last_input = current
