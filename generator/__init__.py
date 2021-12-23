from typing import List
import logging
import io
from os import write
import pathlib
'''
use from setup.py
'''
from clang import cindex
from . import function
from .interpreted_types import wrap_types
from .parser import Parser

logger = logging.getLogger(__name__)

EXCLUDE_TYPES = (
    'va_list',
    'ImGuiTextFilter',
    'ImGuiStorage',
    'ImGuiStorage *',
)


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

EXCLUDE_FUNCS = (
    'CheckboxFlags',
    'Combo',
    'ListBox',
    'PlotLines',
)


IMVECTOR = '''

def iterate(data: ctypes.c_void_p, t: Type[ctypes.Structure], count: int)->Iterable[ctypes.Structure]:
    p = ctypes.cast(data, ctypes.POINTER(t))
    for i in range(count):
        yield p[i]


class ImVector(ctypes.Structure):
    _fields_ = (
        ('Size', ctypes.c_int),
        ('Capacity', ctypes.c_int),
        ('Data', ctypes.c_void_p),
    )

    def each(self, t: Type[ctypes.Structure])->Iterable[ctypes.Structure]:
        return iterate(self.Data, t, self.Size)

'''


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
    def __init__(self, dir: pathlib.Path, file: str, namespace: str) -> None:
        self.header = dir / file
        self.namespace = namespace

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
                        pyx, cursors[-1], overload=count)
                    overload[name] = count


def generate(external_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path, enum_py_path: pathlib.Path) -> List[str]:

    files = [
        'imgui/imgui.h',
        'ImFileDialogWrap.h',
        'ImGuizmo/ImGuizmo.h',
    ]
    namespaces = [
        'ImGui',
        'ifd',
        'ImGuizmo',
    ]
    include_dirs = [
        external_dir,
        external_dir / 'imgui',
        external_dir / 'ImGuizmo',
    ]

    parser = Parser(external_dir, files)
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)

    headers = [Header(external_dir, file, namespace)
               for file, namespace in zip(files, namespaces)]

    #
    # pxd
    #
    with (ext_dir / 'impl.pxd').open('w') as pxd:
        pxd.write(f'''from libcpp cimport bool
from libcpp.string cimport string

''')

        for header in headers:
            header.write_pxd(pxd, parser)

    #
    # pyx
    #
    with (ext_dir / 'impl.pyx').open('w') as pyx:
        pyx.write('''from typing import Tuple, Any, Union, Iterable, Type
import ctypes
from libcpp cimport bool
from libcpp.string cimport string
cimport impl
from libc.stdint cimport uintptr_t
from libc.string cimport memcpy 

''')
        pyx.write(IMVECTOR)

        for header in headers:
            header.write_pyx(pyx, parser)

    #
    # pyi
    #
    with pyi_path.open('w') as pyi:
        pyi.write('''import ctypes
from . imgui_enum import *
from typing import Any, Union, Tuple
''')

        pyi.write(IMVECTOR)

        for v in wrap_types.WRAP_TYPES:
            for cursors in parser.typedef_struct_list:
                if cursors.cursor.spelling == v.name:
                    cursors.write_pyi(pyi, flags=v)

        overload = {}
        for cursors in parser.functions:
            if is_exclude_function(cursors):
                continue

            name = cursors[-1].spelling
            if True:
                # if name in INCLUDE_FUNCS:
                count = overload.get(name, 0) + 1
                function.write_pyx_function(
                    pyi, cursors[-1], pyi=True, overload=count)
                overload[name] = count

    #
    # enum
    #
    with enum_py_path.open('w') as enum_py:
        enum_py.write('''from enum import IntEnum

''')
        for e in parser.enums:
            e.write_to(enum_py)

    return [str(dir) for dir in include_dirs]
