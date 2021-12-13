from typing import NamedTuple
import re
from clang import cindex
from . import utils


TEMPLATE_PATTERN = re.compile(r'<[^>]+>')


def template_filter(src: str) -> str:
    '''
    replace Some<T> to Some[T]
    '''
    def rep_typearg(m):
        ret = f'[{m.group(0)[1:-1]}]'
        return ret
    dst = TEMPLATE_PATTERN.sub(rep_typearg, src)

    return dst


class TypeWrap(NamedTuple):
    '''
    function result_type
    function param type
    struct field type
    '''
    type: cindex.Type
    cursor: cindex.Cursor

    @staticmethod
    def from_function_result(cursor: cindex.Cursor):
        return TypeWrap(cursor.result_type, cursor)

    @staticmethod
    def from_function_param(cursor: cindex.Cursor):
        return TypeWrap(cursor.type, cursor)

    @staticmethod
    def get_function_params(cursor: cindex.Cursor, *, excludes=()):
        return [TypeWrap.from_function_param(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL and child.type.spelling not in excludes]

    @staticmethod
    def from_struct_field(cursor: cindex.Cursor):
        return TypeWrap(cursor.type, cursor)

    @staticmethod
    def get_struct_fields(cursor: cindex.Cursor):
        return [TypeWrap.from_struct_field(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.FIELD_DECL]

    @staticmethod
    def get_struct_methods(cursor: cindex.Cursor, *, excludes=()):
        def method_filter(method: cindex.Cursor) -> bool:
            if method.spelling == 'GetStateStorage':
                pass
            if method.kind != cindex.CursorKind.CXX_METHOD:
                return False
            for param in method.get_children():
                if param.kind == cindex.CursorKind.PARM_DECL and param.type.spelling in excludes:
                    return False
            if method.result_type.spelling in excludes:
                return False
            return True
        return [child for child in cursor.get_children() if method_filter(child)]

    @property
    def name(self) -> str:
        return utils.symbol_filter(self.cursor.spelling)

    @property
    def is_void(self) -> bool:
        return self.type.kind == cindex.TypeKind.VOID

    @property
    def c_type(self) -> str:
        return template_filter(self.type.spelling).replace('[]', '*')

    @property
    def c_type_with_name(self) -> str:
        c_type = self.c_type
        name = self.name
        splitted = c_type.split('(*)', maxsplit=1)
        if len(splitted) == 2:
            return f"{splitted[0]}(*{name}){splitted[1]}"
        else:
            return f"{c_type} {name}"

    @property
    def py_type(self) -> str:
        match self.type.kind:
            case cindex.TypeKind.POINTER:
                pointee = self.type.get_pointee()
                match pointee.kind:
                    case cindex.TypeKind.RECORD:
                        return pointee.spelling

        return self.c_type

    @property
    def user_type_pointer(self) -> bool:
        match self.type.kind:
            case cindex.TypeKind.POINTER:
                pointee = self.type.get_pointee()
                match pointee.kind:
                    case cindex.TypeKind.RECORD:
                        return True

        return False

    @property
    def py_type_with_name(self) -> str:
        '''
        primitive
        bytes: const char*... etc
        wrap type pointer: ImFontAtlas *, ImGuiContext *        
        '''
        name = self.name
        if self.user_type_pointer:
            return f'{name}: {self.py_type}'
        return f'{self.c_type} {name}'
        # match self.cursor.type.spelling:
        #     case 'const char *':
        #         return f'{py_name}: bytes'
        #     case 'const ImVec2 &' | 'ImVec2':
        #         return f'{py_name}: Tuple[float, float]'
        #     case 'const ImVec4 &':
        #         return f'{py_name}: Tuple[float, float, float, float]'
        #     case 'void *' | 'const void *':
        #         return f'unsigned char[::1] {py_name}'
        #     case 'ImTextureID':
        #         return f'{py_name}: int'

        # match self.cursor.type.kind:
        #     case cindex.TypeKind.POINTER:
        #         if is_wrap(self.cursor.type):
        #             return f"{utils.def_pointer_filter(param_type)} {name}"
        #         # TODO: null check
        #         # TODO: default value
        #         # bool *
        #         return f"{self.cursor.type.get_pointee().spelling}[::1] {name}"
        #     case cindex.TypeKind.INCOMPLETEARRAY:
        #         raise NotImplementedError()
        #     case cindex.TypeKind.VARIABLEARRAY:
        #         raise NotImplementedError()
        #     case cindex.TypeKind.CONSTANTARRAY:
        #         if is_wrap(self.cursor.type):
        #             raise NotImplementedError()
        #         # float [2]
        #         return f"{self.cursor.type.get_array_element_type().spelling}[::1] {name}"
        #     case _:
        #         if is_wrap(self.cursor.type):
        #             return f"cpp_imgui.{param_type} {name}"
        #         else:
        #             return f"{param_type} {name}"

    @property
    def pyx_type(self) -> str:
        if self.user_type_pointer:
            return f'cpp_imgui.{self.c_type}'
        return self.c_type

    @property
    def py_to_c(self) -> str:
        if self.user_type_pointer:
            return f'<cpp_imgui.{self.c_type}><uintptr_t>ctypes.addressof({self.name})'
        return self.name
#         param_name, param_type = get_type(self.cursor)
#         name = symbol_filter(param_name)
#         match self.cursor.type.spelling:
#             case 'const char *':
#                 return f'{name}'
#             case 'const ImVec2 &' | 'ImVec2':
#                 return f"cpp_imgui.ImVec2({name}[0], {name}[1])"
#             case 'const ImVec4 &':
#                 return f"cpp_imgui.ImVec4({name}[0], {name}[1], {name}[2], {name}[3])"
#             case 'ImTextureID':
#                 return f'<cpp_imgui.ImTextureID>{name}'
#             case _:
#                 match self.cursor.type.kind:
#                     case cindex.TypeKind.POINTER | cindex.TypeKind.CONSTANTARRAY:
#                         if is_wrap(self.cursor.type):
#                             return f'({name}._ptr if {name} else NULL)'
#                         # TODO: null check
#                         # TODO: default value
#                         # bool *
#                         return f'&{name}[0]'
#                     case _:
#                         return f"{name}"

    def c_to_py(self, name: str) -> str:
        if self.user_type_pointer:
            return f'ctypes.cast(ctypes.c_void_p(<long long>{name}), ctypes.POINTER({self.py_type}))[0]'
        return name
        # result_type = self.type
#         match result_type.kind:
#             case cindex.TypeKind.BOOL | cindex.TypeKind.FLOAT | cindex.TypeKind.SHORT | cindex.TypeKind.INT | cindex.TypeKind.UINT | cindex.TypeKind.INT | cindex.TypeKind.DOUBLE:
#                 return name
#             case cindex.TypeKind.POINTER:
#                 if is_wrap(self.type):
#                     return f'{utils.def_pointer_filter(result_type.spelling)}.from_ptr({name})'
#                 else:
#                     return f'<long long>{name}'

#             case cindex.TypeKind.LVALUEREFERENCE if is_wrap(self.type):
#                 return f'{utils.def_pointer_filter(result_type.spelling)}.from_ptr(&{name})'
#             case cindex.TypeKind.TYPEDEF:
#                 underlying = self.unerlying_type()
#                 match underlying.kind:
#                     case cindex.TypeKind.INT | cindex.TypeKind.UINT | cindex.TypeKind.SHORT | cindex.TypeKind.USHORT:
#                         return name
#                     case cindex.TypeKind.POINTER:
#                         return f'<long long>{name}'
#                     case _:
#                         raise NotImplementedError()

#             case _:
#                 if self.is_bytes:
#                     return f'bytes()'

#                 # ImVec2, ImVec4
#                 match result_type.spelling:
#                     case 'ImVec2':
#                         # copy by value
#                         return f'({name}.x, {name}.y)'
#                     case 'ImVec4':
#                         # copy by value
#                         return f'({name}.x, {name}.y, {name}.z, {name}.w)'
#                     case _:
#                         return name
