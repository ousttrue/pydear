from typing import NamedTuple, Tuple, Union, Callable, Dict
import logging

logger = logging.getLogger(__name__)


class WrapFlags(NamedTuple):
    fields: bool = False
    methods: Union[bool, Tuple[str, ...]] = False


WRAP_TYPES = {
    'ImVec2': WrapFlags(fields=True),
    'ImVec4': WrapFlags(fields=True),
    'ImFont': WrapFlags(),
    'ImFontAtlas': WrapFlags(fields=True, methods=('GetTexDataAsRGBA32', 'ClearTexData',)),
    'ImGuiIO': WrapFlags(fields=True),
    'ImGuiContext': WrapFlags(),
    'ImDrawCmd': WrapFlags(fields=True),
    'ImDrawData': WrapFlags(fields=True),
    'ImDrawCmdHeader': WrapFlags(),
    'ImDrawListSplitter': WrapFlags(),
    'ImDrawList': WrapFlags(fields=True),
    'ImGuiStyle': WrapFlags(),
}


class InType:
    def __init__(self, c_type: str):
        self.c_type = c_type

    @property
    def py_type(self) -> str:
        return self.c_type

    def to_c(self, name: str) -> str:
        return name


class CtypesArrayInType(InType):
    @property
    def py_type(self) -> str:
        return 'ctypes.Array'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class ZeroTerminatedBytesInType(InType):
    @property
    def py_type(self) -> str:
        return 'bytes'

    def to_c(self, name: str) -> str:
        return f'<const char *>{name}'


class DoublePointerResultInType(InType):
    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<uintptr_t>ctypes.addressof({name}) if {name} else NULL'


IN_TYPE_MAP: Dict[str, InType] = {
    'int': InType('int'),
    'bool *': CtypesArrayInType('bool *'),
    'int *': CtypesArrayInType('int *'),
    'const char *': ZeroTerminatedBytesInType('const char *'),
    'unsigned char **': DoublePointerResultInType('unsigned char **'),
}


def in_type(spelling: str):
    value = IN_TYPE_MAP.get(spelling)
    if value:
        return value.py_type

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return deref

    raise NotImplementedError(spelling)


def to_c(spelling: str, name: str) -> str:
    value = IN_TYPE_MAP.get(spelling)
    if value:
        return value.to_c(name)

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return f'<cpp_imgui.{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    raise NotImplementedError(spelling)
