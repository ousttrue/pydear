
import pathlib
import sys
import setuptools
HERE = pathlib.Path(__file__).absolute().parent
sys.path.append(str(HERE))
sys.path.append(str(HERE / '_external/pycindex/src'))
PACKAGE_DIR = HERE / 'src/pydear'
EXTERNAL_DIR = HERE / '_external'
CMAKE_BUILD = HERE / 'build'

import extension_util  # nopep8
extensions = extension_util.get_extensions(
    HERE, EXTERNAL_DIR, PACKAGE_DIR, CMAKE_BUILD,
    extension_util.ExtType.RAWTYPES
)

setuptools.setup(
    name='pydear',
    description='Dear imgui binding using cython',
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
    ext_modules=extensions,  # type: ignore
    use_scm_version={
        'write_to': 'src/pydear/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
