from clang import cindex
from .basetype import BaseType
from . import primitive_types
from .pointer_types import PointerType, ReferenceType


class TypedefType(BaseType):
    pass


class StructType(BaseType):
    cursor: cindex.Cursor

    def __init__(self, name: str, cursor: cindex.Cursor, is_const=False):
        super().__init__(name, is_const)
        self.cursor = cursor


def from_cursor(cursor_type: cindex.Type, cursor: cindex.Cursor) -> BaseType:
    match cursor_type.kind:
        case cindex.TypeKind.VOID:
            return primitive_types.VoidType(cursor_type.is_const_qualified())

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

        case cindex.TypeKind.TYPEDEF:
            ref: cindex.Cursor = next(iter(
                c for c in cursor.get_children() if c.kind == cindex.CursorKind.TYPE_REF))
            underlying = ref.referenced.underlying_typedef_type
            base = from_cursor(underlying, ref.referenced)
            return TypedefType(cursor.spelling, base, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.RECORD:
            return StructType(cursor.spelling, cursor, is_const=cursor_type.is_const_qualified())

    raise RuntimeError(f"unknown type: {cursor_type.kind}")
