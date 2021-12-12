from typing import NamedTuple, Tuple
import io
import re
from clang import cindex


def symbol_filter(src: str) -> str:
    '''
    fix python reserved word
    '''
    match src:
        case 'in':
            return '_' + src
        case _:
            return src


def get_type(cursor: cindex.Cursor):
    name = cursor.spelling
    return (name, cursor.type.spelling)


IMPOINTER_PATTERN = re.compile(r'(Im\w+)(\s*[\*&])(.*)')
CONST_IMPOINTER_PATTERN = re.compile(r'const (Im\w+)(\s*[\*&])(.*)')


def is_pointer(src: str) -> bool:
    if re.search(r'\s*\*', src):
        return True
    else:
        return False


def is_reference(src: str) -> bool:
    if re.search(r'\s*&', src):
        return True
    else:
        return False


def def_pointer_filter(src: str) -> str:
    #  src.replace('[]', '*')
    m = IMPOINTER_PATTERN.match(src)
    if not m:
        m = CONST_IMPOINTER_PATTERN.match(src)
    if m:
        return f'{m.group(1)}{m.group(3)}'
    else:
        return src


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
            case _:
                return def_pointer_filter(result_spelling)

    @property
    def c_to_py(self) -> str:
        result_type = self.cursor.result_type
        match result_type.kind:
            case cindex.TypeKind.BOOL:
                return 'value'
            case cindex.TypeKind.POINTER:
                return f'{self.py_type}.from_ptr(value)'
            case cindex.TypeKind.LVALUEREFERENCE:
                return f'{self.py_type}.from_ptr(&value)'
            case _:
                raise NotImplementedError(f'result_type.kind')

    @property
    def is_void(self) -> bool:
        is_void = self.cursor.result_type.kind == cindex.TypeKind.VOID
        return is_void


def is_wrap(type):
    m = IMPOINTER_PATTERN.search(type.spelling)
    if m:
        # ImXXX
        return True
    else:
        return False


class Param(NamedTuple):
    cursor: cindex.Cursor

    @property
    def c_type_name(self) -> str:
        param_name, param_type = get_type(self.cursor)
        return f"{param_type} {param_name}"

    @property
    def py_type_name(self) -> str:
        param_name, param_type = get_type(self.cursor)
        if self.cursor.type.kind == cindex.TypeKind.POINTER:
            if is_wrap(self.cursor.type):
                return f"{def_pointer_filter(param_type)} {symbol_filter(param_name)}"
            else:
                if self.cursor.type.spelling == 'const char *':
                    return f"str {symbol_filter(param_name)}"
                else:
                    # TODO: null check
                    # TODO: default value
                    # bool *
                    return f"{self.cursor.type.get_pointee().spelling}[::1] {symbol_filter(param_name)}"
        else:
            return f"{param_type} {symbol_filter(param_name)}"

    @property
    def py_to_c(self) -> str:
        param_name, param_type = get_type(self.cursor)
        name = symbol_filter(param_name)
        if self.cursor.type.kind == cindex.TypeKind.POINTER:
            if is_wrap(self.cursor.type):
                return f'{name}._ptr'
            else:
                if self.cursor.type.spelling == 'const char *':
                    return name
                else:
                    # bool[::1]
                    return f'&{name}[0]'
        else:
            return name


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
