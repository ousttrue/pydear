import sys
import logging
from setuptools import Extension, setup
from Cython.Build import cythonize
import pathlib
import subprocess
HERE = pathlib.Path(__file__).parent
sys.path.append(str(HERE / '_external/pycindex/src'))
PACKAGE_DIR = HERE / 'src/pydeer'
EXTERNAL_DIR = HERE / '_external'
CMAKE_BUILD = HERE / 'build'
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]%(name)s:%(lineno)s:%(message)s')

# generate pyd, pyx, pyi from imgui.h
try:
    from clang import cindex
except:
    # get clang
    import _external.pycindex.setup
import generator  # noqa
include_dirs = generator.generate(EXTERNAL_DIR, PACKAGE_DIR)


def rel_path(src: pathlib.Path) -> str:
    return str(src.relative_to(HERE)).replace('\\', '/')


# build imgui to build/Release/lib/imgui.lib
import vcenv
subprocess.run('cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release')
subprocess.run('cmake --build build --config Release')


extensions = [Extension('pydeer.impl',
                        sources=[
                            rel_path(PACKAGE_DIR / 'impl/impl.pyx'),  # generated
                        ],
                        include_dirs=include_dirs,
                        language='c++',
                        extra_compile_args=['/wd4244', '/std:c++17'],
                        # cmake built
                        libraries=["imgui", "Advapi32", "Gdi32"],
                        library_dirs=[str(CMAKE_BUILD / 'Release/lib')],
                        )]

setup(
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
    ext_modules=cythonize(extensions, compiler_directives={
                          'language_level': '3'}),
    use_scm_version={
        'write_to': 'src/pydeer/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
