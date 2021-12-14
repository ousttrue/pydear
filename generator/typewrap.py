from typing import NamedTuple, Type, Tuple, Optional, List
import logging
import io
import re
import ctypes
from clang import cindex
from . import utils
from . import wrap_flags

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


class PyxType(NamedTuple):
    spelling: str
    cpp_imgui: bool = False
    is_reference: bool = False
    is_const: bool = False

    @property
    def cdef(self) -> str:
        spelling = wrap_flags.prepare(self.spelling)
        sio = io.StringIO()
        sio.write('cdef ')
        if self.is_const:
            sio.write('const ')
        if self.cpp_imgui:
            sio.write('cpp_imgui.')
        sio.write(spelling.replace('const ', ''))
        if self.is_reference:
            sio.write(' *')
        return sio.getvalue()


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
    def _is_user_type_pointer(self) -> bool:
        '''
        is type pointer to ImXXX struct
        '''
        match self.type.kind:
            case cindex.TypeKind.POINTER | cindex.TypeKind.LVALUEREFERENCE:
                pointee = self.type.get_pointee()
                match pointee.kind:
                    case cindex.TypeKind.RECORD:
                        return True

        return False

    def get_ctypes_type(self, *, user_type_pointer=False) -> str:

        if '(*)' in self.type.spelling:
            # function pointer
            return 'ctypes.c_void_p'

        if self.type.spelling.startswith('ImVector<'):
            return 'ImVector'

        if user_type_pointer and self._is_user_type_pointer:
            return self.type.get_pointee().spelling

        match self.type.kind:
            case cindex.TypeKind.POINTER | cindex.TypeKind.LVALUEREFERENCE:
                return 'ctypes.c_void_p'
            case cindex.TypeKind.BOOL:
                return 'ctypes.c_bool'
            case cindex.TypeKind.INT:
                return 'ctypes.c_int32'
            case cindex.TypeKind.USHORT:
                return 'ctypes.c_uint16'
            case cindex.TypeKind.UINT:
                return 'ctypes.c_uint32'
            case cindex.TypeKind.FLOAT:
                return 'ctypes.c_float'
            case cindex.TypeKind.DOUBLE:
                return 'ctypes.c_double'
            case cindex.TypeKind.TYPEDEF:
                base = self._typedef_underlying_type
                if not base:
                    raise RuntimeError()
                return base.get_ctypes_type()
            case cindex.TypeKind.CONSTANTARRAY:
                base = TypeWrap(
                    self.type.get_array_element_type(), self.cursor)
                return f'{base.get_ctypes_type()} * {self.type.get_array_size()}'
            case cindex.TypeKind.RECORD:
                return self.type.spelling
            case _:
                raise NotImplementedError()

    @property
    def pyx_cimport_type(self) -> PyxType:
        '''
        cdef
        '''
        is_const = self.type.is_const_qualified()
        match self.type.kind:
            case cindex.TypeKind.POINTER | cindex.TypeKind.LVALUEREFERENCE:
                is_const = is_const or self.type.get_pointee().is_const_qualified()
        if self._is_user_type_pointer:
            pointee = self.type.get_pointee()
            if self.type.kind == cindex.TypeKind.LVALUEREFERENCE:
                # reference to pointer
                return PyxType(pointee.spelling, cpp_imgui=True, is_reference=True, is_const=is_const)
            else:
                return PyxType(self.c_type, cpp_imgui=True, is_const=is_const)
        if self.type.spelling.startswith("Im"):
            return PyxType(self.c_type, cpp_imgui=True, is_const=is_const)
        return PyxType(self.c_type, is_const=is_const)

    def pointer_to_ctypes(self, name: str) -> str:
        if self._is_user_type_pointer:
            return f'ctypes.cast(ctypes.c_void_p(<long long>{name}), ctypes.POINTER({self.get_ctypes_type(user_type_pointer=True)}))[0]'
        return name

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
    def name_in_type_default_value(self) -> str:
        tokens = []
        for child in self.cursor.get_children():
            # logger.debug(child.spelling)
            match child.kind:
                case cindex.CursorKind.UNEXPOSED_EXPR | cindex.CursorKind.INTEGER_LITERAL | cindex.CursorKind.FLOATING_LITERAL | cindex.CursorKind.UNARY_OPERATOR:
                    # default_value = get_default_value(child)
                    # break
                    tokens = [
                        token.spelling for token in self.cursor.get_tokens()]
                    if '=' not in tokens:
                        tokens = []
                case _:
                    logger.debug(f'{self.cursor.spelling}: {child.kind}')

        if tokens:
            # location: cindex.SourceLocation = default_value.location
            # logger.debug(f'{location.file}:{location.line}')
            equal = tokens.index('=')
            value = ' '.join(tokens[equal+1:])
            if value == 'NULL':
                value = 'None'
            elif value.startswith('"'):
                value = 'b' + value
            elif value.endswith('f'):
                value = value[:-1]
            return self.name + ': ' + wrap_flags.in_type(self.underlying_spelling) + '= ' + value
        else:
            return self.name + ': ' + wrap_flags.in_type(self.underlying_spelling)


def get_default_value(cursor: cindex.Cursor) -> cindex.Cursor:
    for child in cursor.get_children():
        if child.kind == cindex.CursorKind.INTEGER_LITERAL:
            return child
        else:
            raise NotImplementedError()

    raise NotImplementedError()
