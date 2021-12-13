from typing import NamedTuple, Tuple
import io
from clang import cindex
from . import utils
from .typewrap import TypeWrap
from .include_flags import IncludeFlags


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

    def write_pyx_ctypes(self, pyx: io.IOBase, *, flags: IncludeFlags = IncludeFlags()):
        cursor = self.cursors[-1]
        definition = cursor.get_definition()
        if definition and definition != cursor:
            return

        pyx.write(f'class {cursor.spelling}(ctypes.Structure):\n')
        fields = TypeWrap.get_struct_fields(
            cursor) if flags.fields else []
        if fields:
            pyx.write('    _fields_=[\n')
            for field in fields:
                pyx.write(
                    f'        ("{field.name}", {field.get_ctypes_type()}),\n')
            pyx.write('    ]\n\n')

        methods = TypeWrap.get_struct_methods(cursor, includes=flags.methods)
        if methods:
            for method in methods:
                params = TypeWrap.get_function_params(method)
                result = TypeWrap.from_function_result(method)

                if result.is_void:
                    pyx.write(f'''    def {method.spelling}(self, {utils.comma_join(param.name_with_ctypes_type for param in params)}):
        cdef cpp_imgui.{self.cursor.spelling} *ptr = <cpp_imgui.{self.cursor.spelling}*><uintptr_t>ctypes.addressof(self)
        ptr.{method.spelling}({utils.comma_join(param.ctypes_to_pointer(param.name) for param in params)})

''')


                # pyx.write(
                #     f'    def {method.spelling}(self, {utils.comma_join(param.name for param in params)}):\n')
                # pyx.write(
                #     f'        (<cpp_imgui.{cursor.spelling}*><uintptr_t>ctypes.addressof(self)).{method.spelling}({utils.comma_join(param.name for param in params)})\n')
                # pyx.write(f'\n')

        if not fields and not methods:
            pyx.write('    pass\n\n')
