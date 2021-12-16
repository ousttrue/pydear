import re
from .basetype import BaseType
from .const import const


class PointerType(BaseType):
    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(.*)$', spelling)
        if m and m.group(1) == self.c_type:
            return True
        return False

    @property
    def py_typing(self) -> str:
        '''
        cast で pointer 化可能な型。bytes....
        '''
        raise NotImplementedError()

    def get_pointer(self, name: str) -> str:
        raise NotImplementedError()

    def const_c_type(self, is_const: bool) -> str:
        return f'{const(is_const)}{self.c_type}'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{self.const_c_type(is_const)}>{self.get_pointer(name)}'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {self.const_c_type(is_const)}'


class BytesType(PointerType):
    '''
    conat char * など
    '''

    def __init__(self, c_type: str):
        super().__init__(c_type)

    @property
    def py_typing(self) -> str:
        return 'Union[bytes, str]'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_void_p'

    def get_pointer(self, name: str) -> str:
        return f'{name} if {name} else NULL'

    def param(self, indent: str, i: int, name: str, is_const: bool) -> str:
        return f'''{indent}pp{i} = {name}.encode("utf-8") if isinstance({name}, str) else {name}
{indent}{self.to_cdef(is_const)} p{i} = {self.to_c(f"pp{i}", is_const)}'''


class CtypesPointerType(PointerType):
    @property
    def py_typing(self) -> str:
        return 'ctypes.c_void_p'

    def get_pointer(self, name: str) -> str:
        return f'<uintptr_t>(ctypes.addressof({name}) if isinstance({name}, ctypes.Array) else {name}.value) if {name} else NULL'

    def to_py(self, name: str) -> str:
        return f'ctypes.c_void_p(<uintptr_t>{name})'


class VoidPointerType(CtypesPointerType):
    def __init__(self):
        super().__init__('void *')


class CtypesArrayType(CtypesPointerType):
    '''
    bool *, float * など
    '''

    def __init__(self, name: str):
        super().__init__(name + ' *')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?([\w _]+)(?: [\*&])$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_typing(self) -> str:
        return 'ctypes.Array'

    @property
    def field_ctypes_type(self) -> str:
        return 'ctypes.c_void_p'
