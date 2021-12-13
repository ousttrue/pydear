import pathlib
from .include_flags import IncludeFlags


EXCLUDE_TYPES = (
    'va_list',
    'ImGuiTextFilter',
    'ImGuiStorage',
    'ImGuiStorage *',
)

INCLUDE_TYPES = {
    'ImVec2': IncludeFlags(fields=True, methods=('o',)),
    'ImVec4': IncludeFlags(fields=True, methods=('o',)),
    'ImFont': IncludeFlags(methods=('o',)),
    'ImFontAtlas': IncludeFlags(fields=True, methods=('GetTexDataAsRGBA32', 'ClearTexData',)),
    'ImGuiIO': IncludeFlags(fields=True, methods=('o',)),
    'ImGuiContext': IncludeFlags(methods=('o',)),
    'ImDrawData': IncludeFlags(fields=True, methods=('o',))
}

INCLUDE_FUNCS = (
    'CreateContext',
    'GetIO',
    'GetCurrentContext',
    'NewFrame',
    'Render',
    'GetDrawData',
    #
    'Begin',
    'End',
    'Text',
)


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path):
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
        for definition in parser.typedef_struct_list:
            if definition.cursor.spelling in EXCLUDE_TYPES:
                # TODO: nested type
                continue

            definition.write_pxd(pxd, excludes=EXCLUDE_TYPES)

        # namespace ImGui
        pxd.write('''
cdef extern from "imgui.h" namespace "ImGui":
''')
        for definition in parser.functions:
            definition.write_pxd(pxd, excludes=EXCLUDE_TYPES)

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
        # for definition in parser.typedef_struct_list:
        #     if definition.cursor.spelling in INCLUDE_TYPES:
        #         definition.write_pyx_ctypes(
        #             pyx, flags=INCLUDE_TYPES[definition.cursor.spelling])
        for k, v in INCLUDE_TYPES.items():
            for definition in parser.typedef_struct_list:
                if definition.cursor.spelling == k:
                    definition.write_pyx_ctypes(pyx, flags=v)

        for definition in parser.functions:
            if definition.cursor.spelling in INCLUDE_FUNCS:
                definition.write_pyx(pyx)

    #
    # pyd
    #
    with pyi_path.open('w') as pyi:
        pass
