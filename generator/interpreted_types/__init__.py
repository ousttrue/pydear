from clang import cindex
from .basetype import BaseType
from . import primitive_types


VOID_TYPE = primitive_types.VoidType()


def from_cursor(cursor_type: cindex.Type, cursor: cindex.Cursor) -> BaseType:
    match cursor_type.kind:
        case cindex.TypeKind.VOID:
            return VOID_TYPE

    raise RuntimeError()
