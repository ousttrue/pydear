import re
from .basetype import BaseType
from .const import const

class VoidPointerType(BaseType):
    def __init__(self):
        super().__init__('void *')

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?void \*$', spelling)
        if m:
            return True
        return False

    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}void *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}{self.c_type}'

    def to_py(self, name: str) -> str:
        return f'ctypes.c_void_p(<uintptr_t>{name})'


class CtypesArrayType(BaseType):
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

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'


class BytesType(BaseType):
    def __init__(self, c_type: str):
        super().__init__(c_type)

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(.*)$', spelling)
        if m and m.group(1) == self.c_type:
            return True
        return False

    @property
    def py_type(self) -> str:
        return 'bytes'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}{self.c_type}>{name}'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}{self.c_type}'


class DoublePointerResultType(BaseType):
    @property
    def py_type(self) -> str:
        return 'ctypes.c_void_p'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{self.c_type}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'
