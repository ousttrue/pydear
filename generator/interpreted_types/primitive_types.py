import io
from .basetype import BaseType


class VoidType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('void', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'None'

    @property
    def typing(self) -> str:
        return 'None'


class PrimitiveType(BaseType):
    @property
    def typing(self) -> str:
        return self.ctypes_type

    def param(self, name: str) -> str:
        return f'{self.name} {name}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'{indent}cdef {self.name} p{i} = {name}'

    def cdef_result(self, indent: str, call: str) -> str:
        sio = io.StringIO()
        sio.write(f'{indent}cdef {self.name} value = {call}\n')
        sio.write(f"{indent}return value\n")
        return sio.getvalue()


class BoolType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('bool', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_bool'


class UInt8Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('unsigned char', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_uint8'


class UInt16Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('unsigned short', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_uint16'


class UInt32Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('unsigned int', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_uint32'


class UInt64Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('unsigned long long', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_uint64'


class Int8Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('char', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_int8'


class Int16Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('short', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_int16'


class Int32Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('int', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_int32'


class Int64Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('long long', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_int64'


class FloatType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('float', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_float'


class DoubleType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('double', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_float'
