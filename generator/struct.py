from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils


class Struct(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        if cursor.spelling in ('ImGuiTextFilter', 'ImGuiStorage'):
            # TODO: nested type
            return

        match cursor.kind:
            case cindex.CursorKind.CLASS_TEMPLATE:
                pxd.write(f'    cdef cppclass {cursor.spelling}[T]')
            case cindex.CursorKind.STRUCT_DECL:
                pxd.write(f'    struct {cursor.spelling}')
            case _:
                raise RuntimeError()

        has_children = False
        for child in cursor.get_children():
            match child.kind:
                case cindex.CursorKind.FIELD_DECL:
                    if not has_children:
                        pxd.write(':\n')
                        has_children = True
                    pxd.write(
                        f'        {utils.type_name(utils.pxd_type_filter(child.type.spelling), child.spelling)}\n')

        if not has_children:
            pxd.write(':\n')
            pxd.write('        pass\n')

    def write_pyx(self, pyx: io.IOBase):
        '''
        wrapper `cdef class`
        '''
        cursor = self.cursors[-1]
        if cursor.spelling in ('ImGuiTextFilter', 'ImGuiStorage'):
            # TODO: nested type
            return
        match cursor.kind:
            case cindex.CursorKind.CLASS_TEMPLATE:
                return

        definition = cursor.get_definition()
        if definition and definition != cursor:
            # skip
            return
        pyx.write(f'''cdef class {cursor.spelling}:
    cdef cpp_imgui.{cursor.spelling} *_ptr
    @staticmethod
    cdef from_ptr(cpp_imgui.{cursor.spelling}* ptr):
        if ptr == NULL:
            return None
        instance = {cursor.spelling}()
        instance._ptr = ptr
        return instance                    
''')

        for child in cursor.get_children():
            match child.kind:
                case cindex.CursorKind.FIELD_DECL:
                    pyx.write(
                        f'    cdef {utils.type_name(utils.pyx_type_filter(child.type.spelling), child.spelling)}\n')

        pyx.write('\n')
