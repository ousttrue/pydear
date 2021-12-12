from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils


class TypedefDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        underlying_type = cursor.underlying_typedef_type
        pxd.write(
            f'    ctypedef {utils.type_name(underlying_type.spelling, cursor.spelling)}\n')

    def write_pyx(self, pyx: io.IOBase):
        pass
