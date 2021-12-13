from typing import NamedTuple
from clang import cindex
import re
from . import utils


def symbol_filter(src: str) -> str:
    '''
    fix python reserved word
    '''
    match src:
        case 'in' | 'id':
            return '_' + src
        case _:
            return src


def is_pointer(src: str) -> bool:
    if re.search(r'\s*\*', src):
        return True
    else:
        return False


def is_reference(src: str) -> bool:
    if re.search(r'\s*&', src):
        return True
    else:
        return False


def get_type(cursor: cindex.Cursor):
    name = cursor.spelling
    return (name, cursor.type.spelling)


def is_wrap(type):
    if type.kind != cindex.TypeKind.RECORD:
        return False
    m = re.search(r'\bIm', type.spelling)
    if m:
        if '**' in type.spelling:
            return False
        else:
            # ImXXX
            return True
    else:
        return False


class Param(NamedTuple):
    cursor: cindex.Cursor

    @property
    def c_type_name(self) -> str:
        param_name, param_type = get_type(self.cursor)
        param_name = symbol_filter(param_name)
        param_type = utils.template_filter(param_type).replace('[]', '*')
        m = re.match(r'(.*)\(\*\)(.*)', param_type)
        if m:
            return f"{m.group(1)}(*{param_name}){m.group(2)}"
        else:
            return f"{param_type} {param_name}"

    @property
    def py_type_name(self) -> str:
        param_name, param_type = get_type(self.cursor)
        name = symbol_filter(param_name)
        match self.cursor.type.spelling:
            case 'const char *':
                return f'{name}: bytes'
            case 'const ImVec2 &' | 'ImVec2':
                return f'{name}: Tuple[float, float]'
            case 'const ImVec4 &':
                return f'{name}: Tuple[float, float, float, float]'
            case 'void *' | 'const void *':
                return f'unsigned char[::1] {name}'
            case 'ImTextureID':
                return f'{name}: int'
            case _:
                match self.cursor.type.kind:
                    case cindex.TypeKind.POINTER:
                        if is_wrap(self.cursor.type):
                            return f"{utils.def_pointer_filter(param_type)} {name}"
                        # TODO: null check
                        # TODO: default value
                        # bool *
                        return f"{self.cursor.type.get_pointee().spelling}[::1] {name}"
                    case cindex.TypeKind.INCOMPLETEARRAY:
                        raise NotImplementedError()
                    case cindex.TypeKind.VARIABLEARRAY:
                        raise NotImplementedError()
                    case cindex.TypeKind.CONSTANTARRAY:
                        if is_wrap(self.cursor.type):
                            raise NotImplementedError()
                        # float [2]
                        return f"{self.cursor.type.get_array_element_type().spelling}[::1] {name}"
                    case _:
                        if is_wrap(self.cursor.type):
                            return f"cpp_imgui.{param_type} {name}"
                        else:
                            return f"{param_type} {name}"

    @property
    def py_to_c(self) -> str:
        param_name, param_type = get_type(self.cursor)
        name = symbol_filter(param_name)
        match self.cursor.type.spelling:
            case 'const char *':
                return f'{name}'
            case 'const ImVec2 &' | 'ImVec2':
                return f"cpp_imgui.ImVec2({name}[0], {name}[1])"
            case 'const ImVec4 &':
                return f"cpp_imgui.ImVec4({name}[0], {name}[1], {name}[2], {name}[3])"
            case 'ImTextureID':
                return f'<cpp_imgui.ImTextureID>{name}'
            case _:
                match self.cursor.type.kind:
                    case cindex.TypeKind.POINTER | cindex.TypeKind.CONSTANTARRAY:
                        if is_wrap(self.cursor.type):
                            return f'({name}._ptr if {name} else NULL)'
                        # TODO: null check
                        # TODO: default value
                        # bool *
                        return f'&{name}[0]'
                    case _:
                        return f"{name}"
