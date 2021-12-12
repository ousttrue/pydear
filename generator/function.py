from typing import NamedTuple, Tuple
import io
from clang import cindex
from .param import Param, def_pointer_filter


class ResultType(NamedTuple):
    cursor: cindex.Cursor

    @property
    def c_type(self) -> str:
        result_type = self.cursor.result_type
        return result_type.spelling

    @property
    def py_type(self) -> str:
        result_type = self.cursor.result_type
        result_spelling = result_type.spelling
        match result_spelling:
            case 'const char *':
                return 'str'
            case 'ImVec2':
                return 'Tuple[float, float]'
            case 'ImU32' | 'ImGuiID' | 'ImGuiMouseCursor':
                return 'int'
            case _:
                return def_pointer_filter(result_spelling)

    @property
    def c_to_py(self) -> str:
        result_type = self.cursor.result_type
        match result_type.kind:
            case cindex.TypeKind.BOOL | cindex.TypeKind.FLOAT | cindex.TypeKind.INT | cindex.TypeKind.DOUBLE:
                return 'value'
            case cindex.TypeKind.POINTER:
                return f'{self.py_type}.from_ptr(value)'
            case cindex.TypeKind.LVALUEREFERENCE:
                return f'{self.py_type}.from_ptr(&value)'
            case _:
                match result_type.spelling:
                    case 'ImVec2':
                        # copy by value
                        return '(value.x, value.y)'
                    case 'ImVec4':
                        # copy by value
                        return '(value.x, value.y, value.z, value.w)'
                    case 'ImU32' | 'ImGuiID' | 'ImGuiMouseCursor':
                        return 'value'
                    case _:
                        raise NotImplementedError(f'result_type.kind')

    @property
    def is_void(self) -> bool:
        is_void = self.cursor.result_type.kind == cindex.TypeKind.VOID
        return is_void


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
