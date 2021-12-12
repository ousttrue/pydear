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

    @property
    def c_to_py(self) -> str:
        return f'{self.py_type}.from_ptr(value)'

    @property
    def is_void(self) -> bool:
        return self.cursor.result_type == cindex.TypeKind.VOID


class Param(NamedTuple):
    cursor: cindex.Cursor

    @property
    def c_type_name(self) -> str:
        param_name, param_type = utils.get_type(self.cursor)
        return f"{param_type} {param_name}"

    @property
    def py_type_name(self) -> str:
        param_name, param_type = utils.get_type(self.cursor)
        return f"{utils.def_pointer_filter(param_type)} {utils.symbol_filter(param_name)}"

    @property
    def py_to_c(self) -> str:
        param_name, param_type = utils.get_type(self.cursor)
        return utils.symbol_filter(param_name, get_ptr=True)


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
            raise NotImplementedError()
        else:
            pyx.write(f'''def {cursor.spelling}({", ".join(param.py_type_name for param in params)})->{result_type.py_type}:
        value = cpp_imgui.{cursor.spelling}({", ".join(param.py_to_c for param in params)})
        return {result_type.c_to_py}
''')
