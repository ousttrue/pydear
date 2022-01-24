from typing import NamedTuple, Callable


class Item(NamedTuple):
    name: str
    show: Callable[[], None]
