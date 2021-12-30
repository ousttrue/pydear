from typing import Iterable, List, Tuple, NamedTuple
import logging
import io
from clang import cindex
from .typewrap import TypeWrap
from .. import interpreted_types

logger = logging.getLogger(__name__)


EXCLUDE_TYPES = (
    'va_list',
    'ImGuiTextFilter',
    'ImGuiStorage',
    'ImGuiStorage *',
)

EXCLUDE_FUNCS = (
    'CheckboxFlags',
    'Combo',
    'ListBox',
    'PlotLines',
)


def cj(src: Iterable[str]) -> str:
    '''
    comma join
    '''
    return '(' + ', '.join(src) + ')'


def self_cj(src: Iterable[str]) -> str:
    '''
    comma join
    '''
    sio = io.StringIO()
    sio.write('(self')
    for x in src:
        sio.write(', ')
        sio.write(x)
    sio.write(')')
    return sio.getvalue()


'''
PXD
'''


def write_pxd_function(pxd: io.IOBase, function: cindex.Cursor):
    params = [param.c_type_with_name for param in TypeWrap.get_function_params(
        function)]
    result = TypeWrap.from_function_result(function)
    pxd.write(
        f'    {result.c_type} {function.spelling}{cj(params)}\n')


def write_pxd_constructor(pxd: io.IOBase, klass: cindex.Cursor, constructor: cindex.Cursor):
    params = TypeWrap.get_function_params(constructor)
    pxd.write(
        f'        {klass.spelling}{cj(param.c_type_with_name for param in params)}\n')


def write_pxd_method(pxd: io.IOBase, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)
    pxd.write(
        f'        {result.c_type} {method.spelling}{cj(param.c_type_with_name for param in params)}\n')


'''
PYX
'''


def extract_parameters(pyx: io.IOBase, params: List[TypeWrap], indent: str) -> List[str]:
    param_names = []
    for i, param in enumerate(params):
        t = interpreted_types.from_cursor(param.cursor.type, param.cursor)
        pyx.write(f'{t.cdef_param(indent, i, param.name)}')
        param_names.append(t.call_param(i))
    return param_names


def write_pyx_function(pyx: io.IOBase, function: cindex.Cursor, *, pyi=False, overload=1, prefix=''):
    result = TypeWrap.from_function_result(function)
    result_t = interpreted_types.from_cursor(result.type, result.cursor)
    params = TypeWrap.get_function_params(function)

    overload = '' if overload == 1 else f'_{overload}'

    # signature
    pyx.write(
        f"def {prefix}{function.spelling}{overload}{cj(interpreted_types.from_cursor(param.type, param.cursor).param(param.name, param.default_value, pyi=pyi) for param in params)}")
    # return type
    pyx.write(f'->{result_t.result_typing(pyi=pyi)}:')

    if pyi:
        pyx.write(' ...\n')
        return

    pyx.write('\n')

    indent = '    '

    # cdef parameters
    param_names = extract_parameters(pyx, params, indent)

    # body
    call = f'impl.{function.spelling}{cj(param_names)}'
    if result.is_void:
        pyx.write(f'{indent}{call}\n')
    else:
        pyx.write(result_t.cdef_result(indent, call))
    pyx.write('\n')


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor, *, pyi=False):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)
    result_t = interpreted_types.from_cursor(result.type, result.cursor)

    # signature
    pyx.write(
        f'    def {method.spelling}{self_cj(interpreted_types.from_cursor(param.cursor.type, param.cursor).param(param.name, param.default_value, pyi=pyi) for param in params)}')
    pyx.write(f'->{result_t.result_typing(pyi=pyi)}:')

    if pyi:
        pyx.write(' ...\n')
        return

    pyx.write('\n')

    indent = '        '

    # self to ptr
    pyx.write(
        f'{indent}cdef impl.{cursor.spelling} *ptr = <impl.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)\n')

    # cdef parameters
    param_names = extract_parameters(pyx, params, indent)

    # body
    call = f'ptr.{method.spelling}{cj(param_names)}'
    if result.is_void:
        pyx.write(f'{indent}{call}\n')
    else:
        pyx.write(result_t.cdef_result(indent, call))
    pyx.write('\n')


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    @property
    def cursor(self) -> cindex.Cursor:
        return self.cursors[-1]

    @property
    def spelling(self) -> str:
        return self.cursor.spelling

    def is_exclude_function(self) -> bool:
        cursor = self.cursor
        if cursor.spelling in EXCLUDE_FUNCS:
            return True
        if cursor.spelling.startswith('operator'):
            logger.debug(f'exclude; {cursor.spelling}')
            return True
        if cursor.result_type.spelling in EXCLUDE_TYPES:
            return True
        for child in cursor.get_children():
            if child.kind == cindex.CursorKind.PARM_DECL:
                if child.type.spelling in EXCLUDE_TYPES:
                    return True
                if 'callback' in child.spelling:
                    # function pointer
                    return True
                if 'func' in child.spelling:
                    # function pointer
                    return True
                if '(*)' in child.type.spelling:
                    # function pointer
                    return True
        return False