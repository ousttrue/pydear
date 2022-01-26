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
HEADERS: List[Header] = [
    # Header(
    #     EXTERNAL_DIR, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
    #     include_dirs=[EXTERNAL_DIR / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
    Header(
        EXTERNAL_DIR / 'imgui/imgui.h',
        include_dirs=[EXTERNAL_DIR / 'imgui']),
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

#
# generate c++ source and relative py and pyi
#
from rawtypes.generator import Generator  # noqa
generator = Generator()
generator.parse(*HEADERS)
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
