import ctypes
from typing import Tuple, Union, Optional, List
import logging
import re


logger = logging.getLogger(__name__)


class BaseType:
    def __init__(self, c_type: str):
        self.c_type = c_type

    def match(self, spelling: str) -> bool:
        return spelling == self.c_type

    @property
    def py_type(self) -> str:
        return self.c_type

    @property
    def cypes_type(self) -> str:
        return self.py_type

    def to_c(self, name: str) -> str:
        return name

    @property
    def cdef(self) -> str:
        return f'cdef {self.c_type}'

    def to_py(self, name: str) -> str:
        return name


class BoolType(BaseType):
    def __init__(self):
        super().__init__('bool')

    @property
    def py_type(self) -> str:
        return 'bool'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_bool'


class UInt16Type(BaseType):
    def __init__(self):
        super().__init__('unsigned short')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_uint16'


class UInt32Type(BaseType):
    def __init__(self):
        super().__init__('unsigned int')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_uint32'


class UInt64Type(BaseType):
    def __init__(self):
        super().__init__('unsigned long long')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_uint64'


class Int32Type(BaseType):
    def __init__(self):
        super().__init__('int')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_int32'


class FloatType(BaseType):
    def __init__(self):
        super().__init__('float')

    @property
    def py_type(self) -> str:
        return 'float'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_float'


class DoubleType(BaseType):
    def __init__(self):
        super().__init__('double')

    @property
    def py_type(self) -> str:
        return 'float'

    @property
    def cypes_type(self) -> str:
        return 'ctypes.c_double'


class VoidInType(BaseType):
    def __init__(self):
        super().__init__('void')

    @property
    def py_type(self) -> str:
        return 'None'


class WrapFlags(BaseType):
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
    WrapFlags('ImGuiViewport'),
]


class VoidPointerInType(BaseType):
    def __init__(self):
        super().__init__('void *')

    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<void *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_py(self, name: str) -> str:
        return f'ctypes.c_void_p(<long long>{name})'


class CtypesArrayInType(BaseType):
    def match(self, spelling: str) -> bool:
        if spelling == self.c_type:
            return True
        if spelling.replace('&', '*') == self.c_type:
            return True
        return False

    @property
    def py_type(self) -> str:
        return 'ctypes.Array'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class BytesInType(BaseType):
    def __init__(self, c_type: str):
        super().__init__(c_type)

    @property
    def py_type(self) -> str:
        return 'bytes'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}>{name}'


class DoublePointerResultInType(BaseType):
    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


VOID_POINTER = VoidPointerInType()

IN_TYPE_MAP: List[BaseType] = [
    VoidInType(),
    BoolType(),
    UInt16Type(),
    Int32Type(),
    UInt32Type(),
    UInt64Type(),
    FloatType(),
    DoubleType(),
    VOID_POINTER,
    CtypesArrayInType('bool *'),
    CtypesArrayInType('int *'),
    CtypesArrayInType('unsigned int *'),
    CtypesArrayInType('float *'),
    CtypesArrayInType('size_t *'),
    BytesInType('const char *'),
    BytesInType('unsigned char *'),
    DoublePointerResultInType('unsigned char **'),
    DoublePointerResultInType('void **'),
]


def get_array_element_type(src: str) -> Optional[re.Match]:
    return re.match(r'(\w+) (\[\w+\])', src)


def get_deref(src: str) -> Optional[str]:
    if src.endswith(' *'):
        return src[:-2]
    m = re.match(r'const (\w+) &', src)
    if m:
        return m.group(1)


def get_type(spelling: str) -> BaseType:
    spelling = spelling.replace('[]', '*')

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

    m = re.match(r'(?:const )?(\w+) [&*]', spelling)
    if m:
        deref = m.group(1)
        for t in WRAP_TYPES:
            if t.match(deref):
                return t

    for t in IN_TYPE_MAP:
        if t.match(spelling):
            return t

    if spelling.endswith('*') or spelling.endswith('&'):
        # unknown pointer
        return VOID_POINTER
    if '(*)' in spelling:
        # function pointer
        return VOID_POINTER

    raise RuntimeError()


def get_field_type(spelling: str) -> str:
    array_type = get_array_element_type(spelling)
    t = get_type(spelling).cypes_type
    if array_type:
        return t + ' ' + array_type.group(2)
    else:
        return t
