from typing import NamedTuple, Tuple
import io
from clang import cindex
from .typewrap import TypeWrap
from . import utils


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase, *, excludes=()):
        cursor = self.cursors[-1]
        if cursor.result_type.spelling in excludes:
            return
        params = [param.c_type_with_name for param in TypeWrap.get_function_params(
            cursor, excludes=excludes)]
        result = TypeWrap.from_function_result(cursor)
        pxd.write(
            f'    {result.c_type} {cursor.spelling}({utils.comma_join(params)})\n')

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result = TypeWrap.from_function_result(cursor)
        params = TypeWrap.get_function_params(cursor)

        if result.is_void:
            pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.py_type_with_name for param in params)}):
        cpp_imgui.{cursor.spelling}({utils.comma_join(param.py_to_c for param in params)})

''')
        else:
            pyx.write(f'''def {cursor.spelling}({utils.comma_join(param.py_type_with_name for param in params)})->{result.py_type}:
        cdef {result.pyx_type} value = cpp_imgui.{cursor.spelling}({utils.comma_join(param.py_to_c for param in params)})
        return {result.c_to_py('value')}

''')

    def write_pyi(self, pyi: io.IOBase):
        cursor = self.cursors[-1]
        result_type = TypeWrap.from_function_result(cursor)
        params = [Param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        if result_type.is_void:
            pyi.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)}):
        cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})

''')
        else:
            pyi.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)})->{result_type.py_type}:
        value = cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})
        return {result_type.c_to_py('value')}

''')
