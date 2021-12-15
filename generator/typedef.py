from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils
from .wrap_flags import WrapFlags


class TypedefDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    @property
    def cursor(self) -> cindex.Cursor:
        return self.cursors[-1]

    def write_pxd(self, pxd: io.IOBase, *, excludes=()):
        cursor = self.cursors[-1]
        underlying_type = cursor.underlying_typedef_type
        pxd.write(
            f'    ctypedef {utils.type_name(underlying_type.spelling, cursor.spelling)}\n')

    def write_pyx_ctypes(self, pyx: io.IOBase, *, flags: WrapFlags = WrapFlags(''), pyi=False):
        pass
