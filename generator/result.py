# from typing import NamedTuple
# import re
# from clang import cindex

# from generator.param import is_wrap
# from . import utils


# class Result(NamedTuple):
#     cursor: cindex.Cursor
#     type: cindex.Type

#     @property
#     def py_type(self) -> str:
#         result_type = self.type
#         result_spelling = result_type.spelling

#         match result_type.kind:
#             case cindex.TypeKind.UINT | cindex.TypeKind.USHORT:
#                 return 'int'
#             # case cindex.TypeKind.POINTER:
#             #     # address
#             #     return 'int'

#             case cindex.TypeKind.TYPEDEF:
#                 underlying = self.unerlying_type()
#                 match underlying.kind:
#                     case cindex.TypeKind.INT | cindex.TypeKind.UINT | cindex.TypeKind.SHORT | cindex.TypeKind.USHORT:
#                         return 'int'

#         if self.is_bytes:
#             return 'bytes'

#         match result_spelling:
#             case 'void *' | 'ImDrawList **' | 'unsigned char *' | 'unsigned int *':
#                 # address
#                 return 'int'
#             case 'ImVec2':
#                 return 'Tuple[float, float]'
#             case 'ImVec4':
#                 return 'Tuple[float, float, float, float]'
#             case 'ImU32' | 'ImGuiID' | 'ImGuiMouseCursor':
#                 return 'int'
#             case _:
#                 return utils.def_pointer_filter(result_spelling)

#     def unerlying_type(self) -> cindex.Type:
#         cursor = self.cursor
#         current = self.type
#         while current.kind == cindex.TypeKind.TYPEDEF:
#             children = [child for child in cursor.get_children(
#             ) if child.kind == cindex.CursorKind.TYPE_REF]
#             match children:
#                 case [ref]:
#                     cursor = ref.referenced
#                     current = cursor.underlying_typedef_type
#                 case _:
#                     raise RuntimeError()
#         return current

#     @property
#     def is_bytes(self) -> bool:
#         if self.type.spelling == 'const char *':
#             return True
#         if self.type.spelling == 'char *':
#             return True

#         # array
#         m = re.match(r'(\w+) \[(\d+)\]', self.type.spelling)
#         if m:
#             return True

#         # ImVector<>
#         m = re.match(r'ImVector<([^>]+)>', self.type.spelling)
#         if m:
#             return True

#         return False
