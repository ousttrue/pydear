from typing import Optional, NamedTuple
import ctypes
import math
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

    def __contains__(self, other: 'Rect') -> bool:
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


MIN_HEIGHT_LATITUDE = 0.05


@dataclasses.dataclass
class View:
    longitude: float = 0  # -180 + 180
    latitude: float = 0  # -90 ~ +90
    height_latitude: float = 180
    aspect_ratio: float = 1

    def __str__(self) -> str:
        return f'{self.longitude:.2f}: {self.latitude:.2f} ({self.height_latitude}) {self.aspect_ratio}'

    @property
    def rect(self) -> Rect:
        height = self.height_latitude
        width = height * self.aspect_ratio * 2
        return Rect(self.longitude-width/2, self.latitude+height/2, width, height)

    def get_matrix(self):

        import glm
        x = self.longitude
        y = self.latitude
        h = self.height_latitude/2
        w = h * self.aspect_ratio*2
        return glm.ortho(
            x-w, x+w,
            y-h, y+h,
            0, 1)

    def wheel(self, d):
        if d < 0:
            self.height_latitude *= 1.1
            if self.height_latitude > 180:
                self.height_latitude = 180
        elif d > 0:
            self.height_latitude *= 0.9
            if self.height_latitude < MIN_HEIGHT_LATITUDE:
                self.height_latitude = MIN_HEIGHT_LATITUDE

    def drag(self, screen_height: int, dx: int, dy: int):
        self.latitude += self.height_latitude * float(dy) / screen_height
        self.longitude -= 2 * self.height_latitude * float(dx) / screen_height


MAX_LEVEL = 4


class Map:
    def __init__(self, zoom_level=0) -> None:
        self.zoom_level = (ctypes.c_int32 * 1)(zoom_level)
        self.view = View()

    def __str__(self) -> str:
        return f'zoom level: {self.zoom_level}, {self.view}'

    @property
    def count(self) -> int:
        return pow(2, self.zoom_level[0])

    @property
    def tile_height(self) -> float:
        count = self.count
        return 180/count

    def iter_visible(self):
        while True:
            ratio = self.view.height_latitude / self.tile_height
            if ratio < 2:
                if self.zoom_level[0] == 8:
                    break
                self.zoom_level[0] += 1

            elif ratio >= 4:
                if self.zoom_level[0] == 0:
                    break
                self.zoom_level[0] -= 1
            else:
                break

        logger.debug(ratio)

        count = self.count
        view_rect = self.view.rect
        x, y, w, h = view_rect
        # left top origin
        l = x+180
        r = l+w
        t = 90-y
        b = t+h

        x_unit = 360/count
        x_start = max(0, int((l) // x_unit))
        x_end = min(count, math.ceil(r // x_unit) + 1)

        y_unit = 180/count
        y_start = max(0, int((t) // y_unit))
        y_end = min(count, math.ceil(b // y_unit) + 1)

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                tile = Tile(self.zoom_level[0], x, y)
                if tile.rect in view_rect:
                    yield tile
