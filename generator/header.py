from typing import List
import logging
import io
import pathlib
#
from clang import cindex
from .parser import Parser
from .declarations import function
from .interpreted_types import wrap_types

logger = logging.getLogger(__name__)


INCLUDE_FUNCS = (
    'CreateContext',
    'DestroyContext',
    'GetIO',
    'GetCurrentContext',
    'NewFrame',
    'Render',
    'GetDrawData',
    'StyleColorsDark',
    #
    'ShowDemoWindow',
    'ShowMetricsWindow',
    'Begin',
    'End',
    'Text',
    'Checkbox',
    'SliderFloat',
    'ColorEdit3',
    'Button',
    'SameLine',
)


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
            for t in types:
                if t.cursor.spelling in function.EXCLUDE_TYPES:
                    # TODO: nested type
                    continue

                t.write_pxd(pxd, excludes=function.EXCLUDE_TYPES)

        # namespace
        funcs = [x for x in parser.functions if pathlib.Path(
            x.cursor.location.file.name) == self.header]
        if funcs:
            pxd.write(f'''
cdef extern from "{self.header.name}" namespace "{self.namespace}":
''')
            for func in funcs:
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
                if True:
                    # if name in INCLUDE_FUNCS:
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
                if True:
                    # if name in INCLUDE_FUNCS:
                    count = overload.get(name, 0) + 1
                    function.write_pyx_function(
                        pyi, func.cursor, pyi=True, overload=count, prefix=self.prefix)
                    overload[name] = count
