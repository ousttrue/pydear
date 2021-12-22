from typing import NamedTuple, Tuple, List, Union
import io
import pathlib
import logging
from clang import cindex
from . typedef import TypedefDecl
from . struct import StructDecl
from .enum import EnumDecl
logger = logging.getLogger(__name__)


class Parser:
    def __init__(self, dir: pathlib.Path, headers: List[str]) -> None:
        sio = io.StringIO()
        for header in headers:
            sio.write(f'#include "{header}"\n')
        import pycindex
        self.entrypoint = dir / headers[0]
        unsaved = pycindex.Unsaved('tmp.h', sio.getvalue())
        self.tu = pycindex.get_tu(
            'tmp.h', includes=[str(dir)], unsaved=[unsaved])
        self.functions: List[Tuple[cindex.Cursor, ...]] = []
        self.enums: List[EnumDecl] = []
        self.typedef_struct_list: List[Union[TypedefDecl, StructDecl]] = []

    def callback(self, *cursor_path: cindex.Cursor) -> bool:
        cursor = cursor_path[-1]
        location: cindex.SourceLocation = cursor.location
        if not location:
            return False
        if not location.file:
            return False

        if self.entrypoint == pathlib.Path(location.file.name):
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
                        self.functions.append(cursor_path)
                case cindex.CursorKind.ENUM_DECL:
                    self.enums.append(EnumDecl(cursor_path))
                case cindex.CursorKind.TYPEDEF_DECL:
                    self.typedef_struct_list.append(TypedefDecl(cursor_path))
                case cindex.CursorKind.STRUCT_DECL:
                    self.typedef_struct_list.append(StructDecl(cursor_path))
                case cindex.CursorKind.CLASS_TEMPLATE:
                    self.typedef_struct_list.append(StructDecl(cursor_path))
                case _:
                    logger.debug(cursor.kind)
        else:
            pass

        return False

    def traverse(self):
        import pycindex
        pycindex.traverse(self.tu, self.callback)
