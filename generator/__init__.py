from typing import List
import logging
import pathlib
from .parser import Parser
from .header import Header

logger = logging.getLogger(__name__)


def generate(external_dir: pathlib.Path, package_dir: pathlib.Path) -> List[str]:
    headers: List[Header] = [
        Header(
            external_dir, 'tinygizmo/tinygizmo/tiny-gizmo.hpp',
            include_dirs=[external_dir / 'tinygizmo/tinygizmo'], prefix='tinygizmo_'),
        Header(
            external_dir, 'imgui/imgui.h',
            include_dirs=[external_dir / 'imgui']),
        Header(
            external_dir, 'ImFileDialogWrap.h',
            include_dirs=[external_dir]),
        Header(
            external_dir, 'ImGuizmo/ImGuizmo.h',
            include_dirs=[external_dir / 'ImGuizmo'], prefix='ImGuizmo_'),
    ]

    parser = Parser([header.header for header in headers])
    parser.traverse()

    from . import cython_writer
    cython_writer.write(package_dir, parser, headers)

    #
    # enum
    #
    enum_py_path = package_dir / 'imgui_enum.py'
    with enum_py_path.open('w') as enum_py:
        enum_py.write('''from enum import IntEnum

''')
        for e in parser.enums:
            e.write_to(enum_py)

    return [str(include_dir) for header in headers for include_dir in header.include_dirs]
