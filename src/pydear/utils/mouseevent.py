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


class MouseEvent:
    def __init__(self) -> None:
        self.callbacks: List[Callback] = []
        self.last_input: Optional[MouseInput] = None

    def __iadd__(self, callback: Callback):
        self.callbacks.append(callback)
        return self

    def process(self, current: MouseInput):
        for callback in self.callbacks:
            callback(current, self.last_input)
        self.last_input = current
