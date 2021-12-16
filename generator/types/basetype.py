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
    def py_type(self) -> str:
        '''
        python param type
        '''
        return self.c_type

    @property
    def field_ctypes_type(self) -> str:
        '''
        ctypes.Structure _fields_ type
        '''
        return self.py_type

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
