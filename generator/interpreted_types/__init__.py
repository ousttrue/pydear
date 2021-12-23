import io
from clang import cindex
from .basetype import BaseType
from . import primitive_types
from .pointer_types import PointerType, ReferenceType, ArrayType


class TypedefType(BaseType):
    @property
    def typing(self) -> str:
        return self.name

    def param(self, name: str) -> str:
        return name

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef p{i} = {name}
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}return {call}
'''


class StructType(BaseType):
    cursor: cindex.Cursor

    def __init__(self, name: str, cursor: cindex.Cursor, is_const=False):
        super().__init__(name, is_const)
        self.cursor = cursor

    @property
    def ctypes_type(self) -> str:
        return self.cursor.spelling

    @property
    def typing(self) -> str:
        return self.cursor.spelling

    def param(self, name: str) -> str:
        return name

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef p{i} = {name}
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef void* value = <void*>{call}
{indent}return ctypes.c_void_p(value)
'''


class ImVector(BaseType):
    def __init__(self):
        super().__init__('ImVector')

    @property
    def ctypes_type(self) -> str:
        return 'ImVector'


IMVECTOR = ImVector()

# @property
# def _typedef_underlying_type(self) -> Optional['TypeWrap']:
#     if self.type.spelling == 'size_t':
#         return None
#     match self.type.kind:
#         case cindex.TypeKind.TYPEDEF:
#             ref: cindex.Cursor = next(iter(
#                 c for c in self.cursor.get_children() if c.kind == cindex.CursorKind.TYPE_REF))
#             return TypeWrap(ref.referenced.underlying_typedef_type, ref.referenced)

#         case _:
#             return None

# @property
# def underlying_spelling(self) -> str:
#     if self.type.kind == cindex.TypeKind.CONSTANTARRAY:
#         tw = TypeWrap(self.type.get_array_element_type(), self.cursor)
#         return f'{tw.underlying_spelling} [{self.type.get_array_size()}]'
#     elif self.type.kind == cindex.TypeKind.POINTER:
#         tw = TypeWrap(self.type.get_pointee(), self.cursor)
#         if tw.underlying_spelling.endswith('*'):
#             return f'{tw.underlying_spelling}*'
#         else:
#             return f'{tw.underlying_spelling} *'
#     else:
#         current = self
#         while True:
#             base = current._typedef_underlying_type
#             if not base:
#                 break
#             current = base
#         value = current.type.spelling
#         if '(*)' in value:
#             # fp
#             return self.cursor.type.spelling
#         return value


def ref_from_children(cursor: cindex.Cursor):
    try:
        return next(iter(
            c for c in cursor.get_children() if c.kind == cindex.CursorKind.TYPE_REF))
    except:
        pass


def from_cursor(cursor_type: cindex.Type, cursor: cindex.Cursor) -> BaseType:
    if cursor.spelling == 'font_cfg':
        pass

    if cursor_type.spelling.startswith('ImVector<'):
        return IMVECTOR

    match cursor_type.kind:
        case cindex.TypeKind.VOID:
            return primitive_types.VoidType(cursor_type.is_const_qualified())

        case cindex.TypeKind.BOOL:
            return primitive_types.BoolType(cursor_type.is_const_qualified())

        case cindex.TypeKind.CHAR_S:
            return primitive_types.Int8Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.SHORT:
            return primitive_types.Int16Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.INT:
            return primitive_types.Int32Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.LONGLONG:
            return primitive_types.Int64Type(cursor_type.is_const_qualified())

        case cindex.TypeKind.UCHAR:
            return primitive_types.UInt8Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.USHORT:
            return primitive_types.UInt16Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.UINT:
            return primitive_types.UInt32Type(cursor_type.is_const_qualified())
        case cindex.TypeKind.ULONGLONG:
            return primitive_types.UInt64Type(cursor_type.is_const_qualified())

        case cindex.TypeKind.FLOAT:
            return primitive_types.FloatType(cursor_type.is_const_qualified())
        case cindex.TypeKind.DOUBLE:
            return primitive_types.DoubleType(cursor_type.is_const_qualified())

        case cindex.TypeKind.POINTER:
            pointee = cursor_type.get_pointee()
            base = from_cursor(pointee, cursor)
            return PointerType(base, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.LVALUEREFERENCE:
            pointee = cursor_type.get_pointee()
            base = from_cursor(pointee, cursor)
            return ReferenceType(base, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.CONSTANTARRAY:
            element = cursor_type.get_array_element_type()
            base = from_cursor(element, cursor)
            return ArrayType(base, cursor_type.get_array_size(), is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.TYPEDEF:
            deref = ref_from_children(cursor)
            assert deref.referenced.kind == cindex.CursorKind.TYPEDEF_DECL
            underlying = deref.referenced.underlying_typedef_type
            base = from_cursor(underlying, deref.referenced)
            return TypedefType(cursor.spelling, base, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.RECORD:
            deref = ref_from_children(cursor)
            assert deref.referenced.kind == cindex.CursorKind.STRUCT_DECL
            return StructType(deref.referenced.spelling, deref.referenced, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.FUNCTIONPROTO:
            return PointerType(primitive_types.VoidType(), is_const=cursor_type.is_const_qualified())

    raise RuntimeError(f"unknown type: {cursor_type.kind}")
