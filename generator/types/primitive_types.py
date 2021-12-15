from .basetype import BaseType


class VoidType(BaseType):
    def __init__(self):
        super().__init__('void')

    @property
    def py_type(self) -> str:
        return 'None'


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
