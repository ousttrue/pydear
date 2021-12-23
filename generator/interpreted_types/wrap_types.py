from typing import NamedTuple, Union, Tuple, Dict
from .basetype import BaseType


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


class ImVec2WrapType(BaseType):
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


class ImVec4WrapType(BaseType):
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


class ImVector(BaseType):
    def __init__(self):
        super().__init__('ImVector')

    @property
    def ctypes_type(self) -> str:
        return 'ImVector'
