from typing import NamedTuple, Optional
import logging
import re
from clang import cindex
from . import utils

logger = logging.getLogger(__name__)

TEMPLATE_PATTERN = re.compile(r'<[^>]+>')


def template_filter(src: str) -> str:
    '''
    replace Some<T> to Some[T]
    '''
    def rep_typearg(m):
        ret = f'[{m.group(0)[1:-1]}]'
        return ret
    dst = TEMPLATE_PATTERN.sub(rep_typearg, src)

    return dst


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
    def get_struct_methods(cursor: cindex.Cursor, *, excludes=(), includes=False):
        def method_filter(method: cindex.Cursor) -> bool:
            if method.spelling == 'GetStateStorage':
                pass
            if method.kind != cindex.CursorKind.CXX_METHOD:
                return False
            for param in method.get_children():
                if param.kind == cindex.CursorKind.PARM_DECL and param.type.spelling in excludes:
                    return False
            match includes:
                case True:
                    # return True
                    pass
                case False:
                    return False
                case (*methods,):
                    if method.spelling not in methods:
                        return False
                    else:
                        pass
            if method.result_type.spelling in excludes:
                return False
            return True
        return [child for child in cursor.get_children() if method_filter(child)]

    @property
    def name(self) -> str:
        return utils.symbol_filter(self.cursor.spelling)

    @property
    def is_void(self) -> bool:
        return self.type.kind == cindex.TypeKind.VOID

    @property
    def c_type(self) -> str:
        '''
        pxd
        '''
        return template_filter(self.type.spelling).replace('[]', '*')

    @property
    def c_type_with_name(self) -> str:
        '''
        pxd
        '''
        c_type = self.c_type
        name = self.name
        splitted = c_type.split('(*)', maxsplit=1)
        if len(splitted) == 2:
            return f"{splitted[0]}(*{name}){splitted[1]}"
        else:
            return f"{c_type} {name}"

    @property
    def _typedef_underlying_type(self) -> Optional['TypeWrap']:
        match self.type.kind:
            case cindex.TypeKind.TYPEDEF:
                ref: cindex.Cursor = next(iter(
                    c for c in self.cursor.get_children() if c.kind == cindex.CursorKind.TYPE_REF))
                return TypeWrap(ref.referenced.underlying_typedef_type, ref.referenced)

            case _:
                return None

    @property
    def underlying_spelling(self) -> str:
        base = self._typedef_underlying_type
        if base:
            return base.type.spelling
        return self.type.spelling

    @property
    def default_value(self) -> str:
        tokens = []
        for child in self.cursor.get_children():
            # logger.debug(child.spelling)
            match child.kind:
                case cindex.CursorKind.UNEXPOSED_EXPR | cindex.CursorKind.INTEGER_LITERAL | cindex.CursorKind.FLOATING_LITERAL | cindex.CursorKind.UNARY_OPERATOR:
                    tokens = [
                        token.spelling for token in self.cursor.get_tokens()]
                    if '=' not in tokens:
                        tokens = []
                case cindex.CursorKind.TYPE_REF:
                    pass
                case _:
                    logger.debug(f'{self.cursor.spelling}: {child.kind}')

        if not tokens:
            return ''

        equal = tokens.index('=')
        value = ' '.join(tokens[equal+1:])
        if value == 'NULL':
            value = 'None'
        elif value.startswith('"'):
            value = 'b' + value
        value = re.sub(r'([0-9\.])f', r'\1', value)
        return '= ' + value
