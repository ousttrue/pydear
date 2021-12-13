from typing import Iterable, Generator
import re


FP_PATTERN = re.compile(r'(.*)\(\*\)(.*)')


def type_name(t: str, name: str) -> str:
    m = FP_PATTERN.match(t)
    if m:
        # function pointer
        return f'{m.group(1)}(*{name}){m.group(2)}'
    else:
        return f'{t} {name}'


IMPOINTER_PATTERN = re.compile(r'(Im\w+)(\s*[\*&])(.*)')
CONST_IMPOINTER_PATTERN = re.compile(r'const (Im\w+)(\s*[\*&])(.*)')


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


def template_filter(src: str) -> str:
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


def comma_join(src: Iterable[str]) -> str:
    return ', '.join(src)
