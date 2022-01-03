from typing import Optional
import dataclasses


@dataclasses.dataclass
class BaseType:
    name: str
    base: Optional['BaseType'] = None
    is_const: bool = False

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.name}'

    @property
    def const_prefix(self) -> str:
        is_const = self.is_const
        if self.base and self.base.is_const:
            is_const = True
        return 'const ' if is_const else ''

    @property
    def ctypes_type(self) -> str:
        '''
        ctypes.Structure fields
        '''
        raise NotImplementedError()

    def pyi_field(self, indent: str, name: str) -> str:
        return f'{indent}{name}: {self.ctypes_type} # {self}\n'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", {self.ctypes_type}), # {self}\n'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        '''
        function param
        '''
        raise NotImplementedError()

    def result_typing(self, pyi: bool) -> str:
        '''
        return
        '''
        raise NotImplementedError()

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        '''
        extract params
        '''
        raise NotImplementedError()

    def call_param(self, i: int) -> str:
        return f'p{i}'

    def cdef_result(self, indent: str, call: str) -> str:
        '''
        extract result
        '''
        raise NotImplementedError()

    def cpp_extract_name(self, i: int):
        return f't{i}'

    def cpp_param_declare(self, indent: str, i: int, name: str) -> str:
        '''
        extract params
        '''
        raise NotImplementedError()

    @property
    def format(self) -> str:
        raise NotImplemented()

    def cpp_from_py(self, indent: str, i: int) -> str:
        raise NotImplementedError()

    def cpp_call_name(self, i: int):
        return f'p{i}'

    def cpp_result(self, indent: str, call: str) -> str:
        raise NotImplementedError()
