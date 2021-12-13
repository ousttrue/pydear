from typing import NamedTuple
import re
from clang import cindex
from . import utils


class TypeWrap(NamedTuple):
    '''
    function result_type
    function param type
    struct field type
    '''
    type: cindex.Type
    cursor: cindex.Cursor

    @staticmethod
    def from_function_result(cursor: cindex.Cursor):
        return TypeWrap(cursor.result_type, cursor)

    @staticmethod
    def from_function_param(cursor: cindex.Cursor):
        return TypeWrap(cursor.type, cursor)

    @staticmethod
    def get_function_params(cursor: cindex.Cursor, *, excludes=()):
        return [TypeWrap.from_function_param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL and child.type.spelling not in excludes]

    @staticmethod
    def from_struct_field(cursor: cindex.Cursor):
        return TypeWrap(cursor.type, cursor)

    @staticmethod
    def get_struct_fields(cursor: cindex.Cursor):
        return [TypeWrap.from_struct_field(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.FIELD_DECL]

    @staticmethod
    def get_struct_methods(cursor: cindex.Cursor, *, excludes=()):
        def method_filter(method: cindex.Cursor) -> bool:
            if method.spelling == 'GetStateStorage':
                pass
            if method.kind != cindex.CursorKind.CXX_METHOD:
                return False
            for param in method.get_children():
                if param.kind == cindex.CursorKind.PARM_DECL and param.type.spelling in excludes:
                    return False
            if method.result_type.spelling in excludes:
                return False
            return True
        return [child for child in cursor.get_children() if method_filter(child)]

    @property
    def is_void(self) -> bool:
        return self.type.kind == cindex.TypeKind.VOID

    @property
    def c_type(self) -> str:
        return utils.template_filter(
            self.type.spelling).replace('[]', '*')

    @property
    def c_type_with_name(self) -> str:
        param_type = self.c_type
        param_name = utils.symbol_filter(self.cursor.spelling)
        splitted = param_type.split('(*)', maxsplit=1)
        if len(splitted) == 2:
            return f"{splitted[0]}(*{param_name}){splitted[1]}"
        else:
            return f"{param_type} {param_name}"
