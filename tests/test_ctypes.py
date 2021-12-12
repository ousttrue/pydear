import unittest
import ctypes


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        class Num(ctypes.Structure):
            _fields_ = [
                ('value', ctypes.c_int)
            ]

        value = ctypes.c_int(123)
        p = ctypes.pointer(value)
        c = ctypes.cast(p, ctypes.POINTER(Num))
        self.assertEqual(123, c[0].value)

        x = c[0]


if __name__ == '__main__':
    unittest.main()
