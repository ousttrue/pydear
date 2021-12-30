from typing import List, Tuple
import logging
import io
import pathlib
#
from clang import cindex
from .parser import Parser
from .declarations import function
from .interpreted_types import wrap_types

logger = logging.getLogger(__name__)


def get_namespace(cursors: Tuple[cindex.Cursor, ...]) -> str:
    namespaces = [cursor for cursor in cursors if cursor.kind ==
                  cindex.CursorKind.NAMESPACE]
    if not namespaces:
        return ''
    return '.'.join(namespace.spelling for namespace in namespaces)


class Header:
    def __init__(self, dir: pathlib.Path, file: str, namespace: str, *, prefix: str = '', include_dirs: List[pathlib.Path] = None) -> None:
        self.header = dir / file
        self.prefix = prefix
        self.include_dirs = include_dirs or ()
        self.current_nemespace = None

    def enter_namespace(self, pxd: io.IOBase, cursors: Tuple[cindex.Cursor, ...]):
        namespace = get_namespace(cursors)
        if namespace == self.current_nemespace:
            return

        if namespace:
            pxd.write(
                f'cdef extern from "{self.header.name}" namespace "{namespace}":\n')
        else:
            pxd.write(
                f'cdef extern from "{self.header.name}":\n')
        self.current_nemespace = namespace

    def write_pxd(self, pxd: io.IOBase, parser: Parser):
        self.current_nemespace = None

        # enum
        for enum in parser.enums:
            if pathlib.Path(enum.cursor.location.file.name) != self.header:
                continue
            self.enter_namespace(pxd, enum.cursors)
            pxd.write(f'    ctypedef enum {enum.cursor.spelling}:\n')
            pxd.write(f'        pass\n')

        # typedef & struct
        for t in parser.typedef_struct_list:
            if pathlib.Path(t.cursor.location.file.name) != self.header:
                continue
            if t.cursor.spelling in function.EXCLUDE_TYPES:
                # TODO: nested type
                continue

            self.enter_namespace(pxd, t.cursors)
            t.write_pxd(pxd, excludes=function.EXCLUDE_TYPES)

        # funcs
        for func in parser.functions:
            if pathlib.Path(func.cursor.location.file.name) != self.header:
                continue
            self.enter_namespace(pxd, func.cursors)
            if func.is_exclude_function():
                continue
            function.write_pxd_function(pxd, func.cursor)

    def write_pyx(self, pyx: io.IOBase, parser: Parser):
        types = [x for x in parser.typedef_struct_list if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if types:
            for v in wrap_types.WRAP_TYPES:
                for func in types:
                    if func.cursor.spelling == v.name:
                        func.write_pyx_ctypes(pyx, flags=v)

        funcs = [x for x in parser.functions if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if funcs:
            overload = {}
            for func in funcs:
                if func.is_exclude_function():
                    continue

                name = func.spelling
                count = overload.get(name, 0) + 1
                function.write_pyx_function(
                    pyx, func.cursor, overload=count, prefix=self.prefix)
                overload[name] = count

    def write_pyi(self, pyi: io.IOBase, parser: Parser):
        types = [x for x in parser.typedef_struct_list if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if types:
            for v in wrap_types.WRAP_TYPES:
                for func in types:
                    if func.cursor.spelling == v.name:
                        func.write_pyi(pyi, flags=v)

        funcs = [x for x in parser.functions if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if funcs:
            overload = {}
            for func in funcs:
                if func.is_exclude_function():
                    continue

                name = func.spelling
                count = overload.get(name, 0) + 1
                function.write_pyx_function(
                    pyi, func.cursor, pyi=True, overload=count, prefix=self.prefix)
                overload[name] = count
