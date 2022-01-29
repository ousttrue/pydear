from rawtypes.interpreted_types import *
from rawtypes import vcenv  # search setup vc path
from rawtypes.parser.header import Header
from rawtypes.parser.struct_cursor import WrapFlags
import os
import pathlib

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext as build_ext_orig

import subprocess
import setuptools
import sys
import pathlib
from typing import List
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s]%(name)s:%(lineno)s:%(message)s')

HERE = pathlib.Path(__file__).absolute().parent
PACKAGE_DIR = HERE / 'src/pydear'
EXTERNAL_DIR = HERE / '_external'
CMAKE_BUILD = HERE / 'build'
CPP_PATH = HERE / 'cpp_src/impl.cpp'

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

CPP_BEGIN = '''
static ImVec2 get_ImVec2(PyObject *src)
{
    float x, y;
    if(PyArg_ParseTuple(src, "ff", &x, &y))
    {
        return {x, y};
    }
    PyErr_Clear();

    return {};
}
'''

HEADERS: List[Header] = [
    # Header(
    #     EXTERNAL_DIR, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
    #     include_dirs=[EXTERNAL_DIR / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
    Header(
        EXTERNAL_DIR / 'imgui/imgui.h',
        include_dirs=[EXTERNAL_DIR / 'imgui'],
        begin=IMVECTOR,
        after_include=CPP_BEGIN),
    # Header(
    #     EXTERNAL_DIR / 'ImFileDialogWrap.h',
    #     include_dirs=[EXTERNAL_DIR]),
    # Header(
    #     EXTERNAL_DIR, 'ImGuizmo/ImGuizmo.h',
    #     include_dirs=[EXTERNAL_DIR / 'ImGuizmo'], prefix='ImGuizmo_'),
    Header(
        EXTERNAL_DIR / 'imnodes/imnodes.h',
        include_dirs=[EXTERNAL_DIR / 'imnodes']),
    Header(
        EXTERNAL_DIR / 'nanovg/src/nanovg.h',
        include_dirs=[EXTERNAL_DIR / 'nanovg/src']),
    Header(
        EXTERNAL_DIR / 'glew-2.1.0/include/GL/glew.h',
        include_dirs=[EXTERNAL_DIR / 'glew-2.1.0/include/GL'],
        definitions=['GLEW_STATIC'],
        if_include=lambda name: name == 'glewInit'),
    Header(
        EXTERNAL_DIR / 'nanovg/src/nanovg_gl.h',
        include_dirs=[EXTERNAL_DIR / 'nanovg/src',
                      EXTERNAL_DIR / 'glew-2.1.0/include'],
        definitions=['NANOVG_GL3_IMPLEMENTATION', 'NOMINMAX'],
        before_include='#include <GL/glew.h>\n'),
]

WRAP_TYPES = [
    WrapFlags('ImVec2', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
''',
    )),
    WrapFlags('ImVec4', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
    yield self.w
    yield self.h
''',
    )),
    WrapFlags('ImFont'),
    WrapFlags('ImFontConfig', fields=True, default_constructor=True),
    WrapFlags('ImFontAtlasCustomRect', fields=True),
    WrapFlags('ImFontAtlas', fields=True, methods=True),
    WrapFlags('ImGuiIO', fields=True, custom_fields={
        'Fonts': '''def Fonts(self)->'ImFontAtlas':
    return ctypes.cast(ctypes.c_void_p(self._Fonts), ctypes.POINTER(ImFontAtlas))[0]
'''
    }),
    WrapFlags('ImGuiContext'),
    WrapFlags('ImDrawCmd', fields=True),
    WrapFlags('ImDrawData', fields=True),
    WrapFlags('ImDrawListSplitter', fields=True),
    WrapFlags('ImDrawCmdHeader', fields=True),
    WrapFlags('ImDrawList', fields=True),
    WrapFlags('ImGuiViewport', fields=True, methods=True),
    WrapFlags('ImGuiStyle'),
    WrapFlags('ImGuiWindowClass'),

    # tinygizmo
    WrapFlags('gizmo_context', fields=True, methods=True),

    # nanovg
    WrapFlags('NVGcolor', True),
    WrapFlags('NVGpaint', True),
    WrapFlags('GLNVGblend', True),
]


class ImVec2WrapType(BaseType):
    def __init__(self):
        super().__init__('ImVec2')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec2'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: Union[ImVec2, Tuple[float, float]]{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec2 p{i} = impl.ImVec2({name}[0], {name}[1]) if isinstance({name}, tuple) else impl.ImVec2({name}.x, {name}.y)
'''

    def result_typing(self, pyi: bool) -> str:
        return 'Tuple[float, float]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec2 value = {call}
{indent}return (value.x, value.y)
'''

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}ImVec2 p{i} = t{i} ? get_ImVec2(t{i}) : {default_value};\n'
        else:
            return f'{indent}ImVec2 p{i} = get_ImVec2(t{i});\n'

    def py_value(self, value: str) -> str:
        return f'Py_BuildValue("(ff)", {value}.x, {value}.y)'


class ImVec4WrapType(BaseType):
    def __init__(self):
        super().__init__('ImVec4')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec4'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: Union[ImVec4, Tuple[float, float, float, float]]{default_value}'

    def result_typing(self, pyi: bool) -> str:
        return 'Tuple[float, float, float, float]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec4 value = {call}
{indent}return (value.x, value.y, value.z, value.w)
'''

    def py_value(self, value: str) -> str:
        return f'Py_BuildValue("(ffff)", {value}.x, {value}.y, {value}.z, {value}.w)'


class ImVector(BaseType):
    def __init__(self):
        super().__init__('ImVector')

    @property
    def ctypes_type(self) -> str:
        return 'ImVector'


class VertexBufferType(BaseType):
    def __init__(self):
        super().__init__('VertexBuffer')

    @property
    def ctypes_type(self) -> str:
        return 'VertexBuffer'

    def result_typing(self, pyi: bool) -> str:
        return 'Tuple[ctypes.c_void_p, int, ctypes.c_void_p, int]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.VertexBuffer value = {call}
{indent}return (ctypes.c_void_p(<uintptr_t>value.vertices), value.vertices_count, ctypes.c_void_p(<uintptr_t>value.indices), value.indices_count)
'''


#
# generate c++ source and relative py and pyi
#
from rawtypes.generator.generator import Generator  # noqa
generator = Generator(*HEADERS)

generator.type_manager.WRAP_TYPES.extend(WRAP_TYPES)

IMVECTOR_TYPE = ImVector()


def if_imvector(c):
    if c.spelling.startswith(
            'ImVector<'):
        return IMVECTOR_TYPE


generator.type_manager.processors = [
    TypeProcessor(if_imvector),
    TypeProcessor(lambda c: ImVec2WrapType() if c.type.spelling in [
                  'ImVec2', 'const ImVec2 &'] else None),
    TypeProcessor(lambda c: ImVec4WrapType() if c.type.spelling ==
                  'ImVec4' else None),
    TypeProcessor(lambda c: VertexBufferType() if c.type.spelling ==
                  'tinygizmo::VertexBuffer' else None),
]


generator.generate(PACKAGE_DIR, CPP_PATH)

#
# build impl to build/Release/lib/imgui.lib
#
build_type = "Release"
if '--debug' in sys.argv:
    build_type = "Debug"
subprocess.run(
    f'cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE={build_type}')
subprocess.run(f'cmake --build build --config {build_type}')


def rel_path(src: pathlib.Path) -> str:
    return str(src.relative_to(HERE)).replace('\\', '/')


class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext(build_ext_orig):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        cwd = pathlib.Path().absolute()

        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        extdir = pathlib.Path(self.get_ext_fullpath(ext.name))
        extdir.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'
        cmake_args = [
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' +
            str(extdir.parent.absolute()),
            '-DCMAKE_BUILD_TYPE=' + config
        ]

        # example of build args
        build_args = [
            '--config', config,
            '--', '-j4'
        ]

        os.chdir(str(build_temp))
        self.spawn(['cmake', str(cwd)] + cmake_args)
        if not self.dry_run:
            self.spawn(['cmake', '--build', '.'] + build_args)
        # Troubleshooting: if fail on line above then delete all possible
        # temporary CMake files including "CMakeCache.txt" in top level dir.
        os.chdir(str(cwd))


EXTENSIONS = [CMakeExtension(
    'pydear.impl',
    # sources=[
    #     # generated
    #     rel_path(cpp_path),
    # ],
    # include_dirs=[
    #     str(include_dir) for header in HEADERS for include_dir in header.include_dirs],
    # language='c++',
    # extra_compile_args=['/wd4244', '/std:c++17',
    #                     '-DNANOVG_GL3_IMPLEMENTATION', '-D_WIN32', '-DNOMINMAX', '-DGLEW_STATIC'],
    # # cmake built
    # libraries=["imgui", "Advapi32", "Gdi32", "OpenGL32"],
    # library_dirs=[
    #     str(CMAKE_BUILD / f'{build_type}/lib')],
)]

setuptools.setup(
    name='pydear',
    description='Dear imgui binding',
    author='ousttrue',
    author_email='ousttrue@gmail.com',
    url='https://github.com/ousttrue/pydear',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=[
        'pydear',
        'pydear.backends',
        'pydear.utils',
    ],
    package_data={
        'pydear': ['py.typed', '*.pyi']
    },
    ext_modules=EXTENSIONS,
    use_scm_version={
        'write_to': 'src/pydear/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
