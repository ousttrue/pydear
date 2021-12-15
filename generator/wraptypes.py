from typing import NamedTuple, Union, Tuple


class WrapFlags(NamedTuple):
    name: str
    fields: bool = False
    methods: Union[bool, Tuple[str, ...]] = False

    # def to_c(self, name: str) -> str:
    #     # deref = get_deref(spelling)
    #     # if deref and deref in WRAP_TYPES:
    #     return f'<cpp_imgui.{self.c_type} *><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    # @property
    # def cdef(self) -> str:
    #     return f'cdef cpp_imgui.{self.c_type} *'

    # def to_py(self, name: str) -> str:
    #     return f'ctypes.cast(ctypes.c_void_p(<long long>{name}), ctypes.POINTER({self.py_type}))[0]'


WRAP_TYPES = [
    WrapFlags('ImVec2', fields=True),
    WrapFlags('ImVec4', fields=True),
    WrapFlags('ImFont'),
    WrapFlags('ImFontAtlas', fields=True, methods=(
        'GetTexDataAsRGBA32', 'ClearTexData',)),
    WrapFlags('ImGuiIO', fields=True),
    WrapFlags('ImGuiContext'),
    WrapFlags('ImDrawCmd', fields=True),
    WrapFlags('ImDrawData', fields=True),
    WrapFlags('ImDrawListSplitter', fields=True),
    WrapFlags('ImDrawCmdHeader', fields=True),
    WrapFlags('ImDrawList', fields=True),
    WrapFlags('ImGuiStyle'),
    WrapFlags('ImGuiViewport'),
]
