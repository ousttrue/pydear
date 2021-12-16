import unittest
import ctypes


class TestStringMethods(unittest.TestCase):

    def test_cast(self):
        class Num(ctypes.Structure):
            _fields_ = [
                ('value', ctypes.c_int)
            ]

        value = ctypes.c_int(123)
        p = ctypes.pointer(value)
        c = ctypes.cast(p, ctypes.POINTER(Num))
        self.assertEqual(123, c[0].value)

        x = c[0]

    def test_address(self):
        p = ctypes.c_void_p()
        self.assertIsInstance(p, ctypes.c_void_p)
        # self.assertEqual(ctypes.addressof(p), p.value)

        pp = ctypes.byref(p)
        # ctypes.addressof(pp)
        print(pp)
        # self.assertIsInstance(pp, ctypes.c_void_p)

        class f2(ctypes.Structure):
            _fields_ = [
                ('x', ctypes.c_float),
                ('y', ctypes.c_float),
            ]
        v = f2()
        self.assertIsInstance(v, ctypes.Structure)
        ctypes.addressof(v)

        a = (ctypes.c_int * 3)()
        self.assertIsInstance(a, ctypes.Array)
        ctypes.addressof(a)
        # ctypes.addressof(a[0])


if __name__ == '__main__':
    unittest.main()
