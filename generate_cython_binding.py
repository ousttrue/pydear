import pathlib
import io
import logging
from clang import cindex
logger = logging.getLogger(__name__)


def get_type(cursor: cindex.Cursor):
    name = cursor.spelling
    return (name, cursor.type.spelling)


class Parser:
    def __init__(self, entrypoint: pathlib.Path) -> None:
        import pycindex
        self.entrypoint = str(entrypoint)
        self.tu = pycindex.get_tu(self.entrypoint)
        self.functions = []
        self.enums = []
        self.typedef_struct_list = []

    def callback(self, *cursor_path: cindex.Cursor) -> bool:
        cursor = cursor_path[-1]
        location: cindex.SourceLocation = cursor.location
        if not location:
            return False
        if not location.file:
            return False

        if location.file.name == self.entrypoint:
            match cursor.kind:
                case cindex.CursorKind.NAMESPACE:
                    # enter namespace
                    # logger.info(f'namespace: {cursor.spelling}')
                    return True
                case (
                    cindex.CursorKind.MACRO_DEFINITION
                    | cindex.CursorKind.MACRO_INSTANTIATION
                    | cindex.CursorKind.INCLUSION_DIRECTIVE
                    | cindex.CursorKind.FUNCTION_TEMPLATE
                    | cindex.CursorKind.CLASS_TEMPLATE
                ):
                    pass
                case cindex.CursorKind.FUNCTION_DECL:
                    if(cursor.spelling.startswith('operator ')):
                        pass
                    else:
                        self.functions.append(cursor_path)
                case cindex.CursorKind.ENUM_DECL:
                    self.enums.append(cursor_path)
                case cindex.CursorKind.TYPEDEF_DECL | cindex.CursorKind.STRUCT_DECL:
                    self.typedef_struct_list.append(cursor_path)
                case _:
                    logger.debug(cursor.kind)
        else:
            pass

        return False

    def traverse(self):
        import pycindex
        pycindex.traverse(self.tu, self.callback)

    def _generate_function(self, pyd: io.IOBase, pyx: io.IOBase, cursor: cindex.Cursor):
        result_type = cursor.result_type
        params = [get_type(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        #
        # pyd
        #
        pyd.write('''cdef extern from "imgui.h":

''')

        pyd.write(
            f'{result_type.spelling} {cursor.spelling}({", ".join(f"{param_type} {param_name}" for param_name, param_type in params)})\n')

        #
        # pyx
        #
        pyx.write('''cimport imgui

''')
        pyx.write(
            f'{result_type.spelling} {cursor.spelling}({", ".join(f"{param_type} {param_name}" for param_name, param_type in params)})\n')

        #
        # pyi
        #

    def generate(self, ext_dir: pathlib.Path):
        ext_dir.mkdir(parents=True, exist_ok=True)
        with (ext_dir / 'imgui.pyd').open('w') as pyd:
            with (ext_dir / 'imgui.pyx').open('w') as pyx:
                self._generate_function(pyd, pyx, self.functions[0][-1])


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path):
    parser = Parser(imgui_dir / 'imgui.h')
    parser.traverse()
    parser.generate(ext_dir)
