from typing import NamedTuple, Tuple
import io
from clang import cindex
from .typewrap import TypeWrap
from . import utils


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    @property
    def cursor(self):
        return self.cursors[-1]

    def write_pxd(self, pxd: io.IOBase, *, excludes=()):
        cursor = self.cursors[-1]
        if cursor.result_type.spelling in excludes:
            return
        params = [param.c_type_with_name for param in TypeWrap.get_function_params(
            cursor, excludes=excludes)]
        result = TypeWrap.from_function_result(cursor)
        pxd.write(
            f'    {result.c_type} {cursor.spelling}({utils.comma_join(params)})\n')

    def call_assign(self, name: str, result, params):
        if result.type.kind == cindex.TypeKind.LVALUEREFERENCE:
            # reference to pointer
            return f'cdef {result.pyx_cimport_type} {name} = &cpp_imgui.{self.cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})'
        else:
            return f'cdef {result.pyx_cimport_type} {name} = cpp_imgui.{self.cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})'

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result = TypeWrap.from_function_result(cursor)
        params = TypeWrap.get_function_params(cursor)

        if result.is_void:
            pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.name_with_ctypes_type for param in params)}):
    cpp_imgui.{cursor.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})

''')
        else:
            pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.name_with_ctypes_type for param in params)})->{result.ctypes_type}:
    {self.call_assign('value', result, params)}
    return {result.pointer_to_ctypes('value')}

''')
