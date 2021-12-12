from typing import NamedTuple, List, Union, Tuple
import pathlib
import io
import logging
import re
from clang import cindex
logger = logging.getLogger(__name__)


def get_type(cursor: cindex.Cursor):
    name = cursor.spelling
    return (name, cursor.type.spelling)


IMPOINTER_PATTERN = re.compile(r'(Im\w+)(\s*\*)(.*)')
CONST_IMPOINTER_PATTERN = re.compile(r'const (Im\w+)(\s*\*)(.*)')


def def_pointer_filter(src: str) -> str:
    #  src.replace('[]', '*')
    m = IMPOINTER_PATTERN.match(src)
    if not m:
        m = CONST_IMPOINTER_PATTERN.match(src)
    if m:
        return f'{m.group(1)}{m.group(3)}'
    else:
        return src


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


def symbol_filter(src: str, *, get_ptr=False) -> str:
    match src:
        case 'in':
            src = '_' + src
    if get_ptr:
        return f'{src}._ptr'
    else:
        return src


FP_PATTERN = re.compile(r'(.*)\(\*\)(.*)')


def type_name(t: str, name: str) -> str:
    m = FP_PATTERN.match(t)
    if m:
        # function pointer
        return f'{m.group(1)}(*{name}){m.group(2)}'
    else:
        return f'{t} {name}'


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


class Enum(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]


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
                        f'        {type_name(pxd_type_filter(child.type.spelling), child.spelling)}\n')

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
                        f'    cdef {type_name(pyx_type_filter(child.type.spelling), child.spelling)}\n')

        pyx.write('\n')


class Typedef(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        underlying_type = cursor.underlying_typedef_type
        pxd.write(
            f'    ctypedef {type_name(underlying_type.spelling, cursor.spelling)}\n')

    def write_pyx(self, pyx: io.IOBase):
        pass


class Function(NamedTuple):
    cursors: Tuple[cindex.Cursor, ...]

    def write_pxd(self, pxd: io.IOBase):
        cursor = self.cursors[-1]
        result_type = cursor.result_type
        params = [get_type(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]
        pxd.write(
            f'    {result_type.spelling} {cursor.spelling}({", ".join(f"{param_type} {param_name}" for param_name, param_type in params)})\n')

    def write_pyx(self, pyx: io.IOBase):
        cursor = self.cursors[-1]
        result_type = cursor.result_type
        params = [get_type(child) for child in cursor.get_children(
        ) if child.kind == cindex.CursorKind.PARM_DECL]

        pyx.write(f'''def {cursor.spelling}({", ".join(f"{def_pointer_filter(param_type)} {symbol_filter(param_name)}" for param_name, param_type in params)})->{def_pointer_filter(result_type.spelling)}:
    value = cpp_imgui.{cursor.spelling}({", ".join(symbol_filter(param_name, get_ptr=True) for param_name, param_type in params)})
    return {def_pointer_filter(result_type.spelling)}.from_ptr(value)

''')


class Parser:
    def __init__(self, entrypoint: pathlib.Path) -> None:
        import pycindex
        self.entrypoint = str(entrypoint)
        self.tu = pycindex.get_tu(self.entrypoint)
        self.functions: List[Function] = []
        self.enums: List[Enum] = []
        self.typedef_struct_list: List[Union[Typedef, Struct]] = []

    def callback(self, *cursor_path: cindex.Cursor) -> bool:
        cursor = cursor_path[-1]
        location: cindex.SourceLocation = cursor.location
        if not location:
            return False
        if not location.file:
            return False

        if location.file.name == self.entrypoint:
            match cursor.kind:
                case cindex.CursorKind.NAMESPACE:
                    # enter namespace
                    # logger.info(f'namespace: {cursor.spelling}')
                    return True
                case (
                    cindex.CursorKind.MACRO_DEFINITION
                    | cindex.CursorKind.MACRO_INSTANTIATION
                    | cindex.CursorKind.INCLUSION_DIRECTIVE
                    | cindex.CursorKind.FUNCTION_TEMPLATE
                ):
                    pass
                case cindex.CursorKind.FUNCTION_DECL:
                    if(cursor.spelling.startswith('operator ')):
                        pass
                    else:
                        self.functions.append(Function(cursor_path))
                case cindex.CursorKind.ENUM_DECL:
                    self.enums.append(Enum(cursor_path))
                case cindex.CursorKind.TYPEDEF_DECL:
                    self.typedef_struct_list.append(Typedef(cursor_path))
                case cindex.CursorKind.STRUCT_DECL:
                    self.typedef_struct_list.append(Struct(cursor_path))
                case cindex.CursorKind.CLASS_TEMPLATE:
                    self.typedef_struct_list.append(Struct(cursor_path))
                case _:
                    logger.debug(cursor.kind)
        else:
            pass

        return False

    def traverse(self):
        import pycindex
        pycindex.traverse(self.tu, self.callback)

    def generate(self, pxd: io.IOBase, pyx: io.IOBase, pyi: io.IOBase):
        pxd.write('''from libcpp cimport bool
cdef extern from "imgui.h":

''')
        pyx.write('''from libcpp cimport bool
cimport cpp_imgui

''')

        for definition in self.typedef_struct_list:
            definition.write_pxd(pxd)
            definition.write_pyx(pyx)

        pxd.write('''
cdef extern from "imgui.h" namespace "ImGui":
''')

        for definition in self.functions:
            definition.write_pxd(pxd)
            definition.write_pyx(pyx)
            break


def generate(imgui_dir: pathlib.Path, ext_dir: pathlib.Path, pyi_path: pathlib.Path):
    parser = Parser(imgui_dir / 'imgui.h')
    parser.traverse()
    ext_dir.mkdir(parents=True, exist_ok=True)
    with (ext_dir / 'cpp_imgui.pxd').open('w') as pxd:
        with (ext_dir / 'imgui.pyx').open('w') as pyx:
            with pyi_path.open('w') as pyi:
                parser.generate(pxd, pyx, pyi)
