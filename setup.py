
import pathlib
import sys
import setuptools
HERE = pathlib.Path(__file__).parent
sys.path.append(str(HERE / '_external/pycindex/src'))
PACKAGE_DIR = HERE / 'src/pydeer'
EXTERNAL_DIR = HERE / '_external'
CMAKE_BUILD = HERE / 'build'

import extension_util  # nopep8
extensions = extension_util.get_extensions(
    HERE, PACKAGE_DIR, EXTERNAL_DIR, CMAKE_BUILD,
    extension_util.ExtType.RAWTYPES
)

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
