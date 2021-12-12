from typing import NamedTuple, Tuple
import io
import re
from clang import cindex
from . import utils


def is_forward_declaration(cursor: cindex.Cursor) -> bool:
    '''
    https://joshpeterson.github.io/identifying-a-forward-declaration-with-libclang    
    '''
    definition = cursor.get_definition()

    # If the definition is null, then there is no definition in this translation
    # unit, so this cursor must be a forward declaration.
    if not definition:
        return True

    # If there is a definition, then the forward declaration and the definition
    # are in the same translation unit. This cursor is the forward declaration if
    # it is _not_ the definition.
    return cursor != definition


IM_PATTERN = re.compile(r'\bIm\w+')
TEMPLAE_PATTERN = re.compile(r'<[^>]+>')


def pxd_type_filter(src: str) -> str:
    def rep_typearg(m):
        ret = f'[{m.group(0)[1:-1]}]'
        return ret
    dst = TEMPLAE_PATTERN.sub(rep_typearg, src)

    return dst


def pyx_type_filter(src: str) -> str:
    def add_prefix(m):
        if m.group(0) == 'ImGuiTextRange':
            return m.group(0)
        ret = f'cpp_imgui.{m.group(0)}'
        return ret
    dst = IM_PATTERN.sub(add_prefix, src)

    def rep_typearg(m):
        ret = f'[{m.group(0)[1:-1]}]'
        return ret
    dst = TEMPLAE_PATTERN.sub(rep_typearg, dst)

    return dst


class StructDecl(NamedTuple):
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
                        f'        {utils.type_name(pxd_type_filter(child.type.spelling), child.spelling)}\n')

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
                        f'    cdef {utils.type_name(pyx_type_filter(child.type.spelling), child.spelling)}\n')

        pyx.write('\n')
