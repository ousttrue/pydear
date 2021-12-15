from typing import Tuple, Union, Optional, List
import logging
import re

logger = logging.getLogger(__name__)


class InType:
    def __init__(self, c_type: str):
        self.c_type = c_type

    def match(self, spelling: str) -> bool:
        return spelling == self.c_type

    @property
    def py_type(self) -> str:
        return self.c_type

    def to_c(self, name: str) -> str:
        return name

    @property
    def cdef(self) -> str:
        return f'cdef {self.c_type}'


class WrapFlags(InType):
    def __init__(self, c_type: str, *, fields: bool = False, methods: Union[bool, Tuple[str, ...]] = False):
        super().__init__(c_type)
        self.fields = fields
        self.methods = methods

    def to_c(self, name: str) -> str:
        # deref = get_deref(spelling)
        # if deref and deref in WRAP_TYPES:
        return f'<cpp_imgui.{self.c_type} *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    @property
    def cdef(self) -> str:
        return f'cdef cpp_imgui.{self.c_type} *'

WRAP_TYPES = [
    WrapFlags('ImVec2', fields=True),
    WrapFlags('ImVec4', fields=True),
    WrapFlags('ImFont'),
    WrapFlags('ImFontAtlas', fields=True, methods=(
        'GetTexDataAsRGBA32', 'ClearTexData',)),
    WrapFlags('ImGuiIO', fields=True),
    WrapFlags('ImGuiContext'),
    WrapFlags('ImDrawCmd', fields=True),
    WrapFlags('ImDrawData', fields=True),
    WrapFlags('ImDrawCmdHeader'),
    WrapFlags('ImDrawListSplitter'),
    WrapFlags('ImDrawList', fields=True),
    WrapFlags('ImGuiStyle'),
]


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
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


IN_TYPE_MAP: List[InType] = [
    InType('bool'),
    InType('int'),
    InType('float'),
    CtypesArrayInType('bool *'),
    CtypesArrayInType('int *'),
    CtypesArrayInType('float *'),
    ZeroTerminatedBytesInType('const char *'),
    DoublePointerResultInType('unsigned char **'),
]


def prepare(src: str) -> str:
    # array to pointer
    m = re.match(r'(\w+) \[\w+\]', src)
    if m:
        return m.group(1) + ' *'
    return src


def get_deref(src: str) -> Optional[str]:
    if src.endswith(' *'):
        return src[:-2]
    m = re.match(r'const (\w+) &', src)
    if m:
        return m.group(1)


def get_type(spelling: str) -> InType:
    spelling = prepare(spelling)

    deref = get_deref(spelling)
    if deref:
        for t in WRAP_TYPES:
            if t.match(deref):
                return t

    m = re.match(r'(?:const )?(\w+) &', spelling)
    if m:
        deref = m.group(1)
        for t in WRAP_TYPES:
            if t.match(deref):
                return t

    for t in IN_TYPE_MAP:
        if t.match(spelling):
            return t

    raise RuntimeError()
