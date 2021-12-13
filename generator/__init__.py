import pathlib

EXCLUDE_TYPES = (
    'va_list',
    'ImGuiTextFilter',
    'ImGuiStorage',
    'ImGuiStorage *',
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

        # funcs namespace
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
from libcpp cimport bool
cimport cpp_imgui

''')
        for definition in parser.typedef_struct_list[:1]:
            definition.write_pyx(pyx)

        # TODO: overload
        return
        used = set()
        for definition in parser.functions:
            if definition.cursors[-1].spelling in used:
                continue
            used.add(definition.cursors[-1].spelling)

            # TODO: callback param... etc
            if definition.cursors[-1].spelling in (
                    'SetNextWindowSizeConstraints',
                    'Combo',
                    'LabelTextV',
                    'BulletTextV',
                    'TextWrappedV',
                    'TextDisabledV',
                    'TextColoredV',
                    'TextV',
                    'InputTextWithHint',
                    'InputTextMultiline',
                    'ImGuiInputTextCallback',
                    'InputText',
                    'ListBox',
                    'TableGetColumnFlags',
                    'PlotLines',
                    'PlotHistogram',
                    'LogTextV',
                    'SetTooltipV',
                    'TreeNodeExV',
                    'TreeNodeV',
                    'AcceptDragDropPayload',
                    'GetDragDropPayload',
                    'GetAllocatorFunctions',
                    'MemAlloc',
                    'SetStateStorage',
                    'GetStateStorage',
                    'ColorConvertU32ToFloat4',
                    'ColorConvertFloat4ToU32',
                    'SetAllocatorFunctions',
            ):
                # skip
                continue
            definition.write_pyx(pyx)

    #
    # pyd
    #
    with pyi_path.open('w') as pyi:
        pass
