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

    def to_py(self, name: str) -> str:
        return name


class VoidInType(InType):
    def __init__(self):
        super().__init__('void')

    @property
    def py_type(self) -> str:
        return 'None'


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

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<long long>{name}), ctypes.POINTER({self.py_type}))[0]'


IMVECTOR_TYPE = WrapFlags('ImVector')

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


class VoidPointerInType(InType):
    def __init__(self):
        super().__init__('void *')

    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class CtypesArrayInType(InType):
    @property
    def py_type(self) -> str:
        return 'ctypes.Array'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class BytesInType(InType):
    def __init__(self, c_type: str):
        super().__init__(c_type)

    @property
    def py_type(self) -> str:
        return 'bytes'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}>{name}'


class DoublePointerResultInType(InType):
    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


VOID_POINTER = VoidPointerInType()

IN_TYPE_MAP: List[InType] = [
    VoidInType(),
    InType('bool'),
    InType('unsigned short'),
    InType('int'),
    InType('unsigned int'),
    InType('float'),
    VOID_POINTER,
    CtypesArrayInType('bool *'),
    CtypesArrayInType('int *'),
    CtypesArrayInType('unsigned int *'),
    CtypesArrayInType('float *'),
    BytesInType('const char *'),
    BytesInType('unsigned char *'),
    DoublePointerResultInType('unsigned char **'),
]


def get_array_element_type(src: str) -> Optional[re.Match]:
    return re.match(r'(\w+) (\[\w+\])', src)


def get_deref(src: str) -> Optional[str]:
    if src.endswith(' *'):
        return src[:-2]
    m = re.match(r'const (\w+) &', src)
    if m:
        return m.group(1)


def get_type(spelling: str) -> InType:
    array_type = get_array_element_type(spelling)
    if array_type:
        spelling = array_type.group(1) + ' *'

    if spelling.startswith('ImVector<'):
        return IMVECTOR_TYPE

    for t in WRAP_TYPES:
        if t.match(spelling):
            return t
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

    if spelling.endswith('*'):
        # unknown pointer
        return VOID_POINTER
    if '(*)' in spelling:
        # function pointer
        return VOID_POINTER

    raise RuntimeError()


def _prim_to_ctypes(src: str) -> str:
    match src:
        case 'bool':
            return 'ctypes.c_bool'
        case 'int':
            return 'ctypes.c_int32'
        case 'unsigned short':
            return 'ctypes.c_uint16'
        case 'unsigned int':
            return 'ctypes.c_uint32'
        case 'float':
            return 'ctypes.c_float'
        case 'double':
            return 'ctypes.c_double'
        case _:
            return src


def get_field_type(spelling: str) -> str:
    array_type = get_array_element_type(spelling)
    t = _prim_to_ctypes(get_type(spelling).py_type)
    if array_type:
        return t + ' ' + array_type.group(2)
    else:
        return t
