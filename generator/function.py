import io
from clang import cindex
from .typewrap import TypeWrap
from . import utils


def write_pxd(pxd: io.IOBase, cursor: cindex.Cursor, *, excludes=()):
    if cursor.result_type.spelling in excludes:
        return
    params = [param.c_type_with_name for param in TypeWrap.get_function_params(
        cursor, excludes=excludes)]
    result = TypeWrap.from_function_result(cursor)
    pxd.write(
        f'    {result.c_type} {cursor.spelling}({utils.comma_join(params)})\n')


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
