import logging
from setuptools import Extension, setup
from Cython.Build import cythonize
import pathlib
import generator
HERE = pathlib.Path(__file__).parent
PYI_PATH = HERE / 'src/cydeer/imgui.pyi'
EXT_DIR = HERE / 'src/cydeer/imgui'
IMGUI_DIR = HERE / '_external/imgui'
logging.basicConfig(level=logging.DEBUG)

# generate pyd, pyx, pyi from imgui.h
generator.generate(IMGUI_DIR, EXT_DIR, PYI_PATH)


def rel_path(src: pathlib.Path) -> str:
    return str(src.relative_to(HERE)).replace('\\', '/')


extensions = [Extension('cydeer.imgui',
                        sources=[
                            rel_path(EXT_DIR / 'imgui.pyx'),  # generated
                            rel_path(IMGUI_DIR / 'imgui.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_widgets.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_draw.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_tables.cpp'),
                            rel_path(IMGUI_DIR / 'imgui_demo.cpp'),
                        ],
                        include_dirs=[str(IMGUI_DIR)],
                        language='c++',
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
    ],
    ext_modules=cythonize(extensions, compiler_directives={
                          'language_level': '3'}),
    use_scm_version={
        'write_to': 'src/cydeer/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
