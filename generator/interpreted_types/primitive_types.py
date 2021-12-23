from .basetype import BaseType


class VoidType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('void', is_const)


class BoolType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('bool', is_const)


class UInt8Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('unsigned char', is_const)


class UInt16Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('unsigned short', is_const)


class UInt32Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('unsigned int', is_const)


class UInt64Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('unsigned long long', is_const)


class Int8Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('char', is_const)


class Int16Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('short', is_const)


class Int32Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('int', is_const)


class Int64Type(BaseType):
    def __init__(self, is_const=False):
        super().__init__('long long', is_const)


class FloatType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('float', is_const)


class DoubleType(BaseType):
    def __init__(self, is_const=False):
        super().__init__('double', is_const)
