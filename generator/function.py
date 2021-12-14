from typing import Iterable, List
import io
from clang import cindex
from .typewrap import TypeWrap
from . import wrap_flags


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
        pyx.write(
            f'{indent}cdef {param.pyx_cimport_type} p{i} = {wrap_flags.to_c(param.underlying_spelling, param.name)}\n')
        param_names.append(f'p{i}')
    return param_names


def write_pyx_function(pyx: io.IOBase, function: cindex.Cursor):
    result = TypeWrap.from_function_result(function)
    params = TypeWrap.get_function_params(function)

    # signature
    pyx.write(
        f"def {function.spelling}{cj(param.name_in_type_default_value for param in params)}")
    # return type
    if result.is_void:
        pyx.write(':\n')
    else:
        pyx.write(f'->{result.get_ctypes_type(user_type_pointer=True)}:\n')

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
            f'{indent}cdef {result.pyx_cimport_type} value = {ref}cpp_imgui.{function.spelling}{cj(param_names)}\n')
        pyx.write(f"{indent}return {result.pointer_to_ctypes('value')}\n\n")


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)

    # signature
    pyx.write(
        f'    def {method.spelling}{self_cj(param.name_in_type_default_value for param in params)}')
    if result.is_void:
        pyx.write(':\n')
    else:
        pyx.write(f'->{result.get_ctypes_type(user_type_pointer=True)}:\n')

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
            f'{indent}cdef {result.pyx_cimport_type} value = {ref}ptr.{method.spelling}{cj(param_names)}\n\n')
        pyx.write(f"{indent}return {result.pointer_to_ctypes('value')}\n\n")
