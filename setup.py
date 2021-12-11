import logging
from setuptools import Extension, setup
from Cython.Build import cythonize
import pathlib
import generate_cython_binding
HERE = pathlib.Path(__file__).parent
EXT_DIR = HERE / 'src/cydeer/imgui'
IMGUI_DIR = HERE / '_external/imgui'
logging.basicConfig(level=logging.DEBUG)

# generate pyd, pyx, pyi from imgui.h
generate_cython_binding.generate(IMGUI_DIR, EXT_DIR)

extensions = [Extension('cydeer.imgui',
                        sources=[
                            str(EXT_DIR / 'imgui.pyx'),  # generated
                            str(IMGUI_DIR / 'imgui.cpp'),
                        ],
                        include_dirs=[str(HERE / '_external/MikkTSpace')],
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
