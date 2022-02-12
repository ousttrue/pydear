from typing import Dict, Optional
import pathlib
import io
import urllib.request
import urllib.parse
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import logging
#
from xyztile import Tile
from pydear import glo

logger = logging.getLevelName(__name__)


class TileTextureManager:
    def __init__(self, base_url: str, cache_dir: pathlib.Path) -> None:
        self.base_url = base_url
        self.texture_map: Dict[Tile, glo.Texture] = {}
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_or_create(self, tile: Tile) -> Optional[glo.Texture]:
        texture = self.texture_map.get(tile)
        if not texture:
            image = self.create_img(tile)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            texture = glo.Texture(
                image.width, image.height,  image.tobytes('raw'))
            self.texture_map[tile] = texture

        return texture

    def get_cache_path(self, tile: Tile) -> pathlib.Path:
        url = urllib.parse.urlparse(self.base_url)
        return self.cache_dir / \
            f'{url.hostname}/{url.path}/{tile.z}/{tile.x}/{tile.y}.png'

    def get_cache(self, tile) -> Optional[bytes]:
        path = self.get_cache_path(tile)
        if path.exists():
            return path.read_bytes()

    def save_cache(self, tile, data):
        path = self.get_cache_path(tile)
        logger.debug(f'save: {tile} => {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def create_img(self, tile: Tile) -> PIL.Image.Image:
        if self.base_url:
            data = self.get_cache(tile)
            if data:
                return PIL.Image.open(io.BytesIO(data))
            url = f'{self.base_url}/{tile.z}/{tile.x}/{tile.y}.png'
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as res:
                data = res.read()
                self.save_cache(tile, data)
                return PIL.Image.open(io.BytesIO(data))
        else:
            img = PIL.Image.new("RGBA", (256, 256))
            draw = PIL.ImageDraw.Draw(img)
            font = PIL.ImageFont.truetype("verdana.ttf", 24)
            draw.text((0, 0), f"[{tile.z}]{tile.x}:{tile.y}",
                      font=font, fill=(255, 0, 0, 255))
            return img
