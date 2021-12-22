from typing import Callable, Optional, Tuple
import unittest
from generator import interpreted_types
from clang import cindex


def parse(src: str) -> cindex.TranslationUnit:
    import pycindex
    unsaved = pycindex.Unsaved('tmp.h', src)
    return pycindex.get_tu('tmp.h', unsaved=[unsaved])


def first(tu: cindex.TranslationUnit, pred: Callable[[cindex.Cursor], bool]) -> cindex.Cursor:
    for cursor in tu.cursor.get_children():
        if pred(cursor):
            return cursor

    raise RuntimeError()


def parse_get_func(src: str) -> Tuple[cindex.TranslationUnit, cindex.Cursor]:
    tu = parse(src)
    return tu, first(tu, lambda cursor: cursor.kind ==
                     cindex.CursorKind.FUNCTION_DECL)


def parse_get_type(src: str) -> interpreted_types.BaseType:
    tu, c = parse_get_func(src)
    return interpreted_types.from_cursor(c.result_type, c)


class TestTypes(unittest.TestCase):

    def test_primitive(self):
        t = parse_get_type('''
        void func();
        ''')
        self.assertEqual(t, interpreted_types.VOID_TYPE)


if __name__ == '__main__':
    unittest.main()
