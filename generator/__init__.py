from typing import List
import logging
import pathlib
from .parser import Parser
from .header import Header

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

PXD_SPAN = '''
cdef struct Span:
    void *_data
    size_t count

'''


def generate(external_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path, enum_py_path: pathlib.Path) -> List[str]:

    headers: List[Header] = [
        # Header(
        #     external_dir, 'imgui/imgui.h', 'ImGui',
        #     include_dirs=[external_dir / 'imgui']),
        # Header(
        #     external_dir, 'ImFileDialogWrap.h', 'ifd',
        #     include_dirs=[external_dir]),
        # Header(
        #     external_dir, 'ImGuizmo/ImGuizmo.h', 'ImGuizmo',
        #     include_dirs=[external_dir / 'ImGuizmo'], prefix='ImGuizmo_'),
        Header(
            external_dir, 'tinygizmo/tinygizmo/tiny-gizmo.hpp', 'tinygizmo',
            include_dirs=[external_dir / 'tinygizmo/tinygizmo'], prefix='tinygizmo_')
    ]

    parser = Parser([header.header for header in headers])
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)

    #
    # pxd
    #
    with (ext_dir / 'impl.pxd').open('w') as pxd:
        pxd.write(f'''from libcpp cimport bool
from libcpp.string cimport string
from libcpp.pair cimport pair

''')

        pxd.write(PXD_SPAN)
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
from libcpp.pair cimport pair
from libc.stdint cimport uintptr_t
from libc.string cimport memcpy 
cimport impl

''')
        pyx.write(IMVECTOR)

        # for header in headers:
        #     header.write_pyx(pyx, parser)

    #
    # pyi
    #
    with pyi_path.open('w') as pyi:
        pyi.write('''import ctypes
from . imgui_enum import *
from typing import Any, Union, Tuple
''')

        pyi.write(IMVECTOR)
        for header in headers:
            header.write_pyi(pyi, parser)

    #
    # enum
    #
    with enum_py_path.open('w') as enum_py:
        enum_py.write('''from enum import IntEnum

''')
        for e in parser.enums:
            e.write_to(enum_py)

    return [str(include_dir) for header in headers for include_dir in header.include_dirs]
