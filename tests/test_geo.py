import unittest
from examples.geo import xyztile


class TestGeo(unittest.TestCase):

    def test_1(self):
        map = xyztile.Map(1)

        self.assertEqual(2, map.count)

        tiles = [tile for tile in map.iter_visible()]
        self.assertEquals(len(tiles), 4)

    def test_2(self):
        map = xyztile.Map(2)

        self.assertEqual(4, map.count)

        tiles = [tile for tile in map.iter_visible()]
        self.assertEquals(len(tiles), 16)

    def test_rect(self):
        tile000 = xyztile.Tile(0, 0, 0)
        self.assertEqual(tile000.rect, (-180, 90, 360, 180))
        tile100 = xyztile.Tile(1, 0, 0)
        self.assertEqual(tile100.rect, (-180, 90, 180, 90))

        view = xyztile.View(0)
        self.assertEqual(view.rect, (-180, 90, 360, 180))
        view = xyztile.View(20, 40, 60)
        self.assertEqual(view.rect, (-40, 70, 120, 60))

        self.assertFalse(xyztile.Rect(1, 2, 10, 20).is_overlap(
            xyztile.Rect(11, 0, 10, 20)))
        self.assertTrue(xyztile.Rect(1, 2, 10, 20).is_overlap(
            xyztile.Rect(9, 2, 10, 20)))

        self.assertFalse(xyztile.Rect(1, 2, 10, 20).is_overlap(
            xyztile.Rect(0, 22, 10, 20)))
        self.assertTrue(xyztile.Rect(1, 2, 10, 20).is_overlap(
            xyztile.Rect(0, 21, 10, 20)))


if __name__ == '__main__':
    unittest.main()
