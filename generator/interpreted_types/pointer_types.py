import re
from typing import Iterable
from .basetype import BaseType
from .const import const


def add_asterisk(src: str):
    # if not src.endswith('*'):
    #     return src + ' *'
    return src + '*'


class PointerType(BaseType):
    base: BaseType

    def __init__(self, base: BaseType, is_const=False):
        super().__init__(add_asterisk(base.name), is_const)


class ReferenceType(BaseType):
    base: BaseType

    def __init__(self, base: BaseType, is_const=False):
        super().__init__(base.name + '&', is_const)


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
