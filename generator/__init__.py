import pathlib


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path):
    from .parser import Parser
    parser = Parser(imgui_dir / 'imgui.h')
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)
    with (ext_dir / 'cpp_imgui.pxd').open('w') as pxd:
        with (ext_dir / 'imgui.pyx').open('w') as pyx:
            with pyi_path.open('w') as pyi:
                pxd.write('''from libcpp cimport bool
cdef extern from "imgui.h":

''')
                pyx.write('''from libcpp cimport bool
cimport cpp_imgui

''')

                for definition in parser.typedef_struct_list:
                    definition.write_pxd(pxd)
                    definition.write_pyx(pyx)

                pxd.write('''
cdef extern from "imgui.h" namespace "ImGui":
''')

                for definition in parser.functions:
                    definition.write_pxd(pxd)
                    definition.write_pyx(pyx)
                    break
