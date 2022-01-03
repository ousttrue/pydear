from typing import List
import setuptools
from enum import Enum
import sys
import logging
import pathlib
import subprocess
#
import vcenv  # search setup vc path
from generator.header import Header
HERE = pathlib.Path(__file__).parent
sys.path.append(str(HERE / '_external/pycindex/src'))
PACKAGE_DIR = HERE / 'src/pydeer'
EXTERNAL_DIR = HERE / '_external'
CMAKE_BUILD = HERE / 'build'
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s]%(name)s:%(lineno)s:%(message)s')

headers: List[Header] = [
    Header(
        EXTERNAL_DIR, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
        include_dirs=[EXTERNAL_DIR / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
    Header(
        EXTERNAL_DIR, 'imgui/imgui.h',
        include_dirs=[EXTERNAL_DIR / 'imgui']),
    Header(
        EXTERNAL_DIR, 'ImFileDialogWrap.h',
        include_dirs=[EXTERNAL_DIR]),
    Header(
        EXTERNAL_DIR, 'ImGuizmo/ImGuizmo.h',
        include_dirs=[EXTERNAL_DIR / 'ImGuizmo'], prefix='ImGuizmo_'),
]


# generate pyd, pyx, pyi from imgui.h
try:
    from clang import cindex
except:
    # get clang
    import _external.pycindex.setup
import generator  # noqa


class ExtType(Enum):
    CYTHON = 'cython'
    RAWTYPES = 'rawtypes'


EXT_TYPE = ExtType.RAWTYPES
match EXT_TYPE:
    case ExtType.RAWTYPES:
        from generator.rawtypes_writer import write
    case ExtType.CYTHON:
        from generator.cython_writer import write

generator.generate(headers, PACKAGE_DIR, write)


def rel_path(src: pathlib.Path) -> str:
    return str(src.relative_to(HERE)).replace('\\', '/')


# build imgui to build/Release/lib/imgui.lib
subprocess.run('cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release')
subprocess.run('cmake --build build --config Release')

extensions = []
match EXT_TYPE:
    case ExtType.RAWTYPES:
        extensions = [setuptools.Extension(
            'pydeer.impl',
            sources=[
                # generated
                rel_path(PACKAGE_DIR / 'rawtypes/implmodule.cpp'),
            ],
            include_dirs=[
                str(include_dir) for header in headers for include_dir in header.include_dirs],
            language='c++',
            extra_compile_args=['/wd4244', '/std:c++17'],
            # cmake built
            libraries=["imgui", "Advapi32", "Gdi32"],
            library_dirs=[
                str(CMAKE_BUILD / 'Release/lib')],
        )]

    case ExtType.CYTHON:
        extensions = [setuptools.Extension(
            'pydeer.impl',
            sources=[
                # generated
                rel_path(PACKAGE_DIR / 'impl/impl.pyx'),
            ],
            include_dirs=[
                str(include_dir) for header in headers for include_dir in header.include_dirs],
            language='c++',
            extra_compile_args=['/wd4244', '/std:c++17'],
            # cmake built
            libraries=["imgui", "Advapi32", "Gdi32"],
            library_dirs=[
                str(CMAKE_BUILD / 'Release/lib')],
        )]
        from Cython.Build import cythonize
        extensions = cythonize(extensions, compiler_directives={
                               'language_level': '3'})

setuptools.setup(
    name='pydeer',
    description='Dear imgui binding using cython',
    author='ousttrue',
    author_email='ousttrue@gmail.com',
    url='https://github.com/ousttrue/pydeer',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=[
        'pydeer',
        'pydeer.impl',  # extension
        'pydeer.backends',
        'pydeer.utils',
    ],
    package_data={
        'pydeer': ['py.typed', '*.pyi']
    },
    ext_modules=extensions,  # type: ignore
    use_scm_version={
        'write_to': 'src/pydeer/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
