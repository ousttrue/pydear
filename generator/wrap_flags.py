from typing import NamedTuple, Tuple
import logging

logger = logging.getLogger(__name__)


class WrapFlags(NamedTuple):
    fields: bool = False
    methods: Tuple[str, ...] = ()


WRAP_TYPES = {
    'ImVec2': WrapFlags(fields=True, methods=('o',)),
    'ImVec4': WrapFlags(fields=True, methods=('o',)),
    'ImFont': WrapFlags(methods=('o',)),
    'ImFontAtlas': WrapFlags(fields=True, methods=('GetTexDataAsRGBA32', 'ClearTexData',)),
    'ImGuiIO': WrapFlags(fields=True, methods=('o',)),
    'ImGuiContext': WrapFlags(methods=('o',)),
    'ImDrawCmd': WrapFlags(fields=True),
    'ImDrawData': WrapFlags(fields=True, methods=('o',)),
    'ImDrawCmdHeader': WrapFlags(),
    'ImDrawListSplitter': WrapFlags(),
    'ImDrawList': WrapFlags(fields=True, methods=('o',)),
    'ImGuiStyle': WrapFlags(methods=('o',)),
}


def in_type(spelling: str):
    match spelling:
        case 'bool *':
            return 'ctypes.Array'
        case 'const char *':
            return 'bytes'

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return deref
        else:
            logger.debug(f'{spelling} => void *')
            return 'ctypes.c_void_p'

    raise NotImplementedError(spelling)

def to_pointer(spelling: str, name: str) -> str:
    match spelling:
        case 'bool *':
            return f'<{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'
        case 'const char *':
            return f'<const char *>{name}'

    if spelling.endswith(' *'):
        deref = spelling[:-2]
        if deref in WRAP_TYPES:
            return f'<cpp_imgui.{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'
        else:
            return f'<{spelling}><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    raise NotImplementedError(spelling)
