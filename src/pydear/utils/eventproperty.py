from typing import TypeVar, Generic, Callable, TypeAlias, List
T = TypeVar('T')

Callback: TypeAlias = Callable[[T], None]


class EventProperty(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
        self.callbacks: List[Callback] = []

    def __iadd__(self, callback: Callback):
        self.callbacks.append(callback)

    def set(self, value):
        if self.value == value:
            return
        self.value = value
        self.fire()

    def fire(self):
        value = self.value
        for callback in self.callbacks:
            callback(value)
