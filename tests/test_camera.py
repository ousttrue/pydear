import unittest
import glm
from glglue.camera import Camera


class TestCamera(unittest.TestCase):

    def test_ray(self):
        camera = Camera()
        ray = camera.get_mouse_ray(
            camera.projection.width/2, camera.projection.height/2)

        self.assertEqual(glm.vec3(0, 0, 5), ray.origin)
        self.assertEqual(glm.vec3(0, 0, -1), ray.dir)

        d = ray.intersect_triangle(
            glm.vec3(-1, -1, 0),
            glm.vec3(1, -1, 0),
            glm.vec3(0, 1, 0))
        self.assertEqual(5, d)
