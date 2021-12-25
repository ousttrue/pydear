from typing import List
import logging
import io
import pathlib
#
from clang import cindex
from .parser import Parser
from .import function
from .interpreted_types import wrap_types

logger = logging.getLogger(__name__)

EXCLUDE_TYPES = (
    'va_list',
    'ImGuiTextFilter',
    'ImGuiStorage',
    'ImGuiStorage *',
)

EXCLUDE_FUNCS = (
    'CheckboxFlags',
    'Combo',
    'ListBox',
    'PlotLines',
)


def is_exclude_function(cursors: tuple) -> bool:
    function: cindex.Cursor = cursors[-1]
    if function.spelling in EXCLUDE_FUNCS:
        return True
    if function.spelling.startswith('operator'):
        logger.debug(f'exclude; {function.spelling}')
        return True
    if function.result_type.spelling in EXCLUDE_TYPES:
        return True
    for child in function.get_children():
        if child.kind == cindex.CursorKind.PARM_DECL:
            if child.type.spelling in EXCLUDE_TYPES:
                return True
            if 'callback' in child.spelling:
                # function pointer
                return True
            if 'func' in child.spelling:
                # function pointer
                return True
            if '(*)' in child.type.spelling:
                # function pointer
                return True
    return False


class Header:
    def __init__(self, dir: pathlib.Path, file: str, namespace: str, *, prefix: str = '', include_dirs: List[pathlib.Path] = None) -> None:
        self.header = dir / file
        self.namespace = namespace
        self.prefix = prefix
        self.include_dirs = include_dirs or ()

    def write_pxd(self, pxd: io.IOBase, parser: Parser):
        # enum
        enums = [x for x in parser.enums if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if enums:
            pxd.write(f'''cdef extern from "{self.header.name}" namespace "{self.namespace}":
''')
            for enum in enums:
                pxd.write(f'    ctypedef enum {enum.cursor.spelling}:\n')
                pxd.write(f'        pass\n')

        # typedef & struct
        types = [x for x in parser.typedef_struct_list if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if types:
            pxd.write(f'''cdef extern from "{self.header.name}":
''')
            for cursors in types:
                if cursors.cursor.spelling in EXCLUDE_TYPES:
                    # TODO: nested type
                    continue

                cursors.write_pxd(pxd, excludes=EXCLUDE_TYPES)

        # namespace
        funcs = [x for x in parser.functions if pathlib.Path(
            x[-1].location.file.name) == self.header]
        if funcs:
            pxd.write(f'''
cdef extern from "{self.header.name}" namespace "{self.namespace}":
''')
            for cursors in funcs:
                if is_exclude_function(cursors):
                    continue
                function.write_pxd_function(pxd, cursors[-1])

    def write_pyx(self, pyx: io.IOBase, parser: Parser):
        types = [x for x in parser.typedef_struct_list if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if types:
            for v in wrap_types.WRAP_TYPES:
                for cursors in types:
                    if cursors.cursor.spelling == v.name:
                        cursors.write_pyx_ctypes(pyx, flags=v)

        funcs = [x for x in parser.functions if pathlib.Path(
            x[-1].location.file.name) == self.header]
        if funcs:
            overload = {}
            for cursors in funcs:
                if is_exclude_function(cursors):
                    continue

                name = cursors[-1].spelling
                if True:
                    # if name in INCLUDE_FUNCS:
                    count = overload.get(name, 0) + 1
                    function.write_pyx_function(
                        pyx, cursors[-1], overload=count, prefix=self.prefix)
                    overload[name] = count

    def write_pyi(self, pyi: io.IOBase, parser: Parser):
        types = [x for x in parser.typedef_struct_list if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if types:
            for v in wrap_types.WRAP_TYPES:
                for cursors in types:
                    if cursors.cursor.spelling == v.name:
                        cursors.write_pyi(pyi, flags=v)

        funcs = [x for x in parser.functions if pathlib.Path(
            x[-1].location.file.name) == self.header]
        if funcs:
            overload = {}
            for cursors in funcs:
                if is_exclude_function(cursors):
                    continue

                name = cursors[-1].spelling
                if True:
                    # if name in INCLUDE_FUNCS:
                    count = overload.get(name, 0) + 1
                    function.write_pyx_function(
                        pyi, cursors[-1], pyi=True, overload=count, prefix=self.prefix)
                    overload[name] = count
