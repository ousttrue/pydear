from typing import NamedTuple, Tuple
import io
from clang import cindex
from .param import Param, is_wrap
from .result import ResultType
from generator import param


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase, *, excludes=()):
        cursor = self.cursors[-1]
        if cursor.result_type.spelling in excludes:
            return
        params = []
        for child in cursor.get_children():
            if child.kind == cindex.CursorKind.PARM_DECL:
                if child.type.spelling in excludes:
                    return
                params.append(Param(child))
        result = ResultType(cursor, cursor.result_type)
        pxd.write(
            f'    {result.type.spelling} {cursor.spelling}({", ".join(param.c_type_name for param in params)})\n')

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result = ResultType(cursor, cursor.result_type)
        params = [Param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        if result.is_void:
            pyx.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)}):
        cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})

''')
        else:
            prefix = ''
            if is_wrap(result.type):
                prefix = 'cpp_imgui.'
            pyx.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)})->{result.py_type}:
        cdef {prefix}{result.type.spelling.replace("const ", "")} value = cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})
        return {result.c_to_py('value')}

''')

    def write_pyi(self, pyi: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor, cursor.result_type)
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
