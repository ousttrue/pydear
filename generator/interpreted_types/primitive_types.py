from .basetype import BaseType

TYPING_MAP = {
    'ctypes.c_bool': 'bool',
    'ctypes.c_uint8': 'int',
    'ctypes.c_uint16': 'int',
    'ctypes.c_uint32': 'int',
    'ctypes.c_uint64': 'int',
    'ctypes.c_int8': 'int',
    'ctypes.c_int16': 'int',
    'ctypes.c_int32': 'int',
    'ctypes.c_int64': 'int',
    'ctypes.c_float': 'float',
    'ctypes.c_double': 'float',
}


class VoidType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('void', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'None'

    def result_typing(self, pyi: bool) -> str:
        return 'None'

    def cpp_result(self, indent: str, call: str) -> str:
        return f'''{indent}{call};
{indent}return nullptr;
'''


class PrimitiveType(BaseType):
    def result_typing(self, pyi: bool) -> str:
        if pyi:
            return TYPING_MAP[self.ctypes_type]
        else:
            return self.ctypes_type

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        if pyi:
            return f'{name}: {TYPING_MAP[self.ctypes_type]}{default_value}'
        else:
            return f'{self.name} {name}{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef {self.name} p{i} = {name}
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef {self.name} value = {call}
{indent}return value
'''


class BoolType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('bool', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_bool'

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}bool p{i} = t{i} ? t{i} == Py_True : {default_value};\n'
        else:
            return f'{indent}bool p{i} = t{i} == Py_True;\n'

    def cpp_result(self, indent: str, call: str) -> str:
        return f'''{indent}auto value = {call};
{indent}return value ? Py_True : Py_False;
'''


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

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}unsigned int p{i} = t{i} ? PyLong_AsUnsignedLong(t{i}) : {default_value};\n'
        else:
            return f'{indent}unsigned int p{i} = PyLong_AsUnsignedLong(t{i});\n'

    def cpp_result(self, indent: str, call: str) -> str:
        return f'''{indent}auto value = {call};
{indent}return PyLong_FromUnsignedLong(value);
'''


class UInt64Type(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('unsigned long long', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_uint64'


class SizeType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('size_t', is_const)

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

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}int p{i} = t{i} ? PyLong_AsLong(t{i}) : {default_value};\n'
        else:
            return f'{indent}int p{i} = PyLong_AsLong(t{i});\n'


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

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}float p{i} = t{i} ? PyFloat_AsDouble(t{i}) : {default_value};\n'
        else:
            return f'{indent}float p{i} = PyFloat_AsDouble(t{i});\n'

    def cpp_result(self, indent: str, call: str) -> str:
        return f'''{indent}auto value = {call};
{indent}return PyFloat_FromDouble(value);
'''


class DoubleType(PrimitiveType):
    def __init__(self, is_const=False):
        super().__init__('double', is_const)

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_float'


def get(src: str, is_const: bool) -> PrimitiveType:
    match src:
        case 'float':
            return FloatType(is_const=is_const)

    raise RuntimeError()
