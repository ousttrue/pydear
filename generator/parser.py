from typing import NamedTuple, Tuple, List, Union
import pathlib
import io
import logging
from clang import cindex
from . function import Function
from . typedef import Typedef
from . struct import Struct
logger = logging.getLogger(__name__)


class Enum(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]


class Parser:
    def __init__(self, entrypoint: pathlib.Path) -> None:
        import pycindex
        self.entrypoint = str(entrypoint)
        self.tu = pycindex.get_tu(self.entrypoint)
        self.functions: List[Function] = []
        self.enums: List[Enum] = []
        self.typedef_struct_list: List[Union[Typedef, Struct]] = []

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
                ):
                    pass
                case cindex.CursorKind.FUNCTION_DECL:
                    if(cursor.spelling.startswith('operator ')):
                        pass
                    else:
                        self.functions.append(Function(cursor_path))
                case cindex.CursorKind.ENUM_DECL:
                    self.enums.append(Enum(cursor_path))
                case cindex.CursorKind.TYPEDEF_DECL:
                    self.typedef_struct_list.append(Typedef(cursor_path))
                case cindex.CursorKind.STRUCT_DECL:
                    self.typedef_struct_list.append(Struct(cursor_path))
                case cindex.CursorKind.CLASS_TEMPLATE:
                    self.typedef_struct_list.append(Struct(cursor_path))
                case _:
                    logger.debug(cursor.kind)
        else:
            pass

        return False

    def traverse(self):
        import pycindex
        pycindex.traverse(self.tu, self.callback)
