import sys
import logging
from setuptools import Extension, setup
from Cython.Build import cythonize
import pathlib
HERE = pathlib.Path(__file__).parent
sys.path.append(str(HERE / '_external/pycindex/src'))
PYI_PATH = HERE / 'src/cydeer/__init__.pyi'
EXT_DIR = HERE / 'src/cydeer/impl'
IMGUI_DIR = HERE / '_external/imgui'
ENUM_PATH = HERE / 'src/cydeer/imgui_enum.py'
logging.basicConfig(level=logging.DEBUG)

# generate pyd, pyx, pyi from imgui.h
try:
    from clang import cindex
except:
    # get clang
    import _external.pycindex.setup
import generator  # noqa
generator.generate(IMGUI_DIR, EXT_DIR, PYI_PATH, ENUM_PATH)


def rel_path(src: pathlib.Path) -> str:
    return str(src.relative_to(HERE)).replace('\\', '/')


extensions = [Extension('cydeer.impl',
                        sources=[
                            rel_path(EXT_DIR / 'impl.pyx'),  # generated
                            rel_path(IMGUI_DIR / 'imgui.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_widgets.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_draw.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_tables.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_demo.cpp'),
                        ],
                        include_dirs=[str(IMGUI_DIR)],
                        language='c++',
                        extra_compile_args=['/wd4244'],
                        )]

setup(
    name='cydeer',
    description='Dear imgui binding using cython',
    author='ousttrue',
    author_email='ousttrue@gmail.com',
    url='https://github.com/ousttrue/cydeer',
    package_dir={'': 'src'},
    include_package_data=True,
    packages=[
        'cydeer',
        'cydeer.imgui',  # from imgui.h
        'cydeer.backends',
        'cydeer.utils',
    ],
    package_data={
        'cydeer': ['py.typed', '*.pyi']
    },
    ext_modules=cythonize(extensions, compiler_directives={
                          'language_level': '3'}),
    use_scm_version={
        'write_to': 'src/cydeer/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
