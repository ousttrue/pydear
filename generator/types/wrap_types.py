from typing import Optional, Callable, NamedTuple, Union, Tuple
import re
from .basetype import BaseType
from .const import const


class WrapFlags(NamedTuple):
    name: str
    fields: bool = False
    methods: Union[bool, Tuple[str, ...]] = False


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
    WrapFlags('ImGuiWindowClass'),
]


class WrapType(BaseType):
    def __init__(self, name: str,
                 to_c: Optional[Callable[[str, bool], str]] = None,
                 to_py: Optional[Callable[[str], str]] = None):
        super().__init__(name)
        self._to_c = to_c
        self._to_py = to_py

    def to_c(self, name: str, is_const: bool) -> str:
        if self._to_c:
            return self._to_c(name, is_const)
        else:
            return name

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef cpp_imgui.{self.c_type}'

    def to_py(self, name: str) -> str:
        if self._to_py:
            return self._to_py(name)
        else:
            return name


class WrapPointerType(BaseType):
    def __init__(self, name: str):
        super().__init__(name + ' *')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: \*)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_type(self) -> str:
        return self._name

    @property
    def field_ctypes_type(self) -> str:
        return f'ctypes.c_void_p'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}cpp_imgui.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}cpp_imgui.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'


class WrapReferenceType(BaseType):
    def __init__(self, name: str):
        super().__init__(name + ' &')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: &)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_type(self) -> str:
        return self._name

    @property
    def field_ctypes_type(self) -> str:
        return self._name

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}cpp_imgui.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}cpp_imgui.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'
