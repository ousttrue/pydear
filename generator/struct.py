from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils
from .typewrap import TypeWrap


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

    @property
    def cursor(self) -> cindex.Cursor:
        return self.cursors[-1]

    def write_pxd(self, pxd: io.IOBase, *, excludes=()):
        cursor = self.cursors[-1]

        constructors = [child for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.CONSTRUCTOR]

        methods = TypeWrap.get_struct_methods(cursor, excludes=excludes)
        if cursor.kind == cindex.CursorKind.CLASS_TEMPLATE:
            pxd.write(f'    cppclass {cursor.spelling}[T]')
        elif constructors or methods:
            pxd.write(f'    cppclass {cursor.spelling}')
        else:
            definition = cursor.get_definition()
            if definition and any(child for child in definition.get_children() if child.kind == cindex.CursorKind.CONSTRUCTOR):
                # forward decl
                pxd.write(f'    cppclass {cursor.spelling}')
            else:
                pxd.write(f'    struct {cursor.spelling}')

        fields = TypeWrap.get_struct_fields(cursor)
        if constructors or fields:
            pxd.write(':\n')

            for field in fields:
                pxd.write(f'        {field.c_type_with_name}\n')

            for child in constructors:
                params = TypeWrap.get_function_params(child)
                pxd.write(
                    f'        {cursor.spelling}({utils.comma_join(param.c_type_with_name for param in params)})\n')

            for child in methods:
                params = TypeWrap.get_function_params(child)
                result = TypeWrap.from_function_result(child)
                pxd.write(
                    f'        {result.c_type} {child.spelling}({utils.comma_join(param.c_type_with_name for param in params)})\n')

        pxd.write('\n')

    def write_pyx(self, pyx: io.IOBase, *, write_property=False):
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

        if write_property:
            for child in cursor.get_children():
                match child.kind:
                    case cindex.CursorKind.FIELD_DECL:
                        if '(*)' in child.type.spelling:
                            # function pointer
                            continue

                        # public = ''
                        # if not is_wrap(child.type) and child.type.kind != cindex.TypeKind.POINTER:
                        #     public = 'public '
                        result_type = TypeWrap.from_struct_field(child)
                        member = f'self._ptr.{child.spelling}'
                        pyx.write(f'''    @property
        def {child.spelling}(self)->{result_type.py_type}:
            return {result_type.c_to_py(member)}
    ''')

            pyx.write('\n')
