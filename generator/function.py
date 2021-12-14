from typing import Iterable
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
    return '(self, ' + ', '.join(src) + ')'


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


def write_pyx_function(pyx: io.IOBase, function: cindex.Cursor):
    if function.spelling == 'Begin':
        pass

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

    # cdef parameters
    def add_module(src: str) -> str:
        if src.startswith("Im"):
            return f'cpp_imgui.{src}'
        return src
    for i, param in enumerate(params):
        pyx.write(
            f'    cdef {add_module(param.underlying_spelling)} p{i} = {wrap_flags.to_c(param.underlying_spelling, param.name)}\n')

    # body
    if result.is_void:
        pyx.write(
            f'    cpp_imgui.{function.spelling}{cj(f"p{i}" for i, param in enumerate(params))}\n\n')
    else:
        ref = ''
        if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
            # reference to pointer
            ref = '&'

        pyx.write(
            f'    cdef {result.pyx_cimport_type} value = {ref}cpp_imgui.{function.spelling}{cj(f"p{i}" for i, param in enumerate(params))}\n')
        pyx.write(f"    return {result.pointer_to_ctypes('value')}\n\n")


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)

    if result.is_void:
        pyx.write(f'''    def {method.spelling}{self_cj(param.name_in_type_default_value for param in params)}:
        cdef cpp_imgui.{cursor.spelling} *ptr = <cpp_imgui.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)
        ptr.{method.spelling}{cj(param.ctypes_to_pointer(param.name) for param in params)}

''')
