from clang import cindex
from .basetype import BaseType
from . import primitive_types
from .pointer_types import PointerType, ReferenceType

VOID = primitive_types.VoidType()
INT8 = primitive_types.Int8Type()
INT16 = primitive_types.Int16Type()
INT32 = primitive_types.Int32Type()
INT64 = primitive_types.Int64Type()
UINT8 = primitive_types.UInt8Type()
UINT16 = primitive_types.UInt16Type()
UINT32 = primitive_types.UInt32Type()
UINT64 = primitive_types.UInt64Type()
FLOAT32 = primitive_types.FloatType()
FLOAT64 = primitive_types.DoubleType()


def from_cursor(cursor_type: cindex.Type, cursor: cindex.Cursor) -> BaseType:
    match cursor_type.kind:
        case cindex.TypeKind.VOID:
            return VOID

        case cindex.TypeKind.CHAR_S:
            return INT8
        case cindex.TypeKind.SHORT:
            return INT16
        case cindex.TypeKind.INT:
            return INT32
        case cindex.TypeKind.LONGLONG:
            return INT64

        case cindex.TypeKind.UCHAR:
            return UINT8
        case cindex.TypeKind.USHORT:
            return UINT16
        case cindex.TypeKind.UINT:
            return UINT32
        case cindex.TypeKind.ULONGLONG:
            return UINT64

        case cindex.TypeKind.FLOAT:
            return FLOAT32
        case cindex.TypeKind.DOUBLE:
            return FLOAT64

        case cindex.TypeKind.POINTER:
            pointee = cursor_type.get_pointee()
            base = from_cursor(pointee, cursor)
            return PointerType(base, is_const=cursor_type.is_const_qualified())

        case cindex.TypeKind.LVALUEREFERENCE:
            pointee = cursor_type.get_pointee()
            base = from_cursor(pointee, cursor)
            return ReferenceType(base, is_const=cursor_type.is_const_qualified())

    raise RuntimeError(f"unknown type: {cursor_type.kind}")
