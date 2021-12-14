from typing import NamedTuple, Tuple, Union
import logging

logger = logging.getLogger(__name__)


class WrapFlags(NamedTuple):
    fields: bool = False
    methods: Union[bool, Tuple[str, ...]] = False


WRAP_TYPES = {
    'ImVec2': WrapFlags(fields=True),
    'ImVec4': WrapFlags(fields=True),
    'ImFont': WrapFlags(),
    'ImFontAtlas': WrapFlags(fields=True, methods=('GetTexDataAsRGBA32', 'ClearTexData',)),
    'ImGuiIO': WrapFlags(fields=True),
    'ImGuiContext': WrapFlags(),
    'ImDrawCmd': WrapFlags(fields=True),
    'ImDrawData': WrapFlags(fields=True),
    'ImDrawCmdHeader': WrapFlags(),
    'ImDrawListSplitter': WrapFlags(),
    'ImDrawList': WrapFlags(fields=True),
    'ImGuiStyle': WrapFlags(),
}


def in_type(spelling: str):
    match spelling:
        case 'int':
            return 'int'
        case 'bool *' | 'int *':
            return 'ctypes.Array'
        case 'const char *':
            return 'bytes'
        case 'unsigned char **':
            return 'ctypes.c_void_p'

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return deref

    raise NotImplementedError(spelling)


def to_pointer(spelling: str, name: str) -> str:
    match spelling:
        case 'int':
            return name
        case 'bool *':
            return f'<{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'
        case 'const char *':
            return f'<const char *>{name}'
        case 'unsigned char **':
            return f'<uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return f'<cpp_imgui.{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    raise NotImplementedError(spelling)
