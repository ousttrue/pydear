import unittest
from pydear import imgui as ImGui


class TestTypes(unittest.TestCase):

    def test_vec2(self):
        v2 = ImGui.ImVec2(1, 2)
        x, y = v2
        self.assertEqual((1, 2), (x, y))


if __name__ == '__main__':
    unittest.main()
