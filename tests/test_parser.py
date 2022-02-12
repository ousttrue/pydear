import unittest
import pathlib
import ctypes
import rawtypes.clang_util
from rawtypes.clang import cindex
from rawtypes.parser import Parser
HERE = pathlib.Path(__file__).absolute().parent
ROOT = HERE.parent


class TestNanoVG(unittest.TestCase):

    def test_forward(self):
        dir = ROOT / '_external/picovg'
        header = dir / 'src/nanovg.h'
#         tu = rawtypes.clang_util.get_tu(
#             'tmp.h',
#             include_dirs=[str(header.parent)],
#             definitions=['NOMINMAX'],
#             unsaved=[rawtypes.clang_util.Unsaved(
#                 'tmp.h', '''
# #include "nanovg.h"
#                 '''
#             )])


#         def callback(*cursors):
#             cursor = cursors[0]
#             location: cindex.SourceLocation = cursor.location
#             if not location:
#                 return False
#             if not location.file:
#                 return False

#             if pathlib.Path(location.file.name) == header:

#             return True

#         rawtypes.clang_util.traverse(tu, callback)

        parser = Parser(
            [header]
        )
        parser.traverse()
        pass

class TestParse(unittest.TestCase):

    def test_forward(self):
        SRC = '''
#include <GL/glew.h>
        '''
        tu = rawtypes.clang_util.get_tu(
            'tmp.h',
            unsaved=[rawtypes.clang_util.Unsaved('tmp.h', SRC)],
            include_dirs=['C:/vcpkg/installed/x64-windows/include'])

        def callback(*cursors):
            spellings = [c.spelling for c in cursors]
            if 'glColor3bv' in spellings:
                print(spellings)
            return True

        rawtypes.clang_util.traverse(tu, callback)
        # glColor3bv
