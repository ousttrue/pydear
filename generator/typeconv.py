# from typing import Optional, List
# import logging
# import re
from . import interpreted_types
# from .interpreted_types.wrap_types import *
# from .interpreted_types.pointer_types import *
# from .interpreted_types.primitive_types import *

# logger = logging.getLogger(__name__)


# class StringType(BaseType):
#     def __init__(self):
#         super().__init__('std::string')

#     @property
#     def py_typing(self) -> Iterable[str]:
#         yield 'string'

#     def to_c(self, name: str, is_const: bool) -> str:
#         return 'string'

#     def to_cdef(self, is_const: bool) -> str:
#         return f'cdef string'


# class FunctionPointer(BaseType):
#     def __init__(self, name: str):
#         super().__init__(name)

#     @property
#     def py_typing(self) -> Iterable[str]:
#         yield 'ctypes.c_void_p'

#     def param(self, indent: str, i: int, name: str, is_const: bool) -> str:
#         return f'{indent}cdef impl.{self.c_type} p{i}= <impl.{self.c_type}><void*><uintptr_t>{name}'


# IMVECTOR_TYPE = WrapType('ImVector')
# VOID_POINTER = VoidPointerType()
# IN_TYPE_MAP: List[BaseType] = [
#     # FunctionPointer(),
#     VoidType(),
#     BoolType(),
#     Int8Type(),
#     Int16Type(),
#     Int32Type(),
#     UInt8Type(),
#     UInt16Type(),
#     UInt32Type(),
#     UInt64Type(),
#     FloatType(),
#     DoubleType(),
#     VOID_POINTER,
#     CtypesArrayType('bool'),
#     CtypesArrayType('int'),
#     CtypesArrayType('unsigned short'),
#     CtypesArrayType('unsigned int'),
#     CtypesArrayType('float'),
#     CtypesArrayType('double'),
#     CtypesArrayType('size_t'),
#     CtypesArrayType('unsigned char *'),
#     BytesType('char *'),
#     BytesType('unsigned char *'),
#     # CtypesPointerType('unsigned char **'),
#     CtypesPointerType('void **'),
#     # CtypesPointerType('unsigned short *'),
#     # out
#     ImVec2WrapType(),
#     ImVec4WrapType(),
#     # field
#     WrapType('ImDrawCmdHeader'),
#     WrapType('ImDrawListSplitter'),
#     StringType(),
# ]
# for w in WRAP_TYPES:
#     IN_TYPE_MAP.append(WrapPointerType(w.name))
#     match w.name:
#         case 'ImVec2':
#             IN_TYPE_MAP.append(ImVec2WrapReferenceType())
#         case _:
#             IN_TYPE_MAP.append(WrapReferenceType(w.name))


# def get_array_element_type(src: str) -> Optional[re.Match]:
#     return re.match(r'([ \w]+) \[(\w+)\]', src)


def get_type(spelling: str) -> interpreted_types.BaseType:
    pass
#     spelling = spelling.replace('[]', '*')

#     array_type = get_array_element_type(spelling)
#     if array_type:
#         spelling = array_type.group(1) + ' *'

#     if spelling.startswith('ImVector<'):
#         return IMVECTOR_TYPE

#     for t in IN_TYPE_MAP:
#         if t.match(spelling):
#             return t

#     if spelling.endswith('*') or spelling.endswith('&'):
#         # unknown pointer
#         logger.debug(f'unknown: void*: {spelling}')
#         return VOID_POINTER
#     # if '(*)' in spelling:
#     #     # function pointer
#     #     return VOID_POINTER

#     # # may function pointer
#     # return VOID_POINTER

#     # raise RuntimeError()
#     logger.debug(f'function pointer?: {spelling}')
#     return FunctionPointer(spelling)


def get_field_type(spelling: str) -> str:
    pass
#     array_type = get_array_element_type(spelling)
#     if array_type:
#         t = get_type(array_type.group(1)).field_ctypes_type
#         return t + '*' + array_type.group(2)
#     else:
#         t = get_type(spelling).field_ctypes_type
#         return t
