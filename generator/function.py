from typing import Iterable, List
import io
from clang import cindex
from .typewrap import TypeWrap
from . import typeconv


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


def write_pxd_function(pxd: io.IOBase, function: cindex.Cursor, *, excludes=()):
    if function.result_type.spelling in excludes:
        return
    params = [param.c_type_with_name for param in TypeWrap.get_function_params(
        function, excludes=excludes)]
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
        t = typeconv.get_type(param.underlying_spelling)
        pyx.write(f'{indent}{t.cdef} p{i} = {t.to_c(param.name)}\n')
        if param.type.kind == cindex.TypeKind.LVALUEREFERENCE:
            # deref
            param_names.append(f'p{i}[0]')
        else:
            param_names.append(f'p{i}')
    return param_names


def write_pyx_function(pyx: io.IOBase, function: cindex.Cursor, *, pyi=False, overload=1):
    result = TypeWrap.from_function_result(function)
    result_t = typeconv.get_type(result.underlying_spelling)
    params = TypeWrap.get_function_params(function)

    overload = '' if overload == 1 else f'_{overload}'

    # signature
    def name_type_default_value(param: TypeWrap) -> str:
        return f'{param.name}: {typeconv.get_type(param.underlying_spelling).py_type}{param.default_value}'
    pyx.write(
        f"def {function.spelling}{overload}{cj(name_type_default_value(param) for param in params)}")
    # return type
    if result.is_void:
        pyx.write(':')
    else:
        pyx.write(f'->{result_t.py_type}:')

    if pyi:
        pyx.write(' ...\n')
        return

    pyx.write('\n')

    indent = '    '

    # cdef parameters
    param_names = extract_parameters(pyx, params, indent)

    # body
    if result.is_void:
        pyx.write(
            f'{indent}cpp_imgui.{function.spelling}{cj(param_names)}\n\n')
    else:
        ref = ''
        if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
            # reference to pointer
            ref = '&'

        pyx.write(
            f'{indent}{result_t.cdef} value = {ref}cpp_imgui.{function.spelling}{cj(param_names)}\n')
        pyx.write(f"{indent}return {result_t.to_py('value')}\n\n")


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor, *, pyi=False):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)
    result_t = typeconv.get_type(result.underlying_spelling)

    # signature
    def name_type_default_value(param: TypeWrap) -> str:
        return f'{param.name}: {typeconv.get_type(param.underlying_spelling).py_type}{param.default_value}'
    pyx.write(
        f'    def {method.spelling}{self_cj(name_type_default_value(param) for param in params)}')
    if result.is_void:
        pyx.write(':')
    else:
        pyx.write(f'->{result_t.py_type}:')

    if pyi:
        pyx.write(' ...\n')
        return

    pyx.write('\n')

    indent = '        '

    # self to ptr
    pyx.write(f'{indent}cdef cpp_imgui.{cursor.spelling} *ptr = <cpp_imgui.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)\n')

    # cdef parameters
    param_names = extract_parameters(pyx, params, indent)

    # body
    if result.is_void:
        pyx.write(
            f'{indent}ptr.{method.spelling}{cj(param_names)}\n\n')
    else:
        ref = ''
        if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
            # reference to pointer
            ref = '&'

        pyx.write(
            f'{indent}{result_t.cdef} value = {ref}ptr.{method.spelling}{cj(param_names)}\n\n')
        pyx.write(f"{indent}return {result_t.to_py('value')}\n\n")
