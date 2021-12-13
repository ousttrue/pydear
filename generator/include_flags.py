from typing import NamedTuple, Tuple


class IncludeFlags(NamedTuple):
    fields: bool = False
    methods: Tuple[str, ...] = ()
