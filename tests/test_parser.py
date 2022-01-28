import unittest
import pathlib
import ctypes
import rawtypes.clang_util
from rawtypes.clang import cindex
HERE = pathlib.Path(__file__).absolute().parent
ROOT = HERE.parent


class TestParse(unittest.TestCase):

    def test_forward(self):
        dir = ROOT / '_external/nanovg'
        header = dir / 'src/nanovg.h'
        self.assertTrue(header.exists())
        gl_header = dir / 'src/nanovg_gl.h'
        self.assertTrue(gl_header.exists())
        glew_dir = ROOT / '_external/glew-2.1.0/include'
        tu = rawtypes.clang_util.get_tu(
            'tmp.h',
            include_dirs=[str(header.parent), str(glew_dir)],
            definitions=['NOMINMAX'],
            unsaved=[rawtypes.clang_util.Unsaved(
                'tmp.h', '''
#include <gl/glew.h>
#include "nanovg.h"
#define NANOVG_GL3_IMPLEMENTATION
#include "nanovg_gl.h"
                '''
            )])

        def callback(*cursors):
            cursor = cursors[0]
            location: cindex.SourceLocation = cursor.location
            if not location:
                return False
            if not location.file:
                return False

            if pathlib.Path(location.file.name) == gl_header:
                spellings = [c.spelling for c in cursors]
                if 'nvglImageHandleGL3' in spellings:
                    print(spellings)
            return True

        rawtypes.clang_util.traverse(tu, callback)


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
