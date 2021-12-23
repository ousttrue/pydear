from typing import Iterable, NamedTuple
import dataclasses


@dataclasses.dataclass
class BaseType:
    name: str
    is_const: bool = False
