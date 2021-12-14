'''
use from setup.py
'''
import pathlib
from . import function
from . import wrap_flags

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


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path, enum_py_path: pathlib.Path):
    from .parser import Parser
    parser = Parser(imgui_dir / 'imgui.h')
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)

    #
    # pxd
    #
    with (ext_dir / 'cpp_imgui.pxd').open('w') as pxd:
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
            function.write_pxd_function(
                pxd, cursors[-1], excludes=EXCLUDE_TYPES)

    #
    # pyx
    #
    with (ext_dir / 'imgui.pyx').open('w') as pyx:
        pyx.write('''from typing import Tuple
import ctypes
from libcpp cimport bool
cimport cpp_imgui
from libc.stdint cimport uintptr_t


class ImVector(ctypes.Structure):
    _fields_ = (
        ('Size', ctypes.c_int),
        ('Capacity', ctypes.c_int),
        ('Data', ctypes.c_void_p),
    )

''')
        for k, v in wrap_flags.WRAP_TYPES.items():
            for cursors in parser.typedef_struct_list:
                if cursors.cursor.spelling == k:
                    cursors.write_pyx_ctypes(pyx, flags=v)

        for cursors in parser.functions:
            if cursors[-1].spelling in INCLUDE_FUNCS:
                function.write_pyx_function(pyx, cursors[-1])

    #
    # pyd
    #
    with pyi_path.open('w') as pyi:
        pass

    #
    # enum
    #
    with enum_py_path.open('w') as enum_py:
        enum_py.write('''from enum import IntEnum

''')
        for e in parser.enums:
            e.write_to(enum_py)
