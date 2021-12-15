from typing import NamedTuple, Union, Tuple


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
