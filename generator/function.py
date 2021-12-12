from typing import NamedTuple, Tuple
import io
from clang import cindex
from .param import Param
from .result import ResultType


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor)
        params = [Param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]
        pxd.write(
            f'    {result_type.c_type} {cursor.spelling}({", ".join(param.c_type_name for param in params)})\n')

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor)
        params = [Param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        if result_type.is_void:
            pyx.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)}):
        cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})

''')
        else:
            pyx.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)})->{result_type.py_type}:
        value = cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})
        return {result_type.c_to_py}

''')

    def write_pyi(self, pyi: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor)
        params = [Param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        if result_type.is_void:
            pyi.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)}):
        cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})

''')
        else:
            pyi.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)})->{result_type.py_type}:
        value = cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})
        return {result_type.c_to_py}

''')
