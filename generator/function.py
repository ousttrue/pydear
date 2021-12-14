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


def _call_assign(cursor: cindex.Cursor, name: str, result, params):
    if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
        # reference to pointer
        return f'cdef {result.pyx_cimport_type} {name} = &cpp_imgui.{cursor.spelling}{cj(param.ctypes_to_pointer(param.name) for param in params)}'
    else:
        return f'cdef {result.pyx_cimport_type} {name} = cpp_imgui.{cursor.spelling}{cj(param.ctypes_to_pointer(param.name) for param in params)}'




def write_pyx_function(pyx: io.IOBase, function: cindex.Cursor):
    result = TypeWrap.from_function_result(function)
    params = TypeWrap.get_function_params(function)

    if result.is_void:
        # TODO: default param
        pyx.write(f'''def {function.spelling}{cj(param.name + ': ' + wrap_flags.in_type(param.type.spelling) for param in params)}:
    cpp_imgui.{function.spelling}{cj(wrap_flags.to_pointer(param.c_type, param.name) for param in params)}

''')
    else:
        pyx.write(f'''def {function.spelling}{cj(param.name_with_ctypes_type for param in params)}->{result.get_ctypes_type(user_type_pointer=True)}:
    {_call_assign(function, 'value', result, params)}
    return {result.pointer_to_ctypes('value')}

''')


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)

    if result.is_void:
        pyx.write(f'''    def {method.spelling}{self_cj(param.name_with_ctypes_type for param in params)}:
        cdef cpp_imgui.{cursor.spelling} *ptr = <cpp_imgui.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)
        ptr.{method.spelling}{cj(param.ctypes_to_pointer(param.name) for param in params)}

''')
