from .basetype import BaseType


class StringType(BaseType):
    def __init__(self):
        super().__init__('std::string')

    @property
    def ctypes_type(self) -> str:
        return 'string'

    @property
    def result_typing(self) -> str:
        return 'string'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}return {call}
'''


class CStringType(BaseType):
    def __init__(self):
        super().__init__('const char *')

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.c_void_p'

    def param(self, name: str, default_value: str) -> str:
        return f'{name}: Union[bytes, str]{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef const char *p{i} = NULL;
{indent}if isinstance({name}, bytes):
{indent}    p{i} = <const char *>{name}
{indent}if isinstance({name}, str):
{indent}    pp{i} = {name}.encode('utf-8')
{indent}    p{i} = <const char *>pp{i}
'''

    @property
    def result_typing(self) -> str:
        return 'bytes'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}return {call}
'''
