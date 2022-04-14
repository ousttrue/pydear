from typing import List, Tuple
from rawtypes.generator.cpp_writer import FunctionCustomization
from rawtypes.interpreted_types import *
# from rawtypes import vcenv  # search setup vc path
from rawtypes.parser.header import Header
from rawtypes.parser.struct_cursor import WrapFlags
import pathlib
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
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

FUNCTIONS = {
    # https://github.com/ocornut/imgui/issues/3885
    'Custom_GetLastItemRect': '''
#include <imgui_internal.h>
static PyObject *Custom_GetLastItemRect(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) return NULL;

  ImRect rect = ImGui::GetCurrentContext()->LastItemData.Rect;
  // PyObject* py_value = Py_BuildValue("(ffff)", rect.Min.x, rect.Min.y, rect.Max.x, rect.Max.y);
  PyObject* py_value = ctypes_copy(rect, "ImRect", "imgui_internal");
  return py_value;
}
    ''',
    'Custom_GetLastItemId': '''
static PyObject *Custom_GetLastItemId(PyObject *self, PyObject *args) {
  if (!PyArg_ParseTuple(args, "")) return NULL;

  ImGuiID id = ImGui::GetCurrentContext()->LastItemData.ID;
  PyObject *py_value = PyLong_FromUnsignedLong(id);
  return py_value;
}
    ''',
}

HEADERS: List[Header] = [
    Header(
        EXTERNAL_DIR / 'imgui/imgui.h',
        include_dirs=[EXTERNAL_DIR / 'imgui'],
        begin=IMVECTOR,
        after_include=CPP_BEGIN,
        additional_functions=FUNCTIONS),
    Header(
        EXTERNAL_DIR / 'imgui/imgui_internal.h',
        begin='from .imgui import ImVec2\n',
        include_dirs=[EXTERNAL_DIR / 'imgui_internal'],
        if_include=lambda name: name in ('ButtonBehavior')),
    Header(
        EXTERNAL_DIR / 'imnodes/imnodes.h',
        include_dirs=[EXTERNAL_DIR / 'imnodes']),
    Header(
        EXTERNAL_DIR / 'picovg/src/nanovg.h',
        include_dirs=[EXTERNAL_DIR / 'picovg/src']),
]

WRAP_TYPES = [
    WrapFlags('imgui', 'ImVec2', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
''',
    )),
    WrapFlags('imgui', 'ImVec4', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
    yield self.w
    yield self.h
''',
    )),
    WrapFlags('imgui', 'ImFont'),
    WrapFlags('imgui', 'ImFontConfig', fields=True, default_constructor=True),
    WrapFlags('imgui', 'ImFontAtlasCustomRect', fields=True),
    WrapFlags('imgui', 'ImFontAtlas', fields=True, methods=True),
    WrapFlags('imgui', 'ImGuiKeyData', fields=True),
    WrapFlags('imgui', 'ImGuiIO', fields=True, methods=True, custom_fields={
        'Fonts': '''def Fonts(self)->'ImFontAtlas':
    return ctypes.cast(ctypes.c_void_p(self._Fonts), ctypes.POINTER(ImFontAtlas))[0]
'''
    }),
    WrapFlags('imgui', 'ImGuiContext'),
    WrapFlags('imgui', 'ImDrawCmd', fields=True),
    WrapFlags('imgui', 'ImDrawData', fields=True),
    WrapFlags('imgui', 'ImDrawListSplitter', fields=True),
    WrapFlags('imgui', 'ImDrawCmdHeader', fields=True),
    WrapFlags('imgui', 'ImDrawList', fields=True),
    WrapFlags('imgui', 'ImGuiViewport', fields=True, methods=True),
    WrapFlags('imgui', 'ImGuiStyle'),
    WrapFlags('imgui', 'ImGuiWindowClass'),
    # internal
    WrapFlags('imgui', 'ImRect', fields=True),

    # tinygizmo
    WrapFlags('tinygizmo', 'gizmo_context', fields=True, methods=True),

    # nanovg
    WrapFlags('nanovg', 'NVGcolor', True),
    WrapFlags('nanovg', 'NVGpaint', True),
    WrapFlags('nanovg', 'GLNVGblend', True),
    WrapFlags('nanovg', 'NVGtextRow', True),
    WrapFlags('nanovg', 'NVGglyphPosition', True),
    WrapFlags('nanovg', 'NVGdrawData', True),
    WrapFlags('nanovg', 'NVGparams', True),
    WrapFlags('nanovg', 'NVGvertex', True),
    WrapFlags('nanovg', 'NVGtextureInfo', True),
    WrapFlags('nanovg', 'NVGcompositeOperationState', True),
    WrapFlags('nanovg', 'GLNVGpath', True),
    WrapFlags('nanovg', 'GLNVGcall', True),
    WrapFlags('nanovg', 'GLNVGfragUniforms', True),
]


class ImVec2WrapType(BaseType):
    def __init__(self):
        super().__init__('ImVec2')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec2'

    @property
    def pyi_types(self) -> Tuple[str, ...]:
        return ('ImVec2', 'Tuple[float, float]', 'None')

    def cpp_from_py(self, indent: str, i: int, default_value: str) -> str:
        if default_value:
            return f'{indent}ImVec2 p{i} = t{i} ? get_ImVec2(t{i}) : {default_value};\n'
        else:
            return f'{indent}ImVec2 p{i} = get_ImVec2(t{i});\n'

    def cpp_to_py(self, value: str) -> str:
        return f'Py_BuildValue("(ff)", {value}.x, {value}.y)'


class ImVec4WrapType(BaseType):
    def __init__(self):
        super().__init__('ImVec4')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec4'

    @property
    def pyi_types(self) -> Tuple[str, ...]:
        return ('ImVec4', 'Tuple[float, float, float, float]')

    def cpp_to_py(self, value: str) -> str:
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

FUNCTION_CUSTOMIZE = [
    FunctionCustomization(
        'nvgTextBreakLines',
        {'string': CharPointerType(),
         'end': CharPointerType(),
         }
    ),
]

generator.generate(PACKAGE_DIR, CPP_PATH, FUNCTION_CUSTOMIZE)


# https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py
class CMakeExtension(Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext_cmake(build_ext):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        ext_path = pathlib.Path(self.get_ext_fullpath(ext.name))
        ext_path.parent.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'

        # os.chdir(str(build_temp))
        self.spawn(['cmake', '-S', '.', '-B', str(build_temp),
                    f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{config.upper()}={ext_path.parent}',
                    f'-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{config.upper()}={ext_path.parent}',
                    f'-DCMAKE_BUILD_TYPE={config}'
                    ])
        if not self.dry_run:  # type: ignore
            self.spawn(
                ['cmake', '--build', str(build_temp), '--config', config])


EXTENSIONS: List[Extension] = [CMakeExtension(
    'pydear.impl',
)]

setuptools.setup(
    name='pydear',
    description='Dear imgui binding',
    author='ousttrue',
    author_email='ousttrue@gmail.com',
    url='https://github.com/ousttrue/pydear',
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=["PyGLM", "glfw"],
    packages=[
        'pydear',
        'pydear.backends',
        'pydear.utils',
    ],
    package_data={
        'pydear': ['py.typed', '*.pyi', 'assets/*']
    },
    cmdclass={
        'build_ext': build_ext_cmake,  # type: ignore
    },
    ext_modules=EXTENSIONS,
    use_scm_version={
        'write_to': 'src/pydear/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
