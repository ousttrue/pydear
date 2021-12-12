from typing import NamedTuple
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
        result_spelling = result_type.spelling
        match result_spelling:
            case 'const char *':
                return 'str'
            case 'ImVec2':
                return 'Tuple[float, float]'
            case 'ImVec4':
                return 'Tuple[float, float, float, float]'
            case 'ImU32' | 'ImGuiID' | 'ImGuiMouseCursor':
                return 'int'
            case _:
                return utils.def_pointer_filter(result_spelling)

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
