from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils


class ResultType(NamedTuple):
    cursor: cindex.Cursor

    @property
    def c_type(self) -> str:
        result_type = self.cursor.result_type
        return result_type.spelling

    @property
    def py_type(self) -> str:
        result_type = self.cursor.result_type
        return utils.def_pointer_filter(result_type.spelling)


class FunctionDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor)
        params = [utils.get_type(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]
        pxd.write(
            f'    {result_type.c_type} {cursor.spelling}({", ".join(f"{param_type} {param_name}" for param_name, param_type in params)})\n')

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result_type = ResultType(cursor)
        params = [utils.get_type(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        pyx.write(f'''def {cursor.spelling}({", ".join(f"{utils.def_pointer_filter(param_type)} {utils.symbol_filter(param_name)}" for param_name, param_type in params)})->{result_type.py_type}:
    value = cpp_imgui.{cursor.spelling}({", ".join(utils.symbol_filter(param_name, get_ptr=True) for param_name, param_type in params)})
    return {result_type.py_type}.from_ptr(value)

''')
