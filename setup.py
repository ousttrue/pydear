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


def generate(EXTERNAL_DIR: pathlib.Path, PACKAGE_DIR: pathlib.Path):
    #

    headers: List[Header] = [
        # Header(
        #     EXTERNAL_DIR, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
        #     include_dirs=[EXTERNAL_DIR / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
        Header(
            EXTERNAL_DIR, 'imgui/imgui.h',
            include_dirs=[EXTERNAL_DIR / 'imgui']),
        Header(
            EXTERNAL_DIR, 'ImFileDialogWrap.h',
            include_dirs=[EXTERNAL_DIR]),
        # Header(
        #     EXTERNAL_DIR, 'ImGuizmo/ImGuizmo.h',
        #     include_dirs=[EXTERNAL_DIR / 'ImGuizmo'], prefix='ImGuizmo_'),
        Header(
            EXTERNAL_DIR, 'imnodes/imnodes.h',
            include_dirs=[EXTERNAL_DIR / 'imnodes']),
    ]

    from rawtypes import generator  # noqa
    generator.generate(headers, PACKAGE_DIR)
    return headers


def build_static(build_type: str):
    # build imgui to build/Release/lib/imgui.lib
    from rawtypes import vcenv  # search setup vc path
    subprocess.run(
        f'cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE={build_type}')
    subprocess.run(f'cmake --build build --config {build_type}')


def get_extensions(
        HERE: pathlib.Path,
        EXTERNAL_DIR: pathlib.Path,
        PACKAGE_DIR: pathlib.Path,
        CMAKE_BUILD: pathlib.Path) -> List[setuptools.Extension]:

    headers = generate(EXTERNAL_DIR, PACKAGE_DIR)

    def rel_path(src: pathlib.Path) -> str:
        return str(src.relative_to(HERE)).replace('\\', '/')

    build_type = "Release"
    if '--debug' in sys.argv:
        build_type = "Debug"

    try:
        build_static(build_type)
    except:
        pass

    extensions = [setuptools.Extension(
        'pydear.impl',
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
            str(CMAKE_BUILD / f'{build_type}/lib')],
    )]
    return extensions


extensions = get_extensions(HERE, EXTERNAL_DIR, PACKAGE_DIR, CMAKE_BUILD)

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
    ext_modules=extensions,
    use_scm_version={
        'write_to': 'src/pydear/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
