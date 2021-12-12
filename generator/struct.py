from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils
from .param import Param, is_wrap
from .result import ResultType


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


class StructDecl(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        if cursor.spelling in ('ImGuiTextFilter', 'ImGuiStorage'):
            # TODO: nested type
            return

        constructors = [child for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.CONSTRUCTOR]
        methods = [child for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.CXX_METHOD and all(param.type.spelling != 'va_list' for param in child.get_children())]
        if cursor.kind == cindex.CursorKind.CLASS_TEMPLATE:
            pxd.write(f'    cppclass {cursor.spelling}[T]')
            constructors.clear()
        elif constructors or methods:
            pxd.write(f'    cppclass {cursor.spelling}')
        else:
            definition = cursor.get_definition()
            if definition and any(child for child in definition.get_children() if child.kind == cindex.CursorKind.CONSTRUCTOR):
                # forward decl
                pxd.write(f'    cppclass {cursor.spelling}')
            else:
                pxd.write(f'    struct {cursor.spelling}')

        fields = [cursor for cursor in cursor.get_children(
        ) if cursor.kind == cindex.CursorKind.FIELD_DECL]
        if constructors or fields:
            pxd.write(':\n')

            for child in fields:
                pxd.write(
                    f'        {utils.type_name(utils.template_filter(child.type.spelling), child.spelling)}\n')

            for child in constructors:
                params = [Param(child) for child in child.get_children(
                ) if child.kind == cindex.CursorKind.PARM_DECL]
                pxd.write(
                    f'        {cursor.spelling}({", ".join(param.c_type_name for param in params)})\n')

            for child in methods:
                params = [Param(child) for child in child.get_children(
                ) if child.kind == cindex.CursorKind.PARM_DECL]
                result_type = ResultType(child)
                pxd.write(
                    f'        {utils.template_filter(result_type.c_type)} {child.spelling}({", ".join(param.c_type_name for param in params)})\n')

        pxd.write('\n')

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
                    public = ''
                    if not is_wrap(child.type) and child.type.kind != cindex.TypeKind.POINTER:
                        public = 'public '
                    pyx.write(
                        f'    cdef {public}{utils.type_name(utils.pyx_type_filter(child.type.spelling), child.spelling)}\n')

        pyx.write('\n')
