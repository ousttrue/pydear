from rawtypes.interpreted_types import *
from rawtypes import vcenv  # search setup vc path
from rawtypes.header import Header
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

HEADERS: List[Header] = [
    # Header(
    #     EXTERNAL_DIR, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
    #     include_dirs=[EXTERNAL_DIR / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
    Header(
        EXTERNAL_DIR / 'imgui/imgui.h',
        include_dirs=[EXTERNAL_DIR / 'imgui'],
        begin=IMVECTOR),
    Header(
        EXTERNAL_DIR / 'ImFileDialogWrap.h',
        include_dirs=[EXTERNAL_DIR]),
    # Header(
    #     EXTERNAL_DIR, 'ImGuizmo/ImGuizmo.h',
    #     include_dirs=[EXTERNAL_DIR / 'ImGuizmo'], prefix='ImGuizmo_'),
    Header(
        EXTERNAL_DIR / 'imnodes/imnodes.h',
        include_dirs=[EXTERNAL_DIR / 'imnodes']),
    # Header(
    #     EXTERNAL_DIR, 'nanovg/src/nanovg.h',
    #     include_dirs=[EXTERNAL_DIR / 'nanovg/src']),
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
from rawtypes.generator import Generator  # noqa
generator = Generator(*HEADERS)

IMVECTOR_TYPE = ImVector()


def if_imvector(c):
    if c.spelling.startswith(
            'ImVector<'):
        return IMVECTOR_TYPE


generator.types.processors = [
    TypeProcessor(if_imvector),
    TypeProcessor(lambda c: ImVec2WrapType() if c.type.spelling in [
                  'ImVec2', 'const ImVec2 &'] else None),
    TypeProcessor(lambda c: ImVec4WrapType() if c.type.spelling ==
                  'ImVec4' else None),
    TypeProcessor(lambda c: VertexBufferType() if c.type.spelling ==
                  'tinygizmo::VertexBuffer' else None),
]


cpp_path = generator.generate(PACKAGE_DIR)

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


EXTENSIONS = [setuptools.Extension(
    'pydear.impl',
    sources=[
        # generated
        rel_path(cpp_path),
    ],
    include_dirs=[
        str(include_dir) for header in HEADERS for include_dir in header.include_dirs],
    language='c++',
    extra_compile_args=['/wd4244', '/std:c++17'],
    # cmake built
    libraries=["imgui", "Advapi32", "Gdi32"],
    library_dirs=[
        str(CMAKE_BUILD / f'{build_type}/lib')],
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
