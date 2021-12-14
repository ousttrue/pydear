import io
from clang import cindex
from .typewrap import TypeWrap
from . import utils


def write_pxd_function(pxd: io.IOBase, function: cindex.Cursor, *, excludes=()):
    if function.result_type.spelling in excludes:
        return
    params = [param.c_type_with_name for param in TypeWrap.get_function_params(
        function, excludes=excludes)]
    result = TypeWrap.from_function_result(function)
    pxd.write(
        f'    {result.c_type} {function.spelling}({utils.comma_join(params)})\n')


def write_pxd_constructor(pxd: io.IOBase, klass: cindex.Cursor, constructor: cindex.Cursor):
    params = TypeWrap.get_function_params(constructor)
    pxd.write(
        f'        {klass.spelling}({utils.comma_join(param.c_type_with_name for param in params)})\n')


def write_pxd_method(pxd: io.IOBase, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)
    pxd.write(
        f'        {result.c_type} {method.spelling}({utils.comma_join(param.c_type_with_name for param in params)})\n')


def _call_assign(cursor: cindex.Cursor, name: str, result, params):
    if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
        # reference to pointer
        return f'cdef {result.pyx_cimport_type} {name} = &cpp_imgui.{cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})'
    else:
        return f'cdef {result.pyx_cimport_type} {name} = cpp_imgui.{cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})'


def write_pyx(pyx: io.IOBase, cursor: cindex.Cursor):
    result = TypeWrap.from_function_result(cursor)
    params = TypeWrap.get_function_params(cursor)

    if result.is_void:
        pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.name_with_ctypes_type for param in params)}):
    cpp_imgui.{cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})

''')
    else:
        pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.name_with_ctypes_type for param in params)})->{result.get_ctypes_type(user_type_pointer=True)}:
    {_call_assign(cursor, 'value', result, params)}
    return {result.pointer_to_ctypes('value')}

''')


def write_pyx_method(pyx: io.IOBase, cursor: cindex.Cursor, method: cindex.Cursor):
    params = TypeWrap.get_function_params(method)
    result = TypeWrap.from_function_result(method)

    if result.is_void:
        pyx.write(f'''    def {method.spelling}(self, {utils.comma_join(param.name_with_ctypes_type for param in params)}):
        cdef cpp_imgui.{cursor.spelling} *ptr = <cpp_imgui.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)
        ptr.{method.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})

''')
