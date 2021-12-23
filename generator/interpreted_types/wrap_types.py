from typing import Optional, Callable, NamedTuple, Union, Tuple, Dict, Iterable
import re
from .basetype import BaseType
from .const import const


class WrapFlags(NamedTuple):
    name: str
    fields: bool = False
    custom_fields: Dict[str, str] = {}
    methods: Union[bool, Tuple[str, ...]] = False
    custom_methods: Tuple[str, ...] = ()
    default_constructor: bool = False


WRAP_TYPES = [
    WrapFlags('ImVec2', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
''',
    )),
    WrapFlags('ImVec4', fields=True, custom_methods=(
        '''def __iter__(self):
    yield self.x
    yield self.y
    yield self.w
    yield self.h
''',
    )),
    WrapFlags('ImFont'),
    WrapFlags('ImFontConfig', fields=True, default_constructor=True),
    WrapFlags('ImFontAtlasCustomRect', fields=True),
    WrapFlags('ImFontAtlas', fields=True, methods=True),
    WrapFlags('ImGuiIO', fields=True, custom_fields={
        'Fonts': '''def Fonts(self)->'ImFontAtlas':
    return ctypes.cast(self._Fonts, ctypes.POINTER(ImFontAtlas))[0]
'''
    }),
    WrapFlags('ImGuiContext'),
    WrapFlags('ImDrawCmd', fields=True),
    WrapFlags('ImDrawData', fields=True),
    WrapFlags('ImDrawListSplitter', fields=True),
    WrapFlags('ImDrawCmdHeader', fields=True),
    WrapFlags('ImDrawList', fields=True),
    WrapFlags('ImGuiViewport', fields=True, methods=True),
    WrapFlags('ImGuiStyle'),
    WrapFlags('ImGuiWindowClass'),
]


class WrapPointerType(BaseType):
    '''
    by pointer
    '''

    def __init__(self, name: str):
        super().__init__(name + ' *')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: \*)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_typing(self) -> Iterable[str]:
        yield self._name

    @property
    def field_ctypes_type(self) -> str:
        return f'ctypes.c_void_p'

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}impl.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}impl.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'


class WrapReferenceType(BaseType):
    '''
    by reference
    '''

    def __init__(self, name: str):
        super().__init__(name + ' &')
        self._name = name

    def match(self, spelling: str) -> bool:
        m = re.match(r'^(?:const )?(\w+)(?: &)?$', spelling)
        if m and m.group(1) == self._name:
            return True
        return False

    @property
    def py_typing(self) -> Iterable[str]:
        yield self._name

    @property
    def field_ctypes_type(self) -> str:
        return self._name

    def to_c(self, name: str, is_const: bool) -> str:
        return f'<{const(is_const)}impl.{self._name}*><uintptr_t>ctypes.addressof({name}) if {name} else NULL'

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {const(is_const)}impl.{self._name} *'

    def to_py(self, name: str) -> str:
        return f'ctypes.cast(ctypes.c_void_p(<uintptr_t>{name}), ctypes.POINTER({self._name}))[0]'


class ImVec2WrapReferenceType(WrapReferenceType):
    def __init__(self):
        super().__init__('ImVec2')

    @property
    def py_typing(self) -> Iterable[str]:
        yield 'ImVec2'
        yield 'Tuple[float, float]'

    def param(self, indent: str, i: int, name: str, is_const: bool) -> str:
        '''
        tuple support
        '''
        return f'''{indent}pp{i} = ImVec2({name}[0], {name}[1]) if isinstance({name}, tuple) else {name}
{indent}{self.to_cdef(is_const)} p{i} = {self.to_c(f"pp{i}", is_const)}'''


class WrapType(BaseType):
    '''
    by value
    '''

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
        return f'cdef impl.{self.c_type}'

    def to_py(self, name: str) -> str:
        if self._to_py:
            return self._to_py(name)
        else:
            return name


class ImVec2WrapType(WrapType):
    def __init__(self):
        super().__init__('ImVec2')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec2'

    def param(self, name: str, default_value: str) -> str:
        return f'{name}: Union[ImVec2, Tuple[float, float]]{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec2 p{i} = impl.ImVec2({name}[0], {name}[1]) if isinstance({name}, tuple) else impl.ImVec2({name}.x, {name}.y)
'''

    @property
    def result_typing(self) -> str:
        return 'Tuple[float, float]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec2 value = {call}
{indent}return (value.x, value.y)
'''


class ImVec4WrapType(WrapType):
    def __init__(self):
        super().__init__('ImVec4')

    @property
    def ctypes_type(self) -> str:
        return 'ImVec4'

    def param(self, name: str, default_value: str) -> str:
        return f'{name}: Union[ImVec4, Tuple[float, float, float, float]]{default_value}'

    @property
    def result_typing(self) -> str:
        return 'Tuple[float, float, float, float]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.ImVec4 value = {call}
{indent}return (value.x, value.y, value.z, value.w)
'''
