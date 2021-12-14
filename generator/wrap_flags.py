from typing import NamedTuple, Tuple, Union, Callable, Dict, Optional
import logging
import re

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
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


IN_TYPE_MAP: Dict[str, InType] = {
    'int': InType('int'),
    'float': InType('float'),
    'bool *': CtypesArrayInType('bool *'),
    'int *': CtypesArrayInType('int *'),
    'float *': CtypesArrayInType('float *'),
    'const char *': ZeroTerminatedBytesInType('const char *'),
    'unsigned char **': DoublePointerResultInType('unsigned char **'),
}


def get_deref(src: str) -> Optional[str]:
    if src.endswith(' *'):
        return src[:-2]
    m = re.match(r'const (\w+) &', src)
    if m:
        return m.group(1)


def prepare(src: str) -> str:
    # array to pointer
    m = re.match(r'(\w+) \[\w+\]', src)
    if m:
        return m.group(1) + ' *'
    return src


def in_type(spelling: str):
    spelling = prepare(spelling)

    value = IN_TYPE_MAP.get(spelling)
    if value:
        return value.py_type

    deref = get_deref(spelling)
    if deref and deref in WRAP_TYPES:
        return deref

    m = re.match(r'const (\w+) &', spelling)
    if m:
        deref = m.group(1)
        if deref in WRAP_TYPES:
            return deref

    raise NotImplementedError(spelling)


def const_ref(src: str) -> str:
    if 'const' in src:
        src = src.replace('const ', '')
        return 'const cpp_imgui.' + prepare(src).replace('&', '*')
    else:
        return 'cpp_imgui.' + prepare(src).replace('&', '*')


def to_c(spelling: str, name: str) -> str:
    spelling = prepare(spelling)

    value = IN_TYPE_MAP.get(spelling)
    if value:
        return value.to_c(name)

    deref = get_deref(spelling)
    if deref and deref in WRAP_TYPES:
        return f'<{const_ref(spelling)}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    raise NotImplementedError(spelling)
