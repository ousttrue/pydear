class BaseType:
    def __init__(self, c_type: str):
        self.c_type = c_type

    def match(self, spelling: str) -> bool:
        return spelling == self.c_type

    @property
    def py_type(self) -> str:
        return self.c_type

    @property
    def field_ctypes_type(self) -> str:
        return self.py_type

    def to_c(self, name: str, is_const: bool) -> str:
        return name

    def to_cdef(self, is_const: bool) -> str:
        return f'cdef {self.c_type}'

    def to_py(self, name: str) -> str:
        return name
