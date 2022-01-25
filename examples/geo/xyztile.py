from typing import Optional, NamedTuple
import dataclasses
import logging
logger = logging.getLogger(__name__)


class Rect(NamedTuple):
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top - self.height

    def is_overlap(self, other: 'Rect') -> bool:
        if self.right <= other.left:
            return False
        if other.right <= self.left:
            return False
        if self.top <= other.bottom:
            return False
        if other.top <= self.bottom:
            return False
        return True


class Tile(NamedTuple):
    z: int
    x: int
    y: int

    @property
    def rect(self) -> Rect:
        count = pow(2, self.z)
        # longitude 360
        x_unit = 360 / count
        l = -180 + self.x * x_unit
        # latitude 180
        y_unit = 180 / count
        t = 90 - self.y * y_unit
        return Rect(l, t, x_unit, y_unit)


@dataclasses.dataclass
class View:
    longitude: float = 0  # -180 + 180
    latitude: float = 0  # -90 ~ +90
    height_longitude: float = 180
    aspect_ratio: float = 1

    @property
    def rect(self) -> Rect:
        height = self.height_longitude
        width = height * self.aspect_ratio * 2
        return Rect(self.longitude-width/2, self.latitude+height/2, width, height)

    def get_matrix(self):
        import glm
        x = self.longitude
        y = self.latitude
        h = self.height_longitude / 2
        w = h * self.aspect_ratio
        return glm.ortho(
            x-w, x+w,
            y-h, y+h,
            0, 1)

    def drag(self, screen_height: int, dx: int, dy: int):
        pass


class Map:
    def __init__(self, zoom_level=0) -> None:
        self.zoom_level = zoom_level
        self.view = View()

    @property
    def count(self) -> int:
        return pow(2, self.zoom_level)

    def iter_visible(self):
        count = self.count
        for x in range(count):
            for y in range(count):
                tile = Tile(self.zoom_level, x, y)
                yield tile
