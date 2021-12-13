# from typing import NamedTuple
# from clang import cindex
# import re
# from . import utils




# def is_pointer(src: str) -> bool:
#     if re.search(r'\s*\*', src):
#         return True
#     else:
#         return False


# def is_reference(src: str) -> bool:
#     if re.search(r'\s*&', src):
#         return True
#     else:
#         return False




# def is_wrap(type):
#     if type.kind != cindex.TypeKind.RECORD:
#         return False
#     m = re.search(r'\bIm', type.spelling)
#     if m:
#         if '**' in type.spelling:
#             return False
#         else:
#             # ImXXX
#             return True
#     else:
#         return False


# class Param(NamedTuple):
#     cursor: cindex.Cursor



