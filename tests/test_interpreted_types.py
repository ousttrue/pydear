from typing import Callable, Tuple
import unittest
from generator import interpreted_types
from clang import cindex


def parse(src: str) -> cindex.TranslationUnit:
    import pycindex
    unsaved = pycindex.Unsaved('tmp.h', src)
    return pycindex.get_tu('tmp.h', unsaved=[unsaved])


def first(tu: cindex.TranslationUnit, pred: Callable[[cindex.Cursor], bool]) -> cindex.Cursor:
    for cursor in tu.cursor.get_children():  # type: ignore
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
        void = parse_get_type('void func();')
        self.assertEqual(void, interpreted_types.VOID_TYPE)

        int8 = parse_get_type('char func();')
        self.assertEqual(int8, interpreted_types.INT8)

        int16 = parse_get_type('short func();')
        self.assertEqual(int16, interpreted_types.INT16)

        int32 = parse_get_type('int func();')
        self.assertEqual(int32, interpreted_types.INT32)

        int64 = parse_get_type('long long func();')
        self.assertEqual(int64, interpreted_types.INT64)

        uint8 = parse_get_type('unsigned char func();')
        self.assertEqual(uint8, interpreted_types.UINT8)

        uint16 = parse_get_type('unsigned short func();')
        self.assertEqual(uint16, interpreted_types.UINT16)

        uint32 = parse_get_type('unsigned int func();')
        self.assertEqual(uint32, interpreted_types.UINT32)

        uint64 = parse_get_type('unsigned long long func();')
        self.assertEqual(uint64, interpreted_types.UINT64)

        float32 = parse_get_type('float func();')
        self.assertEqual(float32, interpreted_types.FLOAT32)

        float64 = parse_get_type('double func();')
        self.assertEqual(float64, interpreted_types.FLOAT64)


if __name__ == '__main__':
    unittest.main()
