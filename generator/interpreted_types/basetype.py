from typing import Iterable


class BaseType:
    def __init__(self, c_type: str):
        '''
        c type without first const

        int, float, bool...
        ImVec2, ImGuiIO...
        int *, float *, void *...

        const char * => char *
        '''
        self.c_type = c_type

    def match(self, spelling: str) -> bool:
        '''
        process if True
        '''
        return spelling == self.c_type

    @property
    def py_typing(self) -> Iterable[str]:
        '''
        python param type annotation and result annotation
        '''
        yield self.c_type

    @property
    def param_typing(self) -> str:
        types = [t for t in self.py_typing]
        match types:
            case [t]:
                return t
            case _:
                return 'Union[' + ','.join(types) + ']'

    @property
    def result_typing(self) -> str:
        return next(iter(self.py_typing))

    @property
    def field_ctypes_type(self) -> str:
        '''
        ctypes.Structure _fields_ type
        '''
        return next(iter(self.py_typing))

    def to_c(self, name: str, is_const: bool) -> str:
        '''
        python param to cdef
        '''
        return name

    def to_cdef(self, is_const: bool) -> str:
        '''
        used param and result
        '''
        return f'cdef {self.c_type}'

    def param(self, indent: str, i: int, name: str, is_const: bool) -> str:
        return f'{indent}{self.to_cdef(is_const)} p{i} = {self.to_c(name, is_const)}'

    def to_py(self, name: str) -> str:
        '''
        return cdef to python
        '''
        return name
