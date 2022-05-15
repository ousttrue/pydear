from typing import List
import pathlib
import setuptools
from setuptools.command.build_ext import build_ext

try:
    import code_generation
    code_generation.run()
except:
    pass


HERE = pathlib.Path(__name__).absolute().parent

# https://stackoverflow.com/questions/42585210/extending-setuptools-extension-to-use-cmake-in-setup-py


class CMakeExtension(setuptools.Extension):

    def __init__(self, name):
        # don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class build_ext_cmake(build_ext):

    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        # these dirs will be created in build_py, so if you don't have
        # any python sources to bundle, the dirs will be missing
        build_temp = pathlib.Path(self.build_temp)
        build_temp.mkdir(parents=True, exist_ok=True)
        ext_path = pathlib.Path(self.get_ext_fullpath(ext.name)).absolute()
        ext_path.parent.mkdir(parents=True, exist_ok=True)

        # example of cmake args
        config = 'Debug' if self.debug else 'Release'

        # os.chdir(str(build_temp))
        self.spawn(['cmake', '-S', '.', '-B', str(build_temp),
                    f'-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{config.upper()}={ext_path.parent}',
                    f'-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{config.upper()}={ext_path.parent}',
                    f'-DCMAKE_BUILD_TYPE={config}'
                    ])
        if not self.dry_run:  # type: ignore
            self.spawn(
                ['cmake', '--build', str(build_temp), '--config', config])


EXTENSIONS: List[setuptools.Extension] = [CMakeExtension(
    'pydear.impl',
)]

setuptools.setup(
    name='pydear',
    description='Dear imgui binding',
    long_description=(HERE / 'README.md').read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    author='ousttrue',
    author_email='ousttrue@gmail.com',
    url='https://github.com/ousttrue/pydear',
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=["PyGLM", "glfw"],
    packages=[
        'pydear',
        'pydear.backends',
        'pydear.utils',
    ],
    package_data={
        'pydear': ['py.typed', '*.pyi', 'assets/*']
    },
    cmdclass={
        'build_ext': build_ext_cmake,  # type: ignore
    },
    ext_modules=EXTENSIONS,
    use_scm_version={
        'write_to': 'src/pydear/_version.py',
    },
    setup_requires=['setuptools_scm'],
)
