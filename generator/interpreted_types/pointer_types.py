from .basetype import BaseType


class PointerType(BaseType):
    def __init__(self, base: BaseType, is_const=False):
        super().__init__(base.name + '*', base, is_const)

    def result_typing(self, pyi: bool) -> str:
        return 'ctypes.c_void_p'

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'ctypes.Array'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: Union[ctypes.c_void_p, ctypes.Array, ctypes.Structure]{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = NULL;
{indent}if isinstance({name}, ctypes.c_void_p):
{indent}    p{i} = <{base_name} *><uintptr_t>({name}.value)
{indent}if isinstance({name}, (ctypes.Array, ctypes.Structure)):
{indent}    p{i} = <{base_name} *><uintptr_t>ctypes.addressof({name})
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef void* value = <void*>{call}
{indent}return ctypes.c_void_p(<uintptr_t>value)
'''


class ReferenceType(BaseType):
    base: BaseType

    def __init__(self, base: BaseType, is_const=False):
        super().__init__(base.name + '&', base, is_const)

    def result_typing(self, pyi: bool) -> str:
        return 'ctypes.c_void_p'

    @property
    def ctypes_type(self) -> str:
        return 'ctypes.Array'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: {self.ctypes_type}{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = <{base_name} *><void*><uintptr_t>(ctypes.addressof({name}))
'''

    def call_param(self, i: int) -> str:
        return f'p{i}[0]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef void* value = <void*>&{call}
{indent}return ctypes.c_void_p(<uintptr_t>value)
'''


class ArrayType(BaseType):
    size: int

    def __init__(self, base: BaseType, size: int, is_const=False):
        super().__init__(f'{base.name}[{size}]', base, is_const)
        self.size = size

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'{self.base.ctypes_type} * {self.size}'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: ctypes.Array{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        base_name = self.base.name
        if base_name.startswith("Im"):
            base_name = 'impl.' + base_name
        return f'''{indent}# {self}
{indent}cdef {base_name} *p{i} = <{base_name}*><void*><uintptr_t>ctypes.addressof({name})
'''

    def result_typing(self, pyi: bool) -> str:
        return 'ctypes.c_void_p'


class PointerToStructType(BaseType):
    def __init__(self, base: BaseType, is_const: bool):
        super().__init__(base.name + '*', base, is_const)

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'{self.base.name}'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: {self.ctypes_type}{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.{self.ctypes_type} *p{i} = NULL
{indent}if {name}:
{indent}    p{i} = <impl.{self.ctypes_type}*><uintptr_t>ctypes.addressof({name})
'''

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef impl.{self.ctypes_type} *value = {call}
{indent}if value:
{indent}    return ctypes.cast(<uintptr_t>value, ctypes.POINTER({self.ctypes_type}))[0]
'''

    def result_typing(self, pyi: bool) -> str:
        return f'{self.ctypes_type}'


class ReferenceToStructType(BaseType):
    def __init__(self, base: BaseType, is_const: bool):
        super().__init__(base.name + '&', base, is_const)

    @property
    def ctypes_type(self) -> str:
        if not self.base:
            raise RuntimeError()
        return f'{self.base.name}'

    def ctypes_field(self, indent: str, name: str) -> str:
        return f'{indent}("{name}", ctypes.c_void_p), # {self}\n'

    def param(self, name: str, default_value: str, pyi: bool) -> str:
        return f'{name}: {self.ctypes_type}{default_value}'

    def cdef_param(self, indent: str, i: int, name: str) -> str:
        return f'''{indent}# {self}
{indent}cdef {self.const_prefix}impl.{self.ctypes_type} *p{i} = NULL
{indent}if isinstance({name}, ctypes.Structure):
{indent}    p{i} = <{self.const_prefix}impl.{self.ctypes_type} *><uintptr_t>ctypes.addressof({name})
'''

    def call_param(self, i: int) -> str:
        return f'p{i}[0]'

    def cdef_result(self, indent: str, call: str) -> str:
        return f'''{indent}# {self}
{indent}cdef {self.const_prefix}impl.{self.ctypes_type} *value = &{call}
{indent}return ctypes.cast(ctypes.c_void_p(<uintptr_t>value), ctypes.POINTER({self.ctypes_type}))[0]
'''

    def result_typing(self, pyi: bool) -> str:
        return f'{self.ctypes_type}'
