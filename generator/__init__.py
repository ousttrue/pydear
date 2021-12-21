'''
use from setup.py
'''
from os import write
import pathlib
from clang import cindex
from . import function
from . import typeconv
from .types import wrap_types

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


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path, enum_py_path: pathlib.Path):
    from .parser import Parser
    parser = Parser(imgui_dir / 'imgui.h')
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)

    #
    # pxd
    #
    with (ext_dir / 'impl.pxd').open('w') as pxd:
        # types
        pxd.write('''from libcpp cimport bool
cdef extern from "imgui.h":

''')
        for cursors in parser.typedef_struct_list:
            if cursors.cursor.spelling in EXCLUDE_TYPES:
                # TODO: nested type
                continue

            cursors.write_pxd(pxd, excludes=EXCLUDE_TYPES)

        # namespace ImGui
        pxd.write('''
cdef extern from "imgui.h" namespace "ImGui":
''')
        for cursors in parser.functions:
            if is_exclude_function(cursors):
                continue
            function.write_pxd_function(pxd, cursors[-1])

    #
    # pyx
    #
    with (ext_dir / 'impl.pyx').open('w') as pyx:
        pyx.write('''from typing import Tuple, Any, Union, Iterable, Type
import ctypes
from libcpp cimport bool
cimport impl
from libc.stdint cimport uintptr_t
from libc.string cimport memcpy 

''')
        pyx.write(IMVECTOR)

        for v in wrap_types.WRAP_TYPES:
            for cursors in parser.typedef_struct_list:
                if cursors.cursor.spelling == v.name:
                    cursors.write_pyx_ctypes(pyx, flags=v)

        overload = {}
        for cursors in parser.functions:
            if is_exclude_function(cursors):
                continue

            name = cursors[-1].spelling
            if True:
                # if name in INCLUDE_FUNCS:
                count = overload.get(name, 0) + 1
                function.write_pyx_function(pyx, cursors[-1], overload=count)
                overload[name] = count

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
