import re
import io
from typing import Iterable
from .basetype import BaseType
from .const import const


def add_asterisk(src: str):
    # if not src.endswith('*'):
    #     return src + ' *'
    return src + '*'


class PointerType(BaseType):
    def __init__(self, base: BaseType, is_const=False):
        super().__init__(add_asterisk(base.name), base, is_const)

    @property
    def result_typing(self) -> str:
        return 'ctypes.c_void_p'

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'ctypes.Array'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str) -> str:
        return f'{name}: {self.ctypes_type}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = <{base_name} *><void*><uintptr_t>(ctypes.addressof({name}))
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef void* value = <void*>{call}
{indent}return ctypes.c_void_p(<uintptr_t>value)
'''


class ReferenceType(BaseType):
    base: BaseType

    def __init__(self, base: BaseType, is_const=False):
        super().__init__(base.name + '&', base, is_const)

    @property
    def result_typing(self) -> str:
        return 'ctypes.c_void_p'

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.Array'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str) -> str:
        return f'{name}: {self.ctypes_type}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = <{base_name} *><void*><uintptr_t>(ctypes.addressof({name}))
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef void* value = <void*>&{call}
{indent}return ctypes.c_void_p(<uintptr_t>value)
'''


class ArrayType(BaseType):
    size: int

    def __init__(self, base: BaseType, size: int, is_const=False):
        super().__init__(f'{base.name}[{size}]', base, is_const)
        self.size = size

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'{self.base.ctypes_type} * {self.size}'

    def param(self, name: str) -> str:
        return f'{name}: ctypes.Array'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = <{base_name}*><void*><uintptr_t>ctypes.addressof({name})
'''

    @property
    def result_typing(self) -> str:
        return 'ctypes.c_void_p'


class PointerToStructType(BaseType):
    def __init__(self, base: BaseType, is_const: bool):
        super().__init__(base.name + '*', base, is_const)

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'{self.base.name}'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str) -> str:
        return f'{name}: {self.ctypes_type}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.{self.ctypes_type} *p{i} = <impl.{self.ctypes_type} *><void*><uintptr_t>(ctypes.addressof({name}))
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.{self.ctypes_type} *value = {call}
{indent}return ctypes.cast(<uintptr_t>value, ctypes.POINTER({self.ctypes_type}))[0]
'''

    @property
    def result_typing(self) -> str:
        return f'{self.ctypes_type}'

# class PointerToPrimitiveType(BaseType):
#     def __init__(self, base: BaseType, is_const: bool):
#         super().__init__(base.name + '*', base, is_const)

#     @property
#     def ctypes_type(self) -> str:
#         if not self.base:
#             raise RuntimeError()
#         return f'ctypes.Array'

#     def param(self, name: str) -> str:
#         return f'{name}: {self.ctypes_type}'

#     def cdef_param(self, indent: str, i: int, name: str) -> str:
#         return f'''{indent}# {self}
# {indent}cdef {self.base.name} *p{i} = <{self.base.name} *><void*><uintptr_t>(ctypes.addressof({name}))
# '''

#     def cdef_result(self, indent: str, call: str) -> str:
#         return f'''{indent}# {self}
# {indent}cdef {self.base.name} *value = {call}
# {indent}return ctypes.c_void_p(<uintptr_t>value)
# '''

#     @property
#     def result_typing(self) -> str:
#         return f'ctypes.c_void_p'

# class BytesType(PointerType):
#     '''
#     conat char * など
#     '''

#     def __init__(self, c_type: str):
#         super().__init__(c_type)

#     @property
#     def py_typing(self) -> Iterable[str]:
#         yield 'bytes'
#         yield 'str'

#     @property
#     def field_ctypes_type(self) -> str:
#         return 'ctypes.c_void_p'

#     def get_pointer(self, name: str) -> str:
#         return f'{name} if {name} else NULL'

#     def param(self, indent: str, i: int, name: str, is_const: bool) -> str:
#         return f'''{indent}pp{i} = {name}.encode("utf-8") if isinstance({name}, str) else {name}
# {indent}{self.to_cdef(is_const)} p{i} = {self.to_c(f"pp{i}", is_const)}'''


# class CtypesPointerType(PointerType):
#     @property
#     def py_typing(self) -> Iterable[str]:
#         yield 'ctypes.c_void_p'

#     def get_pointer(self, name: str) -> str:
#         return f'(<uintptr_t>({name}.value if isinstance({name}, ctypes.c_void_p) else <uintptr_t>ctypes.addressof({name})) if {name} else <uintptr_t>NULL)'

#     def to_py(self, name: str) -> str:
#         return f'ctypes.c_void_p(<uintptr_t>{name})'


# class VoidPointerType(CtypesPointerType):
#     def __init__(self):
#         super().__init__('void *')


# class CtypesArrayType(CtypesPointerType):
#     '''
#     bool *, float * など
#     '''

#     def __init__(self, name: str):
#         super().__init__((name + '*') if name.endswith('*') else (name + ' *'))
#         self._name = name

#     def match(self, spelling: str) -> bool:
#         if spelling.startswith('const '):
#             spelling = spelling[len('const '):]
#         if spelling[-1] in ('*', '&'):
#             if spelling[:-1].rstrip() == self._name:
#                 return True
#         return False

#     @property
#     def py_typing(self) -> Iterable[str]:
#         yield 'ctypes.Array'

#     @property
#     def field_ctypes_type(self) -> str:
#         return 'ctypes.c_void_p'
