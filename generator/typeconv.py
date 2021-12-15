from typing import Optional, List, Callable
import logging
import re
from . import wraptypes


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
    def field_ctypes_type(self) -> str:
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
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_bool'


class UInt16Type(BaseType):
    def __init__(self):
        super().__init__('unsigned short')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_uint16'


class UInt32Type(BaseType):
    def __init__(self):
        super().__init__('unsigned int')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_uint32'


class UInt64Type(BaseType):
    def __init__(self):
        super().__init__('unsigned long long')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_uint64'


class Int32Type(BaseType):
    def __init__(self):
        super().__init__('int')

    @property
    def py_type(self) -> str:
        return 'int'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_int32'


class FloatType(BaseType):
    def __init__(self):
        super().__init__('float')

    @property
    def py_type(self) -> str:
        return 'float'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_float'


class DoubleType(BaseType):
    def __init__(self):
        super().__init__('double')

    @property
    def py_type(self) -> str:
        return 'float'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_double'


class VoidInType(BaseType):
    def __init__(self):
        super().__init__('void')

    @property
    def py_type(self) -> str:
        return 'None'


class WrapInType(BaseType):
    def __init__(self, name: str,
                 to_c: Optional[Callable[[str], str]] = None,
                 to_py: Optional[Callable[[str], str]] = None):
        super().__init__(name)
        self._to_c = to_c
        self._to_py = to_py

    def to_c(self, name: str) -> str:
        if self._to_c:
            return self._to_c(name)
        else:
            return name

    @property
    def cdef(self) -> str:
        return f'cdef cpp_imgui.{self.c_type}'

    def to_py(self, name: str) -> str:
        if self._to_py:
            return self._to_py(name)
        else:
            return name


class WrapPointerInType(BaseType):
    def __init__(self, name: str):
        super().__init__(name + ' *')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: \*)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_type(self) -> str:
        return self._name

    @property
    def field_ctypes_type(self) -> str:
        return f'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<cpp_imgui.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    @property
    def cdef(self) -> str:
        return f'cdef cpp_imgui.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'


class WrapReferenceInType(BaseType):
    def __init__(self, name: str):
        super().__init__(name + ' &')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: &)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_type(self) -> str:
        return self._name

    @property
    def field_ctypes_type(self) -> str:
        return self._name

    def to_c(self, name: str) -> str:
        return f'<cpp_imgui.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    @property
    def cdef(self) -> str:
        return f'cdef cpp_imgui.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'


IMVECTOR_TYPE = WrapInType('ImVector')


class VoidPointerInType(BaseType):
    def __init__(self):
        super().__init__('void *')

    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<void *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_py(self, name: str) -> str:
        return f'ctypes.c_void_p(<uintptr_t>{name})'


class ConstVoidPointerInType(BaseType):
    def __init__(self):
        super().__init__('const void *')

    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<const void *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_py(self, name: str) -> str:
        return f'ctypes.c_void_p(<uintptr_t>{name})'


class CtypesArrayInType(BaseType):
    def __init__(self, name: str):
        super().__init__(name + ' *')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: [\*&])?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_type(self) -> str:
        return 'ctypes.Array'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class BytesInType(BaseType):
    def __init__(self, c_type: str):
        super().__init__(c_type)

    @property
    def py_type(self) -> str:
        return 'bytes'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}>{name}'


class DoublePointerResultInType(BaseType):
    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


CONST_VOID_POINTER = ConstVoidPointerInType()
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
    CONST_VOID_POINTER,
    CtypesArrayInType('bool'),
    CtypesArrayInType('int'),
    CtypesArrayInType('unsigned int'),
    CtypesArrayInType('float'),
    CtypesArrayInType('double'),
    CtypesArrayInType('size_t'),
    BytesInType('const char *'),
    BytesInType('unsigned char *'),
    DoublePointerResultInType('unsigned char **'),
    DoublePointerResultInType('void **'),
    # out
    WrapInType('ImVec2',
               lambda name: f'cpp_imgui.ImVec2({name}.x, {name}.y)',
               lambda name: f'({name}.x, {name}.y)'
               ),
    WrapInType(
        'ImVec4',
        lambda name: f'cpp_imgui.ImVec4({name}.x, {name}.y, {name}.z, {name}.w)',
        lambda name: f'({name}.x, {name}.y, {name}.z, {name}.w)'
    ),
    # field
    WrapInType('ImDrawCmdHeader'),
    WrapInType('ImDrawListSplitter'),
]
for w in wraptypes.WRAP_TYPES:
    IN_TYPE_MAP.append(WrapPointerInType(w.name))
    IN_TYPE_MAP.append(WrapReferenceInType(w.name))


def get_array_element_type(src: str) -> Optional[re.Match]:
    return re.match(r'([ \w]+) \[(\w+)\]', src)


def get_type(spelling: str) -> BaseType:
    spelling = spelling.replace('[]', '*')

    array_type = get_array_element_type(spelling)
    if array_type:
        spelling = array_type.group(1) + ' *'

    if spelling.startswith('ImVector<'):
        return IMVECTOR_TYPE

    for t in IN_TYPE_MAP:
        if t.match(spelling):
            return t

    if spelling.endswith('*') or spelling.endswith('&'):
        # unknown pointer
        if spelling.startswith('const '):
            logger.debug(f'unknown: const void*: {spelling}')
            return CONST_VOID_POINTER
        else:
            logger.debug(f'unknown: void*: {spelling}')
            return VOID_POINTER
    if '(*)' in spelling:
        # function pointer
        return VOID_POINTER

    raise RuntimeError()


def get_field_type(spelling: str) -> str:
    array_type = get_array_element_type(spelling)
    if array_type:
        t = get_type(array_type.group(1)).field_ctypes_type
        return t + '*' + array_type.group(2)
    else:
        t = get_type(spelling).field_ctypes_type
        return t
