from typing import Iterable, NamedTuple, Optional
import dataclasses


@dataclasses.dataclass
class BaseType:
    name: str
    base: Optional['BaseType'] = None
    is_const: bool = False
